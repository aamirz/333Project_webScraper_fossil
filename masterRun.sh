# masterRun.sh
#
# Aamir Zainulabadeen
# 
# Feeds all webscraping utilities properly formatted arguments.
#
#

# launch shell
#!/bin/bash

# cron preamble
cd ~
cd prowler_webScraper/

# for log file index
HOUR="$(date "+%H")"

# now make sure that we run for both today and yesterday
TODAY="$(date "+%Y_%m_%d")"
DAY="$(date "+%m/%d/%Y")"
./pullToday.sh $TODAY $DAY > ./data/log_"${TODAY}"_$HOUR


# run yesterday 
TODAY="$(date -d "yesterday 13:00" "+%Y_%m_%d")"
DAY="$(date -d "yesterday 13:00" "+%m/%d/%Y")"
./pullToday.sh $TODAY $DAY > ./data/log_"${TODAY}"_$HOUR

exit 0
