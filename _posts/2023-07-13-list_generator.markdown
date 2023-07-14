---
layout:     post
title:      "Python中的列表推导式，生成器"
subtitle:   "Python语法"
date:       2022-08-13
author:     "Hunter"
header-img: "img/copy.jpg"
tags:
    - Python
---
列表推导式：一种十分优雅的创建列表方式，Python的列表推导式允许我们使用非常少的代码并使用循环创建列表（一行代码）

生成器：有点类似于列表推导式但并不生成列表对象。生成器是仅当被需要时才产生下一项，而不是像列表推导式一样，生成整个列表并存在内存中。一个有返回的正常函数被调用时，当调用方得到返回时调用结束。但有yield声明的函数保存了函数状态并且能在下一次函数被调用时，以相同状态被唤醒。生成器表达式允许我们无需yield即可创建生成器。

传统的列表创建方式：

```
# initializing the list
a = []

for i in range(100):
    if i % 3 == 0:
        a.append(i)

print(a)
```

列表推导式的列表创建：

```
list_ex = [i for i in range(10) if i % 3 == 0]
```

该语句的输出：

```
[0, 3, 6, 9]
```

生成器表达式的创建：

```
generator_ex = (i for i in range(100) if i % 3 == 0)
```

该语句的输出：

```
<generator object <genexpr> at 0x7f38bdc547d8>
```

可以看出，将列表推导式和生成器表达式外观（语法）上的主要区别在于括号。打印生成器表达式的创建结果，是该对象的存储地址。如果想打印生成器表达式的输出，可以遍历该生成器对象：

```
for i in generator_ex:
    print(i, end = "")  # 内置函数 print 指定 end='' 后不换行打印。
```

该语句的输出：

```
0 3 6 9
```

列表推导式和生成器表达式的区别：

- 内存使用效率：

如下所示，生成器仅在需要时（被调用时）一次产生一项结果存入内存，然而在列表推导式中，Python为整个列表保留内存。可以说，生成器表达式相比于列表在内存使用效率上更高。

```
from sys import getsizeof                                               

a = [i for i in range(99999)]                                           

b = (i for i in range(99999))                                           

x = getsizeof(a)                                                        

y = getsizeof(b)                                                        

print(x)                                                                
824464

print(y)                                                                
88
```

- 时间效率：

如下所示，在执行时间上，列表推导式和生成器表达式在执行时间上也有很明显的差别，因此，生成器表达式比列表推导式更快，更节约时间。

```
import timeit

# 列表推导式
print(timeit.timeit('''list_com = [i for i in range(100) if i % 3 == 0]''',number = 10000000) 
# 生成器表达式
print(timeit.timeit('''gen_exp = (i for i in range(100) if i % 3 == 0)''',number = 10000000) 

# 列表推导式输出：
4.669294930994511
#生成器表达式输出：
0.4217875720351003
```