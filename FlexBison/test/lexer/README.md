# Unit Test for Lexer
## Antônio Amaral Egydio martins

### 1 How to run

#### 1.1 Changes Needed

1. Copy lexer.l into the `test/lexer` directory
2. Copy parser.y into the `test/lexer` directory

##### 1.1.1 Flex Changes

3. Change `#include "parser.tab.h"` to the correct path


#### 1.1.2 Bison Changes

4. Include the following code into the declaration of the `parser.y` file:

```c
// Declare yylex and yyerror
int yylex(void);
int yyerror(const char *msg);
```

5. Remove `main()` function from `parser.y`

#### 1.2 Running

With the `parser.y` and `flex.l` files in the same directory, run the following command:

```bash
./compile.sh
```

This will generate the `lexer_test` executable. To run the tests, use the following command:

```bash
./run_tests.sh
```

### 2 Operating System

If you are using Windows, you can use the following command on `run_tests.sh`:

```bash
gcc -o lexer_test lex.yy.c main.c -lfl
```

if you are using MacOS, you can use the following command on `run_tests.sh`:

```bash
clang -o lexer_test parser.tab.c lex.yy.c main.c -ll
```