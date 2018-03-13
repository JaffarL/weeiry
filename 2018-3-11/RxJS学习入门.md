# RxJS学习入门

[TOC]

## 简单介绍	

> 并不面向纯新手进行介绍，仅仅是对于我来说可以理解的表述顺序或者方式来描述RxJS是什么

1. 观察者模式，迭代器模式，管道模式，函数式编程
2. 响应式编程，用我的话来说好理解的应该叫触发式程序设计
3. 优化编程体验，代码结构可读性可维护性强
4. 上手难度大，对原项目入侵性强

## 核心概念

### Observable  可观察对象（什么屎翻译）

通过RxJS的核心对象`Rx.Obeserble`的静态操作符函数`xx`创建的对象

```js
const observable = Rx.Observable.xx(function(observer){
    //TODO
})
```



### Observer 观察者

可以是一个函数，也可以是一个对象，对象的各个元素是***函数***，指示了`observable`中数据流动的规则

```js
var observer = {
  next: x => console.log('Observer got a next value: ' + x),
  error: err => console.error('Observer got an error: ' + err),
  complete: () => console.log('Observer got a complete notification'),
};
```

然后通过`observable`的`subscribe()`传递进去

```js
observable.subscribe(observer);
```

> 观察者只是有三个回调函数的对象，每个回调函数对应一种 Observable 发送的通知类型。
>
> 如果某种回调函数没有在`observer`中定义也没关系，只是这种通知回调会被忽略

也有可能`observer`直接就是一个函数，例如`x => console.log('Observer got a next value: ' + x)`，此函数会被默认变为`next()`函数并重新封装进一个观察者对象

## 常用静态操作符

### fromPromise()

接受一个`prmoise`对象，生成对应的`obervable`



### concat()

接受两个或者多个`observable`，将其顺序连接起来，当前一个完成时才执行下一个



### forkJoin()

接受两个或者多个`observable`，并行的执行，并且当所有`observable`全部执行完毕之后才返回，并且返回值只一个数组，其中元素是每个`observable`的返回值

> 可以理解为Rx版的`Promise.all()`，当需要并行的执行任务时使用



### mergeMap()

讲道理这个没太看懂，官网给的是这样的例子

```js
//将每个字母映射并打平成一个 Observable ，每1秒钟一次
var letters = Rx.Observable.of('a', 'b', 'c');
var result = letters.mergeMap(x =>
  Rx.Observable.interval(1000).map(i => x+i)
);
result.subscribe(x => console.log(x));
```



### switchMap()

也没看懂





***未完待续***