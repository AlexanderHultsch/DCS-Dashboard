-- DCS-Dashboard export script: sends flight data and MPD text over UDP to the Python bridge.
-- Load it with this line at the end of Export.lua, after the DCS-BIOS line:
--   dofile(lfs.writedir() .. [[Scripts\DCS-Dashboard-Export.lua]])
-- PORT must match [export] port in config/config.toml.
-- Once per minute of model time it writes one "export timing" line to the DCS log (dcs.log, source DCS-Dashboard).

local PORT = 7790
local TIMING_INTERVAL = 60
local FLIGHT_INTERVAL = 0.1
local MPD_INTERVAL = 1.0
local MPD_FAST_INTERVAL = 0.25
local MPD_FAST = {[7] = true, [9] = true, [11] = true, [13] = true}

package.path = package.path .. ";.\\LuaSocket\\?.lua"
package.cpath = package.cpath .. ";.\\LuaSocket\\?.dll"
local socket = require("socket")

local udp = nil
local next_flight = 0
local next_mpd = 0
local next_mpd_fast = 0

local prev_start = LuaExportStart
local prev_stop = LuaExportStop
local prev_after = LuaExportAfterNextFrame

local M_TO_FT = 3.28084
local MS_TO_KT = 1.94384
local MS_TO_FPM = 196.85

