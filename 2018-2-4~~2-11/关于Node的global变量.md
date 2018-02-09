# 关于上周的global

代码如下

```js
var kk = 'kk';
console.log(global.kk)
```

这段代码使用node test.js 这种指令会输出undefined，而在repl中则会正常输出kk。被这个问题困扰了好一会儿，终于在2月4日晚上qq群中宾生老师给了我合理的解答。</br>
简单的说就是作用域的问题，node环境中有一个大的global作用域，它下面管理者该node项目所有的文件，而每个文件有着各自的作用域。以以上代码为例：</br>

```js
var kk = 'kk'；
```

在本文件作用域声明并复制了变量kk，而代码

```js
console.log(global.kk)
```

则试图在全局中访问变量kk，所以自然会报错。</br>
而在repl中则不一样，repl中没有文件的概念，整个repl下都只有一个作用域，所有不在块级作用域或者函数作用域下的变量声明都是在global下的，所以使用global.kk能够直接访问kk变量。
