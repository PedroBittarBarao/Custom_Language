#!/bin/bash

# Compile the lexer and test program
flex lexer.l
bison -d parser.y

# Use clang or gcc for compiling based on the system
clang -o lexer_test parser.tab.c lex.yy.c main.c -ll

# Check if the compilation was successful
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

# Define the number of tests
NUM_TESTS=1

# Loop through each test case
for i in $(seq 1 $NUM_TESTS); do
    INPUT="files/test_input_$i.txt"
    EXPECTED="files/expected_output_$i.txt"
    OUTPUT="files/actual_output_$i.txt"

    # Run the lexer on the input file and capture the output
    ./lexer_test $INPUT > $OUTPUT

    # Ensure a newline at the end of the actual output and expected output
    echo >> $OUTPUT
    echo >> $EXPECTED

    # Remove extra blank lines and trim trailing newlines from both expected and actual outputs
    sed '/^$/d' $OUTPUT | sed '$!N;s/\n$//' > temp_output.txt
    sed '/^$/d' $EXPECTED | sed '$!N;s/\n$//' > temp_expected.txt

    # Filter out the "This is a simple lexer for the C language" line before comparison
    grep -v "This is a simple lexer for the C language" temp_output.txt > cleaned_output.txt
    grep -v "This is a simple lexer for the C language" temp_expected.txt > cleaned_expected.txt

    # Compare the actual output to the expected output
    if diff cleaned_expected.txt cleaned_output.txt; then
        echo "Test $i passed!"
    else
        echo "Test $i failed!"
        diff cleaned_expected.txt cleaned_output.txt
    fi

    # Optionally, clean up actual output
    rm $OUTPUT temp_output.txt temp_expected.txt cleaned_output.txt cleaned_expected.txt
done
