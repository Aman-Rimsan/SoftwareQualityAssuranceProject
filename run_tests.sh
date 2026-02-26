#!/bin/bash

ACCOUNTS="frontend-tests/accounts/bank_accounts.txt"
PROGRAM="front-end/source-code/bank_system.py"

PASS_COUNT=0
FAIL_COUNT=0

echo "Running tests..."
echo "----------------------------"

for input_file in $(find frontend-tests/input -name "*.txt"); do
    
    # Get matching expected output path
    relative_path=${input_file#frontend-tests/input/}
    expected_file="frontend-tests/expected-output/$relative_path"

    # Run program
    python "$PROGRAM" "$ACCOUNTS" test.atf < "$input_file"

    # Compare output
    if diff -q test.atf "$expected_file" > /dev/null; then
        echo "PASS: $relative_path"
        ((PASS_COUNT++))
    else
        echo "FAIL: $relative_path"
        ((FAIL_COUNT++))
    fi

done

echo "----------------------------"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"