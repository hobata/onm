#!/usr/bin/python2.7
# Start Wi-Fi mesh
#
import commands, sys
from time import sleep

meshIf = "mesh1"
bssId= "mesh_test"
meshAddr= "192.168.55."

# stop network service
commands.getoutput("service NetworkManager stop")
commands.getoutput("killall wpa_supplicant")
# get wlanId 
wlanId = ""
mac = ""
str = commands.getoutput("ifconfig -a")
sList = str.split("\n")
for line in sList:
  if not "wlan" in line:
    continue
  elem = line.split(" ")
  wlanId = elem[0]
  elem = line.split(":")
  mac = elem[-1]
  break
if len(wlanId) < 5:
  print "Can not find wlan IF."
  sys.exit()
print "mac:%s" % (mac)
lastAddr = int(mac, 16) # last byte of mac addr

commands.getoutput("ifconfig %s down" % wlanId)
commands.getoutput("iw reg set JP")
sleep(5)
commands.getoutput("iw dev %s interface add %s type mp" % (wlanId, meshIf))
sleep(5)
commands.getoutput("ifconfig %s down" % (wlanId))
commands.getoutput("ifconfig %s %s%d" % (meshIf, meshAddr, lastAddr))

