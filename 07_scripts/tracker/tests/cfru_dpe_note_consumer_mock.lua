-- #713: restricted candidate environment; sole loader resolves accepted #711.
local gateForbidden=0
local init=true
local gateBacking={type=type,pairs=pairs,next=next,ipairs=ipairs,tostring=tostring,error=error,
    getmetatable=getmetatable,setmetatable=setmetatable,math={floor=math.floor}}
gateBacking.debug={getinfo=function() assert(init); return {source="@"..GATE_PATH} end}
gateBacking.dofile=function(path)
    assert(init and path=="03_tools/tracker-extensions/CFRUDPEExtension/source_host_field_bridge.lua")
    return acceptedBridge
end
local gateEnv=setmetatable({}, {__index=function(_,k)
    if gateBacking[k]~=nil then return gateBacking[k] end
    gateForbidden=gateForbidden+1; error("TRAP:gate."..tostring(k),0)
end,__newindex=function(_,k) gateForbidden=gateForbidden+1; error("TRAP:gate.write."..tostring(k),0) end})
local bridgeModule=assert(trustedLoad(GATE_SOURCE,"@"..GATE_PATH,"t",gateEnv))()
init=false; gateBacking.debug=nil; gateBacking.dofile=nil
-- ACCEPTED_FIXTURE_DECLARATIONS
local function witness(opts)
    local w={species=1294,side="PLAYER",slot=1,moveSlot=1,moveId=33,level=51,encounter="fixture-battle"}
    for k,v in pairs(opts or {}) do w[k]=v end; return w
end
local function observed(s,t,w)
    local r=s.bridge.observeMock(t,w or witness()); assert(r.ready,r.reason); return r.ticket
end
local function read(s,t,k,o,side,slot)
    return s.bridge.readMock(t,k,side or "PLAYER",slot or 1,o)
end
local function absent(r,state)
    nonready(r,state); assert(r.reason and r.provenance and r.profileId and r.epoch)
end
local function positive(r)
    label(r); eq(r.ready,true); eq(r.confidence,"VERIFIED"); eq(r.reason,"VERIFIED_SOURCE_SYNTHETIC_ONLY")
    eq(r.value.observedMoveId,33); eq(r.value.species,1294); eq(r.value.side,"PLAYER")
    eq(r.value.slot,1); eq(r.value.level,51)
    eq(r.value.pp,nil); eq(r.value.maxPP,nil); eq(r.value.power,nil); eq(r.value.category,nil)
end
local function historical()
    return {romHash="matching-synthetic",version="9.3.1",trainerID=24,output="fixture-output",
        session="fixture-session",trusted=true,verified=true,confidence="VERIFIED",evidence="TEST_ONLY",
        Tracker={Data={allPokemon={[1294]={note="STALE_NOTE",abilities={{id=65,name="STALE_ABILITY"}},
            moves={{id=99,pp=35,power=999,category=0}},eL=88}}}},
        BattleNotes={FourMovesIfAllKnown={[1294051]={{id=99,pp=35}}}},
        TDAT={allPokemon={[1294]={note="RESTORED_TDAT",moves={{id=99}},abilities={{id=65}},eL=88}}}}
end
for _,id in ipairs({1,1102,1294,1022}) do
    test("quarantine","Gen1/8/9/regional old categories never current "..id,function()
        local s=fixture(); local t=accepted(s,{ids={id},activeIds={id,1}})
        local h=historical(); h.profileId=s.bridge.profileId
        local q=s.bridge.quarantineMock(h); eq(q.status,"QUARANTINED"); eq(q.count,1)
        eq(q.value,nil); eq(q.note,nil); eq(q.key,nil)
        for _,k in ipairs({"note","abilities","moves","eL"}) do absent(read(s,t,k)) end
        absent(read(s,t,"FourMovesIfAllKnown"),"UNAVAILABLE")
        eq(h.Tracker.Data.allPokemon[1294].note,"STALE_NOTE"); zero(s)
    end)
