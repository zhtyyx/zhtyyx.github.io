---
layout:     post
title:      "Python性能优化的20条建议"
subtitle:   "性能优化"
date:       2021-06-26
author:     "Hunter"
header-img: "img/betterpython.jpg"
tags:
    - Python
---

# Python性能优化（一）20条建议

从本文开始，我将总结Python开发时，遇到的性能优化问题的定位和解决。

本系列主要参考并翻译Python官网和stackify上的如下文章，并加上一些思考和代码。如有错漏，欢迎批评指正，转载请联系我获得许可。

https://wiki.python.org/moin/PythonSpeed/PerformanceTips

https://stackify.com/20-simple-python-performance-tuning-tips/stackify.com

本文最后附需要优化的代码转换为C或者机器码的包。

## 概述：

性能优化的原则——优化**需要优化的部分**。

性能优化的一般步骤：

首先，让你的程序跑起来结果一切正常。然后，运行这个结果正常的代码，看看它是不是真的很慢。第三，如果很慢，找出占用大部分时间的代码。一个全面的测试用例可以保证未来的优化不会改变你程序的正确性。简单说，就是：

1. 写代码
2. 检查代码运行结果是否正确
3. 分析慢不慢
4. 优化
5. 返回第二步继续

某些优化等同于好的编程风格，这些应该在你学编程语言的时候就学会，比如，把那些循环内不会改变的值的计算过程移动到循环外。

## 1、使用列表生成式——简洁快速生成新列表

老代码：

```
cube_numbers = []
  for n in range(0,10):
    if n % 2 == 1:
      cube_numbers.append(n**3)
```

新代码：

```
cube_numbers = [n**3 for n in range(1,10) if n%2 == 1]
```

在代码量较少的时候，这两种方法可能差不多，但代码量多一些，可就不一样了。

## 2、尽量使用内置的方法

Python有很多内置的方法，你可以写高质量、高效的代码，但这也很难打败内置的库。这些代码已经被优化和严格测试过，查看内置方法列表，看看你是否重复造轮子了。

## 3、使用xrange()而不是range()

在Python2中，使用xrange()而非range()可以避免在循环中，在内存中存储所有数字，xrange()返回的是一个生成器，当循环这个对象时，在内存中仅仅保存当前对象。

想查看一个对象的内存占用，可以使用：

```
import sys
numbers = range(1,10000)
print(sys.getsizeof(numbers))
```

在Python3中使用range()，相当于Python2中的xrange()

## 4、考虑自己写生成器

前面几点提到了一般的优化模式，即，生成器能用就用。生成器允许我们一次返回一个对象，而不是所有对象。如前所述，xrange()正是一个Python2中实现的生成器，Python3中的range()也是生成器。

如果你工作中使用列表，考虑写自己的生成器，以使用这种延迟加载和高效的内存利用方法。生成器在读大量文件时尤其有用，处理大块文件而不必担心其大小，因为生成器的存在而成为可能。

```
import requests
import re

def get_pages(link):
  pages_to_visit = []
  pages_to_visit.append(link)
  pattern = re.compile('https?')
  while pages_to_visit:
    current_page = pages_to_visit.pop(0)
    page = requests.get(current_page)
    for url in re.findall('<a href="([^"]+)">', str(page.content)):
      if url[0] == '/':
        url = current_page + url[1:]
      if pattern.match(url):
        pages_to_visit.append(url)
    yield current_page
webpage = get_pages('http://www.example.com')
for result in webpage:
  print(result)
```

该例子每次只返回一个页面并执行某种操作，在上述代码中，是打印链接。

如果没有生成器，则需要在开始处理之前，同时获取、处理或者收集所有链接。这样的代码更干净，更快，更容易测试。

## 5、检查元素存在尽可能用in

检查列表中的成员，使用in更快一些。

```
for name in member_list:
    print('{} is a member'.format(name))
```

## 6、局部导入模块

最开始学Python时，我们可能习惯于在代码最前面导入所有我们想使用的模块，甚至用字母顺序排序。。。这种方式让你可以轻松地看到你的代码用了哪些模块，但是，坏处是你所有的导入都在最开始被加载了。（此处不太赞同原文中说的，还是要视情况而定，如果频繁调用的方法，在方法内部局部导入，岂不是重复加载）

