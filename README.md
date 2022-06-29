# Emulator Data Extraction and Logging
These files are used to extract data from comodel servers attached to Strato emulators and subsequently upload them to the Influxdb server for trending.

## Bash Script
The bash script is used in combination with a crontab to periodically check the log file in the comodel directory to see if it has changed (Strato machines do not log when a job is not running).
A crontab to check every ~5minutes to all script to detect changes in the log files. When change is detected, it will move the file to directory of choice (defaults to my personal network drive)

## Python Script
The Python script will take the log file (currently only power) data and parse it for timestamps and associated values, and subsequently upload the data to the Influxdb database.
