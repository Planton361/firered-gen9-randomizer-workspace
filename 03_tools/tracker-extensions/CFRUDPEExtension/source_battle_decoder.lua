-- #693 Phase A: detached synthetic strings only. Never loaded by production.
local ROOT = debug.getinfo(1, "S").source:sub(2):match("^(.*)[/\\]") or "."
local party = dofile(ROOT .. "/source_party_decoder.lua")
local sha256 = dofile(ROOT .. "/profile_sha256.lua")
local MULTI_SHA = "d6872f075e1be795b4253abe72d111f154a95ccb01e4e1900ee1544ad5060088"
-- Accepted T1 ARM ABI, CFRU:include/pokemon.h::BattlePokemon. No addresses.
local SIZE = 88
local ABI = {species={0,2}, moves={12,2}, pp={36,1}, ability={32,1},
    type1={33,1}, type2={34,1}, type3={24,1}, hp={40,2}, level={42,1},
    maxHP={44,2}, item={46,2}, status1={76,4}, status2={80,4}}
local function integer(n) return type(n)=="number" and n==math.floor(n) end
local function plain(t) return type(t)=="table" and getmetatable(t)==nil end
local function copy(t)
    if type(t)~="table" then return t end
    local out={}; for k,v in pairs(t) do out[k]=copy(v) end; return out
end
local function field(state,value,reason,provenance)
    return {confidence=state,value=value,reason=reason,provenance=provenance,
        evidence="TEST_ONLY",liveConfidence="UNKNOWN"}
end
local function unknown(reason) return field("UNKNOWN",nil,reason) end
local function unavailable(reason) return field("UNAVAILABLE",nil,reason) end
local function verified(value,provenance) return field("VERIFIED",value,nil,provenance) end
local function block(s,n) return type(s)=="string" and #s==n end
local function read(s,offset,width)
    local n=0; for i=width-1,0,-1 do n=n*256+s:byte(offset+i+1) end; return n
end
local names={"battler","position","team","partyIndex","partySlot","species","level","hp","maxHP",
    "ability","abilityName","heldItem","type1","type2","type3","status1","status2","status2Meaning"}
local function blankRow(confidence,reason)
    local row={moves={}}
    for _,name in ipairs(names) do row[name]=field(confidence,nil,reason) end
    for i=1,4 do row.moves[i]={identity=field(confidence,nil,reason),pp=field(confidence,nil,reason),
        effective=field(confidence,nil,reason)} end
    return row
