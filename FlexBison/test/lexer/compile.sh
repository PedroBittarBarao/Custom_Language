#!/bin/bash

bison -d parser.y
flex lexer.l
clang -o lexer_test parser.tab.c lex.yy.c main.c -ll