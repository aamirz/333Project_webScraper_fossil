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

# # now make sure that we run for both today and yesterday
# TODAY="$(date "+%Y_%m_%d")"
# DAY="$(date "+%m/%d/%Y")"
# ./pullToday.sh $TODAY $DAY > ./logs/log_"${TODAY}"_$HOUR

# # for testing
# #echo "I love you" > ./data/logs/log_"${TODAY}"_$HOUR

# # run yesterday 
# TODAY="$(date -d "yesterday 13:00" "+%Y_%m_%d")"
# DAY="$(date -d "yesterday 13:00" "+%m/%d/%Y")"
# ./pullToday.sh $TODAY $DAY > ./logs/log_"${TODAY}"_$HOUR


# now run 19th Aril - 30 April
YEAR="2017"
MONTH="04"
# for daynum in {19..30}
# do
# TODAY="${YEAR}_${MONTH}_${daynum}"
# DAY="${MONTH}/${daynum}/${YEAR}"
# ./pullToday.sh $TODAY $DAY > ./logs/log_"${TODAY}"_$HOUR
# done

MONTH="05"
lowDays=("01" "02" "03" "04" "05" "06" "07" "08" "09")
# now pull for the month of may 
for daynum in ${lowDays[@]}
do 
TODAY="${YEAR}_${MONTH}_${daynum}"
DAY="${MONTH}/${daynum}/${YEAR}"
./pullToday.sh $TODAY $DAY > ./logs/log_"${TODAY}"_$HOUR
done

# now pull the beginning of may
MONTH="04"
for daynum in ${lowDays[@]}
do 
TODAY="${YEAR}_${MONTH}_${daynum}"
DAY="${MONTH}/${daynum}/${YEAR}"
./pullToday.sh $TODAY $DAY > ./logs/log_"${TODAY}"_$HOUR
done



exit 0
