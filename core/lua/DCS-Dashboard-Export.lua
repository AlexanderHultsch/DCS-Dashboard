-- DCS-Dashboard export script: sends the control positions and the MPD text over UDP to the Python bridge.
-- Load it with this line at the end of Export.lua, after the DCS-BIOS line:
--   dofile(lfs.writedir() .. [[Scripts\DCS-Dashboard-Export.lua]])
-- PORT must match [export] port in config/config.toml.

local PORT = 7790
local CONTROLS_INTERVAL = 0.1
local MPD_INTERVAL = 0.25
-- list_indication numbers of the MPDs: pilot left and right, CP/G left and right
local MPD_INDICATIONS = {7, 9, 11, 13}
-- export name and cockpit argument of each control position
local CONTROLS = {
    {"plt_cyc_pitch", 470}, {"plt_cyc_roll", 471}, {"plt_coll", 474}, {"plt_pedals", 476},
    {"cpg_cyc_pitch", 472}, {"cpg_cyc_roll", 473}, {"cpg_coll", 475}, {"cpg_pedals", 478},
}

package.path = package.path .. ";.\\LuaSocket\\?.lua"
package.cpath = package.cpath .. ";.\\LuaSocket\\?.dll"
local socket = require("socket")

local udp = nil
local next_controls = 0
local next_mpd = 0

local prev_start = LuaExportStart
local prev_stop = LuaExportStop
local prev_after = LuaExportAfterNextFrame

local function send(packet)
    if udp and packet ~= "" then
        udp:send(packet)
    end
end

-- A missing device or argument leaves the value out.
local function controls_packet()
    local ok, panel = pcall(GetDevice, 0)
    if not ok or not panel then return "" end
    local lines = {}
    for _, control in ipairs(CONTROLS) do
        local ok2, text = pcall(function() return string.format("%.3f", panel:get_argument_value(control[2])) end)
        if ok2 then
            lines[#lines + 1] = control[1] .. "=" .. text
        end
    end
    return table.concat(lines, "\n")
end

-- One packet per indication keeps each packet small.
local function send_mpd()
    for _, n in ipairs(MPD_INDICATIONS) do
        local ok, text = pcall(list_indication, n)
        if ok and type(text) == "string" and text ~= "" then
            send("ind" .. n .. "=" .. (text:gsub("\n", "\\n")))
        end
    end
end

LuaExportStart = function()
    if prev_start then pcall(prev_start) end
    pcall(function()
        udp = socket.udp()
        udp:setpeername("127.0.0.1", PORT)
    end)
    next_controls = 0
    next_mpd = 0
end

LuaExportAfterNextFrame = function()
    if prev_after then pcall(prev_after) end
    pcall(function()
        local t = LoGetModelTime()
        if t >= next_controls then
            next_controls = t + CONTROLS_INTERVAL
            send(controls_packet())
        end
        if t >= next_mpd then
            next_mpd = t + MPD_INTERVAL
            send_mpd()
        end
    end)
end

LuaExportStop = function()
    if prev_stop then pcall(prev_stop) end
    if udp then
        pcall(function() udp:close() end)
        udp = nil
    end
end
