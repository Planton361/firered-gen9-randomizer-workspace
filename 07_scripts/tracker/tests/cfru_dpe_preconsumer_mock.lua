-- #709 extends the immutable #707 controls in the same restricted stock sandbox.
-- guardModule and exact public strings are trusted bootstrap-local dependencies.
local guardedStates={}
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
    for i,id in ipairs(ids) do
        local base=(i-1)*100
        -- Independent literal CFRU ABI fixture: direct, not XOR/shuffled.
        for _,f in ipairs({{0,4,24},{4,4,25},{32,2,id},{34,2,743},{44,2,33},
            {52,1,7},{84,1,50},{86,2,73},{88,2,120}}) do
            s=patch(s,base+f[1],f[2],f[3])
        end
    end
    return {bytes=s,count=#ids}
end
local function battleBytes(ids)
    local s=string.rep("\0",352)
    for i,id in ipairs(ids) do
        local base=(i-1)*88
        for _,f in ipairs({{0,2,id},{12,2,33},{32,1,254},{33,1,12},{34,1,12},
            {24,1,12},{36,1,2},{40,2,11},{42,1,50},{44,2,120},{46,2,743}}) do
            s=patch(s,base+f[1],f[2],f[3])
        end
    end
    return s
end
local seamNames={"Program.updatePokemonTeams","Program.readNewPokemon","Battle.updateViewSlots","Battle.beginNewBattle"}
local function fixture()
    local s=fresh(); local host={Program={},Battle={},Lifecycle={startTracker=function() error("STOCK_RESTART") end}}
    local expected={}
    for _,name in ipairs(seamNames) do
        local ns,key=name:match("^(%w+)%.(%w+)$")
        host[ns][key]=s.env[ns][key]; expected[name]=host[ns][key]
    end
    local d,why=guardModule.newMock(host,expected,SOURCES,MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
    assert(d,why and why.reason)
    s.host,s.expected,s.guard=host,expected,d
    guardedStates[#guardedStates+1]=s
    return s
end
local function zero(s)
    for name in pairs(SOURCES) do eq(s.calls[name] or 0,0) end
    eq(#s.readLog,0); eq(#s.violations,0)
end
local function label(r)
    eq(r.evidence,"TEST_ONLY"); eq(r.liveConfidence,"UNKNOWN"); eq(r.production,"DENIED")
end
local function unknown(r) label(r); eq(r.confidence,"UNKNOWN"); eq(r.ready,false); eq(r.value,nil); eq(r.ticket,nil) end
local function invoke(s,accepted)
    for _,name in ipairs(seamNames) do
        local ns,key=name:match("^(%w+)%.(%w+)$")
        -- Deliberate stock address-shaped arguments: wrappers must never read them.
        local r=s.host[ns][key](s.PLAYER,24); label(r)
        if accepted then eq(r.ready,true); assert(r.ticket) else unknown(r) end
    end
    zero(s)
end
local function arm(s,opts)
    opts=opts or {}; local d=s.guard
    local declaration={epoch=d.statusMock().epoch+1,output="fixture-output",session="fixture-session",
        encounter="fixture-battle",profileId=d.profileId,
        trackerPin="c450ecaee2d8131a2789bb656e3be792a93712fb",evidence="SYNTHETIC_ONLY"}
    if opts.outside then declaration.encounter=false end
    s.host.session=clone(declaration)
    local r,be=d.transitionMock(opts.event or "start",declaration); unknown(r)
    local sample={before=declaration,after=clone(declaration),sampleId=1,
        player=partyBytes(opts.ids or {1294})}
    if not opts.outside then
        sample.enemy=partyBytes({1})
        local context={epoch=be,state="ACTIVE",output=declaration.output,battle=declaration.encounter,
            flags=bytes(opts.flags or 4,4),count=bytes(2,1),positions=bytes(0,1)..bytes(1,1)..bytes(255,1)..bytes(255,1),
            indexes=bytes(0,2)..bytes(0,2)..bytes(65535,2)..bytes(65535,2)}
        sample.battle={epoch=be,before=context,after=clone(context),battleMons=battleBytes({1294,1}),
            ppCaps=bytes(35,1)..string.rep("\0",3)..bytes(35,1)..string.rep("\0",11)}
    end
    return sample
end
local function installed()
    local s=fixture(); unknown(s.guard.installMock()); return s
end
test("early-control","installed late hook cannot stop original pre-hook save-state",function()
    local s=fresh(); s.env.Battle.inBattleScreen=false; local late=0
    s.fixtureNamespace("CustomCode",{afterBattleBegins=function() late=late+1; error("LATE_GUARD") end})
    denied(function() s.env.Battle.beginNewBattle() end,"GameOverScreen.createTempSaveState")
    eq(s.calls["Battle.beginNewBattle"],1); eq(late,0); eq(#s.readLog,0)
end)
test("guard","all four early guards deny before any sample or original side effect",function()
    local s=installed(); invoke(s,false); unknown(s.host.Lifecycle.startTracker()); zero(s)
end)
test("guard","direct nonzero-key Gen9 bytes decoded independently without stock XOR",function()
    local s=installed(); local sample=arm(s); local r=s.guard.submitMock(sample); label(r); eq(r.ready,true)
    local view=s.guard.readMock(r.ticket); eq(view.value.player.slots[1].species.value.id,1294)
    eq(view.value.player.slots[1].hp.value,73); eq(view.value.battle.battlers[1].hp.value,11)
    eq(view.value.battle.battlers[1].moves[1].pp.value,2)
    eq(view.value.player.slots[1].moves[1].pp.value,7)
    eq(view.value.battle.battlers[1].abilityName.confidence,"UNKNOWN")
    eq(view.value.battle.battlers[1].moves[1].effective.confidence,"UNKNOWN")
    invoke(s,true); eq(next(s.env.Program.GameData.PlayerTeam),nil); eq(next(s.env.Program.GameData.EnemyTeam),nil)
    eq(s.env.Battle.Combatants.RightOwn,2)
end)
for _,id in ipairs({1,1102,1294,1022}) do
    test("guard","independent source identity "..id,function()
        local s=installed(); local r=s.guard.submitMock(arm(s,{outside=true,ids={id}}))
        assert(r.ready,r.reason); eq(s.guard.readMock(r.ticket).value.player.slots[1].species.value.id,id)
        for _,name in ipairs({"updatePokemonTeams","readNewPokemon"}) do
            eq(s.host.Program[name]().ready,true)
        end
        zero(s)
    end)
end
test("guard","outside battle cannot synthesize enemy PP from static tables",function()
    local s=installed(); local sample=arm(s,{outside=true}); local r=s.guard.submitMock(sample)
    assert(r.ready,r.reason); local v=s.guard.readMock(r.ticket).value
    eq(v.enemy,nil); eq(v.player.slots[1].moves[1].pp.value,7)
    eq(v.player.slots[1].moves[1].effective.confidence,"UNKNOWN")
    eq(v.player.slots[1].ability.confidence,"UNKNOWN"); zero(s)
end)
local negatives={
    {"invalid occupied player",function(s) s.player.bytes=patch(s.player.bytes,32,2,65535) end},
    {"invalid occupied enemy",function(s) s.enemy.bytes=patch(s.enemy.bytes,32,2,65535) end},
    {"invalid held item",function(s) s.player.bytes=patch(s.player.bytes,34,2,799) end},
    {"invalid move",function(s) s.player.bytes=patch(s.player.bytes,44,2,65535) end},
    {"invalid party HP",function(s) s.player.bytes=patch(s.player.bytes,86,2,121) end},
    {"invalid active HP",function(s) s.battle.battleMons=patch(s.battle.battleMons,40,2,121) end},
    {"invalid active PP",function(s) s.battle.battleMons=patch(s.battle.battleMons,36,1,36) end},
    {"missing effective PP cap",function(s) s.battle.ppCaps=nil end},
    {"poisoned u16 0x0105",function(s) s.battle.before.indexes=bytes(0x0105,2)..s.battle.before.indexes:sub(3); s.battle.after=clone(s.battle.before) end},
    {"illegal zero-based slot 6",function(s) s.battle.before.indexes=bytes(6,2)..s.battle.before.indexes:sub(3); s.battle.after=clone(s.battle.before) end},
    {"index outside occupied prefix",function(s) s.battle.before.indexes=bytes(5,2)..s.battle.before.indexes:sub(3); s.battle.after=clone(s.battle.before) end},
    {"four battlers unsupported",function(s) s.battle.before.count=bytes(4,1); s.battle.before.flags=bytes(5,4); s.battle.after=clone(s.battle.before) end},
    {"missing output",function(s) s.before.output=nil; s.after=clone(s.before) end},
    {"wrong profile",function(s) s.before.profileId="stock"; s.after=clone(s.before) end},
    {"wrong pin",function(s) s.before.trackerPin=string.rep("0",40); s.after=clone(s.before) end},
    {"wrong session",function(s) s.before.session="other-session"; s.after=clone(s.before) end},
    {"wrong epoch",function(s) s.before.epoch=s.before.epoch+1; s.after=clone(s.before) end},
    {"sample drift",function(s) s.after.output="other-output" end},
    {"truncated party",function(s) s.player.bytes="short" end},
    {"truncated battle",function(s) s.battle.battleMons="short" end},
    {"missing battle",function(s) s.battle=nil end},
    {"foreign active output",function(s) s.battle.before.output="other"; s.battle.after=clone(s.battle.before) end},
    {"caller validated boolean",function(s) s.validated=true end},
    {"caller trusted boolean",function(s) s.before.trusted=true; s.after=clone(s.before) end},
    {"trainer trusted boolean",function(s) s.battle.before.trainerA={trusted=true}; s.battle.after=clone(s.battle.before) end},
    {"sample metatable",function(s) setmetatable(s,{__index=function() error("CALLER_CALLBACK") end}) end},
    {"replay sample id",function(s) s.sampleId=1 end},
    {"NaN sample id",function(s) s.sampleId=0/0 end},
}
for _,case in ipairs(negatives) do
    test("guard-negative",case[1].." revokes before original entry",function()
        local s=installed(); local sample=arm(s); local old=s.guard.submitMock(sample); assert(old.ready,old.reason)
        sample.sampleId=2; case[2](sample); unknown(s.guard.submitMock(sample))
        unknown(s.guard.readMock(old.ticket)); invoke(s,false)
    end)
end
for _,event in ipairs({"start","end","switch","reset","reload","output","session","invalid"}) do
    test("lifecycle",event.." revokes retained tickets; caller epoch alone cannot rearm",function()
        local s=installed(); local sample=arm(s); local old=s.guard.submitMock(sample); assert(old.ready,old.reason)
        local epoch=s.guard.statusMock().epoch; unknown(s.guard.transitionMock(event)); assert(s.guard.statusMock().epoch>epoch)
        unknown(s.guard.readMock(old.ticket)); invoke(s,false)
        sample.before.epoch=s.guard.statusMock().epoch; sample.after=clone(sample.before)
        unknown(s.guard.submitMock(sample)); zero(s)
        local freshSample=arm(s,{event="session"}); local freshView=s.guard.submitMock(freshSample)
        assert(freshView.ready,freshView.reason); unknown(s.guard.readMock(old.ticket)); zero(s)
    end)
end
for _,key in ipairs({"session","output","epoch","profileId","trackerPin"}) do
    test("lifecycle","unannounced host "..key.." change caught before entry",function()
        local s=installed(); local r=s.guard.submitMock(arm(s)); assert(r.ready,r.reason)
        s.host.session[key]=key=="epoch" and 999 or "foreign"; invoke(s,false); unknown(s.guard.readMock(r.ticket))
    end)
end
test("lifecycle","six-to-one and 4-to-2 never borrow stale slots",function()
    local s=installed(); local old=s.guard.submitMock(arm(s,{ids={1294,1,1102,1022,26,1439}})); assert(old.ready,old.reason)
    local sample=arm(s); local r=s.guard.submitMock(sample); assert(r.ready,r.reason)
    local v=s.guard.readMock(r.ticket).value; eq(v.player.count.value,1); eq(v.player.slots[6].occupied.value,false)
    eq(v.battle.battlers[3].species.value,nil); eq(v.battle.battlers[4].species.value,nil)
    unknown(s.guard.readMock(old.ticket)); invoke(s,true)
end)
test("lifecycle","returned copies and tickets cannot contaminate owned views or stock teams",function()
    local s=installed(); local r=s.guard.submitMock(arm(s)); local a=s.guard.readMock(r.ticket).value
    a.player.slots[1].hp.value=999; a.battle.battlers[1].hp.value=999
    local b=s.guard.readMock(r.ticket).value; eq(b.player.slots[1].hp.value,73); eq(b.battle.battlers[1].hp.value,11)
    unknown(s.guard.readMock({})); eq(next(s.env.Program.GameData.PlayerTeam),nil); zero(s)
end)
for _,mode in ipairs({"throw","drop"}) do for i=1,4 do
    test("ownership","transaction "..mode.." after "..i.." rolls back all four",function()
        local s=fixture(); unknown(s.guard.installMock({after=i,mode=mode}))
        for _,name in ipairs(seamNames) do
            local ns,key=name:match("^(%w+)%.(%w+)$"); assert(s.host[ns][key]~=s.expected[name])
            unknown(s.host[ns][key]())
        end
        unknown(s.host.Lifecycle.startTracker()); unknown(s.guard.installMock()); zero(s)
    end)
end end
for _,name in ipairs(seamNames) do
    test("ownership","preexisting foreign "..name.." rejects without composing",function()
        local s=fixture(); local ns,key=name:match("^(%w+)%.(%w+)$"); local foreign=function() error("FOREIGN") end
        s.host[ns][key]=foreign; unknown(s.guard.installMock()); eq(s.host[ns][key],foreign); zero(s)
    end)
    test("ownership","later foreign "..name.." revokes and survives teardown",function()
        local s=installed(); local r=s.guard.submitMock(arm(s)); assert(r.ready,r.reason)
        local ns,key=name:match("^(%w+)%.(%w+)$"); local retained=s.host[ns][key]
        local foreign=function() error("FOREIGN") end; s.host[ns][key]=foreign
        unknown(retained()); unknown(s.guard.readMock(r.ticket)); unknown(s.guard.teardownMock())
        eq(s.host[ns][key],foreign); unknown(s.host.Lifecycle.startTracker())
        for _,other in ipairs(seamNames) do
            if other~=name then local n,k=other:match("^(%w+)%.(%w+)$"); unknown(s.host[n][k]()) end
        end
        zero(s)
    end)
end
test("ownership","duplicate install teardown and factory preserve safe tombstones",function()
    local s=installed(); local r=s.guard.submitMock(arm(s)); assert(r.ready,r.reason)
    local epoch=s.guard.statusMock().epoch; local fn=s.host.Program.readNewPokemon
    unknown(s.guard.installMock()); eq(s.host.Program.readNewPokemon,fn); eq(s.guard.statusMock().epoch,epoch)
    local duplicate,why=guardModule.newMock(s.host,s.expected,SOURCES,MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
    eq(duplicate,nil); unknown(why)
    unknown(s.guard.teardownMock()); local tomb=s.host.Program.readNewPokemon
    unknown(s.guard.teardownMock()); eq(s.host.Program.readNewPokemon,tomb)
    invoke(s,false); unknown(fn()); unknown(s.guard.readMock(r.ticket)); unknown(s.host.Lifecycle.startTracker())
end)
for _,ns in ipairs({"Program","Battle","Lifecycle"}) do
    test("ownership","namespace replacement "..ns.." revokes readiness",function()
        local s=installed(); local r=s.guard.submitMock(arm(s)); assert(r.ready,r.reason)
        local retained=s.host.Program.readNewPokemon; local old=s.host[ns]; s.host[ns]={}
        unknown(retained()); unknown(s.guard.readMock(r.ticket)); unknown(s.guard.teardownMock()); zero(s)
        if ns=="Lifecycle" then unknown(old.startTracker()) end
    end)
end
test("ownership","foreign restart owner revokes readiness",function()
    local s=installed(); local r=s.guard.submitMock(arm(s)); local foreign=function() error("FOREIGN_START") end
    s.host.Lifecycle.startTracker=foreign; unknown(s.guard.readMock(r.ticket)); unknown(s.guard.teardownMock())
    eq(s.host.Lifecycle.startTracker,foreign); zero(s)
end)
test("ownership","two preconstructed adapters cannot adopt each other's transaction",function()
    local s=fixture()
    local other,why=guardModule.newMock(s.host,s.expected,SOURCES,MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
    assert(other,why and why.reason); unknown(s.guard.installMock()); unknown(other.installMock())
    invoke(s,false); zero(s)
end)
for _,ns in ipairs({"root","Program","Battle","Lifecycle"}) do
    test("ownership","host metatable "..ns.." rejected without callback",function()
        local s=installed(); local r=s.guard.submitMock(arm(s)); assert(r.ready,r.reason)
        local t=ns=="root" and s.host or s.host[ns]
        setmetatable(t,{__index=function() error("HOST_CALLBACK") end,__newindex=function() error("HOST_WRITE_CALLBACK") end,
            __eq=function() error("HOST_EQUALITY_CALLBACK") end})
        unknown(s.guard.readMock(r.ticket)); unknown(s.guard.teardownMock()); zero(s)
    end)
end
test("source-negative","wrong serialized profile and original source drift reject construction",function()
    local s=fixture()
    for _,raw in ipairs({"wrong-profile", "{}"}) do
        local d,why=guardModule.newMock(s.host,s.expected,SOURCES,raw,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
        eq(d,nil); eq(why.confidence,"UNKNOWN")
    end
    local bodies=clone(SOURCES); bodies["Battle.beginNewBattle"]="function Battle.beginNewBattle() end"
    local d,why=guardModule.newMock(s.host,s.expected,bodies,MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
    eq(d,nil); unknown(why); zero(s)
end)
test("source-negative","source metatables and callback-shaped facts cannot confer trust",function()
    local s=fixture()
    local sources=setmetatable({},{__index=function() error("SOURCE_CALLBACK") end})
    local d,why=guardModule.newMock(s.host,s.expected,SOURCES,MOCK_SOURCE,sources,MOCK_MULTI)
    eq(d,nil); unknown(why)
    sources=clone(MOCK_PUBLIC_SOURCES); sources["CFRU:include/pokemon.h"]=function() error("SOURCE_CALLBACK") end
    d,why=guardModule.newMock(s.host,s.expected,SOURCES,MOCK_SOURCE,sources,MOCK_MULTI)
    eq(d,nil); unknown(why); zero(s)
end)

local failed,hazards,totals=0,0,{}
for _,t in ipairs(tests) do
    local budget=0
    -- Accepted profile validation is warmed; fixed source-negative SHA cases need
    -- more arithmetic than stock bodies. No debug hook is exposed to the host.
    trustedHook(function() budget=budget+1; if budget>100000 then error("Instruction budget exceeded") end end,"",1000)
    local ok,why=pcall(t[3]); trustedHook()
    totals[t[1]]=(totals[t[1]] or 0)+1
    if not ok then failed=failed+1; print("FAIL",t[1],t[2],why)
    else
        if t[4] then hazards=hazards+1 end
        print(t[4] and "EXPECTED_STOCK_HAZARD" or "PASS",t[1],t[2],"TEST_ONLY","liveConfidence=UNKNOWN")
    end
end
local function sorted(t) local out={} for k in pairs(t) do out[#out+1]=k end table.sort(out); return out end
for _,name in ipairs(sorted(SOURCES)) do
    assert((counts[name] or 0)>0,"No original control execution: "..name)
    print("UNGUARDED_ORIGINAL_EXECUTIONS",name,counts[name])
end
for _,name in ipairs(seamNames) do
    local entryCount,stockCount=0,0
    for _,s in ipairs(guardedStates) do
        entryCount=entryCount+(s.guard.metricsMock()[name] or 0)
        stockCount=stockCount+(s.calls[name] or 0)
    end
    eq(stockCount,0); assert(entryCount>0)
    print("GUARDED_ENTRY_EXECUTIONS",name,entryCount,"ORIGINAL_SIDE_EFFECT_CALLS",stockCount)
end
for _,name in ipairs(sorted(traps)) do print("CONFIRMED_CONTROL_TRAP",name,traps[name]) end
for _,class in ipairs(sorted(totals)) do print("CLASS",class,totals[class]) end
print("NOT_RUN production install/unload, actual session/address trust, host field bridge, renderer/BattleDetails/persistence, Lua 5.1, BizHawk, C/Java/Clang generator")
print("RESULT",#tests-failed,"PASS",failed,"FAIL",hazards,"EXPECTED_STOCK_HAZARD","TEST_ONLY","liveConfidence=UNKNOWN","production=DENIED")
assert(failed==0,"Unexpected preconsumer failures")
