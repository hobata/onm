#!/usr/bin/python2.7
# Start Wi-Fi mesh
#
import commands, time, sys

meshIf = "mesh1"
bssId= "mesh_test"
meshAddr= "192.168.55."

# stop network service
commands.getoutput("service NetworkManager stop")
commands.getoutput("killall wpa_supplicant")

# get wlanId 
wlanId = ""
str = commands.getoutput("ifconfig -a")
sList = str.split("\n")
for line in sList:
  mac = line[-2:]
  elem = line.split(" ")
  for s in elem:
    if "wlan" in s:
      wlanId = s
if len(wlanId) < 5:
  print "Can not find wlan IF."
  sys.exit()
lastAddr = int(mac, 16) # last byte of mac addr

commands.getoutput("ifconfig %s down" % wlanId)
commands.getoutput("iw reg set JP"
time.sleep(5)
commands.getoutput("iw dev %s interface add %s type mp" % (wlanId, meshIf)
time.sleep(5)
commands.getoutput("ifconfig %s down" % (wlanId))
commands.getoutput("ifconfig %s %s%d" % (meshIf, meshAddr, lastAddr))

