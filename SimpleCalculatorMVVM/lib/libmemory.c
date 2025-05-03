#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* append_history(const char* expr, const char* result, const char* current_history) {
    char* new_history = malloc(1024);
    snprintf(new_history, 1024, "%s%s = %s\n", current_history, expr, result);
    return new_history;
}

void clear_history(char** history) {
    if (*history) {
        free(*history);
        *history = strdup("");
    }
}