end
test("quarantine","input is never inspected; malicious metatable and claimed labels ignored",function()
    local s=fixture(); local t=accepted(s)
    local h=setmetatable({}, {__index=function() error("historical inspected") end,
        __pairs=function() error("historical traversed") end})
    eq(s.bridge.quarantineMock(h).count,1)
    eq(s.bridge.quarantineMock(function() error("historical callback") end).count,2)
    local claims=historical(); claims.profileId=s.bridge.profileId; claims.epoch=s.bridge.statusMock().epoch
    eq(s.bridge.quarantineMock(claims).count,3); absent(read(s,t,"note")); zero(s)
end)
test("quarantine","positive current battle identity and active level despite party PP 7",function()
    local s=fixture(); local t=accepted(s); local w=witness(); local o=observed(s,t,w)
    w.moveId=99; s.bridge.quarantineMock(historical())
    positive(read(s,t,"moves",o)); absent(read(s,t,"abilities")); absent(read(s,t,"note")); absent(read(s,t,"eL"))
    absent(read(s,t,"FourMovesIfAllKnown",o),"UNAVAILABLE"); zero(s)
end)
for _,bad in ipairs({{species=906},{species=1022},{side="OTHER"},{slot=6},{slot=0},{moveSlot=0},
    {moveSlot=5},{moveId=99},{moveId=0},{level=50},{encounter="other"},{note="text"},
    {verified=true},{trusted=true},{abilityName="name"}}) do
    test("quarantine-negative","unproved witness "..next(bad),function()
        local s=fixture(); local t=accepted(s)
        absent(s.bridge.observeMock(t,witness(bad)),bad.slot==6 and "UNAVAILABLE" or "UNKNOWN")
        absent(read(s,t,"moves",{})); zero(s)
    end)
end
test("quarantine-negative","witness metatable/label cannot manufacture an observation",function()
    local s=fixture(); local t=accepted(s)
    absent(s.bridge.observeMock(t,setmetatable(witness(),{})))
    absent(read(s,t,"moves",{confidence="VERIFIED",value={id=33}})); zero(s)
end)
for _,event in ipairs({"end","reset","reload","switch","session","output","unknown"}) do
    test("quarantine-epoch","revoked on "..event,function()
        local s=fixture(); local t=accepted(s); local o=observed(s,t); local old=read(s,t,"moves",o)
        s.bridge.transitionMock(event); absent(read(s,t,"moves",o)); absent(read(s,t,"note"))
        -- Historical copies are labeled, never live references or reusable tickets.
        positive(old); eq(old.validity,"HISTORICAL_COPY_REQUERY_REQUIRED"); zero(s)
    end)
end
for _,key in ipairs({"epoch","session","output","encounter","profileId","trackerPin"}) do
    test("quarantine-epoch","unannounced host binding change "..key,function()
        local s=fixture(); local t=accepted(s); local o=observed(s,t)
        s.host.session[key]=key=="epoch" and 999 or "foreign"
        absent(read(s,t,"moves",o)); absent(read(s,t,"abilities")); zero(s)
    end)
end
test("quarantine-epoch","replacement in same epoch revokes both ticket kinds",function()
    local s=fixture(); local t,sample=accepted(s); local o=observed(s,t)
    sample.sampleId=2; local n=s.bridge.submitMock(sample); assert(n.ready,n.reason)
    absent(read(s,t,"moves",o)); absent(read(s,n.ticket,"moves",o))
    positive(read(s,n.ticket,"moves",observed(s,n.ticket))); zero(s)
end)
test("quarantine-epoch","replay and missing sample revoke rather than cache",function()
    local s=fixture(); local t,sample=accepted(s); local o=observed(s,t)
    eq(s.bridge.submitMock(sample).ready,false); absent(read(s,t,"moves",o)); zero(s)
    local b=fixture(); local u=accepted(b); local p=observed(b,u)
    eq(b.bridge.submitMock(nil).ready,false); absent(read(b,u,"moves",p)); zero(b)
end)
test("quarantine-epoch","six to one clears old slot and associations",function()
    local s=fixture(); local t=accepted(s,{ids={1,1102,1022,26,1439,1294},playerIndex=5})
    local o=observed(s,t,witness({slot=6})); local old=s.bridge.readMock(t,"moves","PLAYER",6,o)
    eq(old.value.observedMoveId,33)
    local u=accepted(s,{event="switch"}); absent(read(s,t,"moves",o))
    absent(s.bridge.readMock(u,"moves","PLAYER",6,o),"UNAVAILABLE")
    absent(read(s,u,"moves",o)); positive(read(s,u,"moves",observed(s,u))); zero(s)
end)
for _,kind in ipairs({"species","u16","slot6","hp","pp","source-label","missing"}) do
    test("quarantine-negative","invalid sample "..kind,function()
        local s=fixture(); local t=accepted(s); local o=observed(s,t)
        local sample=arm(s,{event="switch"})
        if kind=="species" then sample.player.bytes=patch(sample.player.bytes,32,2,65535)
        elseif kind=="u16" then sample.battle.before.indexes=patch(sample.battle.before.indexes,0,2,0x0105); sample.battle.after=clone(sample.battle.before)
        elseif kind=="slot6" then sample.battle.before.indexes=patch(sample.battle.before.indexes,0,2,6); sample.battle.after=clone(sample.battle.before)
        elseif kind=="hp" then sample.battle.battleMons=patch(sample.battle.battleMons,40,2,65535)
        elseif kind=="pp" then sample.battle.ppCaps=nil
        elseif kind=="source-label" then sample.verified=true
        else sample.player=nil end
        eq(s.bridge.submitMock(sample).ready,false); absent(read(s,t,"moves",o)); zero(s)
    end)
