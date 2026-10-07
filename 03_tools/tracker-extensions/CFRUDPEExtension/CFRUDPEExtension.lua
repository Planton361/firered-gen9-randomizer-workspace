-- #691 Phase A: public source identity and TEST-ONLY transactional lifecycle.
-- Production is deliberately unsupported: real output/session proof is UNKNOWN.
-- No local manifests, emulator memory, source tables or stock initializers are read.
local ROOT = debug.getinfo(1, "S").source:sub(2):match("^(.*)[/\\]") or "."
local sha256 -- Lazy public helper loading; missing helper cannot disable the early stop guard.
local SOURCE_SHA256 = "c89e9767bdd40dc2a2c127c0273cb61ee35c0fdb24ff25c728821ac3271fa353"
local PROFILE_ID = "sha256:3986250cf9fa35ec26b063c785b034c2d96406e681b77e4c557922c948225235"
local TRACKER_PIN = "c450ecaee2d8131a2789bb656e3be792a93712fb"
local KEY = "CFRUDPEExtension"
local function requireThat(ok, reason) if not ok then error(reason, 0) end end
local function integer(n) return type(n) == "number" and n == math.floor(n) end
local function copy(t)
    if type(t) ~= "table" then return t end
    local out = {}
    for k,v in pairs(t) do out[k] = copy(v) end
    return out
end
local function equal(a,b)
    if type(a) ~= type(b) then return false end
    if type(a) ~= "table" then return a == b end
    for k,v in pairs(a) do if not equal(v,b[k]) then return false end end
    for k in pairs(b) do if a[k] == nil then return false end end
    return true
end
local function keys(t, expected, label)
    requireThat(type(t) == "table" and getmetatable(t) == nil, label .. ": plain object required")
    for k in pairs(t) do requireThat(expected[k], label .. ": unexpected key " .. tostring(k)) end
    for k in pairs(expected) do requireThat(t[k] ~= nil, label .. ": missing " .. k) end
end
local function address(a, domain, width, span)
    local ranges = { EWRAM = {0x02000000,0x02040000}, ROM = {0x08000000,0x09000000} }
    -- Pinned Memory.splitDomainAndAddress only handles ROM high byte 0x08.
    local r = ranges[domain]
    requireThat(r and (width == 1 or width == 2 or width == 4) and integer(a)
        and integer(span) and span >= width and a % width == 0
        and a >= r[1] and a + span <= r[2], "invalid domain/bounds/alignment")