原文对这种方法的好处的解释是：该做法有助于均匀的分配模块的加载时间，可以减少内存使用量的峰值。

还是那句话，视情况而定。

## 7、使用集合

过多的循环会给服务器带来不必要的压力。假设你想得到在两个列表中的相同的值，你可以使用多重循环，像这样:

```
a = [1,2,3,4,5]
b = [2,3,4,5,6]

overlaps = []
for x in a:
  for y in b:
    if x==y:
      overlaps.append(x)

print(overlaps)
```

这个代码可以输出正确结果，但时间复杂度是O(n^2) ，可以使用如下代码替换：

```
print(set(a) & set(b))
```

集合是利用Hash算法实现的无序不重复元素集。涉及到如上的，对list求交、并、差、异或，可以转换为set进行操作，如下：

- s.union(t)： s&t， 平均时间复杂度：O(len(s)+ len(t))
- s.intersection(t): s|t 最差时间复杂度同上
- s.difference(t) s-t 平均时间复杂度为O(len(s))
- s.symmetric_difference(t) 平均时间复杂度O(len(s))，最差时间复杂度为O(len(s)*len(t))

使用set代替使用list进行运算，速度和内存占用都得到很大的提升。

## 8、变量赋值

使用如下方式，优雅的赋值：

```
first_name, last_name, city = "Kevin", "Cunningham", "Brighton"
```

交换两个变量的值，你可以：

```
x, y = y, x
```

比下面的这种方式，既优雅，内存占用又少。

```
temp = x 
x = y
y = temp
```

## 9、避免使用全局变量

尽量不使用全局变量是一种有效的设计模式，这是因为这样做可以保持对作用域的跟踪，防止不必要的内存使用。而且，Python检索局部变量比全局变量更快，所以请尽可能避免使用全局关键字。

## 10、使用join()连接字符串

在Python中，字符串是不可变类型，你可以使用+来连接字符串，但是+操作每次都要创建新字符串并且复制旧的内容过去。一个有效的方法是，使用数组array模块修改单个字符，然后使用join来重新创建结果字符串。

+方法：

```
new = "This" + "is" + "going" + "to" + "require" + "a" + "new" + "string" + "for" + "every" + "word"
print(new)
```

得到：

Thisisgoingtorequireanewstringforeveryword

而使用join：

```
new = " ".join(["This", "will", "only", "create", "one", "string", "and", "we", "can", "add", "spaces."])
print(new)
```

得到：

This will only create one string and we can add spaces.

可以看出，使用join()拼接字符串更优雅，更快速

## 11、保持Python的版本更新

Python的维护者对于使Python更快，鲁棒性更强有很大的热情。一般来说，每一个新版本都会提升Python的性能和安全性。但是，要保证你所用的库在新版Python上也能用。

## 12、无限循环中，用 while 1

如果你在听socket，那么你可能想使用无限循环。平时大家会用while True, 这有用，但是你可以使用更轻便的 while 1来达到完全相同的效果。

## 13、换种方式

一旦你在你的应用中使用一种编程方式，你可能会复用、再复用这一种方法。但是，多实验集中不同的方法可以让你看到哪种实现更好。这不仅会让你学习和思考你写的代码的方式，而且还会让你更有创新精神，想想你如何能更有创造性的用新方法来实现更快更稳定的结果。

简言之：花式写代码，多骚，多测，最后稳如老狗。

## 14、尽可能早的离开

当你知道某个方法执行到无法再做有意义的工作时，尝试离开，这样可以减少缩进，增加可读性，还避免了嵌套：

老代码：

```
if positive_case:
  if particular_example: 
    do_something
else:
  raise exception
```

新代码：

```
if not positive_case:
  raise exception
if not particular_example:
  raise exception
do_something 
```

当我们用很多组输入去测试时，会发现新代码中抛出异常更早，而且你不需要一直梳理这些条件中的逻辑链。

## 15、了解itertools

itertools 是个大宝贝。如果你没听过，那么Python的一大部分标准库你就错过了。你可以使用itertools中的方法快速、优雅、内存高效的创建方法。

