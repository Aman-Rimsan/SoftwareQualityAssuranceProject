#!/bin/bash

for input_file in $(find frontend-tests/input -name "*.txt"); do

    relative_path=${input_file#frontend-tests/input/}

    actual_out="frontend-tests/actual-output/${relative_path%.txt}.out"
    actual_atf="frontend-tests/actual-output/${relative_path%.txt}.atf"
    expected_out="frontend-tests/expected-output/${relative_path%.txt}.out"

    mkdir -p "$(dirname "$actual_out")"

    python "front-end/source-code/bank_system.py" "frontend-tests/accounts/bank_accounts.txt" "$actual_atf" < "$input_file" > "$actual_out"

    if diff -q "$actual_out" "$expected_out" > /dev/null; then
        echo "PASS: $relative_path"
    else
        echo "FAIL: $relative_path"
    fi

done