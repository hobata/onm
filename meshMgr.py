#!/usr/bin/python2.7
# Start/Stop Wi-Fi mesh
#
import commands, sys
from time import sleep

meshIf = "mesh1"
meshId= "mesh_test"
meshAddr= "192.168.55."
w_s_conf = "./wpa_supplicant.conf"
ctrl_if="/var/run/wpa_supplicant"

def getNumAdp(sList):
  cnt = 0
  for line in sList:
    if not "wlan" in line:
      continue
    cnt += 1
  return cnt
 
def startMesh():
  print "start mesh"
  # stop network service
  commands.getoutput("service NetworkManager stop")
  commands.getoutput("killall wpa_supplicant")
  # get wlanIf dev name
  wlanIf = ""
  mac = ""
  str = commands.getoutput("ifconfig -a")
  sList = str.split("\n")
  print "get wlan name:%d" % (getNumAdp(sList)) 
  for line in sList:
    if not "wlan" in line:
      continue
    elem = line.split(" ")
    wlanIf = elem[0]
    elem = line.split(":")
    mac = elem[-1]
    break
  if len(wlanIf) < 5:
    print "Can not find wlan IF."
    sys.exit()
  #print "mac:%s" % (mac)
  lastAddr = int(mac, 16) | 0x7f # refer last byte of mac addr

  commands.getoutput("ifconfig %s down" % wlanIf)
  commands.getoutput("iw reg set JP")
  sleep(5)
  commands.getoutput("iw dev %s interface add %s type mp" % (wlanIf, meshIf))
  sleep(5)
  commands.getoutput("ifconfig %s down" % (wlanIf))
  commands.getoutput("ifconfig %s %s%d" % (meshIf, meshAddr, lastAddr))
  print commands.getoutput("ifconfig %s | head -n 2" % (meshIf))

  #commands.getoutput("ifconfig $s mesh join %s" % (meshIf, meshId))
  #test commands.getoutput("wpa_supplicant -d -Dnl80211 -i%s -c %s -B" % (meshIf, w_s_conf))
  sleep(10)
  print "mesh station dump"
  print commands.getoutput("iw dev %s station dump" % (meshIf))

def stopMesh():
  print "stop mesh"
  #commands.getoutput("wpa_cli -p %s -i%s \"terminate\"" % (w_s_conf, meshIf))
  commands.getoutput("iw dev %s del" % (meshIf))
  commands.getoutput("service NetworkManager start")

def print_help():
  print "This program needs one parameter."
  print "Usage:"
  print " python meshMgr.py <start/stop>"

# main
argvs = sys.argv  # list of command line
argc = len(argvs) # prameter number
if argc != 2:
  print_help()
  sys.exit()
cmd = argvs[1].lower()
if cmd == "start":
  startMesh()
elif cmd == "stop":
  stopMesh()
elif cmd == "restart":
  stopMesh()
  startMesh()
else:
  print "no action for the command \"%s\"" % (argvs[1])
print "finished."

