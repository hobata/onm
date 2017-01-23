#!/bin/sh -x
# Wi-Fi mesh for WI-U2-300D
# refer to https://github.com/o11s/open80211s/wiki/HOWTO
# https://wireless.wiki.kernel.org/en/users/documentation/iw/vif

MESH_IFACE=mesh1
MESH_ID=mesh_test

service NetworkManager stop
killall wpa_supplicant

#rcnetwork stop
#killall wpa_supplicant

#iw list
#iw dev
ifconfig wlan0 down

iw reg set JP

sleep 5
iw dev wlan0 interface add $MESH_IFACE type mesh

sleep 5
ifconfig wlan0 down
ifconfig $MESH_IFACE 192.168.3.80
iw $MESH_IFACE mesh join $MESH_ID

sleep 5
# monitor
iw dev $MESH_IFACE station dump
iw dev $MESH_IFACE mpath dump
