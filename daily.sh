#!/bin/bash
# HOW TO RUN:
# chmod +x daily.sh
# ./daily.sh

frontend="front-end/source-code/bank_system.py"
accounts="front-end/source-code/accounts.txt"

backend="back-end/back_end.py"
old_master="back-end/old_master.txt"

trans1="trans1.txt"
trans2="trans2.txt"
trans3="trans3.txt"

merged="merged.txt"
new_master="new_master.txt"
new_current="new_current.txt"

python "$frontend" "$accounts" "$trans1"
python "$frontend" "$accounts" "$trans2"
python "$frontend" "$accounts" "$trans3"

sed '$d' "$trans1" > temp1.txt
sed '$d' "$trans2" > temp2.txt

cat temp1.txt temp2.txt "$trans3" > "$merged"

rm temp1.txt temp2.txt

python "$backend" "$old_master" "$merged" "$new_master" "$new_current"
