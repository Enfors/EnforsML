#!/bin/sh

test_files="text/ngram.py text/bagofwords.py text/word.py text/utils.py"

for test_file in $test_files; do
    echo "=== Running doctests in $test_file"
    python3 -m doctest $test_file
done

