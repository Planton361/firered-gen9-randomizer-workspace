-- CFRU/DPE/Gen9 Ironmon Tracker extension skeleton.
--
-- Install locally by copying this file to the Tracker extension folder as:
--   Lua/extensions/CFRUDPEExtension.lua
-- and copying this directory's data folder next to it as:
--   Lua/extensions/data/
--
-- This extension does not modify Tracker core files, does not depend on
-- NatDexExtension, and never writes emulator memory. It prepares a manual
-- CFRU/DPE profile path, reads committed source-data, loads local
-- non-example manifests if the user provides them, and owns a read-only
-- gBattleMons diagnostic reader.

local EXT_KEY = "CFRUDPEExtension"
local BATTLE_MON_SIZE = 0x58
local ACTIVE_BATTLE_SLOTS = {
	{ key = "playerLeft", label = "player-left", battlerIndex = 0 },
	{ key = "opponentLeft", label = "opponent-left", battlerIndex = 1 },
}
local BATTLE_MON_OFFSETS = {
	species = 0x00,
	moves = 0x0C,
	ability = 0x20,
	pp = 0x24,
	hp = 0x28,
	level = 0x2A,
	maxHP = 0x2C,
	item = 0x2E,
}

local function getSlash()
	if FileManager ~= nil and FileManager.slash ~= nil then
		return FileManager.slash
	end
	return "/"
end

local function joinPath(...)
	local slash = getSlash()
	local parts = {...}
	local path = ""
	for _, part in ipairs(parts) do
		if part ~= nil and part ~= "" then
			part = tostring(part)
			if path == "" then
				path = part
			else
				if string.sub(path, -1) ~= slash then
					path = path .. slash
				end
				path = path .. part
			end
		end
	end
	return path
end

local function normalizeSeparators(path)
	if path == nil then
		return nil
	end
	return string.gsub(tostring(path), "[/\\]", getSlash())
end

local function dirname(filepath)
	filepath = string.gsub(tostring(filepath or ""), "\\", "/")
	if filepath == nil or filepath == "" then
		return nil
	end
	local directory = string.match(filepath, "^(.*)/[^/]*$")
	if directory ~= nil and directory ~= "" then
		return normalizeSeparators(directory)
	end
	return nil
end

local function getLoadedFileDirectory()
	if debug == nil or type(debug.getinfo) ~= "function" then
		return nil
	end
	local info = debug.getinfo(1, "S")
	local source = info and info.source
	if type(source) ~= "string" or string.sub(source, 1, 1) ~= "@" then
		return nil
	end
	return dirname(string.sub(source, 2))
end

local function log(message)
	if print ~= nil then
		print(string.format("> %s: %s", EXT_KEY, message or ""))
	end
end

local function fileExists(filepath)
	if filepath == nil or filepath == "" then
		return false
	end
	if FileManager ~= nil and type(FileManager.fileExists) == "function" then
		return FileManager.fileExists(filepath)
	end
	local handle = io.open(filepath, "r")
	if handle ~= nil then
		handle:close()
		return true
	end
	return false
end

local extension = {
	name = "CFRU/DPE Gen9 Tracker Extension",
	author = "firered-gen9-randomizer-workspace",
	description = "Manual CFRU/DPE/Gen9 profile extension for Ironmon Tracker. Loads local manifests and reads gBattleMons diagnostics.",
	version = "0.1.0",
	extensionKey = EXT_KEY,
	state = {
		prepared = false,
		manifestsLoaded = false,
		sourceDataLoaded = false,
		lastLoadStatus = "not started",
		activeBattleMons = {},
		activeBattleStatus = "active-battle=not checked",
		activeBattleSnapshot = nil,
	},
}

extension.ManifestFiles = {
	sourceData = "source-data.json",
	gameAddresses = "game-addresses.local.json",
	trackerOverrides = "tracker-overrides.local.json",
}

function extension.getExtensionRoot()
	local loadedFileDirectory = getLoadedFileDirectory()
	if loadedFileDirectory ~= nil then
		return loadedFileDirectory
	end
	if FileManager ~= nil and type(FileManager.getExtensionsFolderPath) == "function" then
		return FileManager.getExtensionsFolderPath()
	end
	return "."
end

function extension.getDataRoot()
	return joinPath(extension.getExtensionRoot(), "data")
end

function extension.getManifestPaths()
	local dataRoot = extension.getDataRoot()
	return {
		sourceData = joinPath(dataRoot, extension.ManifestFiles.sourceData),
		gameAddresses = joinPath(dataRoot, extension.ManifestFiles.gameAddresses),
		trackerOverrides = joinPath(dataRoot, extension.ManifestFiles.trackerOverrides),
	}
