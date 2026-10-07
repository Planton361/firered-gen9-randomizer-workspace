-- Independent literal offsets/widths; generated strings, no game data.
local module=dofile("03_tools/tracker-extensions/CFRUDPEExtension/source_battle_decoder.lua")
local partyModule=dofile("03_tools/tracker-extensions/CFRUDPEExtension/source_party_decoder.lua")
local function new()
    local d,f=module.newMock(MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
    assert(d,f and f.reason); return d
end
local function copy(t)
    if type(t)~="table" then return t end
    local out={}; for k,v in pairs(t) do out[k]=copy(v) end; return out
end
local function bytes(n,w)
    local out={}; for i=1,w do out[i]=string.char(n%256); n=math.floor(n/256) end
    return table.concat(out)
end
local function patch(s,o,w,n) return s:sub(1,o)..bytes(n,w)..s:sub(o+w+1) end
local function rows(ids)
    local s=string.rep("\0",352)
    for i,id in ipairs(ids or {1,1294}) do
        local base=(i-1)*88
        for _,f in ipairs({{0,2,id},{12,2,33},{14,2,733},{16,2,991},{18,2,0},
            {24,1,14},{32,1,254},{33,1,17},{34,1,13},{36,1,20},{37,1,5},{38,1,10},
            {40,2,0x123},{42,1,50},{44,2,0x234},{46,2,743},{76,4,0xF80},{80,4,0x80000000}}) do
            s=patch(s,base+f[1],f[2],f[3])
        end
    end
    return s
end
local function sample(d,flags,ids,event)
    local epoch=d.transition(event or "start")
    local c={epoch=epoch,state="ACTIVE",output="synthetic-output",battle="synthetic-encounter",
        flags=bytes(flags or 4,4),count=bytes(2,1),positions=bytes(0,1)..bytes(1,1)..bytes(255,1)..bytes(255,1),
        indexes=bytes(5,2)..bytes(2,2)..bytes(0xFFFF,2)..bytes(0xFFFF,2)}
    return {epoch=epoch,before=c,after=copy(c),battleMons=rows(ids),
        ppCaps=bytes(35,1)..bytes(5,1)..bytes(10,1)..bytes(0,1)..bytes(35,1)..bytes(5,1)..bytes(10,1)..bytes(0,1)..string.rep("\0",8)}
end
local function state(f,c,v)
    assert(f.confidence==c,f.reason or f.confidence)
    assert(f.evidence=="TEST_ONLY" and f.liveConfidence=="UNKNOWN")
    if c~="VERIFIED" then assert(f.value==nil) elseif v~=nil then assert(f.value==v) end
end
local function all(out,c)
    assert(out.evidence=="TEST_ONLY" and out.liveConfidence=="UNKNOWN")
    state(out.context,c); state(out.trainerA,c); state(out.trainerB,c)
    for _,r in ipairs(out.battlers) do
        for k,f in pairs(r) do
            if k=="moves" then for _,m in ipairs(f) do for _,v in pairs(m) do state(v,c) end end
            else state(f,c) end
        end
    end
end
local tests={}
local function test(name,f) tests[#tests+1]={name,f} end
test("detached exact identity and initial unknown",function()
    local d=new(); all(d.snapshot(),"UNKNOWN")
    assert(d.evidence=="TEST_ONLY" and d.liveConfidence=="UNKNOWN")
    assert(d.startup==nil and d.Memory==nil and d.beforeGameDataLoad==nil)
end)
for _,ids in ipairs({{1,26},{1102,1294},{1022,1439}}) do
    test("Gen1/8/9 and regional identity "..ids[1].."/"..ids[2],function()
        local d=new(); local o=d.decodeMock(sample(d,4,ids))
        state(o.context,"VERIFIED"); assert(o.context.value.kind=="WILD")
        for i,id in ipairs(ids) do
            local r=o.battlers[i]; state(r.species,"VERIFIED"); assert(r.species.value.id==id)
            state(r.hp,"VERIFIED",0x123); state(r.maxHP,"VERIFIED",0x234); state(r.level,"VERIFIED",50)
            state(r.ability,"VERIFIED"); assert(r.ability.value.id==254)
            state(r.abilityName,"UNKNOWN"); state(r.heldItem,"VERIFIED"); assert(r.heldItem.value.id==743)
            for k,v in pairs({type1=17,type2=13,type3=14}) do state(r[k],"VERIFIED"); assert(r[k].value.id==v) end
            state(r.status1,"VERIFIED"); assert(r.status1.value.raw==0xF80)
            state(r.status2,"VERIFIED",0x80000000); state(r.status2Meaning,"UNAVAILABLE")
            for m,id2 in ipairs({33,733,991,0}) do state(r.moves[m].identity,"VERIFIED"); assert(r.moves[m].identity.value.id==id2) end
            state(r.moves[2].pp,"VERIFIED",5); state(r.moves[4].pp,"VERIFIED",0)
            state(r.moves[1].effective,"UNKNOWN")
        end
        state(o.trainerA,"UNAVAILABLE"); state(o.trainerB,"UNAVAILABLE")
        assert(o.battlers[1].species.value.constant~="SPECIES_NONE")
    end)
end
test("u16 stride/team ownership/one-based slots; inactive poison bytes ignored",function()
    local d=new(); local o=d.decodeMock(sample(d))
    for i,e in ipairs({{0,"PLAYER",5,6},{1,"ENEMY",2,3}}) do
        local r=o.battlers[i]; state(r.battler,"VERIFIED",e[1]); state(r.position,"VERIFIED",e[1])
        state(r.team,"VERIFIED",e[2]); state(r.partyIndex,"VERIFIED",e[3]); state(r.partySlot,"VERIFIED",e[4])
    end
    state(o.battlers[3].species,"UNAVAILABLE"); state(o.battlers[4].hp,"UNAVAILABLE")
end)
for _,index in ipairs({6,0x100,0x105,0xFFFF}) do
    test("u16 high byte/illegal slot "..index,function()
        local d=new(); local s=sample(d); s.before.indexes=patch(s.before.indexes,2,2,index); s.after=copy(s.before)
        all(d.decodeMock(s),"UNKNOWN"); all(d.snapshot(),"UNKNOWN")
    end)
end
test("trainer A independently trusted u16; trainer B never assumed global",function()
    local d=new(); local s=sample(d,12)
    s.before.trainerA={epoch=s.epoch,bytes=bytes(0x1234,2),trusted=true,source="gTrainerBattleOpponent_A"}
    s.before.trainerB={bytes=bytes(777,2),trusted=true}; s.after=copy(s.before)
    local o=d.decodeMock(s); state(o.trainerA,"VERIFIED"); assert(o.trainerA.value.id==0x1234)
    assert(o.trainerA.value.scope=="synthetic-context-only" and o.trainerA.value.name==nil)
    state(o.trainerB,"UNAVAILABLE"); assert(o.context.value.kind=="TRAINER")
end)
test("missing/untrusted trainer A does not manufacture an identity",function()
    local d=new(); local s=sample(d,12); state(d.decodeMock(s).trainerA,"UNKNOWN")
    s=sample(d,12); s.before.trainerA={epoch=s.epoch,bytes=bytes(7,2),trusted=false,source="gTrainerBattleOpponent_A"}
    s.after=copy(s.before); state(d.decodeMock(s).trainerA,"UNKNOWN")
end)
test("wild context ignores trusted trainer identity",function()
    local d=new(); local s=sample(d)
    s.before.trainerA={epoch=s.epoch,bytes=bytes(7,2),trusted=true,source="gTrainerBattleOpponent_A"}
    s.after=copy(s.before); state(d.decodeMock(s).trainerA,"UNAVAILABLE")
end)
test("trainer trust/epoch/width/source failures discard previous data",function()
    for _,mutate in ipairs({function(t) t.epoch=t.epoch-1 end,function(t) t.bytes="x" end,
        function(t) t.source="vanilla-address" end,function(t) t.trusted="true" end}) do
        local d=new(); local s=sample(d,12); d.decodeMock(s)
        s.before.trainerA={epoch=s.epoch,bytes=bytes(7,2),trusted=true,source="gTrainerBattleOpponent_A"}
        mutate(s.before.trainerA); s.after=copy(s.before); all(d.decodeMock(s),"UNKNOWN")
    end
end)
test("active battle fields take precedence while party/baseline stay separate",function()
    local p=assert(partyModule.newMock(MOCK_SOURCE,MOCK_PUBLIC_SOURCES))
    local raw=string.rep("\0",600); raw=patch(raw,32,2,26); raw=patch(raw,84,1,7)
    raw=patch(raw,86,2,10); raw=patch(raw,88,2,20)
    local partySnapshot=p.decodeMock(raw,1)
    local d=new(); local s=sample(d); s.party=partySnapshot -- Deliberately ignored, no fallback input.
    local r=d.decodeMock(s).battlers[1]
    assert(partySnapshot.slots[1].species.value.id==26 and partySnapshot.slots[1].hp.value==10)
    assert(r.species.value.id==1 and r.hp.value==0x123 and r.type1.value.id==17)
    assert(p.speciesBaseline(1).value.types[1].value.id==12)
    s=sample(d); s.battleMons=""; s.party=partySnapshot; all(d.decodeMock(s),"UNKNOWN")
end)
for _,event in ipairs({"start","end","reset","output-switch","switch","bogus"}) do
    test("transition immediately clears "..event,function()
        local d=new(); local s=sample(d); state(d.decodeMock(s).battlers[1].hp,"VERIFIED")
        d.transition(event); all(d.snapshot(),"UNKNOWN"); all(d.decodeMock(s),"UNKNOWN")
    end)
end
test("new switch sample recovers; previous species and PP never persist",function()
    local d=new(); d.decodeMock(sample(d)); local s=sample(d,12,{1022,1102},"switch")
    s.battleMons=patch(s.battleMons,40,2,0); s.battleMons=patch(s.battleMons,37,1,0)
    local r=d.decodeMock(s).battlers[1]; assert(r.species.value.constant=="SPECIES_RAICHU_A")
    state(r.hp,"VERIFIED",0); state(r.moves[2].pp,"VERIFIED",0)
end)
test("end/reset/output switch stay disarmed even with the new epoch until start",function()
    for _,event in ipairs({"end","reset","output-switch"}) do
        local d=new(); local s=sample(d); d.decodeMock(s)
        local epoch=d.transition(event); s.epoch=epoch; s.before.epoch=epoch; s.after=copy(s.before)
        all(d.decodeMock(s),"UNKNOWN")
        state(d.decodeMock(sample(d)).context,"VERIFIED")
    end
end)
test("single fields carry the current epoch and 0..5 team indices",function()
    local d=new(); local s=sample(d)
    s.before.indexes=bytes(0,2)..bytes(5,2)..bytes(65535,2)..bytes(65535,2); s.after=copy(s.before)
    local o=d.decodeMock(s)
    state(o.battlers[1].partySlot,"VERIFIED",1); state(o.battlers[2].partySlot,"VERIFIED",6)
    assert(o.battlers[1].hp.sampleEpoch==s.epoch and o.trainerB.sampleEpoch==s.epoch)
end)
for _,key in ipairs({"output","battle","flags","count","positions","indexes"}) do
    test("before/after context drift "..key,function()
        local d=new(); local s=sample(d); d.decodeMock(s)
        s.after[key]=s.after[key].."x"; all(d.decodeMock(s),"UNKNOWN")
    end)
end
test("unchanged before/after cannot conceal unannounced switch/output/trainer change",function()
    for _,key in ipairs({"indexes","output","battle","flags"}) do
        local d=new(); local s=sample(d); d.decodeMock(s)
        if key=="indexes" then s.before[key]=patch(s.before[key],0,2,4)
        elseif key=="flags" then s.before[key]=bytes(12,4) else s.before[key]="new" end
        s.after=copy(s.before); all(d.decodeMock(s),"UNKNOWN")
    end
    local d=new(); local s=sample(d,12); d.decodeMock(s)
    s.before.trainerA={epoch=s.epoch,bytes=bytes(7,2),trusted=true,source="gTrainerBattleOpponent_A"}
    s.after=copy(s.before); all(d.decodeMock(s),"UNKNOWN")
end)
for _,flags in ipairs({0,8,1,9,0x44,0x20000C,0x84,0x100004,0x80000004,0xFFFFFFFF}) do
    test("ambiguous/unsupported flag combination "..flags,function()
        local d=new(); all(d.decodeMock(sample(d,flags)),"UNKNOWN")
    end)
end
for _,flags in ipairs({5,13,0x4F,0x20000D,0x40000D}) do
    test("coherent known double/multi explicitly unavailable "..flags,function()
        local d=new(); local s=sample(d,flags)
        s.before.count=bytes(4,1); s.before.positions=bytes(0,1)..bytes(1,1)..bytes(2,1)..bytes(3,1)
        s.before.indexes=bytes(0,2)..bytes(1,2)..bytes(3,2)..bytes(4,2); s.after=copy(s.before)
        all(d.decodeMock(s),"UNAVAILABLE")
        s=sample(d,flags); all(d.decodeMock(s),"UNKNOWN") -- Wrong count is not known unsupported.
    end)
end
for _,count in ipairs({0,1,3,4,5,255}) do
    test("invalid single count "..count,function()
        local d=new(); local s=sample(d); s.before.count=bytes(count,1); s.after=copy(s.before)
        all(d.decodeMock(s),"UNKNOWN")
    end)
end
for _,positions in ipairs({"\0\0\255\255","\1\0\255\255","\0\3\255\255","\0\255\255\255"}) do
    test("illegal/duplicate/reversed single positions "..positions:byte(2),function()
        local d=new(); local s=sample(d); s.before.positions=positions; s.after=copy(s.before)
        all(d.decodeMock(s),"UNKNOWN")
    end)
end
for _,key in ipairs({"flags","count","positions","indexes"}) do
    test("missing/truncated/oversized context block "..key,function()
        for _,mode in ipairs({"missing","short","long","table"}) do
            local d=new(); local s=sample(d)
            if mode=="missing" then s.before[key]=nil elseif mode=="short" then s.before[key]=s.before[key]:sub(2)
            elseif mode=="long" then s.before[key]=s.before[key].."x" else s.before[key]={} end
            s.after=copy(s.before); all(d.decodeMock(s),"UNKNOWN")
        end
    end)
end
test("nil/metatable/wrong input type and incomplete lifecycle context",function()
    for _,input in ipairs({false,42,"x",setmetatable({},{})}) do local d=new(); all(d.decodeMock(input),"UNKNOWN") end
    local d=new(); all(d.decodeMock(nil),"UNKNOWN")
    for _,key in ipairs({"epoch","state","output","battle"}) do
        d=new(); local s=sample(d); s.before[key]=nil; s.after=copy(s.before); all(d.decodeMock(s),"UNKNOWN")
    end
    d=new(); local s=sample(d); s.after=nil; all(d.decodeMock(s),"UNKNOWN")
end)
for _,length in ipairs({0,1,87,88,176,351,353,400}) do
    test("malformed battle buffer "..length,function()
        local d=new(); local s=sample(d); d.decodeMock(s)
        s.battleMons=string.rep("\0",length); all(d.decodeMock(s),"UNKNOWN")
    end)
end
test("non-string battle blocks cannot reach byte reader",function()
    for _,input in ipairs({false,{},42}) do local d=new(); local s=sample(d); s.battleMons=input; all(d.decodeMock(s),"UNKNOWN") end
    local d=new(); local s=sample(d); s.battleMons=nil; all(d.decodeMock(s),"UNKNOWN")
end)
test("unknown species/absence/egg withhold dependent row without stock fallback",function()
    for _,id in ipairs({0,252,706,412,65535}) do
        local d=new(); local s=sample(d); d.decodeMock(s); s.battleMons=patch(s.battleMons,0,2,id)
        local r=d.decodeMock(s).battlers[1]; assert(r.species.confidence~="VERIFIED")
        state(r.hp,"UNKNOWN"); state(r.moves[1].pp,"UNKNOWN"); state(r.ability,"UNKNOWN")
    end
    local d=new(); local s=sample(d); s.battleMons=patch(s.battleMons,23,1,64)
    local r=d.decodeMock(s).battlers[1]; state(r.species,"UNAVAILABLE"); state(r.hp,"UNKNOWN")
end)
test("invalid HP and level clear fields independently",function()
    for _,pair in ipairs({{40,2,0x235},{44,2,0}}) do
        local d=new(); local s=sample(d); d.decodeMock(s); s.battleMons=patch(s.battleMons,pair[1],pair[2],pair[3])
        local r=d.decodeMock(s).battlers[1]; state(r.hp,"UNKNOWN"); state(r.maxHP,"UNKNOWN"); state(r.species,"VERIFIED")
    end
    for _,n in ipairs({0,101,255}) do
        local d=new(); local s=sample(d); s.battleMons=patch(s.battleMons,42,1,n)
        state(d.decodeMock(s).battlers[1].level,"UNKNOWN")
    end
end)
test("PP caps required; invalid PP/unknown move never get baseline PP",function()
    for _,key in ipairs({"missing","short","overcap","unknown","absent"}) do
        local d=new(); local s=sample(d)
        if key=="missing" then s.ppCaps=nil elseif key=="short" then s.ppCaps="x"
        elseif key=="overcap" then s.battleMons=patch(s.battleMons,37,1,6)
        elseif key=="unknown" then s.battleMons=patch(s.battleMons,14,2,65535)
        else s.battleMons=patch(s.battleMons,14,2,0) end
        local r=d.decodeMock(s).battlers[1]; state(r.moves[2].pp,"UNKNOWN"); state(r.hp,"VERIFIED")
    end
end)
test("unknown move/item/ability/types retain explicit states",function()
    for _,f in ipairs({{14,2,65535,"move","UNKNOWN"},{46,2,779,"heldItem","UNAVAILABLE"},
        {46,2,65535,"heldItem","UNKNOWN"},{32,1,255,"ability","UNKNOWN"},
        {33,1,18,"type1","UNKNOWN"},{24,1,9,"type3","UNAVAILABLE"}}) do
        local d=new(); local s=sample(d); s.battleMons=patch(s.battleMons,f[1],f[2],f[3])
        local r=d.decodeMock(s).battlers[1]; state(f[4]=="move" and r.moves[2].identity or r[f[4]],f[5])
        state(r.hp,"VERIFIED")
    end
end)
test("primary status source controls and invalid 32-bit combinations",function()
    for n,label in pairs({[0]="NONE",[7]="SLEEP",[8]="POISON",[16]="BURN",[32]="FROSTBITE",[64]="PARALYSIS",[0xF80]="TOXIC_POISON"}) do
        local d=new(); local s=sample(d); s.battleMons=patch(s.battleMons,76,4,n)
        local f=d.decodeMock(s).battlers[1].status1; state(f,"VERIFIED"); assert(f.value.primary==label)
    end
    for _,n in ipairs({9,24,0x100,0x1080,0x80000000,0xFFFFFFFF}) do
        local d=new(); local s=sample(d); s.battleMons=patch(s.battleMons,76,4,n)
        state(d.decodeMock(s).battlers[1].status1,"UNKNOWN")
    end
    local d=new(); local s=sample(d); s.battleMons=patch(s.battleMons,80,4,128)
    state(d.decodeMock(s).battlers[1].status2,"UNKNOWN")
end)
test("every returned confidence stays TEST_ONLY/live UNKNOWN; caller cannot poison state",function()
    local d=new(); local s=sample(d); local o=d.decodeMock(s)
    local function walk(t)
        if type(t)~="table" then return end
        if t.confidence then state(t,t.confidence) end
        for _,v in pairs(t) do walk(v) end
    end
    walk(o); o.battlers[1].species.value.name="spoof"; o.context.value.flags=0
    local fresh=d.snapshot(); assert(fresh.battlers[1].species.value.name=="Bulbasaur" and fresh.context.value.flags==4)
    all(d.decodeMock({epoch=s.epoch}),"UNKNOWN")
    state(d.decodeMock(sample(d)).battlers[1].hp,"VERIFIED",0x123)
end)
test("wrong profile/source/trainer-B binding construction fails closed",function()
    for _,args in ipairs({{MOCK_SOURCE.." ",MOCK_PUBLIC_SOURCES,MOCK_MULTI},
        {MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI.." "},{MOCK_SOURCE,{},MOCK_MULTI}}) do
        local d,f=module.newMock(table.unpack(args)); assert(d==nil); state(f,"UNKNOWN")
    end
    local d,f=module.newMock(MOCK_SOURCE,MOCK_PUBLIC_SOURCES,nil); assert(d==nil); state(f,"UNKNOWN")
end)
local failures=0
for _,t in ipairs(tests) do
    local ok,why=pcall(t[2]); io.write((ok and "PASS " or "FAIL ")..t[1]..(ok and "" or ": "..tostring(why)).."\n")
    if not ok then failures=failures+1 end
end
io.write("Battle mock tests: "..(#tests-failures).."/"..#tests.." PASS; evidence=TEST_ONLY liveConfidence=UNKNOWN\n")
if failures>0 then os.exit(1) end
