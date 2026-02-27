#!/bin/bash

ACCOUNTS="frontend-tests/accounts/bank_accounts.txt"
PROGRAM="front-end/source-code/bank_system.py"

INPUT_DIR="frontend-tests/input"
EXPECTED_DIR="frontend-tests/expected-output"
ACTUAL_DIR="frontend-tests/actual-output"

PASS_COUNT=0
FAIL_COUNT=0

echo "Running tests..."
echo "----------------------------"

for input_file in $(find "$INPUT_DIR" -name "*.txt"); do

    # Remove input base path
    relative_path=${input_file#$INPUT_DIR/}

    # Build output paths
    actual_atf="$ACTUAL_DIR/${relative_path%.txt}.atf"
    actual_out="$ACTUAL_DIR/${relative_path%.txt}.out"
    expected_file="$EXPECTED_DIR/$relative_path"

    # Create subdirectory inside actual-output if needed
    mkdir -p "$(dirname "$actual_atf")"

    # Run program
    python "$PROGRAM" "$ACCOUNTS" "$actual_atf" < "$input_file" > "$actual_out"

    # Compare transaction output with expected
    if diff -q "$actual_atf" "$expected_file" > /dev/null; then
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