end

function extension.prepareManualProfile()
	extension.state.prepared = true
	extension.state.manifestPaths = extension.getManifestPaths()
	return extension.state.manifestPaths
end

local function decodeJson(filepath)
	if filepath == nil or filepath == "" then
		return nil
	end
	if FileManager ~= nil and type(FileManager.decodeJsonFile) == "function" then
		return FileManager.decodeJsonFile(filepath)
	end
	return nil
end

local function getCountValue(sourceData, key)
	local countInfo = sourceData
		and sourceData.counts
		and sourceData.counts[key]
	if type(countInfo) == "table" then
		return countInfo.value
	end
	return nil
end

local function isArray(value)
	return type(value) == "table" and value[1] ~= nil
end

local function buildIdLookup(entries)
	local lookup = {}
	if type(entries) ~= "table" then
		return lookup
	end

	if isArray(entries) then
		for _, entry in ipairs(entries) do
			if type(entry) == "table" and type(entry.id) == "number" then
				lookup[entry.id] = entry.name or entry.constant or tostring(entry.id)
			end
		end
	else
		for key, entry in pairs(entries) do
			local id = tonumber(key)
			if type(entry) == "table" then
				id = tonumber(entry.id) or id
				if id ~= nil then
					lookup[id] = entry.name or entry.constant or tostring(id)
				end
			elseif id ~= nil then
				lookup[id] = tostring(entry)
			end
		end
	end

	return lookup
end

function extension.buildSourceLookups()
	local sourceData = extension.state.sourceData or {}
	extension.state.sourceLookups = {
		species = buildIdLookup(sourceData.species),
		moves = buildIdLookup(sourceData.moves),
		abilities = buildIdLookup(sourceData.abilities),
		items = buildIdLookup(sourceData.items),
	}
end

local function getDisplayName(section, id)
	if id == nil then
		return nil
	end
	local lookups = extension.state.sourceLookups or {}
	local sectionLookup = lookups[section] or {}
	return sectionLookup[id]
end

local function resolveId(section, id)
	return {
		id = id,
		name = getDisplayName(section, id),
	}
end

local function getConfiguredAddress(key)
	if GameSettings == nil then
		return nil
	end
	local value = GameSettings[key]
	if type(value) == "number" then
		return value
	end
	return nil
end

local function safeRead(reader, address)
	if Memory == nil or type(reader) ~= "function" or type(address) ~= "number" then
		return nil
	end

	local ok, value = pcall(reader, address)
	if ok and type(value) == "number" then
		return value
	end
	return nil
end

local function readU8(address)
	if Memory == nil then
		return nil
	end
	return safeRead(Memory.readbyte, address)
end

local function readU16(address)
	if Memory == nil then
		return nil
	end
	return safeRead(Memory.readword, address)
end

local function setActiveBattleStatus(status)
	extension.state.activeBattleStatus = status
	if extension.state.lastActiveBattleStatus ~= status then
		extension.state.lastActiveBattleStatus = status
		log(status)
	end
end

local function getResolvedName(resolved)
	if type(resolved) ~= "table" then
		return "?"
	end
	return tostring(resolved.name or resolved.id or "?")
end

local function formatMove(move)
	if type(move) ~= "table" or move.id == nil or move.id == 0 then
		return "-"
	end
	local name = move.name or ("move#" .. tostring(move.id))
	local pp = move.pp
	if pp == nil then
		return name
	end
	return string.format("%s(%s)", name, tostring(pp))
end

local function formatMoves(moves)
	local formatted = {}
	for moveIndex = 1, 4 do
		table.insert(formatted, formatMove(moves and moves[moveIndex]))
	end
	return table.concat(formatted, "/")
end

local function formatBattleMonSummary(mon, label)
	if type(mon) ~= "table" or not mon.valid then
		return string.format("%s:-", label)
	end
	return string.format(
		"%s:%s L%s HP %s/%s moves[%s]",
		label,
		getResolvedName(mon.species),
		tostring(mon.level or "?"),
		tostring(mon.hp or "?"),
		tostring(mon.maxHP or "?"),
		formatMoves(mon.moves)
	)
end

local function isPlausibleBattleMon(mon)
	local speciesCount = getCountValue(extension.state.sourceData, "species")
	return mon.species.id ~= nil
		and mon.species.id > 0
		and (type(speciesCount) ~= "number" or mon.species.id < speciesCount)
		and mon.level ~= nil
		and mon.level > 0
		and mon.level <= 100
		and mon.maxHP ~= nil
		and mon.maxHP > 0
