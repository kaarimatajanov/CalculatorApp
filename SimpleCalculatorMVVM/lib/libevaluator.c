#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

double evaluate_expression(const char* expr) {
    // Упрощённый пример: вычисляет простые выражения вида "число + число"
    double result = 0.0;
    char** tokens;
    int token_count;
    extern char** parse_expression(const char* expr, int* token_count);
    tokens = parse_expression(expr, &token_count);

    if (token_count == 3 && strcmp(tokens[1], "+") == 0) {
        result = atof(tokens[0]) + atof(tokens[2]);
    } else {
        result = atof(expr); // Заглушка для других случаев
    }

    extern void free_tokens(char** tokens, int token_count);
    free_tokens(tokens, token_count);
    return result;
}