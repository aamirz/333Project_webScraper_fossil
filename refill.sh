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
./pullToday.sh $TODAY $DAY > ./logs/log_"${TODAY}"_$HOUR

# for testing
#echo "I love you" > ./data/logs/log_"${TODAY}"_$HOUR

# run yesterday 
TODAY="$(date -d "yesterday 13:00" "+%Y_%m_%d")"
DAY="$(date -d "yesterday 13:00" "+%m/%d/%Y")"
./pullToday.sh $TODAY $DAY > ./logs/log_"${TODAY}"_$HOUR

YEAR="2017"
MONTH="04"
for daynum in {19..30}
do
TODAY="${YEAR}_${MONTH}_${daynum}"
DAY="${MONTH}/${daynum}/${YEAR}"
#echo $TODAY
#echo $DAY
# TODAY="$(date -d "yesterday 13:00" "+%Y_%m_%d")"
# DAY="$(date -d "yesterday 13:00" "+%m/%d/%Y")"
./pullToday.sh $TODAY $DAY > ./logs/log_"${TODAY}"_$HOUR
done

exit 0
