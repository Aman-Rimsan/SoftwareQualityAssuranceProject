#!/bin/bash

for input_file in $(find frontend-tests/input -name "*.txt"); do

    relative_path=${input_file#frontend-tests/input/}

    actual="frontend-tests/actual-output/${relative_path%.txt}.atf"
    expected="frontend-tests/expected-output/${relative_path%.txt}.txt"

    mkdir -p "$(dirname "$actual")"

    python "front-end/source-code/bank_system.py" "frontend-tests/accounts/bank_accounts.txt" "$actual" < "$input_file" > /dev/null

    if diff -q "$actual" "$expected" > /dev/null; then
        echo "PASS: $relative_path"
    else
        echo "FAIL: $relative_path"
    fi

done