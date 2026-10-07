-- #692 Phase A only. Detached public-source resolver / synthetic byte decoder.
-- Never loaded by CFRUDPEExtension.lua. No host, session, address or UI API.
local ROOT = debug.getinfo(1, "S").source:sub(2):match("^(.*)[/\\]") or "."
local sha256 = dofile(ROOT .. "/profile_sha256.lua")
local SOURCE_SHA256 = "8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981"
local PROFILE_ID = "sha256:31be9e07697f939b274c56eea5d92a81dd10c43e7c876586effccb335535ca75"
local function check(ok, reason) if not ok then error(reason, 0) end end
local function integer(n) return type(n) == "number" and n == math.floor(n) end
local function copy(t)
    if type(t) ~= "table" then return t end
    local out = {}; for k,v in pairs(t) do out[k] = copy(v) end; return out
end

-- Parse only the accepted canonical JSON, AFTER verifying every byte. No caller
-- decoder/profile object can replace the hashed facts. This restricted parser
-- is not a general JSON importer (unicode escapes/floats are not needed here).
local function parseLockedJson(raw)
    local pos = 1
    local function ws() local _,last = raw:find("^[ \r\n\t]*", pos); pos = last + 1 end
    local function str()
        check(raw:sub(pos,pos) == '"', "expected JSON string"); pos = pos + 1
        local out = {}
        while pos <= #raw do
            local c = raw:sub(pos,pos); pos = pos + 1
            if c == '"' then return table.concat(out) end
            if c == "\\" then
                local escapes = {['"']='"', ['\\']='\\', ['/']='/', b='\b', f='\f', n='\n', r='\r', t='\t'}
                c = escapes[raw:sub(pos,pos)]; pos = pos + 1
                check(c, "unsupported JSON escape")
            end
            out[#out+1] = c
        end
        error("unterminated JSON string", 0)
    end
    local value
    value = function()
        ws(); local c = raw:sub(pos,pos)
        if c == '"' then return str() end
        if c == "{" or c == "[" then
            local object, close, out, index = c == "{", c == "{" and "}" or "]", {}, 1
            pos = pos + 1; ws()
            if raw:sub(pos,pos) == close then pos = pos + 1; return out end
            while true do
                local key = index
                if object then key = str(); ws(); check(raw:sub(pos,pos) == ":", "expected colon"); pos = pos + 1 end
                out[key] = value(); index = index + 1; ws()
                c = raw:sub(pos,pos); pos = pos + 1
                if c == close then return out end
                check(c == ",", "expected JSON separator"); ws()
            end
        end
        for token,v in pairs({["true"]=true, ["false"]=false}) do
            if raw:sub(pos,pos+#token-1) == token then pos = pos + #token; return v end
        end
        if raw:sub(pos,pos+3) == "null" then pos = pos + 4; return nil end
        local number = raw:match("^-?%d+", pos)
        check(number, "unsupported JSON value"); pos = pos + #number; return tonumber(number)
    end
    local p = value(); ws(); check(pos == #raw + 1, "trailing JSON bytes"); return p
end

local function field(state, value, reason, provenance)
    return {confidence=state, value=value, reason=reason, provenance=provenance,
        evidence="TEST_ONLY", liveConfidence="UNKNOWN"}
end
local function unknown(reason) return field("UNKNOWN", nil, reason) end
local function unavailable(reason) return field("UNAVAILABLE", nil, reason) end
local function verified(value, provenance) return field("VERIFIED", value, nil, provenance) end

local function uncomment(text)
    return (text:gsub("/%*.-%*/", ""):gsub("//[^\n]*", ""))
end
local function selectConditionals(text, flags)
    local out, stack, active = {}, {}, true
    for line in (uncomment(text) .. "\n"):gmatch("([^\n]*)\n") do
        local op,name = line:match("^%s*#(ifn?def)%s+([%w_]+)%s*$")
        if op then
            check(type(flags[name]) == "boolean", "unreviewed conditional " .. name)
            local yes = flags[name]; if op == "ifndef" then yes = not yes end
            stack[#stack+1] = {parent=active, yes=yes}; active = active and yes
        elseif line:match("^%s*#else%s*$") then
            local top = stack[#stack]; check(top and not top.other, "invalid else")
            top.other = true; active = top.parent and not top.yes
        elseif line:match("^%s*#endif%s*$") then
            check(#stack > 0, "invalid endif"); active = table.remove(stack).parent
        else
            check(not line:match("^%s*#if") and not line:match("^%s*#elif"), "unsupported conditional")
            if active then out[#out+1] = line end
        end
    end
    check(#stack == 0, "unterminated conditional"); return table.concat(out, "\n")
end
local function arrayBody(text, symbol)
    local start = text:find(symbol .. "%[%]%s*=%s*{")
    check(start, "missing source array " .. symbol)
    start = text:find("{", start, true)
    local depth = 1
    for i = start+1,#text do
        local c = text:sub(i,i)
        if c == "{" then depth = depth + 1 elseif c == "}" then depth = depth - 1 end
        if depth == 0 then return text:sub(start+1,i-1) end
    end
    error("unterminated source array", 0)
end

local M = {}
local acceptedRaw, acceptedProfile
local acceptedSources = {}
function M.newMock(raw, sources)
    local ok, result = pcall(function()
        check(type(raw) == "string" and #raw == 1092720
            and (raw == acceptedRaw or sha256(raw) == SOURCE_SHA256),
            "accepted T1 serialization/schema/pins required")
        local p = raw == acceptedRaw and acceptedProfile or parseLockedJson(raw)
        check(p.metadata.schema == "cfru-dpe-tracker-source-profile" and p.metadata.schemaVersion == 2
            and p.metadata.profileId == PROFILE_ID, "incompatible profile")
        acceptedRaw, acceptedProfile = raw, p -- Private, never returned to callers.
        check(type(sources) == "table" and getmetatable(sources) == nil, "public source text required")
        local allowed = { ["DPE:src/Base_Stats.c"]=true, ["CFRU:src/Tables/battle_moves.c"]=true,
            ["CFRU:include/battle.h"]=true, ["CFRU:include/constants/battle.h"]=true,
            ["CFRU:include/pokemon.h"]=true }
        for locator in pairs(sources) do check(allowed[locator], "unexpected source input") end
        for locator in pairs(allowed) do
            local input = p.metadata.inputs[locator]
            check(type(sources[locator]) == "string" and (sources[locator] == acceptedSources[locator]
                or sha256(sources[locator]) == input.sha256),
                "missing/changed public source " .. locator)
            acceptedSources[locator] = sources[locator] -- Cache only byte-exact hashed text.
        end
        local symbols = {}
        for _,kind in ipairs({"species","moves","abilities","items","types"}) do
            for _,row in ipairs(p[kind]) do
                if row.constant then symbols[row.constant] = row.id end
                for _,alias in ipairs(row.aliases) do symbols[alias.constant] = row.id end
            end
        end
        local battle = uncomment(sources["CFRU:include/battle.h"])
        for name,n in battle:gmatch("#define%s+(SPLIT_%w+)%s+(%d+)") do symbols[name] = tonumber(n) end
        check(symbols.SPLIT_PHYSICAL == 0 and symbols.SPLIT_SPECIAL == 1 and symbols.SPLIT_STATUS == 2,
            "split definitions changed")
        local maxLevel = tonumber(sources["CFRU:include/pokemon.h"]:match("#define%s+MAX_MON_LEVEL%s+(%d+)"))
        check(maxLevel, "level limit missing")
        local baseline = {}
        for _,spec in ipairs({
            {kind="species", locator="DPE:src/Base_Stats.c", symbol="gBaseStats",
                fields={"type1","type2","ability1","ability2","hiddenAbility"}},
            {kind="moves", locator="CFRU:src/Tables/battle_moves.c", symbol="gBattleMoves",
                fields={"type","power","accuracy","pp","split"}},
        }) do
            local body = arrayBody(selectConditionals(sources[spec.locator], p.metadata.configuration), spec.symbol)
            local rows = {}; baseline[spec.kind] = rows
            for constant,decl in body:gmatch("%[([%w_]+)%]%s*=%s*{(.-)}") do
                local id = symbols[constant]; check(id and not rows[id], "ambiguous source row")
                local row = {}; rows[id] = row
                local mapping = p[spec.kind][id+1]
                if mapping.state == "mapped" then
                    for _,name in ipairs(spec.fields) do
                        local token = decl:match("%." .. name .. "%s*=%s*([%w_]+)%s*,")
                        local n = token and (tonumber(token) or symbols[token])
                        check(integer(n) and n >= 0 and n <= 255, "missing/unsupported source field " .. constant .. "." .. name)
                        row[name] = n
                    end
                end
            end
            for _,row in ipairs(p[spec.kind]) do
                check((rows[row.id] ~= nil) == (row.state ~= "hole" and row.baselineData ~= "UNAVAILABLE"),
                    "T1 source row coverage mismatch")
            end
        end
        local statusDefinitions = sources["CFRU:include/constants/battle.h"]
        local status = {}
        for name,n in statusDefinitions:gmatch("#define%s+(STATUS1_[%w_]+)%s+(0x%x+)") do status[name] = tonumber(n) end
        check(status.STATUS1_SLEEP == 7 and status.STATUS1_POISON == 8 and status.STATUS1_BURN == 16
            and status.STATUS1_FREEZE == 32 and status.STATUS1_PARALYSIS == 64
            and status.STATUS1_TOXIC_POISON == 128, "unsupported status definitions")
        local decoder = {evidence="TEST_ONLY", liveConfidence="UNKNOWN", profileId=PROFILE_ID}
        function decoder.resolve(kind, id)
            if not p.counts[kind] then return unknown("unsupported mapping kind") end
            if not integer(id) or id < 0 then return unknown("missing/invalid ID") end
            if kind == "items" then
                for _,excluded in ipairs(p.itemExclusions) do
                    if excluded.id == id then return unavailable(excluded.reason) end
                end
            end
            local row = p[kind][id+1]
            if not row or row.state == "hole" then return unknown("unknown/hole ID") end
            if row.state == "reserved" or row.baselineData == "UNAVAILABLE" then return unavailable("unsupported source row") end
            if row.state == "sentinel" then
                if id == 0 and kind ~= "types" then return verified({id=0, absent=true}, "T1 known absence sentinel") end
                return unavailable("unsupported sentinel")
            end
            return verified({id=id, constant=row.constant, name=row.name, aliases=copy(row.aliases),
                truncated=row.truncated, sourceText=row.sourceText, scope="source-baseline"}, "accepted T1 mapping")
        end
        function decoder.speciesBaseline(id)
            local identity = decoder.resolve("species", id)
            if identity.confidence ~= "VERIFIED" or identity.value.absent then return identity end
            local row = baseline.species[id]
            return verified({identity=identity.value, types={decoder.resolve("types",row.type1), decoder.resolve("types",row.type2)},
                abilities={decoder.resolve("abilities",row.ability1), decoder.resolve("abilities",row.ability2)},
                hiddenAbility=decoder.resolve("abilities",row.hiddenAbility), formSupport=unknown("mapping does not prove form mechanics"),
                effectiveTypes=unknown("output/randomization unproved")}, "DPE:src/Base_Stats.c::gBaseStats (source-baseline)")
        end
        function decoder.moveBaseline(id)
            local identity = decoder.resolve("moves", id)
            if identity.confidence ~= "VERIFIED" or identity.value.absent then return identity end
            local row = baseline.moves[id]
            return verified({identity=identity.value, type=decoder.resolve("types",row.type), power=row.power,
                accuracy=row.accuracy, pp=row.pp, category=row.split, scope="source-baseline"},
                "CFRU:src/Tables/battle_moves.c::gBattleMoves; category = split")
        end
        local fields = p.layouts.records.Pokemon.fields
        local fieldNames = {"occupied","species","baselineSpecies","level","hp","maxHP","status","hiddenAbility","isEgg","heldItem","ability","effectiveTypes"}
        local function blank(reason)
            local snapshot = {evidence="TEST_ONLY", liveConfidence="UNKNOWN", profileId=PROFILE_ID,
                count=unknown(reason), slots={}}
            for slot=1,6 do
                local row = {moves={}}
                for _,name in ipairs(fieldNames) do row[name] = unknown(reason) end
                for i=1,4 do row.moves[i] = {identity=unknown(reason), baseline=unknown(reason), pp=unknown(reason), effective=unknown(reason)} end
                snapshot.slots[slot] = row
            end
            return snapshot
        end
        function decoder.decodeMock(bytes, count)
            local out = blank("invalid/truncated synthetic party block or count")
            if type(bytes) ~= "string" or #bytes ~= p.layouts.records.Pokemon.size * p.limits.PARTY_SIZE.value
                or not integer(count) or count < 0 or count > 6 then return out end
            local function read(slot, name, width, delta)
                local offset = (slot-1)*p.layouts.records.Pokemon.size + fields[name].offset + (delta or 0)
                local n = 0
                for i=width-1,0,-1 do n = n*256 + bytes:byte(offset+i+1) end
                return n
            end
            for slot=1,6 do
                if (read(slot,"species",2) ~= 0) ~= (slot <= count) then return blank("count/occupied-slot mismatch") end
            end
            out.count = verified(count, "synthetic party count; six-slot consistency")
            for slot=1,6 do
                local row, id = out.slots[slot], read(slot,"species",2)
                row.occupied = verified(slot <= count, "Pokemon.species / synthetic count")
                row.species = decoder.resolve("species",id)
                if slot > count then
                    for _,name in ipairs(fieldNames) do
                        if name ~= "occupied" and name ~= "species" then row[name] = unavailable("empty party slot") end
                    end
                    for i=1,4 do for name in pairs(row.moves[i]) do row.moves[i][name] = unavailable("empty party slot") end end
                else
                    local bit = fields.hiddenAbility
                    row.hiddenAbility = verified(math.floor(read(slot,"hiddenAbility",1)/2^bit.bitOffset)%2 == 1, "Pokemon.hiddenAbility bit")
                    bit = fields.isEgg
                    row.isEgg = verified(math.floor(read(slot,"isEgg",1)/2^bit.bitOffset)%2 == 1, "Pokemon.isEgg bit")
                    row.baselineSpecies = decoder.speciesBaseline(id)
                    row.ability = unknown("conditional GetMonAbility/TryRandomizeAbility selection unproved")
                    row.effectiveTypes = unknown("effective output types unproved")
                    local level,hp,maxHP = read(slot,"level",1),read(slot,"hp",2),read(slot,"maxHP",2)
                    row.level = level >= 1 and level <= maxLevel and verified(level,"Pokemon.level") or unknown("invalid level")
                    if maxHP > 0 and hp <= maxHP then
                        row.hp, row.maxHP = verified(hp,"Pokemon.hp"), verified(maxHP,"Pokemon.maxHP")
                    else row.hp, row.maxHP = unknown("inconsistent HP"), unknown("inconsistent HP") end
                    row.heldItem = decoder.resolve("items",read(slot,"item",2))
                    local rawStatus = read(slot,"condition",4)
                    local low,counter = rawStatus%256, math.floor(rawStatus/256)
                    local label
                    if rawStatus == 0 then label = "NONE"
                    elseif low >= 1 and low <= 7 and counter == 0 then label = "SLEEP"
                    elseif low == 128 and counter <= 15 then label = "TOXIC_POISON"
                    elseif counter == 0 then
                        label = ({[8]="POISON",[16]="BURN",[32]=p.metadata.configuration.FROSTBITE and "FROSTBITE" or "FREEZE",[64]="PARALYSIS"})[low]
                    end
                    row.status = label and verified({raw=rawStatus, primary=label, absent=rawStatus==0}, "CFRU STATUS1 masks / configuration")
                        or unknown("unsupported/conflicting status bits")
                    for i=1,4 do
                        local moveId,pp = read(slot,"moves",2,(i-1)*2),read(slot,"pp",1,i-1)
                        local identity = decoder.resolve("moves",moveId)
                        row.moves[i] = {identity=identity, baseline=decoder.moveBaseline(moveId),
                            pp=identity.confidence == "VERIFIED" and (moveId ~= 0 or pp == 0)
                                and verified(pp,"Pokemon.pp byte; effective max PP unproved") or unknown("unmapped move / inconsistent absent PP"),
                            effective=unknown("randomized move power/category/max PP unproved")}
                    end
                    if row.isEgg.value or row.species.confidence == "UNAVAILABLE" then
                        for _,name in ipairs({"level","hp","maxHP","status","ability","effectiveTypes"}) do row[name] = unavailable("unsupported egg/source species") end
                    end
                end
            end
            return out -- Always a fresh object; failed samples cannot reuse prior values.
        end
        return decoder
    end)
    if not ok then return nil, unknown(tostring(result)) end
    return result
end
return M