end
local cachedRaw, cachedProfile
local function validateSource(raw, decode)
    requireThat(type(raw) == "string" and #raw == 1092720, "public profile missing/size mismatch")
    if raw == cachedRaw then return copy(cachedProfile) end
    if not sha256 then
        sha256 = dofile(ROOT .. "/profile_sha256.lua")
        requireThat(type(sha256) == "function", "public hash helper unavailable")
    end
    requireThat(sha256(raw) == SOURCE_SHA256, "public profile content/revision/schema mismatch")
    requireThat(type(decode) == "function", "JSON decoder unavailable")
    local p = decode(raw)
    requireThat(type(p) == "table" and type(p.metadata) == "table", "partial JSON decode")
    requireThat(p.metadata.schema == "cfru-dpe-tracker-source-profile"
        and p.metadata.schemaVersion == 2 and p.metadata.profileId == PROFILE_ID
        and p.metadata.revisions.Tracker == TRACKER_PIN, "incompatible public profile")
    for _,k in ipairs({"counts","species","moves","abilities","items","types","layouts",
        "addresses","capabilities","limits","tableCoverage","limitations"}) do
        requireThat(type(p[k]) == "table", "partial JSON decode: " .. k)
    end
    -- Hash binds ALL serialized fields, including the legacy T1 compatibility
    -- declaration. This adapter supports its source schema only, never live use.
    cachedRaw, cachedProfile = raw, copy(p)
    return p
end
local function newLifecycle(host, mock)
    local ext = {
        name = "CFRU/DPE Gen9 Tracker Extension", author = "firered-gen9-randomizer-workspace",
        description = "Phase A fail-closed source/mock guard; production activation unavailable",
        version = "0.2.0", extensionKey = KEY,
        state = {confidence = "UNKNOWN", status = "UNKNOWN", epoch = 0, reason = "not initialized"},
    }
    local state = ext.state
    local transaction, initializer, restartGuard, input, accepted, source
    local revoked = {}
    local function clear(reason)
        state.epoch = state.epoch + 1
        state.status, state.confidence, state.reason = "UNKNOWN", "UNKNOWN", reason
        state.sourceData, state.sourceLookups, state.binding = nil,nil,nil
        state.snapshots, state.activeBattleMons, state.activeBattleSnapshot = {},{},nil
        state.manifestsLoaded, state.sourceDataLoaded = false,false
        state.capabilities = {partyDecoder = "UNAVAILABLE", battleReader = "UNAVAILABLE", trackerUI = "UNAVAILABLE"}
    end
    local function rollback()
        if not transaction then return end
        for i = #transaction, 1, -1 do
            local entry = transaction[i]
            -- Restore only owned values; keep a later owner's replacement.
            if rawget(entry.parent,entry.key) == entry.value then
                rawset(entry.parent,entry.key,entry.old)
            end
        end
        transaction = nil
    end
    local function quarantine(reason)
        if accepted then revoked[accepted.session .. ":" .. accepted.epoch] = true end
        accepted, source = nil,nil
        rollback()
        clear(reason)
        if host.GameSettings then host.GameSettings.gamename = "Unsupported Game" end
        if host.Options then host.Options["Override Button Mode to LR"] = false end
        if host.Main then host.Main.forceRestart = true end
        if host.log then host.log(KEY .. ": UNKNOWN: " .. reason) end
        return false
    end
    clear("production output/session proof unavailable")
    local function ownRestartGuard()
        local tracker = host.IronmonTracker
        requireThat(type(tracker) == "table" and type(tracker.startTracker) == "function",
            "persistent restart entry unavailable")
        if restartGuard and tracker.startTracker == restartGuard.wrapper then return end
        requireThat(not restartGuard, "restart wrapper conflict")
        local old = tracker.startTracker
        local wrapper = function()
            -- Safety tombstone deliberately survives unload. No script restart
            -- may restore stock interpretations while the selected output is unknown.
            quarantine("restart blocked; new validated lifecycle required")
            return false
        end
        restartGuard = {parent = tracker, old = old, wrapper = wrapper}
        tracker.startTracker = wrapper
    end
    local function readIdentity(binding)
        local d = binding.identity
        keys(d, {address=true,domain=true,widthBytes=true,value=true}, "mock identity")
        requireThat(d.domain == "ROM" and d.widthBytes == 4 and integer(d.value)
            and d.value >= 0 and d.value < 4294967296, "invalid mock identity descriptor")
        address(d.address,d.domain,d.widthBytes,d.widthBytes)
        requireThat(type(host.Memory) == "table" and type(host.Memory.read32) == "function", "read API missing")
        local value = host.Memory.read32(d.address)
        requireThat(integer(value) and value == d.value, "mock identity read failed/mismatch")
    end
    local function sessionMatches(binding)
        requireThat(type(host.getSession) == "function", "session provider missing")
        local s = host.getSession()
        keys(s, {output=true,session=true,epoch=true}, "current mock session")
        requireThat(s.output == binding.output and s.session == binding.session and s.epoch == binding.epoch,
            "stale/output/session mismatch")
    end
    local function validateMockBinding(p, request)
        keys(request, {sourceText=true,binding=true,gameSettings=true,overrides=true}, "mock request")
        local b = request.binding
        keys(b, {schema=true,schemaVersion=true,profileId=true,trackerRevision=true,extensionVersion=true,
            evidence=true,output=true,session=true,epoch=true,capabilities=true,addresses=true,identity=true}, "mock binding")
        requireThat(b.schema == "cfru-dpe-mock-binding" and b.schemaVersion == 1
            and b.profileId == PROFILE_ID and b.trackerRevision == TRACKER_PIN
            and b.extensionVersion == ext.version and host.trackerRevision == TRACKER_PIN,
            "binding schema/revision/compatibility mismatch")
        requireThat(b.evidence == "SYNTHETIC_ONLY" and type(b.output) == "string"
            and b.output:match("^SYNTHETIC:") and type(b.session) == "string"
            and b.session:match("^MOCK:") and integer(b.epoch) and b.epoch > 0,
            "placeholder/unproved binding")
        requireThat(not revoked[b.session .. ":" .. b.epoch], "revoked session; fresh epoch required")
        keys(b.capabilities,{playerParty=true,enemyParty=true},"mock capabilities")
        requireThat(b.capabilities.playerParty == true and b.capabilities.enemyParty == true,
            "mock lifecycle requires both party dependencies")
        local required = {}
        for capability in pairs(b.capabilities) do
            local c = p.capabilities[capability]
            requireThat(type(c) == "table", "missing capability")
            for _,dependency in ipairs(c.dependencies) do
                if p.addresses[dependency] then required[dependency] = true
                else requireThat(p[dependency] or p.layouts.records[dependency], "missing dependency " .. dependency) end
            end
        end
        keys(b.addresses, required, "resolved mock addresses")
        for symbol in pairs(required) do
            local d, resolved = p.addresses[symbol], b.addresses[symbol]
            keys(resolved,{address=true,domain=true,widthBytes=true,kind=true,indirection=true,source=true},symbol)
            -- No repoint-anchor or UNRESOLVED descriptor is permission to read.
            requireThat(d.kind == "fixed-symbol" and d.indirection == 0
                and resolved.kind == d.kind and resolved.indirection == 0
                and resolved.source == d.source and resolved.domain == d.domain
                and resolved.widthBytes == d.widthBytes and resolved.address == d.sourceAddress,
                "unproved address descriptor " .. symbol)
            local span = d.widthBytes
            if symbol == "gPlayerParty" or symbol == "gEnemyParty" then
                span = p.layouts.records.Pokemon.size * p.limits.PARTY_SIZE.value
            end
            address(resolved.address,resolved.domain,resolved.widthBytes,span)
            requireThat(resolved.address % p.layouts.records.Pokemon.alignment == 0
                or symbol == "gPlayerPartyCount", "party ABI alignment")
        end
        sessionMatches(b)
        readIdentity(b)
        sessionMatches(b)
        return copy(b)
    end
    local function expectedPlan(p,b)
        return {
            GameSettings = {pstats=b.addresses.gPlayerParty.address, estats=b.addresses.gEnemyParty.address,
                gPlayerPartyCount=b.addresses.gPlayerPartyCount.address},
            Program = {Addresses={sizeofPokemonStruct=p.layouts.records.Pokemon.size,
                sizeofBaseStatsPokemon=p.layouts.records.BaseStats.size,
                sizeofBattlePokemon=p.layouts.records.BattlePokemon.size,
                sizeofBattleMove=p.layouts.records.BattleMove.size}},
            PokemonData = {Addresses={offsetTypes=p.layouts.records.BaseStats.fields.type1.offset,
                offsetAbilities=p.layouts.records.BaseStats.fields.ability1.offset}},
        }
    end
    local function transact(plan)
        transaction = {}
        local writes = {}
        for _,object in ipairs({"GameSettings","Program","PokemonData"}) do
            local parent = host[object]
            requireThat(type(parent) == "table", "missing consumer " .. object)
            local values = plan[object]
            if object ~= "GameSettings" then
                parent, values = parent.Addresses, values.Addresses
                requireThat(type(parent) == "table", "missing nested consumer " .. object)
            end
            local names = {}
            for k in pairs(values) do names[#names+1] = k end
            table.sort(names)
            for _,k in ipairs(names) do
                writes[#writes+1] = {parent=parent,key=k,value=values[k],old=rawget(parent,k)}
            end
        end
        local function write(index)
            local entry = writes[index]
            requireThat(entry ~= nil and not entry.written, "invalid/duplicate import write")
            entry.written = true
            transaction[#transaction+1] = entry
            entry.parent[entry.key] = entry.value
        end
        if host.importMockOverrides then
            -- An in-memory mocked transport; NEVER Tracker's filesystem importers.
            requireThat(host.importMockOverrides(#writes,write) == true, "mock import failed")
        else
            for i = 1, #writes do write(i) end
        end
        for _,entry in ipairs(writes) do
            requireThat(entry.written and rawget(entry.parent,entry.key) == entry.value,
                "partial import/effective nested read-back failed")
        end
        -- Assert nested tables are still the ones actual pinned consumers use.
        requireThat(host.Program.Addresses == writes[4].parent, "consumer table replaced")
        requireThat(host.PokemonData.Addresses == writes[#writes].parent, "consumer table replaced")
    end
    local function activate()
        if not mock then return quarantine("production activation denied: real output/session identity UNKNOWN") end
        local ok,reason = pcall(function()
            requireThat(type(input) == "table", "missing in-memory manifests")
            local p = validateSource(input.sourceText,host.decodePublicSource)
            local b = validateMockBinding(p,input)
            local plan = expectedPlan(p,b)
            requireThat(equal(input.gameSettings,plan.GameSettings) and equal(input.overrides,
                {Program=plan.Program,PokemonData=plan.PokemonData}), "non-allowlisted/missing override")
            transact(plan)
            sessionMatches(b)
            readIdentity(b)
            sessionMatches(b)
            requireThat(initializer and host.GameSettings.initialize == initializer.wrapper
                and restartGuard and host.IronmonTracker.startTracker == restartGuard.wrapper,
                "wrapper conflict during import")
            source, accepted = p,b
            state.status, state.reason = "TEST_ONLY", "synthetic lifecycle validated; live data remains UNKNOWN"
            state.sourceDataLoaded, state.manifestsLoaded = true,true
            state.binding = copy(b)
            state.snapshots = {}
            -- Even the success fixture must never let Main.Run initialize stock readers.
            host.GameSettings.gamename = "Unsupported Game"
            host.Options["Override Button Mode to LR"] = false
        end)
        if not ok then return quarantine(tostring(reason)) end
        return true
    end
    function ext.validatePublicSource(raw)
        local ok,p = pcall(validateSource,raw,host.decodePublicSource)
        if not ok then return quarantine(tostring(p)) end
        -- Source validation never changes session confidence or authorizes reads.
        return true,copy(p)
    end
    function ext.setMockInputs(request)
        requireThat(mock, "no production mock switch")
        quarantine("mock inputs changed; early initialization required")
        input = copy(request)
    end
    function ext.beforeGameDataLoad()
        rollback()
        clear("early guard pending")
        local ok,reason = pcall(function()
            requireThat(type(host.GameSettings) == "table" and type(host.GameSettings.initialize) == "function",
                "GameSettings.initialize unavailable")
            if initializer then
                if host.GameSettings.initialize ~= initializer.wrapper then
                    -- Quarantine rather than compose the foreign initializer. Keep
                    -- its reference for ownership-safe unload.
                    initializer.old = host.GameSettings.initialize
                    initializer.conflict = true
                    host.GameSettings.initialize = initializer.wrapper
                    error("initializer wrapper conflict", 0)
                end
                ownRestartGuard()
                return
            end
            local old = host.GameSettings.initialize
            local conflict = mock and old ~= host.originalInitialize
            if not mock then
                local info = debug.getinfo(old, "S")
                conflict = not (info and info.linedefined == 284
                    and info.source:match("[/\\]ironmon_tracker[/\\]GameSettings%.lua$"))
            end
            local wrapper = function()
                if not initializer or initializer.conflict then return quarantine("initializer wrapper conflict/unloaded") end
                rollback()
                clear("initializing")
                return activate()
            end
            initializer = {parent=host.GameSettings,old=old,wrapper=wrapper,conflict=conflict}
            host.GameSettings.initialize = wrapper
            ownRestartGuard()
            requireThat(not conflict, "initializer wrapper conflict")
        end)
        if not ok then
            if initializer then initializer.conflict = true end
            return quarantine(tostring(reason))
        end
        host.GameSettings.gamename = "Unsupported Game"
        return true
    end
    function ext.checkSession()
        if state.status ~= "TEST_ONLY" then return false end
        local ok,reason = pcall(function()
            requireThat(mock and accepted and source, "no validated mock lifecycle")
            requireThat(host.GameSettings.initialize == initializer.wrapper
                and host.IronmonTracker.startTracker == restartGuard.wrapper, "wrapper conflict")
            sessionMatches(accepted)
            readIdentity(accepted)
            sessionMatches(accepted)
            requireThat(host.Options["Override Button Mode to LR"] == false, "memory-writing option enabled")
            local plan = expectedPlan(source,accepted)
            for k,v in pairs(plan.GameSettings) do requireThat(host.GameSettings[k] == v,"stale override") end
            for _,object in ipairs({"Program","PokemonData"}) do
                for k,v in pairs(plan[object].Addresses) do
                    requireThat(host[object].Addresses[k] == v,"stale nested override")
                end
            end
        end)
        if not ok then return quarantine(tostring(reason)) end
        return true
    end
    function ext.startup()
        -- Mid-session enable/reload cannot bypass beforeGameDataLoad.
        local ok,reason = pcall(ownRestartGuard)
        if not ok then return quarantine(tostring(reason)) end
        if not initializer or state.status ~= "TEST_ONLY" then
            return quarantine("startup requires early guard; production is unavailable")
        end
        return ext.checkSession()
    end
    function ext.invalidate(reason) return quarantine(reason or "reset/reload/output change") end
    function ext.unload()
        quarantine("unloaded; selected output remains unsupported")
        if initializer and initializer.parent.initialize == initializer.wrapper then
            initializer.parent.initialize = initializer.old
        end
        initializer = nil
        input = nil
        -- Keep only the persistent restart tombstone. A fresh Lua host session
        -- is required to remove it; restoring stock initialize cannot authorize restart.
        return true
    end
    ext.afterEachFrame = ext.checkSession
    ext.afterProgramDataUpdate = ext.checkSession
    ext.afterBattleDataUpdate = ext.checkSession
    function ext.afterBattleBegins() return quarantine("battle decoding UNAVAILABLE in Phase A") end
    ext.afterBattleEnds = ext.afterBattleBegins
    function ext.getActiveBattleMons() return {} end
    function ext.readActiveBattleMons() return false end
    return ext
end
local productionHost = setmetatable({log=print,decodePublicSource=function(raw)
    requireThat(FileManager and FileManager.JsonLibrary and type(FileManager.JsonLibrary.decode) == "function",
        "public JSON decoder unavailable")
    return FileManager.JsonLibrary.decode(raw)
end},{__index=_G})
local production = newLifecycle(productionHost,false)
-- Detached test factory: cannot change production's closed-over mode or inputs.
-- Refuse construction in an emulator/Tracker process, even if a caller claims mock evidence.
function production.newMockHarness(host)
    requireThat(GameSettings == nil and Main == nil and IronmonTracker == nil and emu == nil
        and memory == nil and gameinfo == nil and client == nil and Memory == nil
        and TrackerAPI == nil and Program == nil and FileManager == nil, "mock harness forbidden in Tracker/emulator")
    requireThat(type(host) == "table" and host.testOnly == true, "explicit isolated mock host required")
    return newLifecycle(host,true)
end
return production
