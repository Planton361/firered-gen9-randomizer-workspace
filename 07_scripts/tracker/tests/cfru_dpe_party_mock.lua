-- #692 byte fixtures use independent literal GBA offsets, never a game file.
local module = dofile("03_tools/tracker-extensions/CFRUDPEExtension/source_party_decoder.lua")
local decoder, failure = module.newMock(MOCK_SOURCE, MOCK_PUBLIC_SOURCES)
assert(decoder, failure and failure.reason)
local function copy(t)
    if type(t) ~= "table" then return t end
    local out={}; for k,v in pairs(t) do out[k]=copy(v) end; return out
end
local function patch(raw, offset, width, n)
    local bytes={}
    for i=1,width do bytes[i]=string.char(n%256); n=math.floor(n/256) end
    return raw:sub(1,offset) .. table.concat(bytes) .. raw:sub(offset+width+1)
end
local function fixture(ids)
    local raw=string.rep("\0",600)
    for slot,id in ipairs(ids or {1,501,1102,1294,1022,1439}) do
        local base=(slot-1)*100
        raw=patch(raw,base,4,0xABCD1234) -- Would select a shuffle/XOR path in stock FireRed.
        raw=patch(raw,base+4,4,0x12345678)
        raw=patch(raw,base+32,2,id); raw=patch(raw,base+34,2,743)
        for i,move in ipairs({33,733,991,0}) do raw=patch(raw,base+44+(i-1)*2,2,move) end
        for i,pp in ipairs({20,5,10,0}) do raw=patch(raw,base+52+i-1,1,pp) end
        raw=patch(raw,base+75,1,0x80); raw=patch(raw,base+84,1,50)
        raw=patch(raw,base+86,2,73); raw=patch(raw,base+88,2,120)
    end
    return raw
end
local function state(f,confidence,value)
    assert(f.confidence==confidence, f.reason or f.confidence)
    assert(f.evidence=="TEST_ONLY" and f.liveConfidence=="UNKNOWN")
    if confidence ~= "VERIFIED" then assert(f.value==nil)
    elseif value~=nil then assert(f.value==value) end
end
local function allUnknown(out)
    state(out.count,"UNKNOWN")
    for _,row in ipairs(out.slots) do
        for name,f in pairs(row) do
            if name=="moves" then for _,move in ipairs(f) do for _,v in pairs(move) do state(v,"UNKNOWN") end end
            else state(f,"UNKNOWN") end
        end
    end
