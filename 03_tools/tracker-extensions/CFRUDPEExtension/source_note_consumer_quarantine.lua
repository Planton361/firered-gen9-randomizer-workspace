-- #713 detached TEST_ONLY consumer records. Never imported by production.
local ROOT=debug.getinfo(1,"S").source:sub(2):match("^(.*)[/\\]") or "."
local bridgeModule=dofile(ROOT.."/source_host_field_bridge.lua")
local function plain(t) return type(t)=="table" and getmetatable(t)==nil end
local function integer(n) return type(n)=="number" and n==math.floor(n) end
local function copy(t)
    if type(t)~="table" then return t end
    local out={}; for k,v in pairs(t) do out[k]=copy(v) end; return out
end
local function readonly(t)
    if type(t)~="table" then return t end
    local b={}; for k,v in pairs(t) do b[k]=readonly(v) end
    return setmetatable({},{__index=b,__newindex=function() error("READ_ONLY_TEST_VIEW",0) end,
        __pairs=function() return next,b,nil end,__len=function() return #b end,__metatable=false})
end
local categories={note=true,moves=true,abilities=true,eL=true,FourMovesIfAllKnown=true}
local witnessKeys={species=true,side=true,slot=true,moveSlot=true,moveId=true,level=true,encounter=true}
local M={}
function M.newMock(host,expected,bodies,raw,sources,multi)
    -- The real #711 bridge owns the #709 guard. No injected reader or trusted labels.
    local bridge,why=bridgeModule.newMock(host,expected,bodies,raw,sources,multi)
    if not bridge then return nil,why end
    local revision,current,encounter=0,nil,nil
    local tickets=setmetatable({},{__mode="k"})
    local observations=setmetatable({},{__mode="k"})
    local quarantined=0
    local gate={profileId=bridge.profileId,evidence="TEST_ONLY",liveConfidence="UNKNOWN",production="DENIED"}
    local function record(confidence,reason,epoch,value)
        local r={ready=confidence=="VERIFIED",confidence=confidence,reason=reason,
            provenance="#713 quarantine policy / internal #711 + #709 current synthetic snapshot",
            profileId=bridge.profileId,epoch=epoch,sampleEpoch=epoch,evidence="TEST_ONLY",
            liveConfidence="UNKNOWN",production="DENIED",scope="source/synthetic-only",
            validity="HISTORICAL_COPY_REQUERY_REQUIRED"}
        if confidence=="VERIFIED" then r.value=copy(value) end
        return readonly(r)
    end
    local function clear() revision=revision+1; current=nil; observations=setmetatable({},{__mode="k"}) end
    local function context(ticket)
        -- Even a foreign reference first rechecks bridge ownership/lifecycle.
        local c=bridge.contextMock(current and current.bridgeTicket or nil)
        if not c.ready then clear(); return nil,record(c.confidence,c.reason,c.epoch) end
        if not plain(ticket) or next(ticket)~=nil or tickets[ticket]~=revision then
            return nil,record("UNKNOWN","foreign, mutated or superseded consumer ticket",c.epoch)
        end
        return c
    end
    function gate.installMock(injection) clear(); encounter=nil; return bridge.installMock(injection) end
    function gate.transitionMock(event,declaration)
        clear(); encounter=nil
        local r,b=bridge.transitionMock(event,declaration)
        -- This token associates only accepted synthetic bytes, never real persistence identity.
        if plain(declaration) then encounter=declaration.encounter end
        return r,b
    end
    function gate.submitMock(sample)
        clear()
        local r=bridge.submitMock(sample)
        if not r.ready then return record(r.confidence,r.reason,r.epoch) end
        current={bridgeTicket=r.ticket}
        local t={}; tickets[t]=revision
        return {ready=true,ticket=t,confidence="VERIFIED",epoch=r.epoch,sampleEpoch=r.epoch,
            profileId=bridge.profileId,evidence="TEST_ONLY",liveConfidence="UNKNOWN",production="DENIED"}
    end
    function gate.quarantineMock(_historical)
        -- Deliberately never inspect, copy, retain, traverse or mutate historical input.
        -- Count snapshots presented, not their content. Quarantine is not deletion.
        quarantined=quarantined+1
        return readonly({status="QUARANTINED",count=quarantined,reason="untrusted historical input; no import or reassociation",
            evidence="TEST_ONLY",liveConfidence="UNKNOWN",production="DENIED",profileId=bridge.profileId})
    end
    local function checked(ticket,w)
        local c,why=context(ticket); if not c then return nil,why end
        if not c.inBattle then return nil,record("UNAVAILABLE","outside current encounter",c.epoch) end
        if not plain(w) then return nil,record("UNKNOWN","plain bounded observation required",c.epoch) end
        for k in pairs(w) do if not witnessKeys[k] then return nil,record("UNKNOWN","unproved observation fields",c.epoch) end end
        if w.side~="PLAYER" and w.side~="ENEMY" or not integer(w.moveSlot) or w.moveSlot<1 or w.moveSlot>4
            or type(w.encounter)~="string" or w.encounter~=encounter then
            return nil,record("UNKNOWN","observation association mismatch",c.epoch)
        end
        local row=bridge.selectMock(current.bridgeTicket,w.side,w.slot,"ACTIVE")
        if not row.ready then return nil,record(row.confidence,row.reason,c.epoch) end
        local move=row.moves[w.moveSlot]
        if row.pokemonID.confidence~="VERIFIED" or row.pokemonID.value~=w.species
            or row.level.confidence~="VERIFIED" or row.level.value~=w.level
            or row.slot.confidence~="VERIFIED" or row.slot.value~=w.slot
            or move.id.confidence~="VERIFIED" or move.id.value==0 or move.id.value~=w.moveId
            or move.pp.confidence~="VERIFIED" then
            return nil,record("UNKNOWN","identity/level/slot/move not independently established",c.epoch)
        end
        return c
    end
    function gate.observeMock(ticket,witness)
        local c,why=checked(ticket,witness); if not c then return why end
        local t={}; observations[t]={revision=revision,witness=copy(witness),consumerTicket=ticket}
        local r={ready=true,ticket=t,confidence="VERIFIED",reason="VERIFIED_SOURCE_SYNTHETIC_ONLY",
            profileId=bridge.profileId,epoch=c.epoch,sampleEpoch=c.epoch,evidence="TEST_ONLY",
            liveConfidence="UNKNOWN",production="DENIED"}
        return r
    end
    function gate.readMock(ticket,category,side,slot,observationTicket)
        local c,why=context(ticket); if not c then return why end
        if not categories[category] then return record("UNKNOWN","unknown category",c.epoch) end
        local row=bridge.selectMock(current.bridgeTicket,side,slot,"PARTY")
        if not row.ready then return record(row.confidence,row.reason,c.epoch) end
        if row.occupied.value~=true then return record("UNAVAILABLE","empty current slot",c.epoch) end
        if category=="FourMovesIfAllKnown" then
            return record("UNAVAILABLE","four observed moves/order unproved; historical species+level key quarantined",c.epoch)
        end
        if category~="moves" then
            return record("UNKNOWN","historical "..category.." quarantined; current observation unproved; no fallback",c.epoch)
        end
        local o=plain(observationTicket) and next(observationTicket)==nil and observations[observationTicket]
        if not o or o.revision~=revision or o.consumerTicket~=ticket or o.witness.side~=side or o.witness.slot~=slot then
            return record("UNKNOWN","no current owned move observation",c.epoch)
        end
        local verified,denial=checked(ticket,o.witness); if not verified then return denial end
        return record("VERIFIED","VERIFIED_SOURCE_SYNTHETIC_ONLY",c.epoch,
            {observedMoveId=o.witness.moveId,species=o.witness.species,side=side,slot=slot,level=o.witness.level})
    end
    function gate.statusMock() return bridge.statusMock() end
    function gate.metricsMock() return bridge.metricsMock() end
    function gate.teardownMock() clear(); encounter=nil; return bridge.teardownMock() end
    return gate
end
return M
