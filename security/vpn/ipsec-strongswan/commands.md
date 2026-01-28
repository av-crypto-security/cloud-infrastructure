# Commands reference

This file contains key commands used to verify and
troubleshoot an IPSec VPN tunnel with strongSwan.

## Check IPSec tunnel status
sudo ipsec status

## Restart strongSwan service
sudo systemctl restart strongswan-starter

## Check strongSwan service status
systemctl status strongswan-starter

## View IPSec logs
sudo journalctl -u strongswan-starter

## Verify routing table
ip route

## Test connectivity over VPN
ping <remote_private_ip>
