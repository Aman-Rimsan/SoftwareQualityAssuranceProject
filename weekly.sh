#!/bin/bash

# Make scripts executable:
# chmod +x daily.sh weekly.sh

# Usage:
# ./weekly.sh
#
# Description:
# Runs the daily script 7 times (Day 1 to Day 7),
# simulating a full week of banking operations.
# Each day uses updated account files from the previous day.


echo "===== STARTING WEEKLY RUN ====="

for DAY in {1..7}
do
    echo "===== DAY $DAY ====="
    ./daily.sh $DAY
done

echo "===== WEEKLY RUN COMPLETE ====="