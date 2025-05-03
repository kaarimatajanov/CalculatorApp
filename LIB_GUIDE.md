Руководство по использованию пользовательских библиотек
Описание
Пользовательские библиотеки libcalc.a (статическая) и libcalc.dylib (динамическая) содержат функции для калькулятора SimpleCalculatorMVVM. Библиотеки включают:

Парсинг выражений (libparser).
Вычисление выражений (libevaluator).
Управление памятью (libmemory).
Информация о разработчиках (libinfo).

Установка

Поместите исходные файлы в SimpleCalculatorMVVM/lib.
Скомпилируйте библиотеки:cd SimpleCalculatorMVVM/lib
gcc -c *.c
ar rcs libcalc.a *.o
gcc -shared -o libcalc.dylib *.c -lm



Использование

Статическая библиотека:gcc main.c -LSimpleCalculatorMVVM/lib -lcalc -o calculator -lm
./calculator


Динамическая библиотека:Убедитесь, что libcalc.dylib в DYLD_LIBRARY_PATH:export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:SimpleCalculatorMVVM/lib
python3 SimpleCalculatorMVVM/view.py



Запуск на рабочем столе

Скопируйте файлы:cp SimpleCalculatorMVVM/lib/libcalc.dylib ~/Desktop/
cp SimpleCalculatorMVVM/view.py ~/Desktop/
cp -r SimpleCalculatorMVVM/resources ~/Desktop/SimpleCalculatorMVVM/
cp SimpleCalculatorMVVM/config.json ~/Desktop/SimpleCalculatorMVVM/


Создайте папку для лога:mkdir -p ~/Desktop/SimpleCalculatorMVVM


Настройте путь:export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:~/Desktop


Запустите:python3 ~/Desktop/view.py



Компиляция в исполняемый файл

Установите pyinstaller:pip3 install pyinstaller


Скомпилируйте:pyinstaller --onefile --icon=SimpleCalculatorMVVM/resources/icon.ico \
  --add-data=SimpleCalculatorMVVM/resources:SimpleCalculatorMVVM/resources \
  --add-data=SimpleCalculatorMVVM/config.json:SimpleCalculatorMVVM \
  --add-data=SimpleCalculatorMVVM/lib/libcalc.dylib:SimpleCalculatorMVVM/lib \
  SimpleCalculatorMVVM/view.py


Скопируйте на рабочий стол:cp dist/view ~/Desktop/calculator


Запустите:~/Desktop/calculator



Функции

char** parse_expression(const char* expr, int* token_count): Разбивает выражение на токены.
void free_tokens(char** tokens, int token_count): Освобождает память токенов.
double evaluate_expression(const char* expr): Вычисляет выражение.
char* append_history(const char* expr, const char* result, const char* current_history): Добавляет запись в историю.
void clear_history(char** history): Очищает историю.
char* get_developer_info(): Возвращает информацию о разработчике.

Замечания

Динамическая библиотека требует настройки пути на macOS.
Статическая библиотека увеличивает размер исполняемого файла.
Убедитесь, что папка SimpleCalculatorMVVM/resources/ содержит logo.png, animation.gif, click.wav, icon.ico.

