# react性能优化

---

[TOC]

## React组件性能优化

### 1. 单组件属性传递优化

事件绑定有3种方式：

* 在constructor中
* 箭头函数
* bind()函数

bind()函数在每次渲染时都会执行，这是一个性能隐患

箭头函数的情况在于每次render时事件绑定函数会重新生成

避免在render时重新渲染时生成不需要重新生成的对象

**推荐使用constructor的写法**

### 2. 多组件优化

父组件的state发生变化触发重新渲染导致所有子组件重新渲染，但是传递给某个子组件的state中不包含变化的state属性，即这个子组件其实并不需要重新渲染。

1. 在url后增加/?react_pref可以对react性能优化进行监控
2. chrome perfomance
3. user timing
4. 查看react每个生命周期消耗的性能

在子组件的`shouldComponentUpdate(nextProps,nextState)`中判断state是否遭到了修改，来决定返回值，**pure-component**

但是在比较新旧state的时候会遇到深浅拷贝的问题，而每次渲染都用自实现的深度递归对比复杂度太高，不可接受，所以react官方建议只做浅层比较，所以我们在设计state结构的时候尽量不要深层嵌套

#### immutable.js

如果不得不使用复杂的数据结构，请并且作对比，那可以参考immutable.js，最简单的就是非常轻便的实现对象深度对比

优点：

1. 减少内存使用
2. 并发安全
3. 降低项目复杂度
4. 便于比较复杂数据，定制shouldComponentUpdate
5. 时间旅行功能方便(??)
6. 函数式编程

缺点：

1. 学习成本
2. 库的大小(seamless-immutable.js比较小，可以参考使用)
3. 对现有项目入侵严重：老项目就别改了，新项目可以用

### 3. key值设置

渲染平级数组dom结构的时候需要增加key值，内部diff算法优化，key值尽量不要用数组索引

## Redux性能优化

利用`reselect`实现redux数据缓存(*备忘录设计模式*？？)

## React同构

服务器端渲染，前后端同构，首屏服务端渲染速度快，对seo友好

1. node使用babel-node配置node里的react环境
2. 修改客户端代码，首屏组件抽离，前后端共享
3. 服务端生成dom结构

### 实战

1. 安装babel-cli，利用其中的babel-node，使得node支持ES6语法，在package.json的标签中增加script，`npm run server-node`

```json
"server-node": "NODE-ENV=test nodemon --exec babel-node -- server/server.js"
```

2. 在根目录下创建`.babelrc`文件，将package.json中的babel配置拷贝进去，使得node支持jsx语法，**不需要"babel"键，只需要值**
3. 借助`ReactDomServer`中的`renderToString()`和`renderToMarkup()`方法实现后端渲染页面，主要使用`renderToString()`将react组件转化成原生html代码并发给前端

#### 客户端代码改造

将能复用的代码抽离出来放进app.js文件中(AuthRoute包裹下的所有组件)

#### 服务端代码改造

1. import相应的组件
2. server端用staticRouter取代BrowserRouter，需要额外配置
3. index.js中的Provider组件下内容以及redux代码放到server端
4. 安装css-modules-require-hook来设置node中支持css，配置参考github，记得这个玩意儿在别的前端库import之前import
5. 安装asset-require-hhok来使得node支持图片等其他静态资源，配置参考github，也要在前面import
6. 将/build/public/index.html中的html代码拉到Node中，把`renderToString()`的结果丢进去
7. 动态获取css，js文件地址`import staticPath from '../build/assets-manifest.json'`，并在html中引入`<link></link>,<script></script>`什么的

## React16新特性

1. render可以直接返回数组和字符串，但一定要有key
2. 新的错误处理机制=>`componentDidCatch(err,info)`生命周期
3. Protals组件
4. 更好更快的服务端渲染`renderToNodeStream`，后端服务端渲染代码需要修改，前端`render()`改成`hydrate()`