end
local tests={}
local function test(name,fn) tests[#tests+1]={name,fn} end

test("exact schema-v2 identity and detached TEST_ONLY surface",function()
    assert(decoder.profileId==MOCK_PROFILE.metadata.profileId)
    assert(decoder.evidence=="TEST_ONLY" and decoder.liveConfidence=="UNKNOWN")
    assert(decoder.startup==nil and decoder.Memory==nil and decoder.beforeGameDataLoad==nil)
end)
test("six direct rows Gen1 mid-dex Gen8 Gen9 regional and final species",function()
    local out=decoder.decodeMock(fixture(),6)
    state(out.count,"VERIFIED",6)
    for slot,expect in ipairs({{1,"Bulbasaur"},{501,"Lucario"},{1102,"Grookey"},
        {1294,"Sprigatito"},{1022,"Raichu"},{1439,"Pecharunt"}}) do
        local row=out.slots[slot]
        state(row.occupied,"VERIFIED",true); state(row.species,"VERIFIED")
        assert(row.species.value.id==expect[1] and row.species.value.name==expect[2])
        state(row.level,"VERIFIED",50); state(row.hp,"VERIFIED",73); state(row.maxHP,"VERIFIED",120)
        state(row.hiddenAbility,"VERIFIED",true); state(row.isEgg,"VERIFIED",false)
        state(row.heldItem,"VERIFIED"); assert(row.heldItem.value.name=="Boost Energy")
        assert(row.moves[2].identity.value.name=="Wicked Blow" and row.moves[3].identity.value.name=="PsychicNoise")
        state(row.moves[2].pp,"VERIFIED",5); assert(row.moves[4].identity.value.absent)
        state(row.ability,"UNKNOWN"); state(row.effectiveTypes,"UNKNOWN")
        for _,move in ipairs(row.moves) do state(move.effective,"UNKNOWN") end
    end
end)
test("source types and regional identity remain distinct from effective types",function()
    local a=decoder.speciesBaseline(1).value
    assert(a.types[1].value.id==12 and a.types[2].value.id==3)
    local form=decoder.speciesBaseline(1022).value
    assert(form.identity.constant=="SPECIES_RAICHU_A" and form.types[1].value.id==13 and form.types[2].value.id==14)
    assert(decoder.resolve("species",26).value.constant=="SPECIES_RAICHU")
    state(form.formSupport,"UNKNOWN"); state(form.effectiveTypes,"UNKNOWN")
    assert(decoder.speciesBaseline(1294).value.types[1].value.name=="Grass")
    assert(decoder.speciesBaseline(1439).value.types[1].value.name=="Poison")
end)
test("baseline move values category and actual PP stay separate",function()
    local m=decoder.moveBaseline(733).value
    assert(m.power==75 and m.accuracy==100 and m.pp==5 and m.category==0 and m.type.value.id==17)
    m=decoder.moveBaseline(991).value
    assert(m.power==75 and m.pp==10 and m.category==1 and m.type.value.id==14)
    local row=decoder.decodeMock(patch(fixture(),53,1,0),6).slots[1]
    state(row.moves[2].pp,"VERIFIED",0)
    assert(row.moves[2].baseline.value.pp==5)
end)
test("baseline expanded abilities and contextual aliases never select party ability",function()
    assert(decoder.resolve("abilities",77).value.name=="Lingering Aroma")
    assert(decoder.resolve("abilities",254).value.name=="Pastel Veil")
    assert(decoder.resolve("abilities",179).value.name=="Stall")
    assert(#decoder.resolve("abilities",179).value.aliases==4)
    local row=decoder.decodeMock(fixture(),6).slots[1]
    assert(row.baselineSpecies.value.hiddenAbility.value.name=="Chlorophyll")
    state(row.ability,"UNKNOWN")
end)
test("all mapped species/moves baseline declarations and public mapping slots",function()
    for _,kind in ipairs({"species","moves","abilities","items","types"}) do
        for _,expected in ipairs(MOCK_PROFILE[kind]) do
            local got=decoder.resolve(kind,expected.id)
            if expected.state=="mapped" and expected.baselineData~="UNAVAILABLE" then
                state(got,"VERIFIED"); assert(got.value.name==expected.name and got.value.constant==expected.constant)
                if kind=="species" then state(decoder.speciesBaseline(expected.id),"VERIFIED") end
                if kind=="moves" then state(decoder.moveBaseline(expected.id),"VERIFIED") end
            elseif expected.state=="hole" then state(got,"UNKNOWN")
            elseif expected.id~=0 or kind=="types" then state(got,"UNAVAILABLE") end
        end
    end
end)
test("sentinels and empty slots are explicit known absence",function()
    local out=decoder.decodeMock(fixture({1}),1)
    state(out.count,"VERIFIED",1)
    for i=2,6 do
        state(out.slots[i].occupied,"VERIFIED",false)
        assert(out.slots[i].species.value.absent)
        state(out.slots[i].level,"UNAVAILABLE"); state(out.slots[i].moves[1].pp,"UNAVAILABLE")
    end
    out=decoder.decodeMock(string.rep("\0",600),0)
    state(out.count,"VERIFIED",0)
    for _,kind in ipairs({"species","moves","abilities","items"}) do assert(decoder.resolve(kind,0).value.absent) end
    local row=decoder.decodeMock(patch(fixture(),34,2,0),6).slots[1]
    assert(row.heldItem.value.absent and row.status.value.absent)
end)
test("all supplemental numeric fields agree with independent T1 Python parser",function()
    local function mapped(got,kind,id)
        local expected=decoder.resolve(kind,id)
        state(got,expected.confidence)
        if expected.value then assert(got.value.id==id) end
    end
    for _,expected in ipairs(MOCK_BASELINE.species) do
        local row=decoder.speciesBaseline(expected.id).value
        mapped(row.types[1],"types",expected.fields.type1); mapped(row.types[2],"types",expected.fields.type2)
        mapped(row.abilities[1],"abilities",expected.fields.ability1); mapped(row.abilities[2],"abilities",expected.fields.ability2)
        mapped(row.hiddenAbility,"abilities",expected.fields.hiddenAbility)
    end
    for _,expected in ipairs(MOCK_BASELINE.moves) do
        local row=decoder.moveBaseline(expected.id).value
        mapped(row.type,"types",expected.fields.type)
        assert(row.power==expected.fields.power and row.accuracy==expected.fields.accuracy)
        assert(row.pp==expected.fields.pp and row.category==expected.fields.split)
    end
end)
for _,kind in ipairs({"species","moves","abilities","items","types"}) do
    test(kind .. " missing negative fractional oversized and numeric string IDs",function()
        for _,id in ipairs({-1,1.5,65535,"1",false}) do state(decoder.resolve(kind,id),"UNKNOWN") end
        state(decoder.resolve(kind,nil),"UNKNOWN")
    end)
end
test("species/type holes missing baselines Egg reserved items and DPE-only exclusions",function()
    for _,id in ipairs({252,276}) do state(decoder.resolve("species",id),"UNKNOWN") end
    for _,id in ipairs({706,835,836,412}) do state(decoder.resolve("species",id),"UNAVAILABLE") end
    for _,id in ipairs({18,21,22}) do state(decoder.resolve("types",id),"UNKNOWN") end
    for _,id in ipairs({9,19,20}) do state(decoder.resolve("types",id),"UNAVAILABLE") end
    for id=776,798 do state(decoder.resolve("items",id),"UNAVAILABLE") end
    state(decoder.resolve("items",799),"UNKNOWN")
    assert(decoder.resolve("items",289).value.constant=="ITEM_TM01")
end)
test("unknown move invalidates only its dependent PP and baseline",function()
    local row=decoder.decodeMock(patch(fixture(),46,2,65535),6).slots[1]
    state(row.moves[2].identity,"UNKNOWN"); state(row.moves[2].baseline,"UNKNOWN"); state(row.moves[2].pp,"UNKNOWN")
    state(row.moves[1].pp,"VERIFIED",20); state(row.hp,"VERIFIED",73)
end)
test("absent move with nonzero PP is inconsistent",function()
    local row=decoder.decodeMock(patch(fixture(),55,1,1),6).slots[1]
    assert(row.moves[4].identity.value.absent); state(row.moves[4].pp,"UNKNOWN")
end)
test("species hole invalidates identity and species-derived data",function()
    local row=decoder.decodeMock(patch(fixture(),32,2,252),6).slots[1]
    state(row.species,"UNKNOWN"); state(row.baselineSpecies,"UNKNOWN"); state(row.effectiveTypes,"UNKNOWN")
end)
test("HP zero is valid; overflow and zero maximum invalidate both fields",function()
    state(decoder.decodeMock(patch(fixture(),86,2,0),6).slots[1].hp,"VERIFIED",0)
    for _,raw in ipairs({patch(fixture(),86,2,121),patch(fixture(),88,2,0)}) do
        local row=decoder.decodeMock(raw,6).slots[1]
        state(row.hp,"UNKNOWN"); state(row.maxHP,"UNKNOWN"); state(row.level,"VERIFIED",50)
    end
end)
test("source level bounds",function()
    for _,n in ipairs({0,101,255}) do state(decoder.decodeMock(patch(fixture(),84,1,n),6).slots[1].level,"UNKNOWN") end
    for _,n in ipairs({1,100}) do state(decoder.decodeMock(patch(fixture(),84,1,n),6).slots[1].level,"VERIFIED",n) end
end)
test("hidden ability bit independent of IV and Egg bits",function()
    for _,n in ipairs({0,31,32,63}) do state(decoder.decodeMock(patch(fixture(),75,1,n),6).slots[1].hiddenAbility,"VERIFIED",false) end
    for _,n in ipairs({128,159,160,191}) do state(decoder.decodeMock(patch(fixture(),75,1,n),6).slots[1].hiddenAbility,"VERIFIED",true) end
    local row=decoder.decodeMock(patch(fixture(),75,1,0xC0),6).slots[1]
    state(row.isEgg,"VERIFIED",true); state(row.level,"UNAVAILABLE"); state(row.ability,"UNAVAILABLE")
end)
test("source primary status and toxic counter; malformed combinations unknown",function()
    for n,label in pairs({[0]="NONE",[1]="SLEEP",[7]="SLEEP",[8]="POISON",[16]="BURN",[32]="FROSTBITE",[64]="PARALYSIS",[128]="TOXIC_POISON",[0xF80]="TOXIC_POISON"}) do
        local f=decoder.decodeMock(patch(fixture(),80,4,n),6).slots[1].status
        state(f,"VERIFIED"); assert(f.value.raw==n and f.value.primary==label)
    end
    for _,n in ipairs({9,24,0x100,0x1000,0x80000000,0xFFFFFFFF}) do
        state(decoder.decodeMock(patch(fixture(),80,4,n),6).slots[1].status,"UNKNOWN")
    end
end)
for _,n in ipairs({0,1,99,100,599,601}) do
    test("incomplete/oversized block length " .. n,function() allUnknown(decoder.decodeMock(string.rep("\0",n),0)) end)
end
test("missing and malformed buffers/counts never become zero",function()
    for _,raw in ipairs({false,{},42}) do allUnknown(decoder.decodeMock(raw,0)) end
    allUnknown(decoder.decodeMock(nil,0))
    for _,count in ipairs({-1,7,1.5,"6",false}) do allUnknown(decoder.decodeMock(fixture(),count)) end
    allUnknown(decoder.decodeMock(fixture(),nil))
end)
test("count occupied-prefix consistency",function()
    allUnknown(decoder.decodeMock(fixture(),5))
    allUnknown(decoder.decodeMock(patch(fixture(),132,2,0),6))
    allUnknown(decoder.decodeMock(fixture({1}),0))
end)
test("no stale fields after failed sample and caller mutations",function()
    local old=decoder.decodeMock(fixture(),6)
    old.slots[1].species.value.name="spoof"
    old.slots[1].baselineSpecies.value.types[1].value.name="spoof"
    allUnknown(decoder.decodeMock("",6))
    local fresh=decoder.decodeMock(fixture(),6)
    assert(fresh.slots[1].species.value.name=="Bulbasaur")
    assert(fresh.slots[1].baselineSpecies.value.types[1].value.name=="Grass")
    state(fresh.slots[1].hp,"VERIFIED",73)
end)
for _,case in ipairs({
    {"wrong schema",function(raw) return raw:gsub('"schemaVersion": 2','"schemaVersion": 1',1) end},
    {"wrong pin",function(raw) return raw:gsub(MOCK_PROFILE.metadata.revisions.CFRU,string.rep("0",40),1) end},
    {"profile name",function() return "cfru-dpe-gen9" end},
    {"truncated profile",function(raw) return raw:sub(1,-2) end},
    {"same length corruption",function(raw) return "X" .. raw:sub(2) end},
    {"missing profile",function() return nil end},
    {"caller decoded table",function() return MOCK_PROFILE end},
}) do
    test(case[1] .. " fails entire constructor",function()
        local got,fail=module.newMock(case[2](MOCK_SOURCE),MOCK_PUBLIC_SOURCES)
        assert(got==nil); state(fail,"UNKNOWN")
    end)
end
for locator in pairs(MOCK_PUBLIC_SOURCES) do
    test("missing/changed supplemental source " .. locator,function()
        for _,replacement in ipairs({false,"changed"}) do
            local sources=copy(MOCK_PUBLIC_SOURCES); sources[locator]=replacement
            local got,fail=module.newMock(MOCK_SOURCE,sources)
            assert(got==nil); state(fail,"UNKNOWN")
        end
    end)
end
test("missing/extra public source objects rejected",function()
    local sources=copy(MOCK_PUBLIC_SOURCES); sources.extra="not read"
    local got,fail=module.newMock(MOCK_SOURCE,sources); assert(got==nil); state(fail,"UNKNOWN")
    got,fail=module.newMock(MOCK_SOURCE,nil); assert(got==nil); state(fail,"UNKNOWN")
end)
for _,case in ipairs(tests) do
    local ok,err=pcall(case[2]); assert(ok,case[1] .. ": " .. tostring(err))
end
print("PASS: #692 Lua 5.4 source/synthetic party decoder " .. #tests .. "/" .. #tests)
print("CFRUDPE_TRACKER_PARTY_DECODER_MOCK_READY: candidate tests PASS; review/acceptance pending")
