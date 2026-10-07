-- ROM-free Lua 5.1/5.4 tests. Public text/profile are injected by the Python runner.
local extensionPath = "03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua"
local shaPath = "03_tools/tracker-extensions/CFRUDPEExtension/profile_sha256.lua"
local function clone(t)
    if type(t) ~= "table" then return t end
    local out = {}
    for k,v in pairs(t) do out[k] = clone(v) end
    return out
end
local function loadExtension(globals)
    local env = globals or {}
    setmetatable(env, {__index = _G})
    env._G=env
    local chunk
    if setfenv then
        chunk = assert(loadfile(extensionPath))
        setfenv(chunk,env)
    else chunk = assert(loadfile(extensionPath,"t",env)) end
    return chunk()
end
local function host()
    local h = {testOnly=true,trackerRevision=MOCK_PROFILE.metadata.revisions.Tracker,
        reads=0,writes=0,stockInitializations=0,restarts=0,
        GameSettings={gamename="Pokemon FireRed",pstats=99,estats=98},
        Program={Addresses={sizeofPokemonStruct=77,sizeofBattleMove=9},sizeofPokemonStruct=999},
        PokemonData={Addresses={offsetTypes=3,offsetAbilities=4},offsetTypes=999},
        Options={["Override Button Mode to LR"]=true},Main={forceRestart=false},Memory={},
        current={output="SYNTHETIC:Control",session="MOCK:session",epoch=1},identityValue=691}
    h.originalInitialize = function() h.stockInitializations=h.stockInitializations+1; h.GameSettings.gamename="Pokemon FireRed" end
    h.GameSettings.initialize = h.originalInitialize
    h.IronmonTracker={startTracker=function() h.restarts=h.restarts+1; h.GameSettings.initialize(); return true end}
    h.decodePublicSource=function(raw) assert(raw==MOCK_SOURCE); return clone(MOCK_PROFILE) end
    h.getSession=function() return clone(h.current) end
    h.Memory.read32=function(a) assert(a==0x08001000); h.reads=h.reads+1; return h.identityValue end
    for _,k in ipairs({"write8","write16","write32","writebyte","writeword","writedword",
        "write_u8","write_u16_le","write_u32_le"}) do
        h.Memory[k]=function() h.writes=h.writes+1; error("FORBIDDEN memory write",0) end
    end
    return h
end
local function request(h)
    local b={schema="cfru-dpe-mock-binding",schemaVersion=1,profileId=MOCK_PROFILE.metadata.profileId,
        trackerRevision=h.trackerRevision,extensionVersion="0.2.0",evidence="SYNTHETIC_ONLY",
        output=h.current.output,session=h.current.session,epoch=h.current.epoch,
        capabilities={playerParty=true,enemyParty=true},addresses={},
        identity={address=0x08001000,domain="ROM",widthBytes=4,value=691}}
    for _,k in ipairs({"gPlayerParty","gEnemyParty","gPlayerPartyCount"}) do
        local d=MOCK_PROFILE.addresses[k]
        b.addresses[k]={address=d.sourceAddress,domain=d.domain,widthBytes=d.widthBytes,
            kind=d.kind,indirection=d.indirection,source=d.source}
    end
    return {sourceText=MOCK_SOURCE,binding=b,
        gameSettings={pstats=b.addresses.gPlayerParty.address,estats=b.addresses.gEnemyParty.address,
            gPlayerPartyCount=b.addresses.gPlayerPartyCount.address},
        overrides={Program={Addresses={sizeofPokemonStruct=100,sizeofBaseStatsPokemon=28,
            sizeofBattlePokemon=88,sizeofBattleMove=12}},PokemonData={Addresses={offsetTypes=6,offsetAbilities=22}}}}
end
local mockAPI=loadExtension()
local function fixture()
    local h=host()
    local ext=mockAPI.newMockHarness(h)
    local r=request(h)
    ext.setMockInputs(r)
    assert(ext.beforeGameDataLoad())
    return h,ext,r
end
local function assertBlocked(h,e)
    assert(e.state.status=="UNKNOWN" and e.state.confidence=="UNKNOWN")
    assert(h.GameSettings.gamename=="Unsupported Game")
    assert(h.stockInitializations==0 and h.writes==0)
    assert(next(e.getActiveBattleMons())==nil and not e.readActiveBattleMons())
    assert(e.state.binding==nil and next(e.state.snapshots)==nil)
    assert(h.Options["Override Button Mode to LR"]==false)
