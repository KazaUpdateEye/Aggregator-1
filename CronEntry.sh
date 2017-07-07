#!/bin/bash
camera=$(date +%Y-%m-%d)
crontab -l > $camera".txt"
#echo new cron into cron file
        echo "@reboot Date" >> $camera".txt"
        echo "@reboot Testing &" >> $camera".txt"
