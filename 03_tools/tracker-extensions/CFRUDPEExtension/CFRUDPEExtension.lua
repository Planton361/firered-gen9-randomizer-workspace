-- CFRU/DPE/Gen9 Ironmon Tracker extension skeleton.
--
-- Install locally by copying this file to the Tracker extension folder as:
--   Lua/extensions/CFRUDPEExtension.lua
-- and copying this directory's data folder next to it as:
--   Lua/extensions/data/
--
-- This skeleton does not modify Tracker core files, does not depend on
-- NatDexExtension, and does not read or write emulator memory by itself.
-- It prepares a manual CFRU/DPE profile path, reads committed source-data,
-- and loads local non-example manifests if the user provides them.

local EXT_KEY = "CFRUDPEExtension"

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
	description = "Manual CFRU/DPE/Gen9 profile skeleton for Ironmon Tracker. Loads only user-provided non-example manifests.",
	version = "0.1.0",
	extensionKey = EXT_KEY,
	state = {
		prepared = false,
		manifestsLoaded = false,
		sourceDataLoaded = false,
		lastLoadStatus = "not started",
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
	extension.state.sourceDataStatus = "source-data=unloaded"
	extension.state.lastLoadStatus = "unloaded"
	log("unloaded; no Tracker core overrides to restore")
end

function extension.afterProgramDataUpdate()
	-- Reserved for future lightweight party sanity checks after real manifests exist.
end

function extension.afterBattleDataUpdate()
	-- Reserved for future lightweight battle data checks after real manifests exist.
end

return extension
