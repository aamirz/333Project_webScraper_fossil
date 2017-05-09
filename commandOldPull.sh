# commandOldPull.sh 
# 
# Command the old pull for stuff in the daily Princetonian, over the file in command line arg.
# 
# Aamir Zainulabadeen
#

READ="./param_dates"
READ=$1

mkdir ./logs/old/
#echo $READ

while read p; do
DAYDIR=$(echo $p | cut -f1 -d' ')
DAY=$(echo $p | cut -f2 -d' ')

./oldPull.sh $DAYDIR $DAY > ./logs/old/"log_${DAYDIR}"
#echo "${DAYDIR} ${DAY}"

done < $READ
