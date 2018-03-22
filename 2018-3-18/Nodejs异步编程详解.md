# Nodejs异步编程详解

## 写在前面

公司内部大量使用python作为平时编写脚本的语言，python语法简单易上手，又有大量的库的支持，在工具脚本这格领域体现了它的价值，地位不可动摇。我本来是也是使用python编写一些脚本的，但由于一些巧合、契机，我接触到了Nodejs，基于一些个人原因，我更倾向使用Nodejs来编写平时使用的工具脚本，包括数据采集入库之类，但由于js这个语言本身的一些特性，使得Nodejs作为脚本来开发的话难度曲线相对陡峭，这篇文章我就关于Nodejs中最关键也是最难的异步编程做一些介绍和讲解

$这篇文章面向的读者绝对不是对Nodejs完全没用过的同学，读者需要对Nodejs有简单的了解$

## Nodejs的异步

Nodejs本身是单线程的，底层核心库是Google开发的V8引擎，而主要负责实现Nodejs的异步功能的是一个叫做libuv的开源库，github上可以找到它。

先看几行python代码

```python
file_obj = open('./test.txt')
print(file_obj.read())
```

这行代码逻辑相当简单，打印根目录下一个名为test的txt文件内容

相同的操作用Nodejs写是这样：

```js
const fs = require('fs')
fs.read('./test.txt',(err,doc)=>{
    if(err){
        // throw an err
    }else{
        console.log(doc)
    }
)
```

看起来相当的麻烦。

为什么要这样写？根本原因就是Node的特点，异步机制。关于异步机制的深入理解我可能会另写一篇文章

`fs.read()`本身是一个异步函数，所以返回值是异步的，必须在回调函数中捕获，所以得写成这个样子。

一两个异步操作可能还好，但如果相当多的异步操作需要串行执行，就会出现以下这种代码：

```js
//callbackHell.js
fs.read('./test1.txt',(err,doc)=>{
    //do something
    let input = someFunc(doc)
    fs.read('./test2.txt',(err,doc2)=>{
        //do something
        let input2 = someFunc2(doc2)
        fs.write('./output.txt',input+input2,(err)=>{
            // err capture
            // some other async operations
        })
    })
})
```

连续的回调函数的嵌套，会使得代码变得冗长，易读性大幅度降低并且难以维护，这种情况也被称作***回调地狱***（calllback hell)，为了解决这个问题，ES标准推出了一套异步编程解决方案

## Promise

人们对于新事物的快速理解一般基于此新事物与生活中某种事物或者规律的的相似性，但这个promise并没有这种特点，在我看来，可以去类比promise这个概念的东西相当少，而且类比得相当勉强，但这也并不意味着promise难以理解。

promise本身是一个对象，但是可以看做是是一种工具，一种从未见过的工具，解决的是Nodejs异步接口串行执行导致的回调地狱问题，它本身对代码逻辑没有影响

废话少说，直接上代码：

```js
function promisifyAsyncFunc(){
    return new Promise((resolve,reject)=>{
        fs.read('./test1.txt'.(err.doc)=>{
            if(err)reject(err)
            else resolve(doc)
        })
    })
}
promisifyAsyncFunc()
	.then(res=>{
    	console.log(`read file success ${res}`)
	})
    .catch(rej=>{
    	console.log()
})
```

与之前的异步代码不同的是，我们在异步函数外层包了一层返回promise对象的函数，promise对象向自己包裹的函数里传入了两个函数参数`resolve`和`reject`，在异步函数内部通过调用`resolve`向外传递操作成功数据，调用`reject`向外传递错误信息。

> 关于promise对象使用的语法牵涉到es6的最新规范和函数式编程，这里不做详细介绍

接着我们调用这个函数，链式调用promise对象提供的接口函数`.then(function(res){//TODO})`将异步函数向外传递的值取出来，使用`.catch()`捕获内部传递的错误。

最基本的promise用法大致就是这样，但这样看依然没明白它如何避免了回调地狱，这里我们使用promise改写callbackHell.js文件

```js
//promisifY.js

function promisifyAsyncFunc(){
    return new Promise((resolve,reject)=>{
        fs.read('./test1.txt'.(err.doc)=>{
            if(err)reject(err)
            else resolve(doc)
        })
    })
}

function promisifyAsyncFunc2(input){
    return new Promise((resolve,reject)=>{
        let output1 = someFunc(input)
        fs.read('./test2.txt'.(err.doc)=>{
            if(err)reject(err)
            else resolve({
                output1,
                doc
            })
        })
    })
}

function promisifyAsyncFunc3({output1,doc}){
    return new Promise((resolve,reject)=>{
        let outpu2 = someFunc2(doc)
        fs.write('./output.txt',output1+output2,(err)=>{
                    // err capture
        })
    })
}
// some other prmisify function
promisifyAsyncFunc()
.then(promisifyAsyncFunc2)
.then(promisifyAsyncFunc3)
//.then()
```

