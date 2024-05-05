%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%union {
    int num;
    char* str;
}


%token INT_TYPE STRING_TYPE PRINT WHILE IF ELSE SWITCH CASE READ OPEN_PAR CLOSE_PAR OPEN_BRC CLOSE_BRC
%token OR AND EQ_OP GT_OP LT_OP ADD_OP SUB_OP MUL_OP DIV_OP NOT ASSIGN DEFAULT
%token <num> NUMBER
%token <str> IDENTIFIER STRING

%%

program: BLOCK { printf("Program parsed successfully.\n"); }
       ;



BLOCK: statement_list  { printf("Block parsed.\n"); }
     ;

statement_list: /* empty */
              | statement_list STATEMENT { printf("Statement parsed.\n"); }
              ;

STATEMENT: '\n'
         | INT_TYPE IDENTIFIER { printf("Declaration statement parsed.\n"); }
         | STRING_TYPE IDENTIFIER { printf("Declaration statement parsed.\n"); }
         | STRING_TYPE IDENTIFIER ASSIGN STRING { printf("Declaration statement parsed.\n"); }
         | IDENTIFIER ASSIGN BOOL_EXP { printf("Assignment statement parsed.\n"); }
         | IDENTIFIER ASSIGN STRING { printf("Assignment statement parsed.\n"); }
         | INT_TYPE IDENTIFIER ASSIGN BOOL_EXP { printf("Declaration statement parsed.\n"); }   
         | PRINT OPEN_PAR BOOL_EXP CLOSE_PAR { printf("Print statement parsed.\n"); }
         | WHILE BOOL_EXP empty_space OPEN_BRC  statement_list CLOSE_BRC { printf("While statement parsed.\n"); }
         | IF BOOL_EXP empty_space OPEN_BRC  statement_list CLOSE_BRC else_block { printf("If-else statement parsed.\n"); }
         | SWITCH IDENTIFIER empty_space OPEN_PAR case_list CLOSE_PAR { printf("Switch statement parsed.\n"); }
         ;


case_list: /* empty */
         | empty_space
         | case_list CASE STRING empty_space OPEN_BRC statement_list CLOSE_BRC { printf("Case parsed.\n"); }
         | case_list CASE NUMBER empty_space OPEN_BRC statement_list CLOSE_BRC { printf("Case parsed.\n"); }
         | case_list DEFAULT empty_space OPEN_BRC statement_list CLOSE_BRC { printf("Default case parsed.\n"); }

         ;

else_block: /* empty */
          | ELSE empty_space OPEN_BRC statement_list CLOSE_BRC { printf("Else block parsed.\n"); }
          ;

empty_space:
           | '\n' { printf("Empty space parsed.\n"); }
           | empty_space '\n' { printf("Empty space parsed.\n"); }
           ;

BOOL_EXP: BOOL_TERM { printf("Boolean expression parsed.\n"); }
        | BOOL_EXP OR BOOL_TERM { printf("Boolean expression parsed.\n"); }
        ;

BOOL_TERM: REL_EXP { printf("Boolean term parsed.\n"); }
         | BOOL_TERM AND REL_EXP { printf("Boolean term parsed.\n"); }
         ;

REL_EXP: EXPRESSION { printf("Relational expression parsed.\n"); }
       | EXPRESSION EQ_OP EXPRESSION { printf("Relational expression parsed.\n"); }
       | EXPRESSION GT_OP EXPRESSION { printf("Relational expression parsed.\n"); }
       | EXPRESSION LT_OP EXPRESSION { printf("Relational expression parsed.\n"); }
       ;

EXPRESSION: TERM { printf("Expression parsed.\n"); }
          | EXPRESSION ADD_OP TERM { printf("Expression parsed.\n"); }
          | EXPRESSION SUB_OP TERM { printf("Expression parsed.\n"); }
          ;

TERM: FACTOR { printf("Term parsed.\n"); }
     | TERM MUL_OP FACTOR { printf("Term parsed.\n"); }
     | TERM DIV_OP FACTOR { printf("Term parsed.\n"); }
     ;

FACTOR: NUMBER { printf("Factor parsed.\n"); }
       | STRING { printf("Factor parsed.\n"); }
       | IDENTIFIER { printf("Factor parsed.\n"); }
       | '+' FACTOR { printf("Factor parsed.\n"); }
       | '-' FACTOR { printf("Factor parsed.\n"); }
       | NOT FACTOR { printf("Factor parsed.\n"); }
       | '(' BOOL_EXP ')' { printf("Factor parsed.\n"); }
       | READ '(' ')' { printf("Factor parsed.\n"); }
       ;


%%


int yyerror(const char *msg) {
    fprintf(stderr, "Parser Error: %s\n", msg);
    return 0;
}

int main() {
    yyparse();
    return 0;
}
