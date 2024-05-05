%{
#include "parser.tab.h"
#include <stdlib.h>
%}

%%

"int"       { return INT_TYPE; }
"string"    { return STRING_TYPE; }
"print"     { return PRINT; }
"while"     { return WHILE; }
"if"        { return IF; }
"else"      { return ELSE; }
"switch"    { return SWITCH; }
"case"      { return CASE; }
"default"   { return DEFAULT; }
"=="        { return EQ_OP; }
">"         { return GT_OP; }
"{"        { return OPEN_BRC; }
"}"        { return CLOSE_BRC; }
"("        { return OPEN_PAR; }
")"        { return CLOSE_PAR; }  
"<"         { return LT_OP; }
"or"        { return OR; }
"and"       { return AND; }
"+"         { return ADD_OP; }
"-"         { return SUB_OP; }
"*"         { return MUL_OP; }
"/"         { return DIV_OP; }
"="         { return ASSIGN; }
[0-9]+      { yylval.num = atoi(yytext); return NUMBER; }
[a-zA-Z_][a-zA-Z0-9_]*  { yylval.str = strdup(yytext); return IDENTIFIER; }
\"([^"\\]|\\.)*\"       { /* Match strings */
                            /* Remove quotes and escape sequences */
                            yylval.str = malloc(strlen(yytext) - 1); /* -2 for removing quotes */
                            strncpy(yylval.str, yytext + 1, strlen(yytext) - 2); /* Copy without quotes */
                            yylval.str[strlen(yytext) - 2] = '\0'; /* Null-terminate */
                            return STRING;
                        }
[ \t]       ; /* Skip whitespace */
.           { fprintf(stderr, "Invalid character: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}
