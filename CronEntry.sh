#!/bin/bash
camera=$(date +%Y-%m-%d)
crontab -l > $camera".text"
#echo new cron into cron file
        echo "@reboot Date" >> $camera".text"
        echo "@reboot Testing &" >> $camera".text"
