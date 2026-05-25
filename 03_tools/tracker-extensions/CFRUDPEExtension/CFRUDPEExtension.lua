-- CFRU/DPE/Gen9 Ironmon Tracker extension skeleton.
--
-- Install locally by copying this file to the Tracker Custom folder as:
--   Custom/CFRUDPEExtension.lua
-- and copying this directory's data folder to:
--   Custom/CFRUDPEExtension/data/
--
-- This skeleton does not modify Tracker core files, does not depend on
-- NatDexExtension, and does not read or write emulator memory by itself.
-- It only prepares a manual CFRU/DPE profile path and loads real manifests
-- if the user provides non-example JSON files.

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
		lastLoadStatus = "not started",
	},
}

extension.ManifestFiles = {
	gameAddresses = "game-addresses.json",
	trackerOverrides = "tracker-overrides.json",
}

function extension.getExtensionRoot()
	if FileManager ~= nil and type(FileManager.getExtensionsFolderPath) == "function" then
		return joinPath(FileManager.getExtensionsFolderPath(), EXT_KEY)
	end
	return EXT_KEY
end

function extension.getDataRoot()
	return joinPath(extension.getExtensionRoot(), "data")
end

function extension.getManifestPaths()
	local dataRoot = extension.getDataRoot()
	return {
		gameAddresses = joinPath(dataRoot, extension.ManifestFiles.gameAddresses),
		trackerOverrides = joinPath(dataRoot, extension.ManifestFiles.trackerOverrides),
	}
end

function extension.prepareManualProfile()
	extension.state.prepared = true
	extension.state.manifestPaths = extension.getManifestPaths()
	return extension.state.manifestPaths
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
		local ok = TrackerAPI.loadGameSettingsFromJson(paths.gameAddresses)
		loadedAny = loadedAny or ok
		table.insert(messages, string.format("game addresses=%s", tostring(ok)))
	else
		table.insert(messages, "game addresses=missing")
	end

	if fileExists(paths.trackerOverrides) then
		local ok = TrackerAPI.loadTrackerOverridesFromJson(paths.trackerOverrides)
		loadedAny = loadedAny or ok
		table.insert(messages, string.format("tracker overrides=%s", tostring(ok)))
	else
		table.insert(messages, "tracker overrides=missing")
	end

	extension.state.manifestsLoaded = loadedAny
	extension.state.lastLoadStatus = table.concat(messages, ", ")
	return loadedAny
end

-- Runs before Tracker game data is loaded. Keep this intentionally light:
-- no core wrapping yet and no placeholder/example manifest loading.
function extension.beforeGameDataLoad()
	extension.prepareManualProfile()
	log("manual CFRU/DPE profile prepared; provide data/game-addresses.json and data/tracker-overrides.json to load real values")
end

-- Runs when the extension is enabled. It attempts to load only real manifest
-- filenames, not the committed *.example.json prototypes.
function extension.startup()
	local loaded = extension.loadConfiguredManifests()
	if loaded then
		log("loaded configured manifest files")
	else
		log("no configured manifest files loaded; " .. extension.state.lastLoadStatus)
	end
end

function extension.unload()
	extension.state.prepared = false
	extension.state.manifestsLoaded = false
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
