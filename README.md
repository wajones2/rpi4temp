# rpi4temp

rpi4temp is a program that formats and stores temperature data from Raspberry Pi 4 running Linux. Using crontab, the temperature is taken every minute and written to a text file along with the current date and time, then formatted using Python and stored to a database via sqlite3.

# Crontab Configuration & Database

1.  Execute ```./config``` to generate the crontab configuration and database
2.  Copy the configuation from 'crontab_configuration.txt'
3.  Enter ```crontab -e``` in the command-line
4.  Paste the configuration at the bottom

Use ```python3 x2app.py``` to update the database.
