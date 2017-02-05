#!/usr/bin/python2.7
# Start/Stop Wi-Fi mesh
#
import commands, sys
from time import sleep

meshIf = "mesh1"
bssId= "mesh_test"
meshAddr= "192.168.55."

def getNumAdp(sList):
  cnt = 0
  for line in sList:
    if not "wlan" in line:
      continue
    cnt += 1
  return cnt
 
def startSvc():
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
  print "mac:%s" % (mac)
  lastAddr = int(mac, 16) # last byte of mac addr

  commands.getoutput("ifconfig %s down" % wlanIf)
  commands.getoutput("iw reg set JP")
  sleep(5)
  commands.getoutput("iw dev %s interface add %s type mp" % (wlanIf, meshIf))
  sleep(5)
  commands.getoutput("ifconfig %s down" % (wlanIf))
  commands.getoutput("ifconfig %s %s%d" % (meshIf, meshAddr, lastAddr))
  print commands.getoutput("iw dev %s info" % (meshIf))

def stopSvc():
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
if argvs[1] == "start":
  startSvc()
elif argvs[1] == "stop":
  stopSvc()

