#include <stdio.h>
#include "tokens.l" // Include the lexer file

int main() {
    int token;
    // Call the lexer function repeatedly until the end of input
    while ((token = yylex()) != 0) {
        // Print out each token along with its corresponding value if applicable
        switch (token) {
            case INT_TYPE:
                printf("Token: INT_TYPE\n");
                break;
            case STRING_TYPE:
                printf("Token: STRING_TYPE\n");
                break;
            case PRINT:
                printf("Token: PRINT\n");
                break;
            // Add cases for other tokens as needed
            default:
                printf("Token: %d\n", token);
        }
    }
    return 0;
}
