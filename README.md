# HW01 Алмазов Павел

#### Задание 1
Привести грамматику для языка палиндромов `{ w w^r | w \in {0, 1}* }`. Привести дерево вывода какой-нибудь строки длины не меньше 7 в предложенной грамматике.
#### Решение:

Грамматика:
```
G = {V_T, V_N, P, S}
V_T = {0, 1}
V_N = {S}
P = {S -> 0S0 | 1S1 | ε}
```

Пример для `01011010`:
```
        S
      / | \
     0  S  0
      / | \
     1  S  1
      / | \
     0  S  0
      / | \
     1  S  1
        |
        ε  
```

#### Задание 2
Описать язык, порождаемый грамматикой
  ```
  S -> aSA | aT 
  TA -> bTa
  aA -> Aa
  T -> ba
  ```
#### Решение:

$$ S \rightarrow a^n S A^n \rightarrow a^{n + 1} T A^{n} \rightarrow a^{n + 1} b T A a A^{n - 2} \rightarrow 
\rightarrow a^{n + 1} b^2 T a^2 A^{n - 2} \rightarrow ... \rightarrow a^{n + 1} b^{n} T a^{n} \rightarrow a^{n + 1} b^{n + 1} a^{n + 1}$$
##### Ответ: все слова вида `a^n b^n a^n, где n >= 1`

#### Задание 3
Изучить спецификацию синтаксиса вашего второго самого любимого языка, в отчете привести ссылку на документ, который вы изучали, и отметить 3 новые для вас особенности синтаксиса.



#### Решение:
##### Язык C++
1. noexept оказывается не только qualifier но и [operator](https://en.cppreference.com/w/cpp/language/noexcept):
```C++
#include <iostream>
#include <utility>
#include <vector>
 
void may_throw();
void no_throw() noexcept;
auto lmay_throw = []{};
auto lno_throw = []() noexcept {};
 
class T
{
public:
    ~T(){} // dtor prevents move ctor
           // copy ctor is noexcept
};
 
class U
{
public:
    ~U(){} // dtor prevents move ctor
           // copy ctor is noexcept(false)
    std::vector<int> v;
};
 
class V
{
public:
    std::vector<int> v;
};
 
int main()
{
    T t;
    U u;
    V v;
 
    std::cout << std::boolalpha
        << "Is may_throw() noexcept? " << noexcept(may_throw()) << '\n'
        << "Is no_throw() noexcept? " << noexcept(no_throw()) << '\n'
        << "Is lmay_throw() noexcept? " << noexcept(lmay_throw()) << '\n'
        << "Is lno_throw() noexcept? " << noexcept(lno_throw()) << '\n'
        << "Is ~T() noexcept? " << noexcept(std::declval<T>().~T()) << '\n'
        // note: the following tests also require that ~T() is noexcept because
        // the expression within noexcept constructs and destroys a temporary
        << "Is T(rvalue T) noexcept? " << noexcept(T(std::declval<T>())) << '\n'
        << "Is T(lvalue T) noexcept? " << noexcept(T(t)) << '\n'
        << "Is U(rvalue U) noexcept? " << noexcept(U(std::declval<U>())) << '\n'
        << "Is U(lvalue U) noexcept? " << noexcept(U(u)) << '\n'  
        << "Is V(rvalue V) noexcept? " << noexcept(V(std::declval<V>())) << '\n'
        << "Is V(lvalue V) noexcept? " << noexcept(V(v)) << '\n';  
}
```
2. Узнал про [volatile](https://habr.com/ru/post/673428/)
3. [Variadic arguments](https://en.cppreference.com/w/cpp/language/variadic_arguments) - позволяет функции принимать любое количество дополнительных аргументов:
```C++
#include <iostream>

using namespace std;

void print() {
    cout << endl;
}

template <typename T> void print(const T& t) {
    cout << t << endl;
}

template <typename First, typename... Rest> void print(const First& first, const Rest&... rest) {
    cout << first << ", ";
    print(rest...); // recursive call using pack expansion syntax
}

int main()
{
    print(); // calls first overload, outputting only a newline
    print(1); // calls second overload

    // these call the third overload, the variadic template,
    // which uses recursion as needed.
    print(10, 20);
    print(100, 200, 300);
    print("first", 2, "third", 3.14159);
}
```
