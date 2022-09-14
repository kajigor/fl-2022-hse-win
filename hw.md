# HW01

`S -> 0S0 | 1S1 | \epsilon`


Вывод 01011010:

![alt text for screen readers](t1.png "Text to show on mouseover")


2. 

Сперва нужно применить n(возможно 0) первых правил для S и одно второе. Получим

' a^naTA^n '

Чтобы избавиться от всех A, нужно n раз применить ```TA -> bTa```

```a^nab^nTa^n -> a^nab^nbaa^n```

Т.к. n может быть 0, то общий вид

```a^nb^na^n```

