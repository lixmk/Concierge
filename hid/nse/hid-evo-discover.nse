local comm = require "comm"
local nmap = require "nmap"
local shortport = require "shortport"
local stdnse = require "stdnse"
local string = require "string"
local table = require "table"

description = [[
Uses the discoveryd service on udp port 4070 to enumerate information from HID EVO Door Controllers.
]]

author = "Mike Kelly (@lixmk)"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"discovery", "safe"}

---
-- @usage
-- nmap -sU -p 4070 --script=hid-evo-discover
--
-- @output
-- PORT     STATE         SERVICE
-- 4070/udp open|filtered unknown
-- | hid-discoveryd-enum: 
-- |   MAC Address: 00:06:8E:XX:XX:XX
-- |   Host Name: EdgeEH400-001
-- |   Internal IP: 10.0.0.1
-- |   Device Type: EH400
-- |   Firmware Version: 3.5.1.1483
-- |_  Build Date: 07/02/2015
-- MAC Address: 00:06:8E:XX:XX:XX (HID)
---

portrule = shortport.portnumber(4070, "udp")

action = function(host, port)

  local socket = nmap.new_socket()
  local status, err = socket:connect(host, port)
  local status, err = socket:send('discover;013;')
  local status, data = socket:receive()
  local fld = stdnse.strsplit(";", data)
  local output = {}
  table.insert(output, stdnse.strjoin(" ", {"MAC Address:", fld[3]}))
  table.insert(output, stdnse.strjoin(" ", {"Host Name:", fld[4]}))
  table.insert(output, stdnse.strjoin(" ", {"Internal IP:", fld[5]}))
  table.insert(output, stdnse.strjoin(" ", {"Device Type:", fld[7]}))
  table.insert(output, stdnse.strjoin(" ", {"Firmware Version:", fld[8]}))
  table.insert(output, stdnse.strjoin(" ", {"Build Date:", fld[9]}))
  if string.match(fld[1], "discovered") then
    return stdnse.format_output(true, output)
  end
end