-- A missing function, a nil value or a format error leaves the value out.
local function add(lines, name, fmt, get)
    local ok, text = pcall(function() return string.format(fmt, get()) end)
    if ok then
        lines[#lines + 1] = name .. "=" .. text
    end
end

local function flight_packet()
    local ok, self_data = pcall(LoGetSelfData)
    if not ok then self_data = nil end
    local ok2, engine = pcall(LoGetEngineInfo)
    if not ok2 then engine = nil end
    local ok3, panel = pcall(GetDevice, 0)
    if not ok3 then panel = nil end

    local lines = {}
    add(lines, "lat", "%.5f", function() return self_data.LatLongAlt.Lat end)
    add(lines, "lon", "%.5f", function() return self_data.LatLongAlt.Long end)
    add(lines, "alt", "%.0f", function() return self_data.LatLongAlt.Alt * M_TO_FT end)
    add(lines, "hdg", "%.1f", function() return math.deg(self_data.Heading) end)
    add(lines, "pitch", "%.1f", function() return math.deg(self_data.Pitch) end)
    add(lines, "bank", "%.1f", function() return math.deg(self_data.Bank) end)
    add(lines, "ias", "%.0f", function() return LoGetIndicatedAirSpeed() * MS_TO_KT end)
    add(lines, "tas", "%.0f", function() return LoGetTrueAirSpeed() * MS_TO_KT end)
    add(lines, "ralt", "%.0f", function() return LoGetAltitudeAboveGroundLevel() * M_TO_FT end)
    add(lines, "vs", "%.0f", function() return LoGetVerticalVelocity() * MS_TO_FPM end)
    add(lines, "g", "%.2f", function() return LoGetAccelerationUnits().y end)
    add(lines, "eng_rpm_l", "%.1f", function() return engine.RPM.left end)
    add(lines, "eng_rpm_r", "%.1f", function() return engine.RPM.right end)
    add(lines, "eng_temp_l", "%.0f", function() return engine.Temperature.left end)
    add(lines, "eng_temp_r", "%.0f", function() return engine.Temperature.right end)
    add(lines, "fuel_int", "%.3f", function() return engine.fuel_internal end)
    add(lines, "fuel_ext", "%.3f", function() return engine.fuel_external end)
    add(lines, "fuel_flow_l", "%.3f", function() return engine.FuelConsumption.left end)
    add(lines, "fuel_flow_r", "%.3f", function() return engine.FuelConsumption.right end)
    add(lines, "plt_cyc_pitch", "%.3f", function() return panel:get_argument_value(470) end)
    add(lines, "plt_cyc_roll", "%.3f", function() return panel:get_argument_value(471) end)
    add(lines, "plt_coll", "%.3f", function() return panel:get_argument_value(474) end)
    add(lines, "plt_pedals", "%.3f", function() return panel:get_argument_value(476) end)
    add(lines, "cpg_cyc_pitch", "%.3f", function() return panel:get_argument_value(472) end)
    add(lines, "cpg_cyc_roll", "%.3f", function() return panel:get_argument_value(473) end)
    add(lines, "cpg_coll", "%.3f", function() return panel:get_argument_value(475) end)
    add(lines, "cpg_pedals", "%.3f", function() return panel:get_argument_value(478) end)
    return table.concat(lines, "\n")
end

local function send(packet)
    if udp and packet ~= "" then
        udp:send(packet)
    end
end

local function send_indication(n)
    local ok, text = pcall(list_indication, n)
    if ok and type(text) == "string" and text ~= "" then
        send("ind" .. n .. "=" .. (text:gsub("\n", "\\n")))
    end
end

-- One packet per indication keeps each packet small.
local function send_mpd()
    for n = 0, 30 do
        if not MPD_FAST[n] then
            send_indication(n)
        end
    end
end

-- The four MPD indications are sent more often than the rest.
local function send_mpd_fast()
    for n in pairs(MPD_FAST) do
        send_indication(n)
    end
end

-- Without os.clock or log the timing stays off and the export works as before.
local timing_on = pcall(function() assert(os.clock() and log.write and log.INFO) end)
local timing_work = 0
local timing_busy = 0
local timing_max = 0
local timing_frames = 0
local timing_start = nil
local timing_last = nil

local function timing_reset(t)
    timing_work = 0
    timing_busy = 0
    timing_max = 0
    timing_frames = 0
    timing_start = t
end

local function timing_report(t)
    pcall(function()
        local elapsed = t - timing_start
        if elapsed > 0 then
            local per_second = timing_work * 1000 / elapsed
            log.write("DCS-Dashboard", log.INFO, string.format(
                "export timing: %.2f ms per second of model time (%.2f %% of one core's time), %d busy frames, max frame %.2f ms, %d frames, clock resolution about 1 ms",
                per_second, per_second / 10, timing_busy, timing_max * 1000, timing_frames))
        end
    end)
end

-- Called after the work of one frame; only frames that sent something count as busy.
local function timing_frame(t, started, busy)
    if not t then return end
    local cost = os.clock() - started
    timing_last = t
    timing_frames = timing_frames + 1
    if busy then
        timing_work = timing_work + cost
        timing_busy = timing_busy + 1
        if cost > timing_max then timing_max = cost end
    end
    if not timing_start then
        timing_start = t
    elseif t - timing_start >= TIMING_INTERVAL then
        timing_report(t)
        timing_reset(t)
    end
end

LuaExportStart = function()
    if prev_start then pcall(prev_start) end
    pcall(function()
        udp = socket.udp()
        udp:setpeername("127.0.0.1", PORT)
    end)
    next_flight = 0
    next_mpd = 0
    next_mpd_fast = 0
    timing_reset(nil)
    timing_last = nil
end

LuaExportAfterNextFrame = function()
    if prev_after then pcall(prev_after) end
    pcall(function()
        local t = LoGetModelTime()
        local started = timing_on and os.clock()
        local busy = false
        if t >= next_flight then
            next_flight = t + FLIGHT_INTERVAL
            send(flight_packet())
            busy = true
        end
        if t >= next_mpd then
            next_mpd = t + MPD_INTERVAL
            send_mpd()
            busy = true
        end
        if t >= next_mpd_fast then
            next_mpd_fast = t + MPD_FAST_INTERVAL
            send_mpd_fast()
            busy = true
        end
        if timing_on then pcall(timing_frame, t, started, busy) end
    end)
end

LuaExportStop = function()
    if prev_stop then pcall(prev_stop) end
    if timing_on and timing_start and timing_last and timing_last - timing_start >= 5 then
        timing_report(timing_last)
    end
    if udp then
        pcall(function() udp:close() end)
        udp = nil
    end
end
