#!/bin/bash
camera=$(date +%Y-%m-%d)
crontab -l > $camera".txt"
#echo new cron into cron file
        echo "*/1 * * * * sh /home/Aggregator/vehicleStop.sh" >> $camera".txt"
        echo "@reboot sh /home/Aggregator/drivingTime.sh" >> $camera".txt"
        echo "@reboot sh /home/Aggregator/driverIdelTime.sh" >> $camera".txt"
