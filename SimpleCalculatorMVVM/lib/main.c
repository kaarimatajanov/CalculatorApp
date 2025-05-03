#include <stdio.h>
extern double evaluate_expression(const char* expr);
extern char* get_developer_info();

int main() {
    printf("Result: %f\n", evaluate_expression("2 + 3"));
    printf("%s\n", get_developer_info());
    return 0;
}