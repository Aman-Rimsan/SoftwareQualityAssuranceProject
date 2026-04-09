#!/bin/bash
# HOW TO RUN:
# chmod +x weekly.sh
# ./weekly.sh

daily="./daily.sh"

accounts="front-end/source-code/accounts.txt"

for day in 1 2 3 4 5 6 7; do

    "$daily"
    
    cp new_current.txt "$accounts"

done