end
local tests={}
local function test(name,fn) tests[#tests+1]={name,fn} end

test("sha256 known answers and boundary lengths",function()
    local sha=dofile(shaPath)
    assert(sha("")=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    assert(sha("abc")=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    for _,vector in ipairs(MOCK_SHA_VECTORS) do assert(sha(vector[1])==vector[2]) end
end)

test("production denies before stock initialization and never opens files",function()
    local h=host()
    local env={GameSettings=h.GameSettings,Main=h.Main,Options=h.Options,IronmonTracker=h.IronmonTracker,
        Memory=h.Memory,FileManager={JsonLibrary={decode=h.decodePublicSource},
            decodeJsonFile=function() error("file import forbidden") end},print=function() end}
    local nativeDebug=debug
    env.debug=setmetatable({getinfo=function(f,what)
        if f==h.originalInitialize then return {source="@/mock/ironmon_tracker/GameSettings.lua",linedefined=284} end
        if type(f)=="number" then return nativeDebug.getinfo(f+1,what) end
        return nativeDebug.getinfo(f,what)
    end},{__index=nativeDebug})
    local ext=loadExtension(env)
    assert(ext.validatePublicSource(MOCK_SOURCE))
    assert(ext.beforeGameDataLoad())
    assert(not h.GameSettings.initialize())
    assert(not ext.startup())
    assertBlocked(h,ext)
    assert(h.reads==0)
    assert(not pcall(ext.setMockInputs,request(h)))
    assert(not pcall(ext.newMockHarness,h))
end)

test("complete synthetic transaction is TEST_ONLY with UNKNOWN live confidence",function()
    local h,e=fixture()
    local before=h.GameSettings.initialize
    assert(e.beforeGameDataLoad() and h.GameSettings.initialize==before)
    assert(h.GameSettings.initialize())
    assert(e.state.status=="TEST_ONLY" and e.state.confidence=="UNKNOWN")
    assert(h.GameSettings.pstats==MOCK_PROFILE.addresses.gPlayerParty.sourceAddress)
    assert(h.GameSettings.estats==MOCK_PROFILE.addresses.gEnemyParty.sourceAddress)
    assert(h.Program.Addresses.sizeofPokemonStruct==100 and h.Program.sizeofPokemonStruct==999)
    assert(h.PokemonData.Addresses.offsetTypes==6 and h.PokemonData.offsetTypes==999)
    assert(h.GameSettings.gamename=="Unsupported Game")
    assert(e.startup() and e.checkSession() and h.writes==0 and h.stockInitializations==0)
    assert(e.state.capabilities.partyDecoder=="UNAVAILABLE")
    e.unload()
    assert(h.Program.Addresses.sizeofPokemonStruct==77 and h.Program.Addresses.sizeofBaseStatsPokemon==nil)
    assert(h.PokemonData.Addresses.offsetTypes==3 and h.GameSettings.pstats==99)
    assertBlocked(h,e)
end)

local invalid={
    {"fractional binding schema",function(r) r.binding.schemaVersion=1.5 end},
    {"unsupported binding schema",function(r) r.binding.schemaVersion=2 end},
    {"source schema v1",function(r) r.sourceText=r.sourceText:gsub('"schemaVersion": 2','"schemaVersion": 1',1) end},
    {"source CFRU revision",function(r) r.sourceText=r.sourceText:gsub(MOCK_PROFILE.metadata.revisions.CFRU,string.rep("0",40),1) end},
    {"wrong profile",function(r) r.binding.profileId="sha256:untrusted" end},
    {"wrong Tracker revision",function(r) r.binding.trackerRevision=string.rep("0",40) end},
    {"wrong extension",function(r) r.binding.extensionVersion="0.1.0" end},
    {"claimed production proof",function(r) r.binding.evidence="VERIFIED" end},
    {"manual output selection",function(r) r.binding.output="Control" end},
    {"placeholder session",function(r) r.binding.session="UNKNOWN" end},
    {"missing manifest",function(r) r.overrides=nil end},
    {"extra manifest key",function(r) r.localPath="not-read" end},
    {"missing capability",function(r) r.binding.capabilities.enemyParty=nil end},
    {"disabled dependency",function(r) r.binding.capabilities.playerParty=false end},
    {"missing address",function(r) r.binding.addresses.gEnemyParty=nil end},
    {"unresolved extra address",function(r) r.binding.addresses.gBaseStats={kind="UNRESOLVED"} end},
    {"wrong descriptor",function(r) r.binding.addresses.gPlayerParty.kind="repoint-anchor" end},
    {"pointer indirection",function(r) r.binding.addresses.gPlayerParty.indirection=1 end},
    {"wrong provenance",function(r) r.binding.addresses.gPlayerParty.source="BPRE guess" end},
    {"out of range",function(r) r.binding.addresses.gPlayerParty.address=0x02040000 end},
    {"wrong domain",function(r) r.binding.addresses.gPlayerParty.domain="BIOS" end},
    {"string number",function(r) r.binding.addresses.gPlayerParty.address="02024284" end},
    {"misaligned identity",function(r) r.binding.identity.address=0x08001001 end},
    {"identity domain overflow",function(r) r.binding.identity.address=0x09000000 end},
    {"identity unsupported width",function(r) r.binding.identity.widthBytes=3 end},
    {"flat overrides",function(r) r.overrides.Program={sizeofPokemonStruct=100} end},
    {"wrong effective layout",function(r) r.overrides.Program.Addresses.sizeofPokemonStruct=80 end},
    {"unsafe extra override",function(r) r.overrides.Memory={write8=1} end},
    {"wrong party alias",function(r) r.gameSettings.pstats=123 end},
    {"truncated public source",function(r) r.sourceText=r.sourceText:sub(1,-2) end},
    {"content spoof same length",function(r) r.sourceText="X"..r.sourceText:sub(2) end},
}
for _,case in ipairs(invalid) do
    local name,mutate=case[1],case[2]
    test("reject "..name,function()
        local h,e,r=fixture()
        mutate(r)
        e.setMockInputs(r)
        assert(not h.GameSettings.initialize())
        assert(h.GameSettings.pstats==99 and h.Program.Addresses.sizeofPokemonStruct==77)
        assertBlocked(h,e)
    end)
end

test("partial decoder result and decode failure reject",function()
    for _,decoder in ipairs({function() return {} end,function() error("decode failed") end}) do
        local h=host(); h.decodePublicSource=decoder
        local e=loadExtension().newMockHarness(h)
        e.setMockInputs(request(h)); e.beforeGameDataLoad()
        assert(not h.GameSettings.initialize()); assertBlocked(h,e)
    end
end)

test("all import prefixes roll back including false and thrown errors",function()
    for count=0,8 do
        for _,result in ipairs({"true","false","throw"}) do
            local h,e=fixture()
            h.importMockOverrides=function(n,write)
                for i=1,math.min(count,n) do write(i) end
                if result=="throw" then error("partial transport") end
                return result=="true"
            end
            assert(not h.GameSettings.initialize())
            assert(h.GameSettings.pstats==99 and h.GameSettings.estats==98 and h.GameSettings.gPlayerPartyCount==nil)
            assert(h.Program.Addresses.sizeofPokemonStruct==77 and h.Program.Addresses.sizeofBaseStatsPokemon==nil)
            assert(h.PokemonData.Addresses.offsetTypes==3)
            assertBlocked(h,e)
        end
    end
end)

test("missing public helper cannot bypass early guard",function()
    local h=host()
    local e=loadExtension({dofile=function() error("missing public helper") end}).newMockHarness(h)
    e.setMockInputs(request(h)); assert(e.beforeGameDataLoad())
    assert(not h.GameSettings.initialize()); assertBlocked(h,e)
end)

test("missing restart seam still blocks the stock initializer",function()
    local h=host(); h.IronmonTracker=nil
    local e=mockAPI.newMockHarness(h); e.setMockInputs(request(h))
    assert(not e.beforeGameDataLoad()); assert(not h.GameSettings.initialize())
    assertBlocked(h,e)
end)

test("read-back rejects dropped assignment after successful import",function()
    local h,e=fixture()
    h.Program.Addresses.sizeofBaseStatsPokemon=nil
    setmetatable(h.Program.Addresses,{__newindex=function() end})
    assert(not h.GameSettings.initialize())
    assert(h.GameSettings.pstats==99 and h.Program.Addresses.sizeofPokemonStruct==77)
    assertBlocked(h,e)
end)

test("failed identity read before and after transaction",function()
    for failAt=1,2 do
        local h,e=fixture(); local reads=0
        h.Memory.read32=function() reads=reads+1; if reads==failAt then error("failed read") end; return 691 end
        assert(not h.GameSettings.initialize())
        assert(h.Program.Addresses.sizeofPokemonStruct==77)
        assertBlocked(h,e)
    end
end)

test("invalid identity values never become zero substitutes",function()
    for _,value in ipairs({false,"691",0,692,4294967296}) do
        local h,e=fixture(); h.identityValue=value
        assert(not h.GameSettings.initialize()); assertBlocked(h,e)
    end
end)

test("session changes during transaction discard all state",function()
    local h,e=fixture()
    h.importMockOverrides=function(n,write)
        for i=1,n do write(i) end
        h.current.epoch=2
        return true
    end
    assert(not h.GameSettings.initialize())
    assert(h.Program.Addresses.sizeofPokemonStruct==77)
    assertBlocked(h,e)
end)

test("session changes during identity read invalidate before import",function()
    local h,e=fixture()
    h.Memory.read32=function() h.current.epoch=2; return 691 end
    assert(not h.GameSettings.initialize())
    assert(h.Program.Addresses.sizeofPokemonStruct==77)
    assertBlocked(h,e)
end)

test("accepted session early reentry revokes old epoch and requires fresh binding",function()
    local h,e=fixture(); assert(h.GameSettings.initialize())
    assert(e.state.status=="TEST_ONLY" and e.state.binding.epoch==1)
    local initialize,restart=h.GameSettings.initialize,h.IronmonTracker.startTracker
    local previousEpoch,reads=e.state.epoch,h.reads
    e.state.snapshots={party={species=25}}

    assert(e.beforeGameDataLoad())
    assert(h.GameSettings.initialize==initialize and h.IronmonTracker.startTracker==restart)
    assert(e.state.epoch>previousEpoch)
    assert(h.GameSettings.pstats==99 and h.GameSettings.estats==98)
    assert(h.Program.Addresses.sizeofPokemonStruct==77)
    assert(h.PokemonData.Addresses.offsetTypes==3)
    assertBlocked(h,e)

    assert(not h.GameSettings.initialize())
    assert(e.state.reason:find("revoked session",1,true) and h.reads==reads)
    assertBlocked(h,e)
    h.current.epoch=2
    assert(not h.GameSettings.initialize()) -- advancing host epoch alone is insufficient
    assertBlocked(h,e)

    e.setMockInputs(request(h)) -- new binding for the fresh synthetic epoch
    assert(e.beforeGameDataLoad() and h.GameSettings.initialize())
    assert(e.state.status=="TEST_ONLY" and e.state.binding.epoch==2)
    assert(e.checkSession() and e.state.confidence=="UNKNOWN")
    assert(h.GameSettings.initialize==initialize and h.IronmonTracker.startTracker==restart)
    assert(h.stockInitializations==0 and h.writes==0)
end)

test("stale session invalidation and fresh epoch recovery",function()
    local h,e=fixture(); assert(h.GameSettings.initialize())
    e.state.snapshots={party={species=25}}
    h.current.output="SYNTHETIC:IronMON"
    assert(not e.afterEachFrame()); assertBlocked(h,e)
    h.current.output="SYNTHETIC:Control"
    assert(not h.GameSettings.initialize()) -- revoked old proof cannot recover
    h.current.epoch=2; e.setMockInputs(request(h))
    assert(h.GameSettings.initialize() and e.state.status=="TEST_ONLY")
    e.invalidate("reset"); assertBlocked(h,e)
    assert(not h.GameSettings.initialize())
end)

test("nested mutation, unreadable session and snapshot epochs invalidate",function()
    for _,mutate in ipairs({
        function(h) h.Program.Addresses.sizeofBattleMove=88 end,
        function(h) h.getSession=function() error("session unavailable") end end,
        function(h) h.identityValue=692 end,
        function(h) h.Options["Override Button Mode to LR"]=true end,
    }) do
        local h,e=fixture(); assert(h.GameSettings.initialize())
        e.state.snapshots={old={value=1}}; local epoch=e.state.epoch
        mutate(h); assert(not e.afterProgramDataUpdate())
        assert(e.state.epoch>epoch); assertBlocked(h,e)
    end
end)

test("wrapper conflict before initialization quarantines and preserves foreign reference",function()
    local h=host(); local foreign=function() error("foreign initializer must not run") end
    h.GameSettings.initialize=foreign
    local e=loadExtension().newMockHarness(h); e.setMockInputs(request(h))
    assert(not e.beforeGameDataLoad()); assert(not h.GameSettings.initialize())
    e.unload(); assert(h.GameSettings.initialize==foreign); assertBlocked(h,e)
end)

test("wrapper replacement after activation cannot survive a restart",function()
    local h,e=fixture(); assert(h.GameSettings.initialize())
    local foreign=function() end; h.GameSettings.initialize=foreign
    assert(not e.checkSession()); assertBlocked(h,e)
    assert(not e.beforeGameDataLoad()); assert(not h.GameSettings.initialize())
    e.unload(); assert(h.GameSettings.initialize==foreign)
    assert(not h.IronmonTracker.startTracker() and h.restarts==0)
end)

test("restart conflict after activation fails without restoring over another owner",function()
    local h,e=fixture(); assert(h.GameSettings.initialize())
    local foreign=function() end; h.IronmonTracker.startTracker=foreign
    assert(not e.checkSession()); e.unload()
    assert(h.IronmonTracker.startTracker==foreign); assertBlocked(h,e)
end)

test("unload is idempotent and restart tombstone survives reconstructed globals",function()
    local h,e=fixture(); assert(h.GameSettings.initialize())
    e.unload(); e.unload()
    assert(h.GameSettings.initialize==h.originalInitialize)
    h.GameSettings={gamename="Pokemon FireRed",initialize=h.originalInitialize}
    assert(not h.IronmonTracker.startTracker() and h.restarts==0)
    assert(h.GameSettings.gamename=="Unsupported Game")
    assertBlocked(h,e)
end)

test("late enable and repeated disable/re-enable require fresh early validation",function()
    local h=host(); local e=loadExtension().newMockHarness(h)
    e.setMockInputs(request(h)); assert(not e.startup()); assertBlocked(h,e)
    assert(not h.IronmonTracker.startTracker() and h.restarts==0)
    for epoch=1,3 do
        h.current.epoch=epoch; e.setMockInputs(request(h))
        assert(e.beforeGameDataLoad() and h.GameSettings.initialize())
        e.unload(); assertBlocked(h,e)
    end
end)

test("rollback preserves fields replaced by another owner",function()
    local h,e=fixture(); assert(h.GameSettings.initialize())
    h.Program.Addresses.sizeofPokemonStruct=12345
    local programAddresses=h.Program.Addresses
    e.unload()
    assert(h.Program.Addresses==programAddresses and programAddresses.sizeofPokemonStruct==12345)
    assert(h.PokemonData.Addresses.offsetTypes==3)
    assertBlocked(h,e)
end)

test("snapshot invalidation after previously valid session read failure",function()
    local h,e=fixture(); assert(h.GameSettings.initialize())
    e.state.snapshots={party={value=25}}
    h.Memory.read32=function() error("read failed") end
    assert(not e.afterBattleDataUpdate()); assertBlocked(h,e)
end)

test("memory-write trap is an explicit lifecycle failure",function()
    local h,e=fixture()
    h.importMockOverrides=function() h.Memory.writebyte(0,0); return true end
    assert(not h.GameSettings.initialize())
    assert(h.writes==1 and e.state.reason:find("FORBIDDEN memory write",1,true))
    assert(h.GameSettings.pstats==99 and e.state.status=="UNKNOWN")
    -- This deliberately injected forbidden call must fail; no memory backend
    -- exists and no write can complete. Ordinary cases assert zero invocations.
end)

test("battle transitions discard old diagnostics",function()
    local h,e=fixture(); assert(h.GameSettings.initialize())
    e.state.activeBattleMons={old=25}; e.state.activeBattleSnapshot="old"
    e.afterBattleBegins(); assertBlocked(h,e)
    e.afterBattleEnds(); assertBlocked(h,e)
end)

local passed=0
for _,entry in ipairs(tests) do
    local ok,reason=pcall(entry[2])
    if not ok then error("FAIL: "..entry[1]..": "..tostring(reason),0) end
    passed=passed+1
    print("PASS: "..entry[1])
end
print("Lua ".._VERSION..": "..passed.." mock tests PASS (SYNTHETIC_ONLY; no live activation)")