好好看看文档，寻找教程以充分利用该库。（说的我想单独开一篇文章介绍一下了。。。）

其中一个例子是排列函数，假设你想生成列表['a', 'c', 'b']的全排列，你可以：

```
import itertools
iter = itertools.permutations(["a", "c", 'b'])
list(iter)
```

试试吧！贼有用，贼快。

## 16、使用装饰器缓存

记忆化是一种特定的缓存类型，可以优化软件的运行速度，一般来说，缓存保存着最近操作的结果，该结果可以被呈现为网页或者复杂计算的结果。（没太懂，原文如下）

> Memoization is a specific type of caching that optimizes software running speeds. Basically, a cache stores the results of an operation for later use. The results could be rendered web pages or the results of complex calculations.

你可以自己尝试计算第100个Fibonacci数。

旧代码：

```
def fibonacci(n):
  if n == 0: # There is no 0'th number
    return 0
  elif n == 1: # We define the first number as 1
    return 1
  return fibonacci(n - 1) + fibonacci(n-2)
```

用上述办法计算fibonacci数时，你的电脑会发出轰鸣声，尤其是n较大的时候。。。

如果你使用标准库中的装饰器缓存，就不一样了：

```
import functools

@functools.lru_cache(maxsize=128)
def fibonacci(n):
  if n == 0:
    return 0
  elif n == 1:
    return 1
  return fibonacci(n - 1) + fibonacci(n-2)
```

在Python中，装饰器使用别的方法并且延展其功能。我们使用@symbol这样的符号来标识使用装饰器的方法。在上述代码中，使用了functools.Iru_cache装饰器，将运行结果存入内存。

还有其他形式的装饰器，你也可以写自己的装饰器，但这个装饰器快而且是内置的。有多快？自己试试吧。

## 17、排序时使用keys

文中描述的方法：

```
import operator
my_list = [("Josh", "Grobin", "Singer"), ("Marco", "Polo", "General"), ("Ada", "Lovelace", "Scientist")]
my_list.sort(key=operator.itemgetter(0))
```

事实上我觉得sorted也是很好用的：

```
sorted_my_list = sorted(my_list, key=lambda x: x[0])
```

只能说，都可以吧。

## 18、不要为条件构造一个集合

你有时候是不是想把你的代码构建成这样：

```
if animal in set(animals):
```

上面这个主意看起来很合理。把animals里面的重复数据删掉，感觉上会更快

```
if animal in animals:
```

但是，即使列表中可能有很多项重复，解释器的优化程度仍然很高，以至于先set再检查in可能会减慢速度。一般来说，不使用set而是用下面的那种，总是更快的。

## 19、使用链表

Python 列表数据类型实现为数组。这意味着，在列表开头添加一个元素可能是非常费力的操作，因为每个元素都得移动。链表数据类型这下就派上用场了。不同于数组，链表中每一项都有和表中下一项的连接——由此得名。

列表需要实现分配好内存，这种分配代价高昂，浪费巨大，如果你提前不知道你要多大的数组，那更是如此。

链表允许你在你需要的时候才分配内存，每一项都被存在内存的不同部分，链接将这些项连接起来。

链表的问题是查找时间比较慢，需要做个彻底分析，来确定是不是更好的办法。

## 20、使用基于云的Python性能工具

当你在本地工作时，你可以用一些性能工具来定位你的项目的性能瓶颈。如果你的项目将会被部署到网上，就有点不同了。stackify（文章所在的网站，一波软广告）将让你看到你的网站在生产环境下的表现，也会提供代码分析，错误追踪，服务器指标等。

## 结论：

这些tips只是指出你的代码可能遇到的陷阱，和一些建议的解决方式，具体怎么优化，还是要你自己去考虑。不管怎么样，性能优化之路，就从此开始吧。

我会继续更新Python性能优化的相关文章，发布在如下专栏：



## 参考这些包，将代码转换为C或者机器码：

http://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/www.cosc.canterbury.ac.nz

http://www.scipy.org/Weavewww.scipy.org

http://code.google.com/p/shedskin/

[Mix Other Languages directly Inline with your Python](http://pyinline.sourceforge.net/)