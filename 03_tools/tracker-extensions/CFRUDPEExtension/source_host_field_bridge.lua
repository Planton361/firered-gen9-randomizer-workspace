-- #711 detached accessor model. TEST_ONLY; never imported by production.
local ROOT = debug.getinfo(1, "S").source:sub(2):match("^(.*)[/\\]") or "."
local guardModule = dofile(ROOT .. "/source_preconsumer_guard.lua")
local function plain(t) return type(t)=="table" and getmetatable(t)==nil end
local function integer(n) return type(n)=="number" and n==math.floor(n) end
local function copy(t)
    if type(t)~="table" then return t end
    local out={}; for k,v in pairs(t) do out[k]=copy(v) end; return out
end
-- Backing tables are detached copies. rawset can only contaminate a historical
-- caller proxy; it cannot alter the guard or any subsequent query's fresh copy.
local function readonly(t)
    if type(t)~="table" then return t end
    local backing={}; for k,v in pairs(t) do backing[k]=readonly(v) end
    return setmetatable({}, {__index=backing,__newindex=function() error("READ_ONLY_TEST_VIEW",0) end,
        __pairs=function() return next,backing,nil end,__len=function() return #backing end,__metatable=false})
end
local function result(state,reason,epoch)
    return {confidence=state,reason=reason,sampleEpoch=epoch,epoch=epoch,
        evidence="TEST_ONLY",liveConfidence="UNKNOWN",production="DENIED",
        validity="HISTORICAL_COPY_REQUERY_REQUIRED",scope="source/synthetic-only"}
end
local M={}
function M.newMock(host, expected, bodies, raw, sources, multi)
    -- No caller-supplied guard/readMock/decoded fields/verification callbacks.
    local guard,why=guardModule.newMock(host,expected,bodies,raw,sources,multi)
    if not guard then return nil,readonly(copy(why)) end
    local profileId=guard.profileId
    local current,revision=nil,0
    local tickets=setmetatable({}, {__mode="k"})
    local deniedState,deniedReason="UNKNOWN","no accepted sample"
    local bridge={profileId=profileId,evidence="TEST_ONLY",liveConfidence="UNKNOWN",production="DENIED"}
    local function clear(reason,state)
        current=nil; revision=revision+1
        deniedState,deniedReason=state or "UNKNOWN",reason
    end
    local function field(state,value,reason,provenance,epoch,scope)
        local f=result(state,reason,epoch)
        if state=="VERIFIED" then f.value=copy(value) end
        f.provenance=provenance or "#709 readMock gate / #711 capability policy"
        f.profileId=profileId; f.scope=scope or "accepted synthetic bytes"
        return f
    end
    local function unknown(reason,epoch,state)
        return field(state or "UNKNOWN",nil,reason,nil,epoch)
    end
    local function mapped(f,epoch,locator,id)
        if not f then return unknown("missing accepted field; no fallback",epoch) end
        local value=f.value
        if id and f.confidence=="VERIFIED" then value=value.id end
        return field(f.confidence,value,f.reason or "accepted source field",
            locator.."; "..(f.provenance or "#709 accepted snapshot"),epoch)
    end
    local function snapshot(ticket)
        -- Every request goes through the real guard gate, including foreign tickets.
        local r=guard.readMock(current and current.guardTicket or nil)
        if not r.ready then
            local reason=current and r.reason or deniedReason
            local state=current and "UNKNOWN" or deniedState
            clear(reason,state)
            local out=result(state,reason,r.epoch); out.ready=false; return nil,out
        end
        if not plain(ticket) or next(ticket)~=nil or tickets[ticket]~=revision then
            local out=result("UNKNOWN","foreign, contaminated or superseded bridge ticket",r.epoch)
            out.ready=false; return nil,out
        end
        return r.value
    end
    function bridge.installMock(injection)
        clear("install invalidates bridge views")
        return readonly(copy(guard.installMock(injection)))
    end
    function bridge.transitionMock(event,declaration)
        clear("lifecycle event: "..tostring(event))
        local r,be=guard.transitionMock(event,declaration)
        return readonly(copy(r)),be
    end
    function bridge.submitMock(sample)
        clear("sample awaiting #709 acceptance")
        local r=guard.submitMock(sample)
        if not r.ready then
            -- Denial-only classification, never evidence for a field/value. Known
            -- double/multi requests remain unsupported even when otherwise malformed.
            local b=plain(sample) and sample.battle
            local c=plain(b) and b.before
            if plain(c) and type(c.flags)=="string" and #c.flags==4 then
                local flags=c.flags
                if flags=="\5\0\0\0" or flags=="\13\0\0\0" or flags=="\79\0\0\0"
                    or flags=="\13\0\32\0" or flags=="\13\0\64\0" then
                    deniedState="UNAVAILABLE"
                end
            end
            deniedReason=r.reason
            local out=result(deniedState,r.reason,r.epoch); out.ready=false
            return readonly(out)
        end
        -- Guard ticket/reference stays private; bridge tickets also expire on a
        -- same-epoch replacement sample, unlike a historical copied value.
        current={guardTicket=r.ticket}
        local ticket={}; tickets[ticket]=revision
        local out=result("VERIFIED","accepted #709 revocable sample",r.epoch)
        out.ready=true; out.ticket=ticket
        -- Ticket is intentionally an opaque plain identity, never source data.
        return out
    end
    function bridge.contextMock(ticket)
        local v,why=snapshot(ticket); if not v then return readonly(why) end
        local out=result("VERIFIED","accepted context; requery before selection",v.epoch)
        out.ready=true; out.inBattle=v.battle~=nil
        out.playerCount=mapped(v.player.count,v.epoch,"gPlayerParty synthetic count")
        if v.battle then
            out.context=mapped(v.battle.context,v.epoch,"T4 before/after flags/count gate")
            out.playerSlot=mapped(v.battle.battlers[1].partySlot,v.epoch,"gBattlerPartyIndexes[0] u16")
            out.enemySlot=mapped(v.battle.battlers[2].partySlot,v.epoch,"gBattlerPartyIndexes[1] u16")
            out.trainerA=mapped(v.battle.trainerA,v.epoch,"T4 trainer A capability")
            out.trainerB=mapped(v.battle.trainerB,v.epoch,"ExtensionState.trainerBTrainerId")
        else
            for _,k in ipairs({"context","playerSlot","enemySlot","trainerA","trainerB"}) do
                out[k]=unknown("outside current encounter",v.epoch,"UNAVAILABLE")
            end
        end
        return readonly(out)
    end
    function bridge.selectMock(ticket,team,slot,mode)
        local v,why=snapshot(ticket); if not v then return readonly(why) end
        local function deny(state,reason)
            local out=result(state,reason,v.epoch); out.ready=false; return readonly(out)
        end
        if team~="PLAYER" and team~="ENEMY" then return deny("UNKNOWN","invalid side") end
        if not integer(slot) or slot<1 or slot>6 then return deny("UNKNOWN","invalid one-based slot; never clamp") end
        if mode~="PARTY" and mode~="ACTIVE" then return deny("UNKNOWN","explicit PARTY/ACTIVE selection required") end
        if (team=="ENEMY" or mode=="ACTIVE") and not v.battle then
            return deny("UNAVAILABLE","no current encounter / active battle")
        end
        local row,locator,active
        if mode=="ACTIVE" then
            row=v.battle.battlers[team=="PLAYER" and 1 or 2]
            if row.partySlot.value~=slot then return deny("UNAVAILABLE","slot is not the active left battler") end
            locator="CFRU:include/battle.h::BattlePokemon / synthetic gBattleMons"; active=true
        else
            row=(team=="PLAYER" and v.player or v.enemy).slots[slot]
            locator="CFRU:include/pokemon.h::Pokemon / synthetic "..(team=="PLAYER" and "gPlayerParty" or "gEnemyParty")
        end
        local out=result("VERIFIED","detached per-field accessor model; not DefaultPokemon",v.epoch)
        out.ready=true; out.profileId=profileId; out.selection=mode
        out.team=field("VERIFIED",team,"explicit side selection",locator,v.epoch)
        out.slot=field("VERIFIED",slot,"one-based side-specific party slot",active and "gBattlerPartyIndexes u16 +2 stride / T4" or locator,v.epoch)
        out.occupied=active and field("VERIFIED",true,"validated active species",locator,v.epoch) or mapped(row.occupied,v.epoch,locator)
        out.pokemonID=mapped(row.species,v.epoch,locator..".species internal ID, never Dex number",true)
        out.speciesIdentity=mapped(row.species,v.epoch,locator..".species + T1 mapping")
        out.speciesIdentity.scope="source-baseline identity; form mechanics unproved"
        out.level=mapped(row.level,v.epoch,locator..".level")
        out.curHP=mapped(row.hp,v.epoch,locator..".hp")
        out.stats={hp=mapped(row.maxHP,v.epoch,locator..".maxHP")}
        for _,k in ipairs({"atk","def","spa","spd","spe"}) do out.stats[k]=unknown("full effective stats unproved",v.epoch) end
        out.heldItem=mapped(row.heldItem,v.epoch,locator..".heldItem",true)
        out.status=mapped(active and row.status1 or row.status,v.epoch,locator..".status1; locked FROSTBITE")
        out.abilityID=mapped(row.ability,v.epoch,locator..".ability",active)
        out.abilityName=unknown("contextual ability name unproved; no catalog substitution",v.epoch)
        out.types={}
        for i=1,3 do out.types[i]=active and mapped(row["type"..i],v.epoch,locator..".type"..i,true)
            or unknown("effective party types unproved",v.epoch) end
        for _,k in ipairs({"personality","trainerID","abilityNum","nature","experience","nickname","statStages"}) do
            out[k]=unknown("missing/incompatible host field; no default substitution",v.epoch)
        end
        out.moves={}
        for i=1,4 do
            local m=row.moves[i]
            out.moves[i]={id=mapped(m.identity,v.epoch,locator..".moves["..i.."]",true),
                pp=mapped(m.pp,v.epoch,locator..".pp["..i.."]")}
            for _,k in ipairs({"maxPP","power","category","type","accuracy"}) do
                out.moves[i][k]=unknown("effective "..k.." unproved; no source/stock fallback",v.epoch)
            end
            if not active and out.occupied.value==false then
                for _,k in ipairs({"maxPP","power","category","type","accuracy"}) do
                    out.moves[i][k]=unknown("empty party slot",v.epoch,"UNAVAILABLE")
                end
            end
        end
        return readonly(out)
    end
    function bridge.statusMock()
        local r=guard.readMock(current and current.guardTicket or nil)
        local out=result(r.ready and "VERIFIED" or "UNKNOWN",r.reason,r.epoch); out.ready=r.ready
        return readonly(out)
    end
    function bridge.teardownMock()
        clear("unload invalidates bridge tickets")
        return readonly(copy(guard.teardownMock()))
    end
    function bridge.metricsMock()
        guard.readMock(current and current.guardTicket or nil)
        return copy(guard.metricsMock())
    end
    return bridge
end
return M
