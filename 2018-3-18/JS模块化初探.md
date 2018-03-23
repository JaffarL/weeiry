# JS模块化初探

[TOC]

JS创建之初作为一个浏览器端的脚本编程语言，仅仅是用来实现一些简单的网页逻辑，代码不长，易于维护，所以也并没有模块化的概念，但随着互联网技术的发展，web端逻辑日渐复杂，JS也负责着越来越多的网页行为，代码量也越来越大，JS也需要一个模块化规范来管理项目中的代码。

## 远古时期的模块化

基本没有模块化，仅仅是依据各个脚本的依赖顺序使用`<script>`标签来加载各个脚本，顶多使用一下立即执行匿名函数来避免变量命名冲突，但这样很显然是非常丑陋的。

## Node的模块化

Node采用的是CommonJS规范，很好用，简单看一下代码

```js
const someModule = require('whatever')
someModule()
```

CommonJS规范的模块加载是同步的，对于node来说，所有模块文件都在本地磁盘上，读取的速度比较快，程序的阻塞几乎可以忽略不计，而对于浏览器端来说，有些脚本资源很有可能是存储在远程服务器上的，读取的速度比较慢，如果采用CommonJS的规范，同步读取时候浏览器内容渲染遭到阻塞，用户体验会很差，所以浏览器端的模块加载方式必须是异步的。

## AMD

在浏览器对模块的特殊需求背景下，AMD应运而生了，AMD全称是Asynchronous Module Defination，异步模块定义，望文生义，这个模块规范下的模块加载是异步的，并且依赖这个模块的代码都放在一个回调函数中。

模块化代码必然分为两部分：一是将模块暴露出去，二是将模块引进来，这个思想和CommonJS的实现很像，就是语法不太一样。

### define

我们必须利用`define()`这个函数将我们需要模块化的函数包起来，而暴露给外部是`define()`函数的返回值

```js
//module1.js
define(function(){
    //do something
    return {
        string:'module1'
    }
})
```

```js
//moduel2.js
define(()=>{
    return function(v){
        //do something
        return v + ' module2'
    }
})
```

如果需要导出的模块自己本身也依赖别的模块，那么就需要这样写

```js
//module3.js
define(['module2'],(m2)=>{
    console.log(m2('mudule3 and '))
    return 'module3'
})
```





### require

引入模块的时候我们得使用`require()`函数，`require()`有两个参数，第一个参数是数组，数组元素是js文件名的字符串，要引入多少模块数组就有多少字符串元素。第二个参数是一个回调函数，这个回调函数在依赖的模块加载完毕之后会执行，有多少模块这个回调函数就有多少个参数，我们在这个回调函数内部定义模块文件导出对象的调用逻辑。

```js
//main.js
require(['module1','module2'],(m1,m2)=>{
    console.log(m1['string'])  // 'module1'
    console.log(m2('from')) // 'from module2'
})
```

main.js内这样写那是因为module1.js和module2.js文件和main.js在同一目录下，如果在不同目录或者在远程，可以通过在main.js中自定义`require.config()`函数指定依赖的每个模块的路径

```js
//main.js
require.config({
	paths:{
		'module1':'./test/module1',
		'module2':'./test/module2',
        'module3':'./test/module3'
	}
})


require(['module1','module2'],(m1,m2)=>{
    console.log(m1['string'])  // 'module1'
    console.log(m2('from')) // 'from module2'
})
```

如果是远程的

```js
　require.config({
　　　　paths: {
　　　　　　"jquery": "https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min"
　　　　}
　　});
```

AMD功能不仅如此，其他功能以后用到再补充吧。