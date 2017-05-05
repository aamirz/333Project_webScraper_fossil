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

# now make sure that we run for both today and yesterday
TODAY="$(date "+%Y_%m_%d")"
DAY="$(date "+%m/%d/%Y")"

#./pullToday.sh $TODAY $DAY
echo $TODAY

# run yesterday 
TODAY="$(date "yesterday 13:00" "+%Y_%m_%d")"
DAY="$(date "yesterday 13:00" "+%m/%d/%Y")"

echo $TODAY
#./pullToday.sh $TODAY $DAY

exit 0