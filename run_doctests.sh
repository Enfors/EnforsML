#!/bin/sh

test_files="enforsml/text/ngram.py \
enforsml/text/bagofwords.py \
enforsml/text/word.py \
enforsml/text/utils.py \
enforsml/text/nlp.py"

for test_file in $test_files; do
    echo "=== Running doctests in $test_file"
    python3 -m doctest $test_file
done

