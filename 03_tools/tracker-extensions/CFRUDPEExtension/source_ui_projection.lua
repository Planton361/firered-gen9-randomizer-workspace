-- #694 Phase A: detached TEST_ONLY view model, never a Tracker adapter.
local ROOT = debug.getinfo(1, "S").source:sub(2):match("^(.*)[/\\]") or "."
local partyModule = dofile(ROOT .. "/source_party_decoder.lua")
local battleModule = dofile(ROOT .. "/source_battle_decoder.lua")
local function plain(t) return type(t)=="table" and getmetatable(t)==nil end
local function integer(n) return type(n)=="number" and n<math.huge and n==math.floor(n) end
local function copy(t)
    if type(t)~="table" then return t end
    local out={}; for k,v in pairs(t) do out[k]=copy(v) end; return out
end
local function keys(t, allowed)
    if not plain(t) then return false end
    for k in pairs(t) do if not allowed[k] then return false end end
    return true
end
local function token(t) return type(t)=="string" and #t>0 and #t<=256 end
local contextKeys={epoch=true,profileId=true,evidence=true,trusted=true,output=true,
    session=true,battle=true,playerRoster=true,enemyRoster=true}
local contextNames={"epoch","profileId","evidence","trusted","output","session","battle","playerRoster","enemyRoster"}
local rowNames={"occupied","species","level","hp","maxHP","status","heldItem","abilityId",
    "abilityName","effectiveTypes","type1","type2","type3","partySlot","team","hpPercent"}
