#!/bin/bash
camera=$(date +%Y-%m-%d)
crontab -l > $camera".text"
#echo new cron into cron file
        echo "*/1 * * * * sh /home/Aggregator/vehicleStop.sh" >> $camera".text"
        echo "@reboot sh /home/Aggregator/drivingTime.sh" >> $camera".text"
        echo "@reboot sh /home/Aggregator/driverIdelTime.sh" >> $camera".text"
