-- #707 trusted bootstrap. SOURCES contains only Python-verified original definitions.
-- Nothing below is installed into the real Tracker. No launcher or module is loaded.
local trustedLoad, trustedHook, trustedStringMeta = load, debug.sethook, debug.setmetatable
local tests, counts, traps = {}, {}, {}
-- Lua strings otherwise inherit the complete process string library (including dump).
-- Restrict that intrinsic lookup in this disposable standalone interpreter as well.
local safeStringMethods={lower=string.lower,find=string.find,match=string.match,sub=string.sub}
trustedStringMeta('',{__index=function(_,key)
    if safeStringMethods[key] then return safeStringMethods[key] end
    local name='string.'..tostring(key); traps[name]=(traps[name] or 0)+1
    error('TRAP:'..name,0)
end,__metatable=false})
local function test(class,name,fn,hazard) tests[#tests+1]={class,name,fn,hazard} end
local function eq(a,b) assert(a==b, tostring(a)..' != '..tostring(b)) end
local function denied(fn, expected)
    local ok,why=pcall(fn)
    assert(not ok and tostring(why):find('TRAP:'..expected,1,true), tostring(why))
end
local function fresh()
    local calls, reads, violations = {}, {}, {}
    local function trap(name)
        return function() violations[#violations+1]=name; traps[name]=(traps[name] or 0)+1; error('TRAP:'..name,0) end
    end
    local function forbidden(name)
        return setmetatable({}, {__index=function(_,k) return trap(name..'.'..tostring(k)) end,
            __newindex=function() trap(name..'.mutation')() end, __call=trap(name..'.call'), __metatable=false})
    end
    local function frozen(value,name)
        if type(value)~='table' then return value end
        local backing={}; for k,v in pairs(value) do backing[k]=frozen(v,name..'.'..tostring(k)) end
        return setmetatable({}, {__index=backing, __newindex=trap(name..'.mutation'),
            __pairs=function() return function(_,key) return next(backing,key) end,nil,nil end, __len=function() return #backing end, __metatable=false})
    end
    local env, stores, locked = {}, {}, false
    local mutable={Battle={inBattleScreen=true,dataReady=true,numBattlers=true,isGhost=true,
        isViewingOwn=true,isViewingLeft=true,isWildEncounter=true,Combatants=true,BattleParties=true},
        GameOverScreen={isDisplayed=true}}
    local function namespace(name,values)
        local backing=values or {}; stores[name]=backing
        return setmetatable({}, {
            __index=function(_,key)
                if backing[key]~=nil then return backing[key] end
                return trap(name..'.'..tostring(key))
            end,
            __newindex=function(_,key,value)
                if locked and not (mutable[name] and mutable[name][key]) then
                    trap(name..'.unapproved-write.'..tostring(key))()
                end
                backing[key]=value
            end, __metatable=false})
    end
    local state={bytes={}, allowed={}, readLog=reads, calls=calls, violations=violations}
    -- Symbolic synthetic addresses; not GBA addresses or runtime bindings.
    local PLAYER, ENEMY, INDEX=0x1000,0x2000,0x3000
    state.PLAYER, state.ENEMY, state.INDEX=PLAYER,ENEMY,INDEX
    local function read(width,address,domain)
        if domain~=nil and domain~='SYNTHETIC' then trap('read.domain')() end
        if type(address)~='number' or not state.allowed[width..':'..address] then trap('read.address-width')() end
        local value=0
        for i=0,width-1 do
            local b=state.bytes[address+i]; if b==nil then trap('read.truncated')() end
            value=value+b*256^i
        end
        reads[#reads+1]={width,address,domain or 'SYNTHETIC'}
        return value
    end
    function state.put(address,width,value)
        for i=0,width-1 do state.bytes[address+i]=value%256; value=math.floor(value/256) end
    end
    function state.allow(address,width) state.allowed[width..':'..address]=true end
    env.Memory=namespace('Memory',{readbyte=function(a,d) return read(1,a,d) end,
        readword=function(a,d) return read(2,a,d) end,readdword=function(a,d) return read(4,a,d) end})
    for _,name in ipairs({'memory','io','os','package','debug','socket','http','emu','event','client','forms','gui',
        'savestate','FileManager','QuickloadScreen','CustomCode','Drawing'}) do env[name]=forbidden(name) end
    for _,name in ipairs({'require','load','loadfile','dofile','loadstring','collectgarbage','rawset','rawget',
        'setmetatable','getmetatable','print','_G'}) do env[name]=trap(name) end
    for _,name in ipairs({'assert','error','ipairs','pairs','next','tonumber','tostring','type','pcall','select'}) do
        env[name]=_G[name]
    end
    env.math=frozen({floor=math.floor,min=math.min,max=math.max},'math')
    env.table=frozen({insert=table.insert,concat=table.concat},'table')
    env.string=frozen({lower=string.lower},'string')
    env.Constants=frozen({HIDDEN_INFO='?',BLANKLINE='',OrderedLists={STATSTAGES={'hp','atk','def','spa','spd','spe'}}},'Constants')
    env.Options=frozen({['Reveal info if randomized']=true},'Options')
    env.GameSettings=frozen({pstats=PLAYER,estats=ENEMY,gBattlerPartyIndexes=INDEX,game=3,GameCharMap={}},'GameSettings')
    env.Program=namespace('Program',{
        Addresses=frozen({sizeofPokemonStruct=100,offsetPokemonSubstruct=32,sizeofPokemonNickname=10,
            nicknameCharEnd=255,offsetPokemonStatus=80,offsetPokemonStatsLvCurHp=84,
            offsetPokemonStatsMaxHpAtk=88,offsetPokemonStatsDefSpe=92,offsetPokemonStatsSpaSpd=96},'Program.Addresses'),
        Values={ShinyOdds=8},DefaultPokemon={new=function(_,row) return row end},
        GameData={PlayerTeam={},EnemyTeam={},Items={},friendshipRequired=220,mapId=0},
        getNextLevelExp=function() return 10,100 end,isValidMapLocation=function() return true end,
        getPokemonTypes=function() return {12,3} end,getExtras=function() return {} end})
    env.Battle=namespace('Battle',{inBattleScreen=true,dataReady=true,numBattlers=2,isGhost=false,
        isViewingOwn=true,isViewingLeft=true,isWildEncounter=true,
        Combatants={LeftOwn=1,LeftOther=1,RightOwn=2,RightOther=2},BattleParties={[0]={},[1]={}},
        getDoublesCursorTargetInfo=function() return {slot=1,isOwner=false,isLeft=true} end})
    env.Tracker=namespace('Tracker',{Data=frozen({isNewGame=true,hasCheckedSummary=true,centerHeals=0},'Tracker.Data'),
        BattleNotes=frozen({},'Tracker.BattleNotes'),
        verifyDataForPlayer=function(id) assert(type(id)=='number'); calls.verifyStub=(calls.verifyStub or 0)+1 end,
        getDefaultPokemon=function() return state.mon(0) end,
        getLastLevelSeen=function() return nil end,getMoves=function() return {} end,
        getEncounters=function() return 0 end})
    env.GachaMonData=namespace('GachaMonData',{getAssociatedRecentMon=function() return nil end})
    env.GameOverScreen=namespace('GameOverScreen',{isDisplayed=false})
    local catalog={
        [0]={name='Blank',types={0,0},baseStats={}},
        [1]={name='Synthetic Bulbasaur',types={12,3},baseStats={},bst=318},
        [906]={name='Synthetic conflicting internal ID',types={0,0},baseStats={}},
        [1294]={name='Synthetic Sprigatito',types={12,12},baseStats={},bst=310},
        [1022]={name='Synthetic Raichu regional',types={13,14},baseStats={},bst=485}}
    env.PokemonData=namespace('PokemonData',{Pokemon=frozen(catalog,'PokemonData.Pokemon'),BlankPokemon=catalog[0],
        Values={GhostId=999,DefaultBaseFriendship=70},Evolutions={FRIEND='Friend'},IsRand={types=false},
        isValid=function(id) return catalog[id]~=nil end,isGameDataRandomized=function() return false end,
        getAbilityId=function() return 65 end,canShowUnknownStats=function() return false end,
        canShowUnknownAbilities=function() return false end,canShowUnknownMoveLearnSets=function() return true end})
    env.MoveData=namespace('MoveData',{Moves=frozen({[33]={id=33,name='Synthetic move',pp='35',power='40',category=0,type=0}},'MoveData.Moves'),
        BlankMove=frozen({id=0,name='Blank',pp='0',power='0',accuracy='0'},'MoveData.BlankMove'),
        Values={HiddenPowerId=237},IsRand={},isValid=function(id) return id==33 end})
    env.AbilityData=namespace('AbilityData',{Abilities=frozen({[65]={name='Synthetic baseline ability'}},'AbilityData.Abilities'),
        isValid=function(id) return id==65 end})
    env.MiscData=namespace('MiscData',{TableData=frozen({growth={1,1},attack={2,2},effort={3,4},misc={4,3}},'MiscData.TableData'),
        getMonGender=function() return 0 end,getTotalItems=function() return 798 end,StatusCodeMap={[0]=''},Items={}})
    env.Utils=namespace('Utils',{bit_xor=function(a,b) return a ~ b end,
        getbits=function(a,start,width) return (a >> start) & ((1 << width)-1) end,
        formatSpecialCharacters=function(s) return s end,convertIVNumberToTable=function() return {} end,
        inlineIf=function(b,y,n) if b then return y else return n end end,
        isNilOrEmpty=function(s) return s==nil or s=='' end,toLowerUTF8=string.lower,
        getNatureMultiplier=function() return 1 end,getMovesLearnedHeader=function() return '',0,0 end,
        isSTAB=function() return false end})
    env.RouteData=namespace('RouteData',{hasRoute=function() return false end})
    env.TrackerAPI=namespace('TrackerAPI'); env.DataHelper=namespace('DataHelper')
    local backing=env
    env=setmetatable({},{__index=function(_,key)
        if backing[key]~=nil then return backing[key] end
        trap('global.'..tostring(key))()
    end,
        __newindex=function(_,key) trap('global.write.'..tostring(key))() end,__metatable=false})
    state.env=env
    function state.override(ns,key,value) assert(stores[ns][key]~=nil); stores[ns][key]=value end
    state.originals={}
    -- Trusted load is unavailable inside env. Only immutable reviewed text is compiled.
    for name,body in pairs(SOURCES) do
        assert(trustedLoad(body,'@PIN/'..name,'t',env))()
    end
    for name in pairs(SOURCES) do
        local ns,key=name:match('^(%w+)%.(%w+)$')
        local original=env[ns][key]; state.originals[name]=original
        env[ns][key]=function(...)
            counts[name]=(counts[name] or 0)+1; calls[name]=(calls[name] or 0)+1
            return original(...)
        end
    end
    -- Team update's positive path needs a pure verification dependency; the ORIGINAL
    -- verification function is tested separately and is blocked at Tracker.Data writes.
    state.verifyOriginal=env.Tracker.verifyDataForPlayer
    env.Tracker.verifyDataForPlayer=function(id) eq(id,24); calls.verifyStub=(calls.verifyStub or 0)+1 end
    function state.mon(id)
        return {personality=24,trainerID=24,pokemonID=id or 1,heldItem=0,level=50,isEgg=0,
            stats={hp=120},statStages={},moves={{id=33,pp=7},{id=0,pp=0},{id=0,pp=0},{id=0,pp=0}},
            curHP=73,nature=0,status=0,abilityNum=0,friendship=70,experience=1000}
    end
    -- Literal independent fixture: personality=OTID=24 => key zero; GAEM permutation.
    -- Physical field offsets are fixture declarations, not output-derived values.
    function state.row(base,id,personality,otid)
        for i=0,99 do state.bytes[base+i]=0 end
        state.put(base,4,personality or 24); state.put(base+4,4,otid or 24)
        state.put(base+8,1,255); state.put(base+32,2,id or 1)
        state.put(base+36,4,1000); state.put(base+44,2,33); state.put(base+52,1,7)
        state.put(base+84,4,0x00490032); state.put(base+88,4,0x003c0078)
        state.put(base+92,4,0x00460028); state.put(base+96,4,0x00500032)
        for _,offset in ipairs({0,4,32,36,40,44,48,52,56,60,72,80,84,88,92,96}) do state.allow(base+offset,4) end
        state.allow(base+8,1)
    end
    function state.emptyTeams()
        for _,base in ipairs({PLAYER,ENEMY}) do
            for slot=0,5 do
                for i=0,99 do state.bytes[base+slot*100+i]=0 end
                state.allow(base+slot*100,4); state.allow(base+slot*100+4,4)
            end
        end
    end
    state.emptyTeams()
    function state.indices(a,b,c,d)
        for i,value in ipairs({a,b,c or 0,d or 0}) do
            state.put(INDEX+(i-1)*2,2,value); state.allow(INDEX+(i-1)*2,1)
        end
    end
    locked=true
    return state
end

for _,id in ipairs({1,1294,906,1022}) do
    test('party','literal GAEM species '..id,function()
        local s=fresh(); s.row(s.PLAYER,id)
        local p=s.env.Program.readNewPokemon(s.PLAYER,24)
        eq(p.pokemonID,id); eq(p.level,50); eq(p.curHP,73); eq(p.stats.hp,120)
        eq(p.moves[1].id,33); eq(p.moves[1].pp,7); eq(p.trainerID,24)
    end)
end
test('party','nonzero XOR and GA ME shuffle control',function()
    local s=fresh(); s.row(s.PLAYER,1,25,24) -- key=1, permutation G A M E
    for _,pair in ipairs({{32,0},{36,1001},{40,1},{44,32},{48,1},{52,6},{56,1},{60,1},{68,1},{72,1}}) do
        s.put(s.PLAYER+pair[1],4,pair[2]); s.allow(s.PLAYER+pair[1],4)
    end
    local p=s.env.Program.readNewPokemon(s.PLAYER,25)
    eq(p.pokemonID,1); eq(p.experience,1000); eq(p.moves[1].id,33); eq(p.moves[1].pp,7)
end)
test('party','direct CFRU bytes interpreted through stock XOR',function()
    local s=fresh(); s.row(s.PLAYER,1294,24,25) -- direct bytes; stock key=1
    local p=s.env.Program.readNewPokemon(s.PLAYER,24)
    eq(p.pokemonID,1295); assert(p.pokemonID~=1294)
end,true)
test('party','Gen9 internal identity versus Dex collision remains distinct',function()
    local s=fresh(); s.row(s.PLAYER,1294)
    s.env.Program.GameData.PlayerTeam[1]=s.env.Program.readNewPokemon(s.PLAYER,24)
    local view=s.env.DataHelper.buildTrackerScreenDisplay(true)
    eq(view.p.id,1294); eq(view.p.name,'Synthetic Sprigatito')
    s.row(s.PLAYER,906); s.env.Program.GameData.PlayerTeam[1]=s.env.Program.readNewPokemon(s.PLAYER,24)
    eq(s.env.DataHelper.buildTrackerScreenDisplay(true).p.name,'Synthetic conflicting internal ID')
end)
test('party','six to one and empty slots clear',function()
    local s=fresh()
    for slot=0,5 do s.row(s.PLAYER+slot*100,1); s.row(s.ENEMY+slot*100,1) end
    s.env.Program.updatePokemonTeams()
    for i=1,6 do eq(s.env.Program.GameData.PlayerTeam[i].curHP,73); eq(s.env.Program.GameData.EnemyTeam[i].moves[1].pp,7) end
    s.emptyTeams(); s.row(s.PLAYER,1022); s.env.Program.updatePokemonTeams()
    eq(s.env.Program.GameData.PlayerTeam[1].pokemonID,1022)
    for i=2,6 do eq(s.env.Program.GameData.PlayerTeam[i],nil) end
    for i=1,6 do eq(s.env.Program.GameData.EnemyTeam[i],nil) end
end)
test('party','invalid occupied player and enemy retain old references',function()
    local s=fresh(); s.row(s.PLAYER,1); s.row(s.ENEMY,1); s.env.Program.updatePokemonTeams()
    local old=s.env.Program.GameData.PlayerTeam[1]; local other=s.env.Program.GameData.EnemyTeam[1]
    s.row(s.PLAYER,65535); s.row(s.ENEMY,65535); s.env.Program.updatePokemonTeams()
    eq(s.env.Program.GameData.PlayerTeam[1],old); eq(s.env.Program.GameData.EnemyTeam[1],other)
end,true)
test('party','invalid held item and move retain old data',function()
    for _,case in ipairs({{34,2,799},{44,2,65535}}) do
        local s=fresh(); s.row(s.PLAYER,1); s.env.Program.updatePokemonTeams()
        local old=s.env.Program.GameData.PlayerTeam[1]
        s.put(s.PLAYER+case[1],case[2],case[3]); s.env.Program.updatePokemonTeams()
        eq(s.env.Program.GameData.PlayerTeam[1],old)
    end
end,true)
test('party','enemy PP replaced outside battle',function()
    local s=fresh(); s.env.Battle.inBattleScreen=false; s.row(s.ENEMY,1)
    s.env.Program.updatePokemonTeams(); eq(s.env.Program.GameData.EnemyTeam[1].moves[1].pp,35)
end,true)
test('party','missing static maximum PP becomes nil',function()
    local s=fresh(); s.env.Battle.inBattleScreen=false; s.row(s.ENEMY,1)
    s.override('MoveData','Moves',{[33]={name='Synthetic move'}})
    s.env.Program.updatePokemonTeams(); eq(s.env.Program.GameData.EnemyTeam[1].moves[1].pp,nil)
end,true)
for _,case in ipairs({{0x0105,6,'poisoned u16 high byte'},{6,1,'illegal slot clamped to lead'}}) do
    test('battle',case[3],function()
        local s=fresh(); s.indices(case[1],0); s.env.Battle.updateViewSlots()
        eq(s.env.Battle.Combatants.LeftOwn,case[2]); eq(#s.readLog,2); eq(s.readLog[1][1],1)
    end,true)
end
test('battle','four slots and byte read stride',function()
    local s=fresh(); s.env.Battle.numBattlers=4; s.indices(0,1,2,5); s.env.Battle.updateViewSlots()
    eq(s.env.Battle.Combatants.LeftOwn,1); eq(s.env.Battle.Combatants.LeftOther,2)
    eq(s.env.Battle.Combatants.RightOwn,3); eq(s.env.Battle.Combatants.RightOther,6)
    for i,r in ipairs(s.readLog) do eq(r[1],1); eq(r[2],s.INDEX+(i-1)*2) end
end)
test('battle','switch callback trapped before uncontrolled dependency',function()
    local s=fresh(); s.indices(1,0); s.env.Battle.BattleParties[0][1]={}
    denied(function() s.env.Battle.updateViewSlots() end,'Battle.resetAbilityMapPokemon')
end)
test('battle','singles retains former doubles right slot',function()
    local s=fresh(); s.env.Battle.numBattlers=4; s.indices(0,0,5,5); s.env.Battle.updateViewSlots()
    s.env.Battle.numBattlers=2; s.indices(0,0); s.env.Battle.updateViewSlots()
    eq(s.env.Battle.Combatants.RightOwn,6)
end,true)
test('api','party versus effective active battle and shared references',function()
    local s=fresh(); local own=s.mon(1294); local enemy=s.mon(1)
    s.env.Program.GameData.PlayerTeam[1]=own; s.env.Program.GameData.EnemyTeam[1]=enemy
    local syntheticBattle={pokemonID=1294,curHP=11,ability=254,moves={{id=33,pp=2}}}
    local out=s.env.TrackerAPI.getActiveBattlePokemon()
    eq(out[1],own); eq(out[2],enemy); eq(out[1].curHP,73); assert(out[1].curHP~=syntheticBattle.curHP)
    out[1].curHP=999; eq(s.env.TrackerAPI.getPlayerPokemon().curHP,999)
    eq(s.env.TrackerAPI.getEnemyPokemon(),enemy)
end,true)
test('api','explicit invalid slots do not return a fabricated team member',function()
    local s=fresh(); s.env.Program.GameData.PlayerTeam[1]=s.mon(1)
    for _,slot in ipairs({0,7,-1,1.5}) do eq(s.env.TrackerAPI.getPlayerPokemon(slot),nil) end
end)
test('api','battle end empties active API but enemy party survives',function()
    local s=fresh(); local old=s.mon(1); s.env.Program.GameData.EnemyTeam[1]=old
    eq(s.env.TrackerAPI.getActiveBattlePokemon()[2],old)
    s.env.Battle.inBattleScreen=false
    eq(next(s.env.TrackerAPI.getActiveBattlePokemon()),nil); eq(s.env.TrackerAPI.getEnemyPokemon(),old)
end,true)
test('api','four battlers select party slots explicitly',function()
    local s=fresh(); s.env.Battle.numBattlers=4
    for i=1,2 do s.env.Program.GameData.PlayerTeam[i]=s.mon(i==1 and 1 or 1022); s.env.Program.GameData.EnemyTeam[i]=s.mon(1294) end
    local out=s.env.TrackerAPI.getActiveBattlePokemon(); eq(#out,4); eq(out[3].pokemonID,1022)
end)
test('api','reset output session replacement cannot revoke old table references',function()
    local s=fresh(); s.env.Program.GameData.PlayerTeam[1]=s.mon(1)
    local old=s.env.TrackerAPI.getPlayerPokemon()
    for _,transition in ipairs({'reset','output-switch','session-switch'}) do
        s.env.Program.GameData.PlayerTeam={}; s.env.Program.GameData.EnemyTeam={}
        eq(s.env.TrackerAPI.getPlayerPokemon(),nil); eq(old.pokemonID,1)
    end
    -- These are synthetic owner replacement stimuli, NOT execution of stock lifecycle.
end,true)
test('display','safe regional display and independent move copy',function()
    local s=fresh(); s.env.Battle.inBattleScreen=false; s.env.Program.GameData.PlayerTeam[1]=s.mon(1022)
    local out=s.env.DataHelper.buildTrackerScreenDisplay(true)
    eq(out.p.id,1022); eq(out.p.name,'Synthetic Raichu regional'); eq(out.p.types[1],13); eq(out.p.types[2],14)
    eq(out.m.moves[1].pp,7); out.m.moves[1].power='999'; eq(s.env.MoveData.Moves[33].power,'40')
end)
test('display','unknown effective ability falls back to baseline selection',function()
    local s=fresh(); local p=s.mon(1294); p.ability=nil; p.effectiveAbilityConfidence='UNKNOWN'
    s.env.Program.GameData.PlayerTeam[1]=p
    eq(s.env.DataHelper.buildTrackerScreenDisplay(true).p.line2,'Synthetic baseline ability')
end,true)
test('display','missing effective PP category power replaced by static catalog',function()
    local s=fresh(); s.env.Program.GameData.PlayerTeam[1]=s.mon(1294)
    local m=s.env.DataHelper.buildTrackerScreenDisplay(true).m.moves[1]
    eq(m.pp,7); eq(m.category,0); eq(m.power,'40'); eq(m.effectiveMaxPP,nil)
end,true)
test('display','missing catalog category remains absent',function()
    local s=fresh(); s.override('MoveData','Moves',{[33]={id=33,name='Synthetic move',pp='35'}})
    s.env.Program.GameData.PlayerTeam[1]=s.mon(1)
    eq(s.env.DataHelper.buildTrackerScreenDisplay(true).m.moves[1].category,nil)
end)
test('display','invalid map hides fields via stock default dependency',function()
    local s=fresh(); s.override('Program','isValidMapLocation',function() return false end)
    s.env.Program.GameData.PlayerTeam[1]=s.mon(1294)
    local out=s.env.DataHelper.buildTrackerScreenDisplay(true); eq(out.p.id,0); eq(out.x.infoIsHidden,true)
end)
test('display','enemy notes path refused',function()
    local s=fresh(); s.env.Program.GameData.EnemyTeam[1]=s.mon(1)
    denied(function() s.env.DataHelper.buildTrackerScreenDisplay(false) end,'Tracker.getAbilities')
end)
test('safety','real begin battle traps early save state before hook or memory',function()
    local s=fresh(); s.env.Battle.inBattleScreen=false
    denied(function() s.env.Battle.beginNewBattle() end,'GameOverScreen.createTempSaveState')
    eq(#s.readLog,0); eq(s.env.Battle.inBattleScreen,false)
end)
test('safety','real save and load blocked at file boundary',function()
    local s=fresh()
    denied(function() s.env.Tracker.saveData('SYNTHETIC.tdat') end,'FileManager.writeTableToFile')
    denied(function() s.env.Tracker.loadData('SYNTHETIC.tdat',true) end,'FileManager.extractFileExtensionFromPath')
end)
test('safety','real player verification persistence mutation trapped',function()
    local s=fresh(); denied(function() s.verifyOriginal(24) end,'Tracker.Data.mutation')
end)
test('safety','team update persistence and capture seams cannot escape',function()
    local s=fresh(); s.env.Battle.inBattleScreen=false; s.row(s.PLAYER,1)
    denied(function() s.env.Program.updatePokemonTeams() end,'GachaMonData.tryAddToRecentMons')
    s=fresh(); s.row(s.PLAYER,1); s.override('Tracker','verifyDataForPlayer',s.verifyOriginal)
    denied(function() s.env.Program.updatePokemonTeams() end,'Tracker.Data.mutation')
end)
for _,namespace in ipairs({'memory','Memory','io','os','package','debug','socket','http','emu','event','client','forms','gui','savestate','FileManager','CustomCode'}) do
    test('safety',namespace..' explicit forbidden call',function()
        local s=fresh(); local method=({memory='write_u8',Memory='writebyte',io='open',os='execute',
            package='loadlib',debug='getregistry',socket='connect',http='request',emu='frameadvance',event='onexit',
            client='getversion',forms='newform',gui='drawText',savestate='load',FileManager='readTableFromFile',CustomCode='afterBattleBegins'})[namespace]
        denied(function() s.env[namespace][method]() end,namespace..'.'..method)
    end)
end
for _,name in ipairs({'require','load','loadfile','dofile','loadstring','rawset','rawget','setmetatable','getmetatable','_G'}) do
    test('safety','loader/reflection '..name,function()
        local s=fresh(); denied(function() s.env[name]() end,name)
    end)
end
test('safety','all arbitrary memory writes and save-state calls refused',function()
    local s=fresh()
    for _,n in ipairs({'write_u16_le','write_u32_le','write_bytes_as_array'}) do denied(function() s.env.memory[n]() end,'memory.'..n) end
    denied(function() s.env.savestate.save() end,'savestate.save')
end)
test('safety','wrong address width domain and truncation refused',function()
    local s=fresh(); s.row(s.PLAYER,1)
    denied(function() s.env.Memory.readbyte(s.PLAYER) end,'read.address-width')
    denied(function() s.env.Memory.readdword(s.PLAYER,'EWRAM') end,'read.domain')
    denied(function() s.env.Memory.readdword(-1) end,'read.address-width')
    s.bytes[s.PLAYER+1]=nil
    denied(function() s.env.Memory.readdword(s.PLAYER) end,'read.truncated')
end)
test('safety','global and immutable dependency mutation refused',function()
    local s=fresh()
    denied(function() s.env.invented={} end,'global.write.invented')
    denied(function() s.env.io={} end,'global.write.io')
    denied(function() return s.env.invented end,'global.invented')
    denied(function() s.env.GameSettings.pstats=0 end,'GameSettings.mutation')
    denied(function() s.env.math.floor=function() end end,'math.mutation')
    denied(function() s.env.Tracker.BattleNotes.any={} end,'Tracker.BattleNotes.mutation')
end)
test('safety','fresh environments do not inherit previous teams or wrappers',function()
    local a=fresh(); local foreign=function() return 'foreign' end
    a.override('TrackerAPI','getPlayerPokemon',foreign)
    local b=fresh(); eq(b.env.TrackerAPI.getPlayerPokemon(),nil); eq(a.env.TrackerAPI.getPlayerPokemon,foreign)
    -- No production wrapper installation/unload is claimed here.
end)

test('safety','compiled hostile fixture resolves only restricted environment',function()
    local s=fresh()
    for _,case in ipairs({{'io.open("SYNTHETIC")','io.open'},
        {'os.execute("SYNTHETIC")','os.execute'}, {'require("foreign")','require'},
        {'memory.write_u8(1,1)','memory.write_u8'}, {'savestate.save()','savestate.save'},
        {'io={}','global.write.io'},
        {'("x").dump(function() end)','string.dump'},
        {'Memory.readbyte=function() return 0 end','Memory.unapproved-write.readbyte'}, {'Tracker.Data.isNewGame=false','Tracker.Data.mutation'},
        {'local _,backing=pairs(Tracker.Data); assert(backing==nil)','SAFE'}}) do
        local chunk=assert(trustedLoad(case[1],'@deliberate-negative-fixture','t',s.env))
        if case[2]=='SAFE' then chunk() else denied(chunk,case[2]) end
    end
end)

local failed, hazards, totals=0,0,{}
-- Trusted hook enforces an instruction budget; debug/reflection is absent in env.
for _,t in ipairs(tests) do
    local budget=0
    trustedHook(function() budget=budget+1; if budget>2000 then error('Instruction budget exceeded') end end,'',1000)
    local ok,why=pcall(t[3]); trustedHook()
    totals[t[1]]=(totals[t[1]] or 0)+1
    if not ok then failed=failed+1; print('FAIL',t[1],t[2],why)
    else
        if t[4] then hazards=hazards+1 end
        print(t[4] and 'EXPECTED_STOCK_HAZARD' or 'PASS',t[1],t[2],'TEST_ONLY','liveConfidence=UNKNOWN')
    end
end
local function keys(t) local out={} for k in pairs(t) do out[#out+1]=k end table.sort(out); return out end
for _,name in ipairs(keys(SOURCES)) do
    assert((counts[name] or 0)>0,'No execution coverage: '..name)
    print('FUNCTION_EXECUTIONS',name,counts[name])
end
for _,name in ipairs(keys(traps)) do print('CONFIRMED_TRAP',name,traps[name]) end
for _,class in ipairs(keys(totals)) do print('CLASS',class,totals[class]) end
print('NOT_RUN stock lifecycle/reset/output/session hooks; production wrapper ownership; complete enemy display; BattleDetails; TrackerScreen rendering; real host; Lua 5.1')
print('RESULT',#tests-failed,'PASS',failed,'FAIL',hazards,'EXPECTED_STOCK_HAZARD','TEST_ONLY','liveConfidence=UNKNOWN','production=DENIED')
assert(failed==0,'Unexpected sandbox failures')