local moveNames={"identity","pp","maxPP","effective","damage"}
local M={}
function M.newMock(raw, sources, multi)
    local party,failure=partyModule.newMock(raw,sources)
    if not party then return nil,failure end
    local battle; battle,failure=battleModule.newMock(raw,sources,multi)
    if not battle then return nil,failure end
    local epoch,battleEpoch,binding,lastSample,current,roster=0,0,nil,0,nil,nil
    local function field(state,value,reason,scope)
        return {confidence=state,value=value,reason=reason or "validated synthetic decoder result",
            scope=scope or "synthetic-current",label="TEST_ONLY",evidence="TEST_ONLY",
            liveConfidence="UNKNOWN",profileId=party.profileId,sampleEpoch=epoch}
    end
    local function unknown(reason) return field("UNKNOWN",nil,reason) end
    local function unavailable(reason) return field("UNAVAILABLE",nil,reason) end
    local function row(state,reason)
        local r={moves={}}
        for _,name in ipairs(rowNames) do r[name]=field(state,nil,reason) end
        for i=1,4 do
            r.moves[i]={}
            for _,name in ipairs(moveNames) do r.moves[i][name]=field(state,nil,reason) end
        end
        r.sourceBaseline=field(state,nil,reason,"source-baseline")
        return r
    end
    local function blank(reason,battleState)
        local out={evidence="TEST_ONLY",label="TEST_ONLY",liveConfidence="UNKNOWN",
            profileId=party.profileId,epoch=epoch,diagnostic=reason,playerParty={},enemyParty={},active={}}
        for i=1,6 do out.playerParty[i]=row("UNKNOWN",reason); out.enemyParty[i]=row("UNKNOWN",reason) end
        for i=1,4 do out.active[i]=row(battleState or "UNKNOWN",reason) end
        out.playerCount=unknown(reason); out.enemyCount=unknown(reason)
        out.battleContext=field(battleState or "UNKNOWN",nil,reason)
        out.trainerA=field(battleState or "UNKNOWN",nil,reason)
        out.trainerB=field(battleState or "UNKNOWN",nil,reason)
        out.battleDetails=unavailable("secondary/field/counter semantics intentionally unsupported")
        out.notes=unavailable("no persistence input or output")
        out.coverage=unavailable("effective move semantics/calculator intentionally unsupported")
        return out
    end
    current=blank("no trusted synthetic session")
    local ui={evidence="TEST_ONLY",liveConfidence="UNKNOWN",profileId=party.profileId}
    function ui.snapshot() return copy(current) end
    local function retire(reason,state)
        epoch=epoch+1; binding=nil; lastSample=0; roster=nil
        battleEpoch=battle.transition("reset")
        current=blank(reason,state); return ui.snapshot()
    end
    local function context(c)
        return keys(c,contextKeys) and c.epoch==epoch and c.profileId==party.profileId
            and c.evidence=="SYNTHETIC_ONLY" and c.trusted==true
            and token(c.output) and token(c.session) and token(c.playerRoster)
            and token(c.enemyRoster) and (c.battle==false or token(c.battle))
    end
    local function same(a,b)
        if not context(a) or not context(b) then return false end
        for _,k in ipairs(contextNames) do if a[k]~=b[k] then return false end end
        return true
    end
    -- Every event clears immediately. Only a fresh, explicit synthetic proof arms it.
    -- Returned epochs are declarations for fixtures, never live identity acceptance.
    function ui.transition(event,proof)
        if type(event)~="string" then event="invalid-event" end
        retire("synthetic transition: "..event)
        if (event=="start" or event=="switch" or event=="session" or event=="output") and context(proof) then
            binding=copy(proof)
            battleEpoch=battle.transition(proof.battle and "start" or "end")
        end
        return epoch,battleEpoch
    end
    local function project(f,expectedEpoch,scope)
        if not plain(f) or f.evidence~="TEST_ONLY" or f.liveConfidence~="UNKNOWN"
            or (expectedEpoch and f.sampleEpoch~=expectedEpoch) then return unknown("invalid decoder field evidence/epoch") end
        if f.confidence=="UNAVAILABLE" then return unavailable(f.reason or "unsupported decoder field") end
        if f.confidence~="VERIFIED" or f.value==nil then return unknown(f.reason or "missing decoder field") end
        local value=copy(f.value)
        local function stamp(t)
            if type(t)~="table" then return end
            if t.confidence then
                t.label="TEST_ONLY"; t.evidence="TEST_ONLY"; t.liveConfidence="UNKNOWN"
                t.profileId=party.profileId; t.sampleEpoch=epoch; t.scope=scope or "source-baseline"
                t.reason=t.reason or t.provenance or "source-only decoder fact"
                if t.confidence~="VERIFIED" then t.value=nil end
            end
            for _,v in pairs(t) do stamp(v) end
        end
        stamp(value)
        return field("VERIFIED",value,f.provenance,scope)
    end
    local function projectRow(r,active)
        local e=active and battleEpoch or nil
        local out=row("UNKNOWN","field dependencies unproved")
        out.species=project(r.species,e,"source-baseline identity")
        if out.species.confidence~="VERIFIED" then return out end
        if out.species.value.absent then
            local empty=row("UNAVAILABLE","empty slot")
            empty.species=out.species; empty.occupied=project(r.occupied)
            return empty
        end
        if not active and (r.isEgg.confidence~="VERIFIED" or r.isEgg.value) then
            local egg=row("UNAVAILABLE","egg display intentionally unsupported")
            egg.species=out.species; return egg
        end
        for _,name in ipairs({"level","hp","maxHP","heldItem"}) do out[name]=project(r[name],e) end
        out.status=project(active and r.status1 or r.status,e)
        out.abilityId=project(r.ability,e,"synthetic ID; contextual name unproved")
        if out.abilityId.value then
            out.abilityId.value={id=out.abilityId.value.id,absent=out.abilityId.value.absent}
        end
        out.abilityName=unknown("contextual ability selection/name unproved; no catalog-name fallback")
        out.occupied=active and field("VERIFIED",true,"supported active species") or project(r.occupied)
        if active then
            for _,name in ipairs({"type1","type2","type3","partySlot","team"}) do out[name]=project(r[name],e) end
        else
            out.effectiveTypes=project(r.effectiveTypes)
            -- Baseline remains separate, cannot drive effective fields/calculations.
            out.sourceBaseline=project(r.baselineSpecies,nil,"source-baseline")
        end
        if out.hp.confidence=="VERIFIED" and out.maxHP.confidence=="VERIFIED" then
            out.hpPercent=field("VERIFIED",100*out.hp.value/out.maxHP.value,"synthetic HP / maxHP only")
        end
        for i=1,4 do
            local m=r.moves[i]; local dest=out.moves[i]
            dest.identity=project(m.identity,e,"source-baseline identity")
            if dest.identity.confidence=="VERIFIED" then
                dest.pp=project(m.pp,e,active and "synthetic cap-checked current PP" or "synthetic stored current PP; cap unproved")
                dest.effective=project(m.effective,e)
            end
            dest.maxPP=unknown("effective maximum PP unproved; baseline PP is not a cap")
            dest.damage=unknown("effective move power/category/context unproved")
        end
        return out
    end
    local function decodeParty(input)
        if input==nil then return nil end
        if not keys(input,{bytes=true,count=true}) then error("untrusted party table",0) end
        local result=party.decodeMock(input.bytes,input.count)
        if result.count.confidence~="VERIFIED" then error("invalid party block/count",0) end
        return result
    end
    function ui.decodeMock(sample)
        -- External field/Tracker/default/persistence tables are never evidence.
        if not keys(sample,{before=true,after=true,sampleId=true,player=true,enemy=true,battle=true})
            or not binding or not same(sample.before,sample.after) or not same(sample.before,binding)
            or not integer(sample.sampleId) or sample.sampleId<=lastSample then
            return retire("missing/untrusted/stale synthetic context or sample")
        end
        local ok,result=pcall(function()
            local p=decodeParty(sample.player)
            local b
            if binding.battle then
                if not keys(sample.battle,{epoch=true,before=true,after=true,battleMons=true,ppCaps=true})
                    or sample.battle.epoch~=battleEpoch then error("missing/stale battle sample",0) end
                for _,c in ipairs({sample.battle.before,sample.battle.after}) do
                    if not plain(c) or c.output~=binding.output or c.battle~=binding.battle then
                        error("cross-output/battle decoder sample",0)
                    end
                end
                b=battle.decodeMock(sample.battle)
                if b.context.confidence~="VERIFIED" then return retire(b.context.reason,b.context.confidence) end
            elseif sample.battle~=nil or sample.enemy~=nil then error("enemy/battle input outside battle",0) end
            local enemy=b and decodeParty(sample.enemy) or nil
            -- Species roster changes must be declared even if the caller reuses tokens.
            local signature={}
            for _,team in ipairs({{p},{enemy}}) do
                for i=1,6 do
                    local f=team[1] and team[1].slots[i].species
                    signature[#signature+1]=f and f.value and tostring(f.value.id) or "?"
                end
            end
            if b then
                for i=1,2 do
                    local f=b.battlers[i].species
                    signature[#signature+1]=f.value and tostring(f.value.id) or "?"
                end
            end
            signature=table.concat(signature,",")
            if roster and roster~=signature then error("party changed without transition",0) end
            roster=signature
            local out=blank("fresh synthetic projection; unresolved fields withheld")
            if p then
                out.playerCount=project(p.count)
                for i=1,6 do out.playerParty[i]=projectRow(p.slots[i],false) end
            end
            if enemy then
                out.enemyCount=project(enemy.count)
                for i=1,6 do out.enemyParty[i]=projectRow(enemy.slots[i],false) end
            end
            if b then
                out.battleContext=project(b.context,battleEpoch)
                out.trainerA=project(b.trainerA,battleEpoch); out.trainerB=project(b.trainerB,battleEpoch)
                for i=1,4 do out.active[i]=projectRow(b.battlers[i],true) end
            else
                out.battleContext=unavailable("outside battle")
                out.trainerA=unavailable("outside battle"); out.trainerB=unavailable("outside battle")
                for i=1,4 do out.active[i]=row("UNAVAILABLE","outside battle") end
                for i=1,6 do out.enemyParty[i]=row("UNAVAILABLE","outside battle") end
                out.enemyCount=unavailable("outside battle")
            end
            lastSample=sample.sampleId; current=out; return ui.snapshot()
        end)
        if not ok then return retire("invalid synthetic data: "..tostring(result)) end
        return result
    end
    return ui
end
return M