end
local M={}
local acceptedMulti
function M.newMock(raw,sources,multiText)
    -- The existing resolver owns the complete T1/profile and five-source lock.
    local resolver,failure=party.newMock(raw,sources)
    if not resolver then return nil,failure end
    if type(multiText)~="string" or (multiText~=acceptedMulti and sha256(multiText)~=MULTI_SHA) then
        return nil,unknown("missing/changed accepted trainer-B source")
    end
    acceptedMulti=multiText -- Cache immutable, byte-exact accepted source only.
    local definitions=sources["CFRU:include/constants/battle.h"]
    local constants={}
    for name,token in definitions:gmatch("#define%s+([%w_]+)%s+([%w_]+)") do
        if tonumber(token) then constants[name]=tonumber(token) end
    end
    assert(constants.MAX_BATTLERS_COUNT==4 and constants.B_POSITION_PLAYER_LEFT==0
        and constants.B_POSITION_OPPONENT_LEFT==1 and constants.BIT_SIDE==1)
    local maxLevel=tonumber(sources["CFRU:include/pokemon.h"]:match("#define%s+MAX_MON_LEVEL%s+(%d+)"))
    local epoch,armed,signature=0,false,nil
    local current
    local function blank(confidence,reason)
        local out={evidence="TEST_ONLY",liveConfidence="UNKNOWN",profileId=resolver.profileId,
            epoch=epoch,context=field(confidence,nil,reason),trainerA=field(confidence,nil,reason),
            trainerB=field(confidence,nil,reason),battlers={}}
        for i=1,4 do out.battlers[i]=blankRow(confidence,reason) end
        return out
    end
    current=blank("UNKNOWN","no synthetic battle")
    local decoder={evidence="TEST_ONLY",liveConfidence="UNKNOWN",profileId=resolver.profileId}
    function decoder.snapshot()
        local out=copy(current)
        local function stamp(t)
            if type(t)~="table" then return end
            if t.confidence then t.sampleEpoch=out.epoch end
            for _,v in pairs(t) do stamp(v) end
        end
        stamp(out); return out
    end
    function decoder.transition(event)
        epoch=epoch+1; signature=nil
        armed=event=="start" or event=="switch"
        current=blank("UNKNOWN","synthetic transition: "..tostring(event))
        return epoch -- end/reset/output-switch (and unknown events) disarm.
    end
    local function reject(reason,confidence)
        -- Every failed sample retires its epoch, including any formerly good rows.
        epoch=epoch+1; signature=nil
        current=blank(confidence or "UNKNOWN",reason)
        return decoder.snapshot()
    end
    local function contextKey(c)
        if not plain(c) or c.epoch~=epoch or c.state~="ACTIVE" or not armed
            or type(c.output)~="string" or c.output=="" or type(c.battle)~="string" or c.battle==""
            or not block(c.flags,4) or not block(c.count,1) or not block(c.positions,4)
            or not block(c.indexes,8) then return nil end
        -- Length-prefix tokens so caller strings cannot create signature collisions.
        return #c.output..":"..c.output..#c.battle..":"..c.battle..c.flags..c.count..c.positions..c.indexes
    end
    local function trainerKey(t)
        if t==nil then return "absent" end
        if not plain(t) or t.epoch~=epoch or not block(t.bytes,2) or type(t.trusted)~="boolean"
            or t.source~="gTrainerBattleOpponent_A" then return nil end
        return t.bytes..tostring(t.trusted)
    end
    function decoder.decodeMock(sample)
        if not plain(sample) or sample.epoch~=epoch then return reject("missing/stale sample epoch") end
        local before,after=sample.before,sample.after
        local key=contextKey(before)
        if not key or key~=contextKey(after) then return reject("incomplete/changing synthetic context") end
        local akey=trainerKey(before.trainerA)
        if not akey or akey~=trainerKey(after.trainerA) then return reject("changing/malformed trainer context") end
        key=key..akey
        if signature and signature~=key then return reject("context changed without a transition") end
        if not block(sample.battleMons,SIZE*4) then return reject("malformed BattlePokemon block") end
        local count,flags=read(before.count,0,1),read(before.flags,0,4)
        if count~=2 and count~=4 then return reject("unexpected battler count") end
        local unsupported={
            [constants.BATTLE_TYPE_IS_MASTER+constants.BATTLE_TYPE_DOUBLE]=true,
            [constants.BATTLE_TYPE_IS_MASTER+constants.BATTLE_TYPE_DOUBLE+constants.BATTLE_TYPE_TRAINER]=true,
            [constants.BATTLE_TYPE_IS_MASTER+constants.BATTLE_TYPE_DOUBLE+constants.BATTLE_TYPE_TRAINER
                +constants.BATTLE_TYPE_LINK+constants.BATTLE_TYPE_MULTI]=true,
            [constants.BATTLE_TYPE_IS_MASTER+constants.BATTLE_TYPE_DOUBLE+constants.BATTLE_TYPE_TRAINER
                +constants.BATTLE_TYPE_TWO_OPPONENTS]=true,
            [constants.BATTLE_TYPE_IS_MASTER+constants.BATTLE_TYPE_DOUBLE+constants.BATTLE_TYPE_TRAINER
                +constants.BATTLE_TYPE_INGAME_PARTNER]=true,
        }
        local trainer=flags==constants.BATTLE_TYPE_IS_MASTER+constants.BATTLE_TYPE_TRAINER
        local single=flags==constants.BATTLE_TYPE_IS_MASTER or trainer
        if not single and not unsupported[flags] then return reject("unknown/ambiguous or unproved flags") end
        if (single and count~=2) or (not single and count~=4) then return reject("flags/count mismatch") end
        local seen={}
        for i=0,count-1 do
            local position,index=read(before.positions,i,1),read(before.indexes,2*i,2)
            if position>=count or seen[position] or index>=6 then return reject("illegal position/party index") end
            seen[position]=true
            -- Non-link singles in this bounded contract use the source's left slots.
            if single and position~=i then return reject("non-link single position mismatch") end
        end
        if not single then return reject("double/multi mapping intentionally unsupported","UNAVAILABLE") end
        signature=key
        current=blank("UNKNOWN","field prerequisites not established")
        current.context=verified({kind=trainer and "TRAINER" or "WILD",flags=flags,count=count},
            "synthetic before/after gate; CFRU battle constants")
        current.trainerB=unavailable("single context; B is ExtensionState.trainerBTrainerId, no absolute binding")
        if not trainer then current.trainerA=unavailable("wild battle")
        elseif before.trainerA and before.trainerA.trusted then
            current.trainerA=verified({id=read(before.trainerA.bytes,0,2),scope="synthetic-context-only"},
                "explicit synthetic gTrainerBattleOpponent_A u16; no gTrainers team")
        else current.trainerA=unknown("trainer A needs independent synthetic trust") end
        for i=0,1 do
            local row=current.battlers[i+1]
            local function r(name,delta)
                local f=ABI[name]; return read(sample.battleMons,i*SIZE+f[1]+(delta or 0),f[2])
            end
            local identity=resolver.resolve("species",r("species"))
            if identity.confidence=="VERIFIED" and not identity.value.absent
                and math.floor(read(sample.battleMons,i*SIZE+23,1)/64)%2==0 then
                row.species=identity
                -- These mappings refer to each side's own team, never battler ID == slot.
                row.battler=verified(i,"gBattleMons row index")
                row.position=verified(i,"gBattlerPositions u8 / source left position")
                row.team=verified(i==0 and "PLAYER" or "ENEMY","CFRU BIT_SIDE / separate party owner")
                local index=read(before.indexes,2*i,2)
                row.partyIndex=verified(index,"gBattlerPartyIndexes u16 +2 stride")
                row.partySlot=verified(index+1,"explicit zero-based to one-based conversion")
                local level,hp,maxHP=r("level"),r("hp"),r("maxHP")
                row.level=level>=1 and level<=maxLevel and verified(level,"BattlePokemon.level") or unknown("invalid level")
                if maxHP>0 and hp<=maxHP then
                    row.hp=verified(hp,"BattlePokemon.hp"); row.maxHP=verified(maxHP,"BattlePokemon.maxHP")
                else row.hp=unknown("invalid HP pair"); row.maxHP=unknown("invalid HP pair") end
                row.ability=resolver.resolve("abilities",r("ability"))
                row.abilityName=unknown("contextual dynamic ability name unproved")
                row.heldItem=resolver.resolve("items",r("item"))
                for _,name in ipairs({"type1","type2","type3"}) do row[name]=resolver.resolve("types",r(name)) end
                local status=r("status1")
                local low,counter=status%256,math.floor(status/256)
                local label
                if status==0 then label="NONE"
                elseif low>=1 and low<=7 and counter==0 then label="SLEEP"
                elseif low==constants.STATUS1_TOXIC_POISON and counter<=15 then label="TOXIC_POISON"
                elseif counter==0 then label=({[8]="POISON",[16]="BURN",[32]="FROSTBITE",[64]="PARALYSIS"})[low] end
                row.status1=label and verified({raw=status,primary=label,absent=status==0},"CFRU STATUS1; locked FROSTBITE")
                    or unknown("invalid/conflicting primary status")
                -- Bit 7 has no STATUS2 declaration. Other bits are opaque, not interpreted.
                local status2=r("status2")
                row.status2=math.floor(status2/128)%2==0 and verified(status2,"BattlePokemon.status2 opaque u32")
                    or unknown("undeclared secondary status bit")
                row.status2Meaning=unavailable("secondary status semantics intentionally unsupported")
                for m=1,4 do
                    local move=resolver.resolve("moves",r("moves",2*(m-1)))
                    local pp=r("pp",m-1)
                    local cap=block(sample.ppCaps,16) and read(sample.ppCaps,i*4+m-1,1) or nil
                    row.moves[m].identity=move
                    row.moves[m].pp=move.confidence=="VERIFIED" and cap and pp<=cap
                        and ((move.value.absent and cap==0 and pp==0) or (not move.value.absent and cap>0))
                        and verified(pp,"BattlePokemon.pp; explicit same-epoch synthetic effective cap")
                        or unknown("missing effective PP cap / invalid PP or move")
                    row.moves[m].effective=unknown("randomized move data/semantics unproved")
                end
            else
                row.species=identity.value and identity.value.absent and unknown("no active species") or identity
                -- Unknown/unsupported species and eggs suppress every dependent active field.
                if math.floor(read(sample.battleMons,i*SIZE+23,1)/64)%2==1 then row.species=unavailable("battle egg unsupported") end
            end
        end
        for i=3,4 do current.battlers[i]=blankRow("UNAVAILABLE","inactive single slot") end
        return decoder.snapshot()
    end
    return decoder
end
return M