代码这样写应该会看的比较清楚，我们把每个异步函数都封装在promise对象里面，然后通过promise的链式调用来传递数据，从而避免了回调地狱。

这样的代码可读性和维护性要好上不少，但很显然代码量增加了一些，就是每个函数的封装过程，但node里的util库中的`promisify`函数提供了将满足node回调规则的函数自动转换为promise对象的功能，若没有对异步操作的复杂订制，可以使用这个函数减少代码量

******************

虽然promise相对于原生的回调来说已经是相当良好的编程体验，但对于追求完美的程序员来说，这依旧不够优美，于是es规范在演进的过程中又推出了新的异步编程方式

## Generator

Generator并不是最终的异步解决方案，而是Promise向最终方案演进的中间产物，但是其中利用到的迭代器设计模式值得我们学习和参考。这里不对这种方法多做介绍，因为有了async，一般就不再使用Generator了。

## async/await

Async/Await其实是Generator的语法糖，但是因为使用的时候使异步编程似乎完全变成了同步编程，体验异常的好，而且这是官方推出的最新规范，所以广受推崇，这里就对如何使用它进行一些介绍说明。

先看Async的语法，用起来真的是相当简单

```js
async function main(){
    const ret = await someAsynFunc();
    const ret2 = await otherAsyncFunc(ret)
    return someSyncFunc(ret,ret2)
}
```

1. 定义一个函数，函数申明前加上一个`async`关键字，说明这个函数内部有需要同步执行的异步函数
2. 此函数需要同步执行的异步函数必须返回的是promise对象，就是我们之前用promise包裹的那个形式
3. 在需同步执行的异步函数调用表达式前加上`await`关键字，这时函数会同步执行并将promise对象resolve出来的数据传递给等号之前的变量

我们再使用async/await改写promisify.js文件

```js
//async/await.js
const promisify = require('util').promisify  //引入promisify函数，简化promise代码
const read = promisify(fs.read)
const write = promisify(fs.write)

async function callAsyncSync(){
    const res1 = await read('./test1.txt')
    const res2 = await read('./test2.txt')
    const output1 = someFunc(res1)
    const output2 = someFunc(res2)
    write('./output.txt',output1+output2)
    return 
}
```

这样看代码就像是同步的， 比python速度还快很多，可惜的就是相对于python学习曲线比较陡峭。

这种方式写出的代码可读性可维护性可以说是非常强，完全没有之前的回调地狱或者原生promise带来的副作用。



## 进阶

试想这么一种场景：

> * 我们需要从多个数据库中读取数据，读取完成的顺序无所谓.
> * 我们需要在多次数据读取全部完成之后再从每个数据中筛选出某种相同的属性
> * 再对这些属性进行一些自定义操作，得到结果数据
> * 最后将结果数据插入某个数据库

假设每一步的具体实现函数全部已经编写完成，所有异步的函数都已经封装成promise，那么用原生js组装以上四步代码需要怎么写？

我粗略估计一下可能需要二十行左右，而且代码的可读性不会很好，这里我简单介绍一个库:RxJS，中文名为响应式JS。

响应式编程发展已久，许多语言都有实现相应的库，对应的名字也以Rx开头，比如RxJava。

不说RxJS的设计原理，它的使用都牵涉到多种设计模式和技术，包括观察者模式，管道模式，函数式编程等，可以说这是一个上手难度相当大的技术，但它带来的编程体验是相当的好，这里我给出使用RxJS实现以上四步的代码

```js
const Ob = require('rxjs/Rx').Observerble   //Rxjs的核心观察者对象
const promiseArray = require('./readDatabase') //封装好的读数据库函数数组
const myfilter = require('./filter')//数据属性过滤函数
const operation = require('./operation')//自定义的逻辑操作
const insert = require('./insert')//数据库插入函数

Ob.forkJoin(...promiseArray.map(v=>Ob.fromPromise(v))) 
	.filter(myfilter)
	.switchMap(operations)
	.subscribe(insert)
```

除去将自定义的函数引入，四步操作每步只对应一行代码，这样写真的是非常简洁。

我们平时常用的，甚至是不常用的对数据的操作，基本都能在RxJS官网里都能找到封装好的API，有兴趣的同学可以多关注这个库，就我自己平时开发时的体验来看，这个库是相当的好用，但是要有一定的心理准备，因为确实有一些难度。