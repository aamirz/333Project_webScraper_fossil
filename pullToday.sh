# pullToday.sh
#
# Author: Aamir Zainulabadeen
#
#
# Pull today's contents for all publications. 
# Save them all to the data/ directory. Then removes all 
# the data after posting. 
#

# the path to this directory (for cron)
DIR="~/"

# get today's date 
TODAY="$(date "+%Y_%m_%d")"
DAY="$(date "+%m/%d/%Y")"
#DAY="04/13/2017"
#TODAY="2017_04_13"

# make the date directories for each publication 
for file in ./data/*
do 
# affix prefix to this for cron
mkdir "${file}/${TODAY}"
done

# grab all of today's articles
python getTodaysArticles.py "./data" $DAY

# post all of today's articles, generate a count
for file in ./data/*
do
# get the number of articles 
echo "${file}"
# remember to affix the prefix!
N="$(ls "${file}/${TODAY}/" | wc -l)"
echo $N
python princeToDB.py "./${file}/${TODAY}" $N $TODAY

# now remove the parent directory and all contents
rm -rf "./${file}/${TODAY}"
done


# success
exit 0
