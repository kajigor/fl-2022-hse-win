# Проект

[Ссылка на репозиторий с подзадачей](https://github.com/jegorpopow/EBNF/tree/parser)

* Парсер написан на языке `Python` с использованием библиотеки `ply`
* В рамках подзадачи реализован [лексер](https://github.com/jegorpopow/EBNF/blob/parser/lexer.py) и [парсер](https://github.com/jegorpopow/EBNF/blob/parser/parser.py). Оба модуля могут быть использованы отдельно в качестве консольного приложения, и могут импортироваться в другие модули.
* Используемые структуры и некоторые вспомогательные функции можно найти [здесь](https://github.com/jegorpopow/EBNF/blob/parser/EBNF.py).
* Консольное приложение принимает обязательный аргумент `<input.file>` -- имя файла с грамматикой -- и необязательный аргумент `<output.file>` -- имя файла для вывода. Если второй аргумент опущен, вывод производится в файл `<input.file.out>`.
    ```bash
    python3 lexer.py <input.file> [<output.file>]
    ```
* Также реализован [скрипт для тестирования](https://github.com/jegorpopow/EBNF/blob/parser/parser.py): он запускает модуль на всех тестах с расширением `.in`, чьи имена указаны в `tests/tests.txt`, и сохраняет результат в файл `tests/test_name-module_name.out`. Для запуска нужно указать имя модуля.
    ```bash
    ./run-tests.sh ebnf_parser
    ```
