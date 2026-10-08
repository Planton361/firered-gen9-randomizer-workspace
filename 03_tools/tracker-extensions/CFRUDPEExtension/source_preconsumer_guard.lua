-- #709: detached synthetic interposer. Never loaded by the production entrypoint.
local ROOT = debug.getinfo(1, "S").source:sub(2):match("^(.*)[/\\]") or "."
local partyModule = dofile(ROOT .. "/source_party_decoder.lua")
local battleModule = dofile(ROOT .. "/source_battle_decoder.lua")
local sha256 = dofile(ROOT .. "/profile_sha256.lua")
local PIN = "c450ecaee2d8131a2789bb656e3be792a93712fb"
local seams = {
    {"Program", "updatePokemonTeams", "c3a5a646deebcf9e1fcf628c3cdf2442f56aac53e08b595a425a223c0fc6894f"},
    {"Program", "readNewPokemon", "a3e31f4f1aac4e0bbd97c94b6e9c9de6e922f22b98f4b7d57681dff12c00398c"},
    {"Battle", "updateViewSlots", "fed774b25386214c09e4c31a4a01c63ea3d75fe10e0465bab346785890760b17"},
    {"Battle", "beginNewBattle", "dc40497a14d8446e6fb4f29ded71fd3314a58c14d331ade6d7e8e1d636fd853d"},
}
-- Process-local ownership; a second factory cannot adopt the first one's wrappers.
local owners = setmetatable({}, {__mode="k"})
local acceptedBodies={}
local function plain(t) return type(t)=="table" and getmetatable(t)==nil end
local function keys(t, allowed)
    if not plain(t) then return false end
    for k in pairs(t) do if not allowed[k] then return false end end
    return true
end
local function integer(n) return type(n)=="number" and n>=0 and n<math.huge and n==math.floor(n) end
local function token(s) return type(s)=="string" and #s>0 and #s<=256 end
local function copy(t)
    if type(t)~="table" then return t end
    local out={}; for k,v in pairs(t) do out[k]=copy(v) end; return out
end
local function result(reason, epoch, ticket)
    return {confidence=ticket and "VERIFIED" or "UNKNOWN", ready=ticket~=nil,
        reason=reason, epoch=epoch, ticket=ticket, evidence="TEST_ONLY", label="TEST_ONLY",
        liveConfidence="UNKNOWN", production="DENIED"}