end
test("quarantine-negative","outside/unsupported battle and unknown capabilities retain states",function()
    local s=fixture(); local t=accepted(s,{outside=true})
    absent(s.bridge.observeMock(t,witness()),"UNAVAILABLE"); absent(read(s,t,"moves")); absent(read(s,t,"abilities"))
    absent(s.bridge.readMock(t,"note","ENEMY",1),"UNAVAILABLE"); zero(s)
    local b=fixture(); local r=b.bridge.submitMock(arm(b,{flags=5})); absent(r,"UNAVAILABLE"); zero(b)
end)
for _,kind in ipairs({"wrapper","namespace","restart"}) do
    test("quarantine-negative","foreign owner "..kind,function()
        local s=fixture(); local t=accepted(s); local o=observed(s,t)
        if kind=="wrapper" then s.host.Program.readNewPokemon=function() error("foreign called") end
        elseif kind=="namespace" then s.host.Battle={}
        else s.host.Lifecycle.startTracker=function() error("foreign restart called") end end
        absent(read(s,t,"moves",o)); zero(s)
    end)
end
test("quarantine-negative","foreign gate, retained alias and mutated opaque tickets",function()

    local a,b=fixture(),fixture(); local t=accepted(a); local u=accepted(b); local o=observed(a,t)
    absent(read(b,u,"moves",o)); absent(read(b,t,"note")); absent(read(a,u,"moves",o))
    local old=read(a,t,"moves",o); local ok=pcall(function() old.value.observedMoveId=99 end); eq(ok,false)
    rawset(old.value,"observedMoveId",99); positive(read(a,t,"moves",o))
    o.verified=true; absent(read(a,t,"moves",o)); t.verified=true; absent(read(a,t,"note")); zero(a); zero(b)
end)
for _,kind in ipairs({"raw","public","multi","body"}) do
    test("quarantine-negative","factory locked input "..kind,function()
        local s=fixture(false); local raw,texts,multi,bodies=MOCK_SOURCE,clone(MOCK_PUBLIC_SOURCES),MOCK_MULTI,clone(SOURCES)
        if kind=="raw" then raw=raw.." " elseif kind=="public" then for k in pairs(texts) do texts[k]=texts[k].." "; break end
        elseif kind=="multi" then multi="-- wrong public multi source" else bodies["Program.readNewPokemon"]=bodies["Program.readNewPokemon"].." " end
        local g=bridgeModule.newMock(s.host,s.expected,bodies,raw,texts,multi); eq(g,nil); zero(s)
    end)
