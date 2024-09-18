#include <stdio.h>
#include "../../parser.tab.h" 

extern int yylex();
extern char* yytext;
extern FILE* yyin;

int main(int argc, char** argv) {

    fprintf(stderr, "This is a simple lexer for the C language\n");

    if (argc < 2) {
        fprintf(stderr, "Usage: %s <input file>\n", argv[0]);
        return 1;
    }

    yyin = fopen(argv[1], "r");
    if (!yyin) {
        fprintf(stderr, "Error opening file: %s\n", argv[1]);
        return 1;
    }

    int token;
    while ((token = yylex())) {
        printf("Token: %d, Lexeme: %s\n", token, yytext);
    }

    fclose(yyin);
    return 0;
}