end

function extension.readBattleMon(baseAddress, slotInfo)
	local moves = {}
	for moveIndex = 0, 3 do
		local moveId = readU16(baseAddress + BATTLE_MON_OFFSETS.moves + (moveIndex * 2))
		local pp = readU8(baseAddress + BATTLE_MON_OFFSETS.pp + moveIndex)
		table.insert(moves, {
			slot = moveIndex + 1,
			id = moveId,
			name = getDisplayName("moves", moveId),
			pp = pp,
		})
	end

	local speciesId = readU16(baseAddress + BATTLE_MON_OFFSETS.species)
	local abilityId = readU8(baseAddress + BATTLE_MON_OFFSETS.ability)
	local itemId = readU16(baseAddress + BATTLE_MON_OFFSETS.item)
	local mon = {
		slot = slotInfo.label,
		key = slotInfo.key,
		battlerIndex = slotInfo.battlerIndex,
		species = resolveId("species", speciesId),
		level = readU8(baseAddress + BATTLE_MON_OFFSETS.level),
		hp = readU16(baseAddress + BATTLE_MON_OFFSETS.hp),
		maxHP = readU16(baseAddress + BATTLE_MON_OFFSETS.maxHP),
		moves = moves,
		pp = {
			moves[1].pp,
			moves[2].pp,
			moves[3].pp,
			moves[4].pp,
		},
		ability = resolveId("abilities", abilityId),
		heldItem = resolveId("items", itemId),
	}
	mon.valid = isPlausibleBattleMon(mon)
	return mon
end

function extension.formatActiveBattleMons(activeBattleMons)
	activeBattleMons = activeBattleMons or extension.state.activeBattleMons or {}
	return string.format(
		"active-battle=snapshot %s | %s",
		formatBattleMonSummary(activeBattleMons.playerLeft, "P"),
		formatBattleMonSummary(activeBattleMons.opponentLeft, "E")
	)
end

function extension.logActiveBattleSnapshot(activeBattleMons)
	local snapshot = extension.formatActiveBattleMons(activeBattleMons)
	extension.state.activeBattleSnapshot = snapshot
	if extension.state.lastActiveBattleSnapshot ~= snapshot then
		extension.state.lastActiveBattleSnapshot = snapshot
		log(snapshot)
	end
end

function extension.readActiveBattleMons()
	if not extension.state.sourceDataLoaded then
		extension.state.activeBattleMons = {}
		extension.state.activeBattleSnapshot = nil
		extension.state.lastActiveBattleSnapshot = nil
		setActiveBattleStatus("active-battle=source-data missing")
		return false
	end

	local battleMonsAddress = getConfiguredAddress("gBattleMons")
	if battleMonsAddress == nil then
		extension.state.activeBattleMons = {}
		extension.state.activeBattleSnapshot = nil
		extension.state.lastActiveBattleSnapshot = nil
		setActiveBattleStatus("active-battle=missing gBattleMons")
		return false
	end
	if Memory == nil or type(Memory.readbyte) ~= "function" or type(Memory.readword) ~= "function" then
		extension.state.activeBattleMons = {}
		extension.state.activeBattleSnapshot = nil
		extension.state.lastActiveBattleSnapshot = nil
		setActiveBattleStatus("active-battle=memory reader unavailable")
		return false
	end

	local battlersCountAddress = getConfiguredAddress("gBattlersCount")
	if battlersCountAddress ~= nil then
		local battlersCount = readU8(battlersCountAddress)
		if battlersCount ~= nil and battlersCount < 2 then
			extension.state.activeBattleMons = {}
			extension.state.activeBattleSnapshot = nil
			extension.state.lastActiveBattleSnapshot = nil
			setActiveBattleStatus(string.format("active-battle=waiting battlers=%s", tostring(battlersCount)))
			return false
		end
	end

	local active = {}
	local validRows = 0
	for _, slotInfo in ipairs(ACTIVE_BATTLE_SLOTS) do
		local rowAddress = battleMonsAddress + (slotInfo.battlerIndex * BATTLE_MON_SIZE)
		local mon = extension.readBattleMon(rowAddress, slotInfo)
		active[slotInfo.key] = mon
		if mon.valid then
			validRows = validRows + 1
		end
	end

	extension.state.activeBattleMons = active
	if validRows == 0 then
		extension.state.activeBattleSnapshot = nil
		extension.state.lastActiveBattleSnapshot = nil
		setActiveBattleStatus("active-battle=idle/no valid rows")
		return false
	end

	setActiveBattleStatus(string.format("active-battle=loaded rows=%d", validRows))
	extension.logActiveBattleSnapshot(active)
	return true