end
test("quarantine-epoch","teardown and different synthetic session never recover old battle key",function()
    local s=fixture(); local t=accepted(s); local o=observed(s,t); s.bridge.teardownMock(); absent(read(s,t,"moves",o)); zero(s)
    local b=fixture(); local u=accepted(b); b.bridge.quarantineMock(historical())
    absent(read(b,u,"moves",o)); absent(read(b,u,"FourMovesIfAllKnown"),"UNAVAILABLE"); zero(b)
end)
test("quarantine-epoch","new output/session retains no species+level history or observations",function()
    local s=fixture(); local t=accepted(s); local o=observed(s,t)
    local sample=arm(s,{event="session"})
    local d=clone(sample.before); d.output="second-output"; d.session="second-session"; d.encounter="second-battle"
    -- Re-arm a genuinely different synthetic declaration through the owned chain.
    d.epoch=s.bridge.statusMock().epoch+1; s.host.session=clone(d)
    local _,be=s.bridge.transitionMock("output",d)
    sample.before=d; sample.after=clone(d); sample.battle.epoch=be
    for _,c in ipairs({sample.battle.before,sample.battle.after}) do
        c.epoch=be; c.output=d.output; c.battle=d.encounter
    end
    local r=s.bridge.submitMock(sample); assert(r.ready,r.reason)
    s.bridge.quarantineMock(historical()); absent(read(s,r.ticket,"moves",o)); absent(read(s,t,"note"))
    local n=observed(s,r.ticket,witness({encounter="second-battle"}))
    positive(read(s,r.ticket,"moves",n)); zero(s)
end)
test("quarantine-negative","enemy observation cannot cross side or slot",function()
    local s=fixture(); local t=accepted(s)
    local o=observed(s,t,witness({side="ENEMY",species=1}))
    absent(read(s,t,"moves",o))
    local r=read(s,t,"moves",o,"ENEMY",1)
    eq(r.confidence,"VERIFIED"); eq(r.value.species,1); eq(r.value.side,"ENEMY"); eq(r.value.observedMoveId,33)
    zero(s)
end)
-- Original getter characterization is wholly separate from corrected gate queries.
local noteOriginalCounts,stubCounts={},{}
local function oracle(inBattle,data,battleNotes,session)
    local s=fresh()
    local function stub(name,fn) return function(...)
        stubCounts[name]=(stubCounts[name] or 0)+1; return fn(...)
    end end
    local function trap(name) return function() error("TRAP:"..name,0) end end
    s.fixtureNamespace("Tracker",{Data=s.fixtureFrozen({allPokemon=data,session=session},"Historical.Tracker.Data"),
        BattleNotes=s.fixtureFrozen({FourMovesIfAllKnown=battleNotes},"Historical.BattleNotes"),
        getOrCreateTrackedPokemon=stub("Tracker.getOrCreateTrackedPokemon",function(id,create)
            eq(create,false); return s.env.Tracker.Data.allPokemon[id] or s.fixtureFrozen({},"Historical.empty")
        end),recordBattleMoveByPokemonLevel=trap("Tracker.recordBattleMoveByPokemonLevel"),
        saveData=trap("Tracker.saveData"),loadData=trap("Tracker.loadData"),verifyDataForPlayer=trap("Tracker.verifyDataForPlayer"),
        AutoSave=s.fixtureFrozen({loadFromFile=trap("Tracker.AutoSave.loadFromFile"),saveToFile=trap("Tracker.AutoSave.saveToFile")},"AutoSave")})
    s.fixtureNamespace("Battle",{isViewingOwn=false,inActiveBattle=stub("Battle.inActiveBattle",function() return inBattle end)})
    s.fixtureNamespace("PokemonData",{Values=s.fixtureFrozen({GhostId=999},"GhostId_STUB")})
    s.fixtureNamespace("DataHelper",{buildTrackerScreenDisplay=trap("DataHelper.buildTrackerScreenDisplay")})
    for name,body in pairs(NOTE_SOURCES) do
        local original=s.fixtureDefinition(name,body); local _,key=name:match("^(%w+)%.(%w+)$")
        s.override("Tracker",key,function(...)
            noteOriginalCounts[name]=(noteOriginalCounts[name] or 0)+1; return original(...)
        end)
    end
    return s
