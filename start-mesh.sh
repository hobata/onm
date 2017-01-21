#!/bin/sh -x
# refer to https://github.com/o11s/open80211s/wiki/HOWTO

MESH_IFACE=mesh1
MESH_ID=mesh_test

iw list
ifconfig wlan0 down

sleep 5
iw dev wlan0 interface add $MESH_IFACE type mp
ifconfig $MESH_IFACE
sleep 5
ifconfig $MESH_IFACE 192.168.3.80
# SIOCSIFFLAGS:resource busy but the interface has the adress
ifconfig $MESH_IFACE | grep inet

sleep 5
iw dev $MESH_IFACE mesh join $MESH_ID
# command failed: Operation not supported (-95)

sleep 5
# monitor
iw dev $MESH_IFACE station dump
iw dev $MESH_IFACE mpath dump
