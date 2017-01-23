#!/bin/sh -x
# refer to https://github.com/o11s/open80211s/wiki/HOWTO

MESH_IFACE=mesh1
MESH_ID=mesh_test

# down
#iw dev $MESH_IFACE leave
iw $MESH_IFACE del 
service NetworkManager start

#ifconfig wlan0 up
# Sometimes: disconnect and connect wi-fi device
