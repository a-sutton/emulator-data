#!/bin/bash
data_file=monitoring_data.log
power_file=PMG_monitoring.log
time_now=$(date "+%Y-%m-%d--%H:%M:%S")
home=/home/asutton/emulator-data
demog=/u/black10/EMULATORS/DEMOGORGON/Maint
diff --brief <(sort $home/power/$power_file-latest.log) <(sort $demog/$power_file) >/dev/null
comp_value1=$?
if [ $comp_value1 -eq 1 ]
then 
	cp $home/power/$power_file-latest.txt $home/power/ARCHIVED-$time_now--$power_file.txt
	cp $demog/$power_file $home/power/$power_file-latest.txt
	cp $demog/$power_file $home/power/$power_file-latest.log
else
	:
fi
diff --brief <(sort $home/$data_file-latest.log) <(sort $demog/$data_file) >/dev/null
comp_value2=$?
if [ $comp_value2 -eq 1 ]
then
	cp $home/$data_file-latest.txt $home/ARCHIVED-$time_now--$data_file.txt
	cp $demog/$data_file $home/$data_file-latest.txt
	cp $demog/$data_file $home/$data_file-latest.log
else
	:
fi
