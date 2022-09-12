# ДЗ по формальным языкам №1
## Бондарь Федор Николаевич

### Задание 1:
V_T = {0, 1}.

V_N = {S}.

Тогда G = <{0, 1}, {S}, {S -> 0S0 | 1S1 | e}, S>.

Пример вывода строки 10100101:

```c++
           S
         / | \   
        1  S  1
         / | \   
        0  S  0
         / | \   
        1  S  1
         / | \   
        0  S  0
           |
           e
```

### Задание 2:

Дана грамматика:

S -> aSA | aT

TA -> bTa

aA -> Aa

T -> ba

Построим некоторые последовательности:

S -> aT -> aba.

S -> aSA -> aaTA -> aabTa -> aabbaa.

S -> aSA -> aaSAA -> aaaTAA -> aaabTaA -> aaabTAa -> aaabbTaa -> aaabbbaaa.

Далее аналогично. Получаем, что L(G) = {(a^k)(b^k)(a^k) | k - натуральное число}.

### Задание 3:

Python

1) Легально использовать " \ ", чтобы перейти на новую строку и сделать код читаемым:
```python
if expr1 and expr2 and expr3 and expr4 and expr5:
    pass

if expr1 and expr2 and expr3 \
         and expr4 and expr5:
    pass
```
2) Функция raise, вызывающая ошибку во время исполнения, на самом деле не только 
опционально принимает как параметр объект ошибки, но и место, откуда её нужно 
выбросить, с помощью from:
```python
raise RuntimeError("oops")

raise RuntimeError("oops") from exc
```
3) Функция assert, упрощающая синтаксис raise:
```python
if not expr1: raise AssertionError(expr2)
# одно и то же
assert expr1, expr2
```

Ссылка на документ: https://docs.python.org/3/reference/
