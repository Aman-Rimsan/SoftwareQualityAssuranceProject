#!/bin/bash

# Make scripts executable:
# chmod +x daily.sh weekly.sh

# Usage:
# ./daily.sh <day_number>
#
# Example:
# ./daily.sh 1
#
# Description:
# Runs 2 front-end sessions using input files for the given day,
# merges transactions, runs the back end, and updates accounts
# for the next day.


DAY=$1

echo "===== STARTING DAILY RUN (Day $DAY) ====="

# Clean old files
rm -f session_*.txt merged.txt back-end/new_master.txt back-end/new_current.txt

# ---------- SESSION 1 ----------
echo "Running Session 1..."
py front-end/source-code/bank_system.py front-end/source-code/accounts.txt session_1.txt < inputs/day${DAY}_session1.txt

# ---------- SESSION 2 ----------
echo "Running Session 2..."
py front-end/source-code/bank_system.py front-end/source-code/accounts.txt session_2.txt < inputs/day${DAY}_session2.txt

# ---------- MERGE ----------
echo "Merging transaction files..."
cat session_1.txt session_2.txt > merged.txt || { echo "Merge failed"; exit 1; }

# ---------- RUN BACKEND ----------
echo "Running Back End..."
py back-end/back_end.py back-end/old_master.txt merged.txt back-end/new_master.txt back-end/new_current.txt

# ---------- PREPARE MASTER ----------
echo "Preparing old master..."
cp back-end/new_master.txt back-end/old_master.txt

# ---------- UPDATE ----------
echo "Updating accounts.txt..."
cp back-end/new_current.txt front-end/source-code/accounts.txt

echo "===== DAILY RUN COMPLETE ====="