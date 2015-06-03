#!/bin/bash

for dir in "/opt/Logs_single" "/opt/iostat_single" "/opt/Logs_dual" "/opt/iostat_dual"; do
  if [ ! -d $dir ]; then
    mkdir $dir
  fi
done

sudo python fioMain.py workload/workload_numjobs.csv
mv Logs/* /opt/Logs_single
mv IOSTATs/* /opt/iostat_single

sudo python fioMain.py workload/workload_dualdevices.csv
mv Logs/* /opt/Logs_dual
mv IOSTATs/* /opt/iostat_dual

#sudo python fioMain.py workload/workload_quaddevices.csv 

