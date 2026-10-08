-- #711 extends #707's SHA-locked controls. No original body is changed.
local bridgeStates,oracleStates={},{}
local seams={"Program.updatePokemonTeams","Program.readNewPokemon","Battle.updateViewSlots","Battle.beginNewBattle"}
local oracleNames={"TrackerAPI.getPlayerPokemon","TrackerAPI.getEnemyPokemon","TrackerAPI.getActiveBattlePokemon","Battle.getViewedPokemon"}
local function clone(t)
    if type(t)~="table" then return t end
    local out={}; for k,v in pairs(t) do out[k]=clone(v) end; return out
end
local function bytes(n,w)
    local out={}; for i=1,w do out[i]=string.char(n%256); n=math.floor(n/256) end
    return table.concat(out)
end
local function patch(s,o,w,n) return s:sub(1,o)..bytes(n,w)..s:sub(o+w+1) end
local function partyBytes(ids)
    local s=string.rep("\0",600)
    -- Literal CFRU Pokemon ABI, include/pokemon.h; direct source T1 ARM layout.
    for i,id in ipairs(ids) do
        for _,f in ipairs({{0,4,24},{4,4,25},{32,2,id},{34,2,743},{44,2,33},
            {52,1,7},{80,4,32},{84,1,50},{86,2,73},{88,2,120}}) do
            s=patch(s,(i-1)*100+f[1],f[2],f[3])
        end
    end
    return {bytes=s,count=#ids}
end
local function battleBytes(ids)
    local s=string.rep("\0",352)
    -- Literal BattlePokemon ABI include/battle.h: 0x58-byte rows, separate HP/PP.
    for i,id in ipairs(ids) do
        for _,f in ipairs({{0,2,id},{12,2,33},{32,1,254},{33,1,12},{34,1,12},
            {24,1,12},{36,1,2},{40,2,11},{42,1,51},{44,2,121},{46,2,744},{76,4,16}}) do
            s=patch(s,(i-1)*88+f[1],f[2],f[3])
        end
    end
    return s
end
local function fixture(install)
    local s=fresh(); local host={Program={},Battle={},Lifecycle={startTracker=function() error("STOCK_RESTART") end}}
    local expected={}
    for _,name in ipairs(seams) do
        local ns,key=name:match("^(%w+)%.(%w+)$")
        host[ns][key]=s.env[ns][key]; expected[name]=host[ns][key]
    end
    local d,why=bridgeModule.newMock(host,expected,SOURCES,MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
    assert(d,why and why.reason); s.host,s.expected,s.bridge=host,expected,d
    bridgeStates[#bridgeStates+1]=s
    if install~=false then d.installMock() end
    return s
end
local function arm(s,opts)
    opts=opts or {}; local d=s.bridge
    local declaration={epoch=d.statusMock().epoch+1,output="fixture-output",session="fixture-session",
        encounter=opts.outside and false or "fixture-battle",profileId=d.profileId,
        trackerPin="c450ecaee2d8131a2789bb656e3be792a93712fb",evidence="SYNTHETIC_ONLY"}
    -- Lua's and/or idiom cannot represent false here.
    if opts.outside then declaration.encounter=false end
    s.host.session=clone(declaration)
    local _,be=d.transitionMock(opts.event or "start",declaration)
    local sample={before=declaration,after=clone(declaration),sampleId=1,
        player=partyBytes(opts.ids or {1294})}
    if not opts.outside then
        sample.enemy=partyBytes(opts.enemyIds or {1})
        local context={epoch=be,state="ACTIVE",output=declaration.output,battle=declaration.encounter,
            flags=bytes(opts.flags or 4,4),count=bytes(2,1),positions=bytes(0,1)..bytes(1,1)..bytes(255,1)..bytes(255,1),
            indexes=bytes(opts.playerIndex or 0,2)..bytes(opts.enemyIndex or 0,2)..bytes(65535,2)..bytes(65535,2)}
        sample.battle={epoch=be,before=context,after=clone(context),battleMons=battleBytes(opts.activeIds or {1294,1}),
            ppCaps=bytes(35,1)..string.rep("\0",3)..bytes(35,1)..string.rep("\0",11)}
    end
    return sample
end
local function accepted(s,opts)
    local sample=arm(s,opts); local r=s.bridge.submitMock(sample); assert(r.ready,r.reason)
    return r.ticket,sample
end
local function label(r)
    eq(r.evidence,"TEST_ONLY"); eq(r.liveConfidence,"UNKNOWN"); eq(r.production,"DENIED")
    eq(r.validity,"HISTORICAL_COPY_REQUERY_REQUIRED")
end
local function nonready(r,state)
    label(r); eq(r.ready,false); eq(r.value,nil); eq(r.confidence,state or "UNKNOWN")
end
local function field(f,state,value)
    label(f); eq(f.confidence,state); eq(f.value,value)
    assert(f.reason and f.provenance and f.scope and f.sampleEpoch and f.profileId)
end
local function zero(s)
    for _,name in ipairs(seams) do eq(s.calls[name] or 0,0) end
    eq(#s.readLog,0); eq(#s.violations,0)
    eq(next(s.env.Program.GameData.PlayerTeam),nil); eq(next(s.env.Program.GameData.EnemyTeam),nil)
end
local function view(s,t,team,slot,mode)
    return s.bridge.selectMock(t,team or "PLAYER",slot or 1,mode or "PARTY")
end
for _,id in ipairs({1,1102,1294,1022}) do
    test("bridge","independent Gen1/Gen8/Gen9/regional internal ID "..id,function()
        local s=fixture(); local t=accepted(s,{outside=true,ids={id}}); local p=view(s,t)
        field(p.pokemonID,"VERIFIED",id); field(p.curHP,"VERIFIED",73); field(p.stats.hp,"VERIFIED",120)
        field(p.level,"VERIFIED",50); field(p.heldItem,"VERIFIED",743); field(p.moves[1].id,"VERIFIED",33)
        field(p.moves[1].pp,"VERIFIED",7); field(p.occupied,"VERIFIED",true)
        eq(p.speciesIdentity.value.id,id); assert(p.speciesIdentity.scope:find("source-baseline",1,true))
        field(p.abilityID,"UNKNOWN",nil); field(p.abilityName,"UNKNOWN",nil)
        for _,k in ipairs({"personality","trainerID","abilityNum","nature","experience","nickname","statStages"}) do field(p[k],"UNKNOWN",nil) end
        for _,k in ipairs({"maxPP","power","category","type","accuracy"}) do field(p.moves[1][k],"UNKNOWN",nil) end
        zero(s)
    end)
end
test("bridge","known empty slot and absent move differ from unknown",function()
    local s=fixture(); local t=accepted(s,{outside=true}); local empty=view(s,t,"PLAYER",6)
    field(empty.occupied,"VERIFIED",false); field(empty.pokemonID,"VERIFIED",0)
    field(empty.curHP,"UNAVAILABLE",nil); field(empty.moves[1].id,"UNAVAILABLE",nil)
    local p=view(s,t); field(p.moves[2].id,"VERIFIED",0); field(p.moves[2].pp,"VERIFIED",0)
    field(p.moves[2].maxPP,"UNKNOWN",nil); zero(s)
end)
test("bridge","party versus active precedence HP 73/11 PP 7/2 item status level types",function()
    local s=fixture(); local t=accepted(s); local p=view(s,t); local a=view(s,t,"PLAYER",1,"ACTIVE")
    field(p.curHP,"VERIFIED",73); field(a.curHP,"VERIFIED",11)
    field(p.moves[1].pp,"VERIFIED",7); field(a.moves[1].pp,"VERIFIED",2)
    field(a.stats.hp,"VERIFIED",121); field(a.level,"VERIFIED",51); field(a.heldItem,"VERIFIED",744)
    eq(p.status.value.raw,32); eq(p.status.value.primary,"FROSTBITE")
    eq(a.status.value.raw,16); eq(a.status.value.primary,"BURN")
    field(a.abilityID,"VERIFIED",254); field(a.abilityName,"UNKNOWN",nil); field(a.abilityNum,"UNKNOWN",nil)
    for i=1,3 do field(a.types[i],"VERIFIED",12); field(p.types[i],"UNKNOWN",nil) end
    for _,k in ipairs({"maxPP","power","category","type"}) do field(a.moves[1][k],"UNKNOWN",nil) end
    assert(a.curHP.provenance:find("BattlePokemon",1,true)); assert(p.curHP.provenance:find("Pokemon",1,true))
    zero(s)
end)
test("bridge","active form identity never replaces separate party identity",function()
    local s=fixture(); local t=accepted(s,{activeIds={1022,1102}})
    field(view(s,t).pokemonID,"VERIFIED",1294)
    field(view(s,t,"PLAYER",1,"ACTIVE").pokemonID,"VERIFIED",1022)
    field(view(s,t,"ENEMY",1).pokemonID,"VERIFIED",1)
    field(view(s,t,"ENEMY",1,"ACTIVE").pokemonID,"VERIFIED",1102); zero(s)
end)
test("bridge","side-specific u16 indexes select player slot 6 and enemy slot 2",function()
    local s=fixture(); local t=accepted(s,{ids={1,1102,1022,26,1439,1294},enemyIds={1102,1},playerIndex=5,enemyIndex=1})
    local c=s.bridge.contextMock(t); field(c.playerSlot,"VERIFIED",6); field(c.enemySlot,"VERIFIED",2)
    field(view(s,t,"PLAYER",6,"ACTIVE").slot,"VERIFIED",6)
    field(view(s,t,"ENEMY",2,"ACTIVE").slot,"VERIFIED",2)
    nonready(view(s,t,"PLAYER",1,"ACTIVE"),"UNAVAILABLE"); zero(s)
end)
test("bridge","supported trainer context does not fabricate trainer A/B identity",function()
    local s=fixture(); local t=accepted(s,{flags=12}); local c=s.bridge.contextMock(t)
    eq(c.context.value.kind,"TRAINER"); field(c.trainerA,"UNKNOWN",nil); field(c.trainerB,"UNAVAILABLE",nil); zero(s)
end)
test("bridge","enemy and active unavailable outside encounter",function()
    local s=fixture(); local t=accepted(s,{outside=true})
    nonready(view(s,t,"ENEMY",1),"UNAVAILABLE"); nonready(view(s,t,"PLAYER",1,"ACTIVE"),"UNAVAILABLE")
    eq(s.bridge.contextMock(t).inBattle,false); field(view(s,t).curHP,"VERIFIED",73); zero(s)
end)
for _,slot in ipairs({0,7,-1,1.5,math.huge}) do
    test("bridge-negative","invalid one-based slot "..slot.." never clamps",function()
        local s=fixture(); local t=accepted(s); nonready(view(s,t,"PLAYER",slot)); zero(s)
    end)
end
local negatives={
    {"invalid occupied row",function(s) s.player.bytes=patch(s.player.bytes,32,2,65535) end},
    {"truncated party",function(s) s.player.bytes="short" end},
    {"truncated active",function(s) s.battle.battleMons="short" end},
    {"poisoned u16 0x0105",function(s) s.battle.before.indexes=bytes(0x0105,2)..s.battle.before.indexes:sub(3); s.battle.after=clone(s.battle.before) end},
    {"illegal zero-based slot 6",function(s) s.battle.before.indexes=bytes(6,2)..s.battle.before.indexes:sub(3); s.battle.after=clone(s.battle.before) end},
    {"missing effective PP caps",function(s) s.battle.ppCaps=nil end},
    {"missing active ability",function(s) s.battle.battleMons=patch(s.battle.battleMons,32,1,255) end},
    {"missing active HP",function(s) s.battle.battleMons=patch(s.battle.battleMons,44,2,0) end},
    {"active PP above declared cap",function(s) s.battle.battleMons=patch(s.battle.battleMons,36,1,36) end},
    {"unknown flags",function(s) s.battle.before.flags=bytes(0x80000004,4); s.battle.after=clone(s.battle.before) end},
    {"missing trainer master flag",function(s) s.battle.before.flags=bytes(8,4); s.battle.after=clone(s.battle.before) end},
    {"caller trusted trainer A",function(s) s.battle.before.trainerA={trusted=true}; s.battle.after=clone(s.battle.before) end},
    {"caller trainer B",function(s) s.battle.before.trainerB={trusted=true}; s.battle.after=clone(s.battle.before) end},
    {"wrong profile",function(s) s.before.profileId="stock"; s.after=clone(s.before) end},
    {"wrong pin",function(s) s.before.trackerPin=string.rep("0",40); s.after=clone(s.before) end},
    {"foreign session",function(s) s.before.session="other"; s.after=clone(s.before) end},
    {"changing sample",function(s) s.after.output="foreign" end},
    {"replay",function(s) s.sampleId=1 end},
    {"predecoded verified table",function(s) s.player={bytes={confidence="VERIFIED"},count=1} end},
    {"caller readMock closure",function(s) s.readMock=function() error("UNTRUSTED_CALLBACK") end end},
    {"sample metatable",function(s) setmetatable(s,{__index=function() error("CALLER_CALLBACK") end}) end},
}
for _,case in ipairs(negatives) do
    test("bridge-negative",case[1].." revokes every current view",function()
        local s=fixture(); local t,sample=accepted(s); local old=view(s,t)
        sample.sampleId=2; case[2](sample); nonready(s.bridge.submitMock(sample))
        nonready(view(s,t)); nonready(s.bridge.contextMock(t)); field(old.curHP,"VERIFIED",73); zero(s)
    end)
end
for _,flags in ipairs({5,13,0x4F,0x20000D,0x40000D}) do
    test("bridge-negative","explicit unsupported flags "..flags.." expose UNAVAILABLE without any value",function()
        local s=fixture(); local t,sample=accepted(s); sample.sampleId=2
        sample.battle.before.flags=bytes(flags,4); sample.battle.before.count=bytes(4,1)
        sample.battle.before.positions=bytes(0,1)..bytes(1,1)..bytes(2,1)..bytes(3,1)
        sample.battle.before.indexes=string.rep("\0",8); sample.battle.after=clone(sample.battle.before)
        nonready(s.bridge.submitMock(sample),"UNAVAILABLE"); nonready(view(s,t),"UNAVAILABLE"); zero(s)
    end)
end
for _,event in ipairs({"start","end","switch","reset","reload","output","session","invalid"}) do
    test("bridge-lifecycle",event.." invalidates historical tickets",function()
        local s=fixture(); local t=accepted(s); local old=view(s,t)
        s.bridge.transitionMock(event); nonready(view(s,t)); eq(old.curHP.value,73); label(old)
        local nt=accepted(s,{event="session"}); nonready(view(s,t)); field(view(s,nt).curHP,"VERIFIED",73); zero(s)
    end)
end
for _,key in ipairs({"profileId","trackerPin","session","output","encounter","epoch"}) do
    test("bridge-lifecycle","every request rechecks unannounced "..key,function()
        local s=fixture(); local t=accepted(s); s.host.session[key]=key=="epoch" and 999 or "foreign"
        nonready(view(s,t)); nonready(s.bridge.contextMock(t)); zero(s)
    end)
end
test("bridge-lifecycle","same-epoch sample supersedes bridge ticket and failed replay clears",function()
    local s=fixture(); local t,sample=accepted(s); local epoch=s.bridge.statusMock().epoch
    sample.sampleId=2; sample.player.bytes=patch(sample.player.bytes,86,2,72)
    local r=s.bridge.submitMock(sample); assert(r.ready,r.reason); eq(r.epoch,epoch)
    nonready(view(s,t)); field(view(s,r.ticket).curHP,"VERIFIED",72)
    nonready(s.bridge.submitMock(sample)); nonready(view(s,r.ticket)); zero(s)
end)
test("bridge-lifecycle","six to one slots and enemy end clear without retained fallback",function()
    local s=fixture(); local t=accepted(s,{ids={1,1102,1022,26,1439,1294},playerIndex=5})
    local nt=accepted(s,{outside=true}); nonready(view(s,t)); field(view(s,nt,"PLAYER",6).occupied,"VERIFIED",false)
    field(view(s,nt,"PLAYER",6).curHP,"UNAVAILABLE",nil); nonready(view(s,nt,"ENEMY",1),"UNAVAILABLE"); zero(s)
end)
test("bridge-lifecycle","readonly and rawset contamination cannot reach source; foreign tickets denied",function()
    local s=fixture(); local t=accepted(s); local p=view(s,t)
    local ok,why=pcall(function() p.curHP.value=999 end); eq(ok,false); eq(why,"READ_ONLY_TEST_VIEW")
    rawset(p.curHP,"value",999); eq(p.curHP.value,999); field(view(s,t).curHP,"VERIFIED",73)
    nonready(view(s,{})); t.value={confidence="VERIFIED"}; nonready(view(s,t)); zero(s)
end)
test("bridge-lifecycle","foreign bridge reference and guard-issued ticket cannot be adopted",function()
    local a,b=fixture(),fixture(); local ta=accepted(a); local tb=accepted(b)
    nonready(view(a,tb)); nonready(view(b,ta)); nonready(view(a,a.host.Program.readNewPokemon().ticket))
    field(view(a,ta).pokemonID,"VERIFIED",1294); zero(a); zero(b)
end)
for _,name in ipairs(seams) do
    test("bridge-ownership","foreign wrapper "..name.." rechecked and preserved on unload",function()
        local s=fixture(); local t=accepted(s); local ns,key=name:match("^(%w+)%.(%w+)$")
        local foreign=function() error("FOREIGN_CALLBACK") end; s.host[ns][key]=foreign
        nonready(view(s,t)); s.bridge.teardownMock(); eq(s.host[ns][key],foreign); zero(s)
    end)
end
for _,ns in ipairs({"Program","Battle","Lifecycle"}) do
    test("bridge-ownership","namespace takeover "..ns.." invalidates fields",function()
        local s=fixture(); local t=accepted(s); s.host[ns]={}; nonready(view(s,t)); s.bridge.teardownMock(); zero(s)
    end)
end
test("bridge-ownership","restart owner takeover revokes",function()
    local s=fixture(); local t=accepted(s); s.host.Lifecycle.startTracker=function() error("FOREIGN_RESTART") end
    nonready(view(s,t)); zero(s)
end)
test("bridge-ownership","duplicate install unload and factory cannot reopen",function()
    local s=fixture(); local t=accepted(s); s.bridge.installMock(); nonready(view(s,t))
    local other,why=bridgeModule.newMock(s.host,s.expected,SOURCES,MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
    eq(other,nil); eq(why.confidence,"UNKNOWN")
    s.bridge.teardownMock(); s.bridge.teardownMock(); nonready(view(s,t)); s.bridge.installMock(); nonready(view(s,t)); zero(s)
end)
for i=1,4 do
    test("bridge-ownership","transaction failure "..i.." never publishes fields",function()
        local s=fixture(false); s.bridge.installMock({after=i,mode="throw"}); nonready(view(s,{}))
        for _,name in ipairs(seams) do local ns,key=name:match("^(%w+)%.(%w+)$"); eq(s.host[ns][key]().ready,false) end
        zero(s)
    end)
end
for _,which in ipairs({"profile","source","multi","body"}) do
    test("bridge-source",which.." drift fails internal construction",function()
        local s=fixture(false); local raw,texts,multi,bodies=MOCK_SOURCE,clone(MOCK_PUBLIC_SOURCES),MOCK_MULTI,clone(SOURCES)
        if which=="profile" then raw="{}" elseif which=="source" then texts["CFRU:include/pokemon.h"]="wrong"
        elseif which=="multi" then multi="wrong" else bodies["Battle.beginNewBattle"]="wrong" end
        local d,why=bridgeModule.newMock(s.host,s.expected,bodies,raw,texts,multi)
        eq(d,nil); eq(why.confidence,"UNKNOWN"); zero(s)
    end)
end
-- Trusted synthetic facade: replaces these dependencies ONLY in a fresh #707 env.
-- Tracker.getPokemon and Battle.inActiveBattle are stubs, never original coverage.
local function oracle(s,t,mode)
    local state=fresh(); local c=s.bridge.contextMock(t); assert(c.ready)
    state.fixtureNamespace("Tracker",{getPokemon=function(slot,own)
        local r=s.bridge.selectMock(t,own and "PLAYER" or "ENEMY",slot,mode)
        if r.ready and r.occupied.value then return r end
        return nil
    end})
    state.fixtureNamespace("Battle",{
        inActiveBattle=function() local now=s.bridge.contextMock(t); return now.ready and now.inBattle end,
        numBattlers=c.inBattle and 2 or 0,isViewingLeft=true,isViewingOwn=true,
        Combatants={LeftOwn=c.inBattle and c.playerSlot.value or 1,LeftOther=c.inBattle and c.enemySlot.value or nil}})
    -- No catalog/default/persistence path exists in this oracle environment.
    for _,ns in ipairs({"Program","PokemonData","MoveData","AbilityData","DataHelper","MiscData","GameSettings"}) do
        state.fixtureNamespace(ns,{})
    end
    -- Install only immutable original accessor closures captured by #707 fresh().
    state.fixtureNamespace("TrackerAPI",{
        getPlayerPokemon=function(...) state.calls[oracleNames[1]]=(state.calls[oracleNames[1]] or 0)+1; return state.originals[oracleNames[1]](...) end,
        getEnemyPokemon=function(...) state.calls[oracleNames[2]]=(state.calls[oracleNames[2]] or 0)+1; return state.originals[oracleNames[2]](...) end,
        getActiveBattlePokemon=function(...) state.calls[oracleNames[3]]=(state.calls[oracleNames[3]] or 0)+1; return state.originals[oracleNames[3]](...) end})
    local b=state.env.Battle
    state.fixtureNamespace("Battle",{inActiveBattle=b.inActiveBattle,numBattlers=b.numBattlers,
        isViewingLeft=true,isViewingOwn=true,Combatants=b.Combatants,
        getViewedPokemon=function(...) state.calls[oracleNames[4]]=(state.calls[oracleNames[4]] or 0)+1; return state.originals[oracleNames[4]](...) end})
    oracleStates[#oracleStates+1]=state
    return state
end
for _,mode in ipairs({"PARTY","ACTIVE"}) do
    test("bridge-original",mode.." facade executes four unchanged pinned selection bodies",function()
        local s=fixture(); local t=accepted(s,{ids={1,1102,1022,26,1439,1294},enemyIds={1102,1},playerIndex=5,enemyIndex=1})
        local o=oracle(s,t,mode); local api=o.env.TrackerAPI
        local p,e=api.getPlayerPokemon(),api.getEnemyPokemon()
        field(p.slot,"VERIFIED",6); field(e.slot,"VERIFIED",2)
        field(p.curHP,"VERIFIED",mode=="ACTIVE" and 11 or 73)
        local list=api.getActiveBattlePokemon(); eq(#list,2); eq(list[3],nil); eq(list[4],nil)
        field(list[1].moves[1].pp,"VERIFIED",mode=="ACTIVE" and 2 or 7)
        eq(o.env.Battle.getViewedPokemon(true).team.value,"PLAYER")
        o.env.Battle.isViewingOwn=false; eq(o.env.Battle.getViewedPokemon().team.value,"ENEMY")
        eq(api.getPlayerPokemon(7),nil); eq(api.getEnemyPokemon(0),nil)
        if mode=="ACTIVE" then eq(api.getPlayerPokemon(1),nil) else field(api.getPlayerPokemon(1).pokemonID,"VERIFIED",1) end
        s.bridge.transitionMock("end"); eq(api.getPlayerPokemon(),nil); eq(api.getEnemyPokemon(),nil)
        eq(#api.getActiveBattlePokemon(),0); eq(o.env.Battle.getViewedPokemon(),nil)
        eq(#o.readLog,0); eq(#o.violations,0); zero(s)
    end)
end
test("bridge-original","outside battle original getters retain player only",function()
    local s=fixture(); local t=accepted(s,{outside=true}); local o=oracle(s,t,"PARTY")
    field(o.env.TrackerAPI.getPlayerPokemon().pokemonID,"VERIFIED",1294)
    eq(o.env.TrackerAPI.getEnemyPokemon(),nil); eq(#o.env.TrackerAPI.getActiveBattlePokemon(),0)
    field(o.env.Battle.getViewedPokemon().curHP,"VERIFIED",73); eq(#o.readLog,0); eq(#o.violations,0); zero(s)
end)
local failed,hazards,totals=0,0,{}
for _,t in ipairs(tests) do
    local budget=0
    trustedHook(function() budget=budget+1; if budget>100000 then error("Instruction budget exceeded") end end,"",1000)
    local ok,why=pcall(t[3]); trustedHook()
    totals[t[1]]=(totals[t[1]] or 0)+1
    if not ok then failed=failed+1; print("FAIL",t[1],t[2],why)
    else if t[4] then hazards=hazards+1 end
        print(t[4] and "EXPECTED_STOCK_HAZARD" or (t[1]:find("bridge",1,true) and "PASS_TEST_ONLY" or "PASS"),t[1],t[2])
    end
end
local function sorted(t) local out={} for k in pairs(t) do out[#out+1]=k end table.sort(out); return out end
for _,name in ipairs(oracleNames) do
    local n=0; for _,s in ipairs(oracleStates) do n=n+(s.calls[name] or 0) end
    assert(n>0,"Missing original bridge oracle execution: "..name)
    print("BRIDGE_ORIGINAL_EXECUTIONS",name,n)
end
for _,name in ipairs({"Tracker.getPokemon","Battle.inActiveBattle","Utils.inlineIf"}) do print("ORACLE_SYNTHETIC_STUB",name) end
for _,s in ipairs(bridgeStates) do zero(s) end
for _,s in ipairs(oracleStates) do
    eq(#s.readLog,0); eq(#s.violations,0)
    for _,name in ipairs(seams) do eq(s.calls[name] or 0,0) end
end
print("BRIDGE_ZERO stock reader calls / host reads / writes / persistence / defaults / catalog fallbacks")
for _,name in ipairs(sorted(counts)) do print("REPEATED_707_ORIGINAL_EXECUTIONS",name,counts[name]) end
for _,name in ipairs(sorted(traps)) do print("CONFIRMED_CONTROL_TRAP",name,traps[name]) end
for _,name in ipairs(sorted(totals)) do print("CLASS",name,totals[name]) end
print("NOT_RUN live install/session/address, renderer/BattleDetails/persistence, Lua 5.1, BizHawk, C/Java/Clang")
print("RESULT",#tests-failed,"PASS",failed,"FAIL",hazards,"EXPECTED_STOCK_HAZARD","TEST_ONLY","liveConfidence=UNKNOWN","production=DENIED")
assert(failed==0,"Unexpected host field bridge failures")
