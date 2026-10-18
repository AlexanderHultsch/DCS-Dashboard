-- Usage: lua5.1 gen_json.lua [OUTPUT_DIR]
-- Needs the environment variable DCSBIOS_REPO: a DCS-BIOS source checkout (the folder that contains Scripts/DCS-BIOS).
-- Writes MetadataStart, CommonData, A-10C and AH-64D JSON files into OUTPUT_DIR/Scripts/DCS-BIOS/doc/json
-- (default: logs/test/sg in the repo), a stand-in for the Saved Games folder.
local windows = package.config:sub(1, 1) == "\\"
local here = arg[0]:match("^(.*)[/\\][^/\\]*$") or "."
local repo = here .. "/../../.."

local bios_root = os.getenv("DCSBIOS_REPO")
if not bios_root or bios_root == "" then
	io.stderr:write("set DCSBIOS_REPO to a DCS-BIOS source checkout\n")
	os.exit(2)
end
bios_root = bios_root:gsub("[/\\]+$", ""):gsub("[/\\]Scripts[/\\]DCS%-BIOS$", "")

local sg = (arg[1] or (repo .. "/logs/test/sg")):gsub("[/\\]+$", "") .. "/"

local function mkdir(path)
	if windows then
		os.execute('mkdir "' .. path:gsub("/", "\\") .. '" 2> nul')
	else
		os.execute("mkdir -p '" .. path .. "'")
	end
end

mkdir(sg .. "Scripts/DCS-BIOS/doc/json")
mkdir(sg .. "Scripts/DCS-BIOS/doc/doc_assets")

package.path = bios_root .. "/?.lua;" .. package.path

lfs = { writedir = function() return sg end }

-- DCS globals the module files touch while loading (same as test/compile/DCS_API_mocks.lua)
require("Scripts.DCS-BIOS.test.compile.DCS_API_mocks")

local BIOSConfig = require("Scripts.DCS-BIOS.BIOSConfig")
BIOSConfig.dev_mode = true

local Protocol = require("Scripts.DCS-BIOS.lib.Protocol")
local CommonData = require("Scripts.DCS-BIOS.lib.modules.common_modules.CommonData")
local MetadataStart = require("Scripts.DCS-BIOS.lib.modules.common_modules.MetadataStart")

local modules = {
	MetadataStart,
	CommonData,
	require("Scripts.DCS-BIOS.lib.modules.aircraft_modules.A-10C"),
	require("Scripts.DCS-BIOS.lib.modules.aircraft_modules.AH-64D"),
}

for _, module in ipairs(modules) do
	Protocol.writeNewModule(module)
	print("wrote " .. module.name)
end