end
local bindingKeys={epoch=true,output=true,session=true,encounter=true,profileId=true,trackerPin=true,evidence=true}
local bindingNames={"epoch","output","session","encounter","profileId","trackerPin","evidence"}
local sampleKeys={before=true,after=true,sampleId=true,player=true,enemy=true,battle=true}
local M={}
function M.newMock(host, expected, bodies, raw, sources, multi)
    -- Only synthetic function-table facades, not emulator globals or caller validators.
    if not keys(host,{Program=true,Battle=true,Lifecycle=true,session=true})
        or not keys(host.Program,{updatePokemonTeams=true,readNewPokemon=true})
        or not keys(host.Battle,{updateViewSlots=true,beginNewBattle=true})
        or not keys(host.Lifecycle,{startTracker=true})
        or type(host.Lifecycle.startTracker)~="function" or not plain(expected) or not plain(bodies) then
        return nil,result("restricted synthetic host required",0)
    end
    if type(raw)~="string" or type(multi)~="string" or not keys(sources,{
        ["DPE:src/Base_Stats.c"]=true,["CFRU:src/Tables/battle_moves.c"]=true,
        ["CFRU:include/battle.h"]=true,["CFRU:include/constants/battle.h"]=true,["CFRU:include/pokemon.h"]=true}) then
        return nil,result("plain immutable public source strings required",0)
    end
    for _,text in pairs(sources) do
        if type(text)~="string" then return nil,result("public source callback/object rejected",0) end
    end
    local journal={}
    for i,seam in ipairs(seams) do
        local ns,key,digest=seam[1],seam[2],seam[3]; local name=ns.."."..key
        if type(bodies[name])~="string" or (acceptedBodies[name]~=bodies[name] and sha256(bodies[name])~=digest)
            or type(expected[name])~="function" or host[ns][key]~=expected[name] then
            return nil,result("foreign wrapper or pinned source mismatch: "..name,0)
        end
        acceptedBodies[name]=bodies[name]
        journal[i]={table=host[ns],key=key,original=expected[name],name=name}
    end
    if owners[host] then return nil,result("host already owned/tombstoned",0) end
    local party,failure=partyModule.newMock(raw,sources)
    if not party then return nil,result(failure.reason or "public source rejected",0) end
    local battle; battle,failure=battleModule.newMock(raw,sources,multi)
    if not battle then return nil,result(failure.reason or "battle source rejected",0) end
    local epoch,battleEpoch,binding,current,lastSample=0,0,nil,nil,0
    local installed,closed=false,false
    local tickets=setmetatable({}, {__mode="k"})
    local entries={}
    local adapter={evidence="TEST_ONLY",liveConfidence="UNKNOWN",production="DENIED",profileId=party.profileId}
    local lifecycle=host.Lifecycle; local start=lifecycle.startTracker
    local function retire(reason)
        epoch=epoch+1; binding=nil; current=nil; lastSample=0
        battleEpoch=battle.transition("reset")
        return result(reason,epoch)
    end
    local function same(a,b)
        if not keys(a,bindingKeys) or not keys(b,bindingKeys) then return false end
        for _,name in ipairs(bindingNames) do if a[name]~=b[name] then return false end end
        return true
    end
    local function declared(d)
        return keys(d,bindingKeys) and d.epoch==epoch and token(d.output) and token(d.session)
            and (d.encounter==false or token(d.encounter)) and d.profileId==party.profileId
            and d.trackerPin==PIN and d.evidence=="SYNTHETIC_ONLY"
    end
    -- Persistent restart stop is separate from the four-function install transaction.
    -- It never invokes the original initializer, even after failed install/unload.
    local tombstone=function() return retire("selected synthetic profile requires guarded restart") end
    local function ownership()
        if closed or not installed or not plain(host) or not plain(host.Program) or not plain(host.Battle)
            or not plain(host.Lifecycle) or not plain(journal[1].table) or not plain(journal[3].table)
            or not plain(lifecycle) or host.Program~=journal[1].table or host.Battle~=journal[3].table
            or host.Lifecycle~=lifecycle or lifecycle.startTracker~=tombstone then return false end
        for _,j in ipairs(journal) do if j.table[j.key]~=j.wrapper then return false end end
        return true
    end
    local function gate()
        if not ownership() then return retire("wrapper ownership lost or inactive") end
        if not binding or not same(host.session,binding) then return retire("missing/stale synthetic session") end
    end
    local function issue()
        local ticket={}; tickets[ticket]=epoch
        return result("independent adapter-owned synthetic view; no stock delegation",epoch,ticket)
    end
    for _,j in ipairs(journal) do
        j.stop=function() return result("non-ready selected-profile tombstone",epoch) end
        j.wrapper=function(...)
            entries[j.name]=(entries[j.name] or 0)+1
            -- Stock arguments/addresses are deliberately not consumed. A complete
            -- snapshot must have been submitted through the separate synthetic API.
            local denied=gate(); if denied then return denied end
            if not current then return result("no coherent synthetic sample",epoch) end
            if j.name:sub(1,6)=="Battle" and binding.encounter==false then
                return retire("battle consumer outside encounter")
            end
            return issue()
        end
    end
    function adapter.installMock(injection)
        if closed then return result("closed/tombstoned adapter",epoch) end
        if installed then
            local denied=gate(); return denied or result("already installed; no new transaction",epoch)
        end
        if injection~=nil and (not keys(injection,{after=true,mode=true}) or not integer(injection.after)
            or injection.after<1 or injection.after>4 or (injection.mode~="throw" and injection.mode~="drop")) then
            return retire("invalid synthetic fault declaration")
        end
        if owners[host] or not plain(host) or not plain(host.Program) or not plain(host.Battle)
            or not plain(host.Lifecycle) or not plain(lifecycle)
            or not plain(journal[1].table) or not plain(journal[3].table)
            or host.Lifecycle~=lifecycle or lifecycle.startTracker~=start then
            return retire("foreign restart owner")
        end
        for _,j in ipairs(journal) do
            if host[j.name:match("^(%w+)")]~=j.table or j.table[j.key]~=j.original then
                return retire("pre-existing foreign wrapper conflict")
            end
        end
        owners[host]=adapter; lifecycle.startTracker=tombstone
        -- Establish owned deny-only staging references before the data-wrapper
        -- transaction. No callbacks/yields occur while these four slots are staged.
        for _,j in ipairs(journal) do rawset(j.table,j.key,j.stop) end
        local ok,why=pcall(function()
            for i,j in ipairs(journal) do
                rawset(j.table,j.key,j.wrapper)
                if injection and injection.after==i then
                    if injection.mode=="throw" then error("synthetic install injection",0) end
                    rawset(j.table,j.key,j.stop)
                end
                if j.table[j.key]~=j.wrapper then error("install read-back failed",0) end
            end
        end)
        if not ok then
            -- Abort restores owned staging stops, never stock or foreign replacements.
            for _,j in ipairs(journal) do
                if rawget(j.table,j.key)==j.wrapper then rawset(j.table,j.key,j.stop) end
            end
            closed=true; return retire("transaction aborted: "..tostring(why))
        end
        installed=true; return retire("all four guards installed; session non-ready")
    end
    function adapter.transitionMock(event, declaration)
        retire("synthetic lifecycle invalidation")
        if not ownership() then return result("inactive/conflicting ownership",epoch) end
        if event~="start" and event~="switch" and event~="session" and event~="output" then
            return result("event remains non-ready",epoch)
        end
        if not declared(declaration) or not same(host.session,declaration) then
            return result("invalid synthetic declaration; booleans are not evidence",epoch)
        end
        binding=copy(declaration); battleEpoch=battle.transition(binding.encounter and "start" or "end")
        return result("armed synthetic session; awaiting bytes",epoch),battleEpoch
    end
    function adapter.submitMock(sample)
        local denied=gate(); if denied then return denied end
        if not keys(sample,sampleKeys) or not same(sample.before,binding) or not same(sample.after,binding)
            or not integer(sample.sampleId) or sample.sampleId<=lastSample then
            return retire("malformed/replayed/cross-session sample")
        end
        local ok,view=pcall(function()
            local function decode(input)
                if not keys(input,{bytes=true,count=true}) then error("party input required",0) end
                local p=party.decodeMock(input.bytes,input.count)
                if p.count.confidence~="VERIFIED" then error("malformed party sample",0) end
                for i=1,input.count do
                    local row=p.slots[i]
                    for _,name in ipairs({"species","level","hp","maxHP","heldItem","status"}) do
                        if row[name].confidence~="VERIFIED" then error("invalid occupied field: "..name,0) end
                    end
                    for _,move in ipairs(row.moves) do
                        if move.identity.confidence~="VERIFIED" or move.pp.confidence~="VERIFIED" then
                            error("invalid occupied move",0)
                        end
                    end
                end
                return p
            end
            local p=decode(sample.player); local e,b
            if binding.encounter then
                if not keys(sample.battle,{epoch=true,before=true,after=true,battleMons=true,ppCaps=true})
                    or sample.battle.epoch~=battleEpoch then error("missing/stale battle sample",0) end
                for _,c in ipairs({sample.battle.before,sample.battle.after}) do
                    if not keys(c,{epoch=true,state=true,output=true,battle=true,flags=true,count=true,positions=true,indexes=true})
                        or c.output~=binding.output or c.battle~=binding.encounter then
                        error("unproved battle/trainer context",0)
                    end
                end
                b=battle.decodeMock(sample.battle)
                if b.context.confidence~="VERIFIED" then error("invalid/unsupported battle context",0) end
                e=decode(sample.enemy)
                for i=1,2 do
                    local r=b.battlers[i]
                    if r.species.confidence~="VERIFIED" or not r.species.value or r.species.value.absent then
                        error("invalid active species",0)
                    end
                    for _,name in ipairs({"level","hp","maxHP","ability","heldItem","type1","type2","type3","status1"}) do
                        if r[name].confidence~="VERIFIED" then error("invalid active field: "..name,0) end
                    end
                    for _,move in ipairs(r.moves) do
                        if move.identity.confidence~="VERIFIED" or move.pp.confidence~="VERIFIED" then
                            error("invalid active move/cap",0)
                        end
                    end
                    local team=r.team.value=="PLAYER" and p or e
                    if not r.partySlot.value or r.partySlot.value>team.count.value then
                        error("active index outside occupied party",0)
                    end
                end
            elseif sample.battle~=nil or sample.enemy~=nil then error("enemy outside encounter",0) end
            return {player=p,enemy=e,battle=b,epoch=epoch,profileId=party.profileId,
                evidence="TEST_ONLY",liveConfidence="UNKNOWN",production="DENIED"}
        end)
        if not ok then return retire("synthetic sample rejected: "..tostring(view)) end
        -- Fresh data never reaches GameData/Combatants/DefaultPokemon/Trainer/notes.
        if not same(host.session,binding) or not ownership() then return retire("sample commit gate failed") end
        local function stamp(t)
            if type(t)~="table" then return end
            if t.confidence then
                t.sampleEpoch=epoch; t.label="TEST_ONLY"; t.production="DENIED"
                t.reason=t.reason or t.provenance or "source/synthetic field only"
            end
            for _,v in pairs(t) do stamp(v) end
        end
        stamp(view)
        current=view; lastSample=sample.sampleId; return issue()
    end
    function adapter.readMock(ticket)
        local denied=gate(); if denied then return denied end
        if not plain(ticket) or tickets[ticket]~=epoch or not current then
            return result("revoked/foreign view ticket",epoch)
        end
        -- Values are explicitly historical copies at this epoch, never live references.
        local out=result("fresh historical copy; re-query ticket for current readiness",epoch)
        out.confidence="VERIFIED"; out.ready=true; out.value=copy(current); return out
    end
    function adapter.teardownMock()
        if closed then return result("already closed; tombstones retained",epoch) end
        retire("unload revoked all tickets")
        -- Post-install rollback replaces owned guards with deny-only tombstones.
        -- Restoring vanilla here would reopen selected unknown-profile consumers.
        for _,j in ipairs(journal) do
            if rawget(j.table,j.key)==j.wrapper then
                rawset(j.table,j.key,j.stop)
            end
        end
        closed=true; installed=false
        return result("owned guards removed safely; foreign replacements preserved",epoch)
    end
    function adapter.statusMock() return result(binding and "synthetic binding armed" or "non-ready",epoch) end
    function adapter.metricsMock() return copy(entries) end
    return adapter
end
return M
