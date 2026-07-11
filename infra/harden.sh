#!/bin/bash
# Durcissement de base 
sudo ufw allow OpenSSH
sudo ufw allow from 192.168.195.0/24
sudo ufw enable

sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
