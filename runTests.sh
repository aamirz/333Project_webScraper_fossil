#!/bin/bash
py=python
#pyENVOP=PYTHONIOENCODING=UTF-8
# set the encoding for this bash session
PYTHONIOENCODING=UTF-8
export PYTHONIOENCODING

# run our tests
$py scrapePrince.py > test01

