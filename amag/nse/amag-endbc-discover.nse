local comm = require "comm"
local nmap = require "nmap"
local shortport = require "shortport"
local stdnse = require "stdnse"
local string = require "string"
local table = require "table"

description = [[
Uses AMAGs discovery service on udp port 49107 to enumerate information from AMAG EN series door controllers.
]]

author = "Mike Kelly (@lixmk)"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"discovery", "safe"}

---
-- @usage
-- nmap -sU -p 49107 --disable-arp-ping --script=amag-endbc-discover.nse 10.0.0.1
--
-- @output
--PORT      STATE         SERVICE
--49107/udp open|filtered unknown
--| amag-endbc-discover: 
--|   Device Type: AMAG EN-1DBC
--|_  Firmware Version: 03.60
--MAC Address: 00:15:BD:XX:XX:XX (Group 4 Technology)
---

portrule = shortport.portnumber(49107, "udp")

action = function(host, port)

  local socket = nmap.new_socket()
  local status, err = socket:bind("0.0.0.0", 49107)
  local status, err = socket:connect(host, port)
  local status, err = socket:send(stdnse.fromhex('000004b2ab9913de000001a000000000bddf3c00000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
  local status, data = socket:receive()
  local clean = string.gsub(string.gsub(string.gsub(string.gsub(data, "%.", "ZZZZ"), "(%W+)", ";"), "ZZZZ", "."), "^%z+%.", "")
  local output = {}
  if string.match(data, "1DBC") then
    local fld = stdnse.strsplit(";", string.gsub(clean, "^.*;h;", "", 1))
    table.insert(output, stdnse.strjoin("-", {"Device Type: AMAG EN", fld[3]}))
    table.insert(output, stdnse.strjoin(" ", {"Firmware Version:", fld[2]}))
    return stdnse.format_output(true, output)
  end
  if string.match(data, "2DBC") then
    local fld = stdnse.strsplit(";", string.gsub(clean, "^.*UUUU;", "", 1))
    table.insert(output, stdnse.strjoin("-", {"Device Type: AMAG EN-1DBC+ or EN", fld[3]}))
    table.insert(output, stdnse.strjoin(" ", {"Firmware Version:", fld[2]}))
    return stdnse.format_output(true, output)
  end
end