end

function extension.getActiveBattleMons()
	return extension.state.activeBattleMons or {}
end

function extension.loadSourceData()
	local paths = extension.prepareManualProfile()
	if not fileExists(paths.sourceData) then
		extension.state.sourceDataLoaded = false
		extension.state.sourceDataStatus = "source-data=missing"
		return false
	end

	local sourceData = decodeJson(paths.sourceData)
	if type(sourceData) ~= "table" or sourceData.counts == nil then
		extension.state.sourceDataLoaded = false
		extension.state.sourceDataStatus = "source-data=invalid"
		return false
	end

	extension.state.sourceData = sourceData
	extension.buildSourceLookups()
	extension.state.sourceDataLoaded = true
	extension.state.sourceDataStatus = string.format(
		"source-data=loaded species=%s moves=%s abilities=%s items=%s",
		tostring(getCountValue(sourceData, "species") or "?"),
		tostring(getCountValue(sourceData, "moves") or "?"),
		tostring(getCountValue(sourceData, "abilities") or "?"),
		tostring(getCountValue(sourceData, "items") or "?")
	)
	return true
end

local function safeLoad(label, filepath, loader)
	local ok = false
	local loaded = false
	if type(loader) ~= "function" then
		return false, string.format("%s=loader unavailable", label)
	end

	ok = xpcall(function()
		loaded = loader(filepath)
	end, function(errorMessage)
		if FileManager ~= nil and type(FileManager.logError) == "function" then
			FileManager.logError(errorMessage)
		else
			log(tostring(errorMessage))
		end
	end)

	if not ok then
		return false, string.format("%s=error", label)
	end
	return loaded == true, string.format("%s=%s", label, tostring(loaded == true))
end

function extension.loadConfiguredManifests()
	if TrackerAPI == nil then
		extension.state.lastLoadStatus = "TrackerAPI unavailable"
		return false
	end

	local paths = extension.prepareManualProfile()
	local loadedAny = false
	local messages = {}

	if fileExists(paths.gameAddresses) then
		local ok, message = safeLoad("game-addresses.local", paths.gameAddresses, TrackerAPI.loadGameSettingsFromJson)
		loadedAny = loadedAny or ok
		table.insert(messages, message)
	else
		table.insert(messages, "game-addresses.local=missing")
	end

	if fileExists(paths.trackerOverrides) then
		local ok, message = safeLoad("tracker-overrides.local", paths.trackerOverrides, TrackerAPI.loadTrackerOverridesFromJson)
		loadedAny = loadedAny or ok
		table.insert(messages, message)
	else
		table.insert(messages, "tracker-overrides.local=missing")
	end

	extension.state.manifestsLoaded = loadedAny
	extension.state.lastLoadStatus = table.concat(messages, ", ")
	return loadedAny
end

-- Runs before Tracker game data is loaded. Keep this intentionally light:
-- no core wrapping yet and no placeholder/example manifest loading.
function extension.beforeGameDataLoad()
	extension.prepareManualProfile()
	log("manual CFRU/DPE profile prepared; local manifests are data/game-addresses.local.json and data/tracker-overrides.local.json")
end

-- Runs when the extension is enabled. It reads committed source-data and
-- attempts to load only local *.local.json manifests, not the committed
-- *.example.json prototypes.
function extension.startup()
	extension.loadSourceData()
	log(extension.state.sourceDataStatus or "source-data=not checked")

	local loaded = extension.loadConfiguredManifests()
	if loaded then
		log("loaded local manifest files; " .. extension.state.lastLoadStatus)
	else
		log("no local manifest files loaded; " .. extension.state.lastLoadStatus)
	end
end

function extension.unload()
	extension.state.prepared = false
	extension.state.manifestsLoaded = false
	extension.state.sourceDataLoaded = false
	extension.state.sourceData = nil
	extension.state.sourceLookups = nil
	extension.state.sourceDataStatus = "source-data=unloaded"
	extension.state.lastLoadStatus = "unloaded"
	extension.state.activeBattleMons = {}
	extension.state.activeBattleStatus = "active-battle=unloaded"
	extension.state.activeBattleSnapshot = nil
	extension.state.lastActiveBattleStatus = nil
	extension.state.lastActiveBattleSnapshot = nil
	log("unloaded; no Tracker core overrides to restore")
end

function extension.afterProgramDataUpdate()
	extension.readActiveBattleMons()
end

function extension.afterBattleDataUpdate()
	-- Active battle reads are handled by afterProgramDataUpdate so this stays
	-- independent from stock battle detection.
end

return extension
