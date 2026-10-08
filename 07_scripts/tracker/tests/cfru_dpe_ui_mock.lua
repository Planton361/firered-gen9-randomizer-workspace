-- Synthetic bytes with independent literal offsets; no real screen or host.
local module=dofile("03_tools/tracker-extensions/CFRUDPEExtension/source_ui_projection.lua")
local function copy(t)
    if type(t)~="table" then return t end
    local out={}; for k,v in pairs(t) do out[k]=copy(v) end; return out
end
local function bytes(n,w)
    local out={}; for i=1,w do out[i]=string.char(n%256); n=math.floor(n/256) end
    return table.concat(out)
end
local function patch(s,o,w,n) return s:sub(1,o)..bytes(n,w)..s:sub(o+w+1) end
local function party(ids)
    local s=string.rep("\0",600)
    for i,id in ipairs(ids) do
        local base=(i-1)*100
        for _,f in ipairs({{32,2,id},{34,2,743},{44,2,33},{46,2,733},{48,2,991},
            {52,1,20},{53,1,5},{54,1,10},{80,4,32},{84,1,50},{86,2,100},{88,2,200}}) do
            s=patch(s,base+f[1],f[2],f[3])
        end
    end
    return {bytes=s,count=#ids}
end
local function mons(ids)
    local s=string.rep("\0",352)
    for i,id in ipairs(ids) do
        local base=(i-1)*88
        for _,f in ipairs({{0,2,id},{12,2,33},{14,2,733},{16,2,991},{24,1,14},
            {32,1,254},{33,1,17},{34,1,13},{36,1,20},{37,1,5},{38,1,10},
            {40,2,50},{42,1,50},{44,2,200},{46,2,743},{76,4,32}}) do
            s=patch(s,base+f[1],f[2],f[3])
        end
    end
    return s
end
local function new()
    local d,f=module.newMock(MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
    assert(d,f and f.reason); return d
end
local function start(d,opts)
    opts=opts or {}
    local proof={epoch=d.snapshot().epoch+1,profileId=d.profileId,evidence="SYNTHETIC_ONLY",trusted=true,
        output=opts.output or "fixture-output",session=opts.session or "fixture-session",
        battle="fixture-encounter",playerRoster="fixture-party-A",enemyRoster="fixture-party-B"}
    if opts.outside then proof.battle=false end
    local epoch,be=d.transition(opts.event or "start",proof)
    assert(epoch==proof.epoch)
    local c={epoch=be,state="ACTIVE",output=proof.output,battle=proof.battle,
        flags=bytes(opts.flags or 4,4),count=bytes(2,1),positions=bytes(0,1)..bytes(1,1)..bytes(255,1)..bytes(255,1),
        indexes=bytes(0,2)..bytes(0,2)..bytes(65535,2)..bytes(65535,2)}
    local s={before=proof,after=copy(proof),sampleId=1,player=party(opts.ids or {1,1102,1294,1022,1439,26})}
    if not opts.outside then
        s.enemy=party({1294})
        s.battle={epoch=be,before=c,after=copy(c),battleMons=mons({1,1294}),
            ppCaps=bytes(35,1)..bytes(5,1)..bytes(10,1)..bytes(0,1)..bytes(35,1)..bytes(5,1)..bytes(10,1)..bytes(0,1)..string.rep("\0",8)}
    end
    return s
end
local function state(f,c,v)
    assert(f.confidence==c,f.reason or f.confidence)
    assert(f.evidence=="TEST_ONLY" and f.liveConfidence=="UNKNOWN" and f.label=="TEST_ONLY")
    assert(type(f.reason)=="string" and f.reason~="")
    if c~="VERIFIED" then assert(f.value==nil) elseif v~=nil then assert(f.value==v) end
end
local function walk(t,epoch)
    if type(t)~="table" then return end
    if t.confidence then
        state(t,t.confidence); assert(t.sampleEpoch==epoch)
        if t.confidence=="VERIFIED" then assert(t.value~=nil) end
    end
    for _,v in pairs(t) do walk(v,epoch) end
end
local function cleared(o)
    for _,group in ipairs({o.playerParty,o.enemyParty,o.active}) do
        for _,r in ipairs(group) do
            assert(r.species.value==nil and r.hp.value==nil and r.hpPercent.value==nil)
            for _,m in ipairs(r.moves) do assert(m.pp.value==nil and m.damage.value==nil) end
        end
    end
    assert(o.trainerA.value==nil and o.trainerB.value==nil); walk(o,o.epoch)
end
local tests={}
local function test(name,f) tests[#tests+1]={name,f} end
test("initial detached/live unknown",function()
    local d=new(); cleared(d.snapshot())
    assert(d.startup==nil and d.beforeGameDataLoad==nil and d.drawScreen==nil)
end)
test("Gen1/8/9/regional six-slot party plus wild active precedence",function()
    local d=new(); local o=d.decodeMock(start(d)); walk(o,o.epoch)
    state(o.playerCount,"VERIFIED",6); state(o.enemyCount,"VERIFIED",1)
    for i,id in ipairs({1,1102,1294,1022,1439,26}) do
        assert(o.playerParty[i].species.value.id==id)
        state(o.playerParty[i].hpPercent,"VERIFIED",50)
        state(o.playerParty[i].abilityId,"UNKNOWN"); state(o.playerParty[i].abilityName,"UNKNOWN")
        state(o.playerParty[i].moves[1].pp,"VERIFIED",20)
        state(o.playerParty[i].moves[1].maxPP,"UNKNOWN")
        assert(o.playerParty[i].sourceBaseline.scope=="source-baseline")
        state(o.playerParty[i].effectiveTypes,"UNKNOWN")
    end
    state(o.active[1].hp,"VERIFIED",50); state(o.active[1].hpPercent,"VERIFIED",25)
    assert(o.active[2].species.value.id==1294 and o.enemyParty[1].species.value.id==1294)
    assert(o.active[1].abilityId.value.id==254 and o.active[1].abilityId.value.name==nil)
    state(o.active[1].abilityName,"UNKNOWN"); state(o.active[1].type3,"VERIFIED")
    state(o.active[1].status,"VERIFIED"); assert(o.active[1].status.value.primary=="FROSTBITE")
    state(o.trainerA,"UNAVAILABLE"); state(o.battleDetails,"UNAVAILABLE"); state(o.notes,"UNAVAILABLE")
end)
test("one-slot outside battle and absence sentinels",function()
    local d=new(); local s=start(d,{outside=true,ids={1294}})
    s.player.bytes=patch(s.player.bytes,34,2,0)
    local o=d.decodeMock(s); state(o.playerCount,"VERIFIED",1)
    assert(o.playerParty[1].heldItem.value.absent)
    state(o.playerParty[2].occupied,"VERIFIED",false); assert(o.playerParty[2].species.value.absent)
    state(o.playerParty[2].hp,"UNAVAILABLE"); state(o.enemyCount,"UNAVAILABLE")
    state(o.active[1].hp,"UNAVAILABLE"); state(o.trainerA,"UNAVAILABLE")
end)
for _,trusted in ipairs({true,false}) do
    test("trainer trust "..tostring(trusted),function()
        local d=new(); local s=start(d,{flags=12})
        s.battle.before.trainerA={epoch=s.battle.epoch,bytes=bytes(0x1234,2),trusted=trusted,source="gTrainerBattleOpponent_A"}
        s.battle.after=copy(s.battle.before)
        local o=d.decodeMock(s); state(o.battleContext,"VERIFIED")
        state(o.trainerA,trusted and "VERIFIED" or "UNKNOWN")
        if trusted then assert(o.trainerA.value.id==0x1234 and o.trainerA.value.name==nil) end
        state(o.trainerB,"UNAVAILABLE")
    end)
end
for _,event in ipairs({"switch","end","reset","session","output","error","epoch"}) do
    test("immediate clear and revoked epoch "..event,function()
        local d=new(); local s=start(d); state(d.decodeMock(s).active[2].species,"VERIFIED")
        d.transition(event); cleared(d.snapshot()); cleared(d.decodeMock(s))
        -- Advancing caller fields alone cannot re-arm; fresh proof is needed.
        s.before.epoch=d.snapshot().epoch; s.after=copy(s.before); cleared(d.decodeMock(s))
        local fresh=start(d,{outside=true,ids={26},event="session"})
        local o=d.decodeMock(fresh); assert(o.playerParty[1].species.value.id==26)
        state(o.active[2].species,"UNAVAILABLE")
    end)
end
test("trusted switch clears before fresh sample and new Gen9 view",function()
    local d=new(); d.decodeMock(start(d))
    local s=start(d,{event="switch",ids={1439}}); cleared(d.snapshot())
    local o=d.decodeMock(s); assert(o.playerParty[1].species.value.id==1439)
    state(o.playerParty[6].hp,"UNAVAILABLE")
end)
test("malformed transition cannot execute caller callbacks or retain rows",function()
    local d=new(); d.decodeMock(start(d))
    d.transition(setmetatable({},{__tostring=function() error("caller callback executed") end}))
    cleared(d.snapshot())
end)
for _,mutate in ipairs({
    function(s) s.before.trusted=false; s.after=copy(s.before) end,
    function(s) s.before.evidence="LIVE"; s.after=copy(s.before) end,
    function(s) s.before.profileId="plausible-stock"; s.after=copy(s.before) end,
    function(s) s.before.session="other-session"; s.after=copy(s.before) end,
    function(s) s.before.output="other-output"; s.after=copy(s.before) end,
    function(s) s.after.playerRoster="switch-during-sample" end,
    function(s) s.before.epoch=s.before.epoch+1; s.after=copy(s.before) end,
    function(s) s.battle.before.output="other-output"; s.battle.after=copy(s.battle.before) end,
    function(s) s.battle.before.battle="other-battle"; s.battle.after=copy(s.battle.before) end,
    function(s) s.battle.epoch=s.battle.epoch+1 end,
    function(s) s.player.bytes="truncated" end,
    function(s) s.player.count=5 end,
    function(s) s.enemy.bytes="truncated" end,
    function(s) s.battle.battleMons="truncated" end,
    function(s) s.battle=nil end,
    function(s) s.sampleId=0 end,
    function(s) s.sampleId=math.huge end,
    function(s) setmetatable(s,{__index=function() error("metatable executed") end}) end,
}) do
    test("identity/data fail clears populated projection "..#tests,function()
        local d=new(); local s=start(d); d.decodeMock(s); s.sampleId=2; mutate(s)
        cleared(d.decodeMock(s)); cleared(d.snapshot())
    end)
end
test("same-sample replay and undeclared roster/index switch",function()
    local d=new(); local s=start(d); d.decodeMock(s); cleared(d.decodeMock(s))
    s=start(d); d.decodeMock(s); s.sampleId=2; s.player=party({26})
    cleared(d.decodeMock(s))
    s=start(d); d.decodeMock(s); s.sampleId=2
    s.battle.before.indexes=patch(s.battle.before.indexes,2,2,1); s.battle.after=copy(s.battle.before)
    cleared(d.decodeMock(s))
end)
test("fresh same-context HP update; omitted teams erase old data",function()
    local d=new(); local s=start(d); d.decodeMock(s); s.sampleId=2
    s.player.bytes=patch(s.player.bytes,86,2,0)
    state(d.decodeMock(s).playerParty[1].hpPercent,"VERIFIED",0)
    -- Omission changes the roster signature and retires, rather than retaining.
    s.sampleId=3; s.player=nil; cleared(d.decodeMock(s))
    local fresh=start(d); fresh.player=nil; fresh.enemy=nil
    local o=d.decodeMock(fresh); state(o.playerCount,"UNKNOWN"); state(o.active[2].species,"VERIFIED")
end)
test("active species switch needs new synthetic epoch",function()
    local d=new(); local s=start(d); d.decodeMock(s); s.sampleId=2
    s.battle.battleMons=patch(s.battle.battleMons,88,2,1439)
    cleared(d.decodeMock(s))
    s=start(d,{event="switch"}); s.battle.battleMons=patch(s.battle.battleMons,88,2,1439)
    assert(d.decodeMock(s).active[2].species.value.id==1439)
end)
test("unknown active species cannot borrow valid party or old active row",function()
    local d=new(); local s=start(d); d.decodeMock(s)
    s=start(d,{event="switch"}); s.battle.battleMons=patch(s.battle.battleMons,0,2,252)
    local o=d.decodeMock(s); state(o.active[1].species,"UNKNOWN")
    state(o.active[1].hp,"UNKNOWN"); state(o.active[1].moves[1].pp,"UNKNOWN")
    state(o.playerParty[1].hp,"VERIFIED",100)
end)
for _,flags in ipairs({5,13,79,0x20000D,0x40000D,0,0x80000004}) do
    test("unsupported/unknown context "..flags,function()
        local d=new(); d.decodeMock(start(d)); local s=start(d,{flags=flags})
        if flags~=0 and flags~=0x80000004 then
            s.battle.before.count=bytes(4,1); s.battle.before.positions=bytes(0,1)..bytes(1,1)..bytes(2,1)..bytes(3,1)
            s.battle.before.indexes=string.rep("\0",8); s.battle.after=copy(s.battle.before)
        end
        local o=d.decodeMock(s); cleared(o)
        state(o.battleContext,(flags==0 or flags==0x80000004) and "UNKNOWN" or "UNAVAILABLE")
    end)
end
for _,id in ipairs({252,1440,65535,706}) do
    test("invalid/unsupported species suppress party dependencies "..id,function()
        local d=new(); local s=start(d,{outside=true,ids={id}}); local o=d.decodeMock(s)
        assert(o.playerParty[1].species.value==nil)
        assert(o.playerParty[1].hp.value==nil and o.playerParty[1].heldItem.value==nil)
        assert(o.playerParty[1].moves[1].pp.value==nil)
    end)
end
test("move/item errors independent of HP; no effective baseline promotion",function()
    local d=new(); local s=start(d)
    s.player.bytes=patch(s.player.bytes,44,2,65535)
    s.battle.battleMons=patch(s.battle.battleMons,46,2,799)
    local o=d.decodeMock(s); state(o.playerParty[1].moves[1].identity,"UNKNOWN")
    state(o.playerParty[1].moves[1].pp,"UNKNOWN"); state(o.playerParty[1].hp,"VERIFIED",100)
    assert(o.active[1].heldItem.value==nil); state(o.active[1].hp,"VERIFIED",50)
    state(o.active[1].moves[1].effective,"UNKNOWN"); state(o.active[1].moves[1].damage,"UNKNOWN")
end)
test("invalid HP pair clears derived HP; eggs never inherit display defaults",function()
    local d=new(); local s=start(d)
    s.battle.battleMons=patch(s.battle.battleMons,40,2,201)
    s.player.bytes=patch(s.player.bytes,75,1,64)
    local o=d.decodeMock(s); state(o.active[1].hp,"UNKNOWN"); state(o.active[1].hpPercent,"UNKNOWN")
    state(o.playerParty[1].hp,"UNAVAILABLE"); state(o.playerParty[1].moves[1].pp,"UNAVAILABLE")
end)
test("missing/excessive PP caps never use baseline maximum",function()
    local d=new(); local s=start(d); s.battle.ppCaps=nil
    local o=d.decodeMock(s); state(o.active[1].moves[1].pp,"UNKNOWN")
    state(o.playerParty[1].moves[1].pp,"VERIFIED",20)
    s=start(d); s.battle.ppCaps=patch(s.battle.ppCaps,0,1,19)
    state(d.decodeMock(s).active[1].moves[1].pp,"UNKNOWN")
end)
test("unknown active ability cannot take party/source catalog name",function()
    local d=new(); local s=start(d); s.battle.battleMons=patch(s.battle.battleMons,32,1,255)
    local o=d.decodeMock(s); state(o.active[1].abilityId,"UNKNOWN"); state(o.active[1].abilityName,"UNKNOWN")
    state(o.active[1].hp,"VERIFIED",50)
end)
for _,key in ipairs({"stock","Tracker","notes","save","persistence","slots"}) do
    test("untrusted field/fallback input "..key,function()
        local d=new(); local s=start(d); d.decodeMock(s); s.sampleId=2
        local forged={confidence="VERIFIED",value=150,evidence="TEST_ONLY",liveConfidence="UNKNOWN"}
        forged.cycle=forged; s[key]=forged
        cleared(d.decodeMock(s)); assert(forged.value==150)
    end)
end
test("input/output/cross-instance alias contamination",function()
    local d=new(); local s=start(d); local o=d.decodeMock(s)
    o.playerParty[1].species.value.id=150; o.active[1].hp.value=999
    o.playerParty[1].sourceBaseline.value.types[1].value.id=999
    assert(d.snapshot().playerParty[1].species.value.id==1)
    assert(d.snapshot().active[1].hp.value==50)
    s.before.output="mutated-after-use"
    assert(d.snapshot().playerParty[1].species.value.id==1)
    local other=new(); assert(other.decodeMock(start(other)).playerParty[1].species.value.id==1)
    d.transition("reset"); cleared(d.snapshot())
    -- Returned old copies remain historical, never the current model.
    assert(o.epoch~=d.snapshot().epoch)
end)
test("no synthetic proof cannot arm or promote forged decoder tables",function()
    local d=new(); d.transition("start")
    cleared(d.decodeMock({player={slots={{species={confidence="VERIFIED",value={id=1}}}}}}))
    local s=start(d); s.player={slots={{species={confidence="VERIFIED",value={id=1}}}},count=1}
    cleared(d.decodeMock(s))
end)
test("host/notes/persistence/memory traps remain unused; mock sink is local",function()
    local calls=0
    local function forbidden() calls=calls+1; error("FORBIDDEN host/persistence/memory") end
    local trap=setmetatable({},{__index=forbidden,__newindex=forbidden})
    for _,name in ipairs({"Tracker","TrackerAPI","Memory","memory","Program","GameSettings","FileManager"}) do _G[name]=trap end
    local savedOpen=io.open; io.open=forbidden
    local d=new(); local localSink=d.decodeMock(start(d)); d.transition("end"); localSink=d.snapshot()
    cleared(localSink); assert(calls==0)
    local ok=pcall(function() trap.notes={} end); assert(not ok and calls==1)
    io.open=savedOpen
    for _,name in ipairs({"Tracker","TrackerAPI","Memory","memory","Program","GameSettings","FileManager"}) do _G[name]=nil end
end)
for _,corrupt in ipairs({
    function() return MOCK_SOURCE.." ",MOCK_PUBLIC_SOURCES,MOCK_MULTI end,
    function() return MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI.." " end,
    function() local s=copy(MOCK_PUBLIC_SOURCES); s["CFRU:include/pokemon.h"]=s["CFRU:include/pokemon.h"].." "; return MOCK_SOURCE,s,MOCK_MULTI end,
}) do
    test("exact public evidence lock rejects corruption "..#tests,function()
        local a,b,c=corrupt(); local d,f=module.newMock(a,b,c); assert(d==nil and f.confidence=="UNKNOWN")
    end)
end
local failed=0
for _,t in ipairs(tests) do
    local ok,err=pcall(t[2])
    if ok then print("PASS "..t[1]) else failed=failed+1; print("FAIL "..t[1]..": "..tostring(err)) end
end
print(string.format("UI projection mock tests: %d/%d PASS; TEST_ONLY; live UNKNOWN",#tests-failed,#tests))
if failed>0 then os.exit(1) end
