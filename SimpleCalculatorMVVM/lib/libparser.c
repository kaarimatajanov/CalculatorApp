#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char** parse_expression(const char* expr, int* token_count) {
    char** tokens = malloc(100 * sizeof(char*));
    *token_count = 0;
    char buffer[256] = {0};
    int buf_idx = 0;

    for (int i = 0; expr[i]; i++) {
        if (isspace(expr[i])) continue;
        if (isdigit(expr[i]) || expr[i] == '.') {
            buffer[buf_idx++] = expr[i];
        } else if (strchr("+-*/^%()", expr[i]) || strncmp(&expr[i], "sin", 3) == 0 ||
                   strncmp(&expr[i], "cos", 3) == 0 || strncmp(&expr[i], "tan", 3) == 0 ||
                   strncmp(&expr[i], "ln", 2) == 0) {
            if (buf_idx > 0) {
                buffer[buf_idx] = '\0';
                tokens[*token_count] = strdup(buffer);
                (*token_count)++;
                buf_idx = 0;
            }
            if (expr[i] == 's' || expr[i] == 'c' || expr[i] == 't' || expr[i] == 'l') {
                char func[4] = {0};
                int j = 0;
                while (isalpha(expr[i]) && j < 3) {
                    func[j++] = expr[i++];
                }
                i--;
                tokens[*token_count] = strdup(func);
                (*token_count)++;
            } else {
                char op[2] = {expr[i], '\0'};
                tokens[*token_count] = strdup(op);
                (*token_count)++;
            }
        }
    }
    if (buf_idx > 0) {
        buffer[buf_idx] = '\0';
        tokens[*token_count] = strdup(buffer);
        (*token_count)++;
    }
    return tokens;
}

void free_tokens(char** tokens, int token_count) {
    for (int i = 0; i < token_count; i++) {
        free(tokens[i]);
    }
    free(tokens);
}