end
for _,session in ipairs({"session-A","session-B"}) do
    test("note-original",session.." identical species+level stale key wins",function()
        local s=oracle(true,{[1294]={note="STALE_NOTE",moves={{id=99,pp=35}},abilities={{id=65}},eL=88}},
            {[1294051]={{id=98,pp=44}}},session)
        eq(s.env.Tracker.getMoves(1294,51)[1].id,98)
        eq(s.env.Tracker.getAbilities(1294)[1].id,65); eq(s.env.Tracker.getNote(1294),"STALE_NOTE")
        eq(s.env.Tracker.getLastLevelSeen(1294),88); eq(#s.readLog,0); eq(#s.violations,0)
        denied(function() s.env.Tracker.Data.allPokemon[1294].note="overwrite" end,"Historical.Tracker.Data.allPokemon.1294.mutation")
    end,true)
end
test("note-original","stored moves win outside battle without output/session proof",function()
    local s=oracle(false,{[1294]={moves={{id=99,pp=35}}}}, {[1294051]={{id=98}}})
    eq(s.env.Tracker.getMoves(1294,51)[1].id,99); eq(#s.readLog,0); eq(#s.violations,0)
end,true)
test("note-original","empty note/zero ability defaults are expected stock hazards",function()
    local s=oracle(false,{},{}); eq(s.env.Tracker.getNote(1294),"")
    local a=s.env.Tracker.getAbilities(1294); eq(a[1].id,0); eq(a[2].id,0)
    eq(#s.env.Tracker.getMoves(1294),0); eq(s.env.Tracker.getLastLevelSeen(1294),nil)
    eq(#s.readLog,0); eq(#s.violations,0)
end,true)
test("note-safety","persistence/render entry points trapped; no full original paths executed",function()
    local s=oracle(false,{}, {})
    for _,name in ipairs({"recordBattleMoveByPokemonLevel","saveData","loadData","verifyDataForPlayer"}) do
        denied(function() s.env.Tracker[name]() end,"Tracker."..name)
    end
    denied(function() s.env.Tracker.AutoSave.loadFromFile() end,"Tracker.AutoSave.loadFromFile")
    denied(function() s.env.Tracker.AutoSave.saveToFile() end,"Tracker.AutoSave.saveToFile")
    denied(function() s.env.DataHelper.buildTrackerScreenDisplay() end,"DataHelper.buildTrackerScreenDisplay")
end)
local failed,hazards,totals=0,0,{}
for _,t in ipairs(tests) do
    local budget=0
    trustedHook(function() budget=budget+1; if budget>100000 then error("Instruction budget exceeded") end end,"",1000)
    local ok,why=pcall(t[3]); trustedHook()
    totals[t[1]]=(totals[t[1]] or 0)+1
    if not ok then failed=failed+1; print("FAIL",t[1],t[2],why)
    else if t[4] then hazards=hazards+1 end
        print(t[4] and "EXPECTED_STOCK_HAZARD" or "PASS_TEST_ONLY",t[1],t[2])
    end
end
local function sorted(t) local a={} for k in pairs(t) do a[#a+1]=k end table.sort(a); return a end
for _,name in ipairs(sorted(NOTE_SOURCES)) do
    assert((noteOriginalCounts[name] or 0)>0); print("NOTE_ORIGINAL_EXECUTIONS",name,noteOriginalCounts[name])
end
for _,name in ipairs(sorted(stubCounts)) do print("NOTE_ORACLE_STUB_EXECUTIONS",name,stubCounts[name]) end
print("NOTE_GHOST_CATALOG_CONSTANT_STUB GhostId=999; ghost branch NOT_RUN; catalog calls zero")
for _,s in ipairs(bridgeStates) do zero(s) end
eq(gateForbidden,0)
print("NOTE_GATE_ZERO originals / host reads / forbidden operations / persistence / UI / catalog fallback")
for _,name in ipairs(sorted(counts)) do print("REPEATED_707_ORIGINAL_EXECUTIONS",name,counts[name]) end
for _,name in ipairs(sorted(traps)) do print("CONFIRMED_CONTROL_TRAP",name,traps[name]) end
for _,name in ipairs(sorted(totals)) do print("CLASS",name,totals[name]) end
print("NOT_RUN live identities, actual notes/TDAT, rendering, emulator/BizHawk, Lua5.1, Clang/C/Java")
print("RESULT",#tests-failed,"PASS",failed,"FAIL",hazards,"EXPECTED_STOCK_HAZARD","TEST_ONLY","liveConfidence=UNKNOWN","production=DENIED")
assert(failed==0,"Unexpected note consumer failures")
