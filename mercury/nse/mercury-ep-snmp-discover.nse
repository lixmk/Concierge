local nmap = require "nmap"
local shortport = require "shortport"
local snmp = require "snmp"
local string = require "string"
local stdnse = require "stdnse"

description = [[
Leverages SNMP to identify door controllers manufactured by, or using firmware from, Mercury Security.
]]

---
-- @usage
-- nmap -sU -p 161 --script=mercury-ep-snmp-discover.nse 10.0.0.1
--
-- @output
-- PORT    STATE SERVICE
161/udp open  snmp
-- | mercury-ep-snmp-discover:: 
-- |   Description: EP-1502 Configuration Manager
-- |   Device Type: EP-1502
-- |   Firmware Verison: 1.19.4
-- |_  Build Number: 415
---
author = "Mike Kelly (@lixmk)"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"default", "discovery", "safe"}
dependencies = {"snmp-brute"}

portrule = shortport.portnumber(161, "udp", {"open", "open|filtered"})

---
action = function(host, port)

  local snmpHelper = snmp.Helper:new(host, port)
  snmpHelper:connect()
  local status, sysdescr = snmpHelper:get({reqId=28428}, "1.3.6.1.2.1.1.1.0")
  if not status then
    return
  end
  nmap.set_port_state(host, port, "open")
  local status, devtype = snmpHelper:get({reqId=28428}, "1.3.6.1.2.1.1.5.0")
  description = stdnse.strsplit(";", string.gsub(string.gsub(sysdescr[1][1], " Firmware Version ", ";Firmware Verion;", 1), " Build ", ";Build;", 1))
  local output = {}
  table.insert(output, stdnse.strjoin(" ", {"Description:", description[1]}))
  table.insert(output, stdnse.strjoin(" ", {"Device Type:", devtype[1][1]}))
  table.insert(output, stdnse.strjoin(" ", {"Firmware Verison:", description[3]}))
  table.insert(output, stdnse.strjoin(" ", {"Build Number:", description[5]}))
  if string.match(sysdescr[1][1], "Firmware Version.*Build") then
    return stdnse.format_output(true, output)
  end
end
