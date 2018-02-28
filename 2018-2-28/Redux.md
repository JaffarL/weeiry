# Redux学习

---

[TOC]



## 原则

1. 唯一数据源 store
2. 数据状态保持只读
3. 数据状态修改只可以通过定制的纯函数实现 dispatch分发消息，reducer根据收到的消息派生出下一个状态



## 基础使用

1. 状态对象state

```js
const initValues={
    'First':0,
    'Second':10,
    'Third':20
}
```

2. 规约函数reducer,根据actions计算新的state

```js
function reducer(state=0,action){
    switch(action.type){
        case 'ADD_GUN':
            return state+1;
        case 'DELETE_GUN':
            return state-1
        default:
            return state
    }
}
```

3. 动作对象aciton

```js
const action = {
    type:'ADD_GUN'
    payload:'someMessage'
}
```

4. store创建器

```js
const store = createStore(reducer,initValues)
```

5. 动作对象生成器action creator，一个根据入参生成action的函数

```js
function addGun(){
    return {type:'ADD_GUN'}
}
```

6. 动作派发器store.dispatch，是view发出action的唯一方法

```js
store.dispatch({
    type:'ADD_GUN'
    payload:'someMessage'
})
```

7. 状态监听器subscribe

```js
store.subscribe(someFun)
```

当store内部状态变化时会触发someFun函数，在react中一般将setState等触发渲染函数放进去

8. 状态获取函数`getState()`，获取store内部目前的状态

```js
const state = store.getState()
```



## 如何使用异步redux

1. 安装redux-thunk
2. 使用applyMiddleware开启中间件
3. **可以使用action返回一个函数了，而不是对象**

```js
const store = createStore(reducer,applyMiddleware(thunk))
// some operations
function async(){
    return dispatch=>{
        setTimeout(()=>{
            dispatch(addGun())
        },1000)
    }
}
```



## Chrome中安装redux调试插件

翻墙进扩展找redux安装，然后

```js
const reduxDevtools = window.devToolsExtension?window.devToolsExtension():f=>f//判断是否存在redux调试插件
const store = createStore(reducer,compose(   //compose合并中间件
	applyMiddleware(thunk),
    reduxDevTools
))
```



## React-redux

### 简单说明

1. 需额外安装react-redux
2. 不再需要subscribe这种接口
3. Provider：用这个组件把所有组件都包起来，传入store，只需一次
4. Connect：从外部获得state数据以及派发函数，此函数可以用装饰器方式来写

### connect函数

1. 第一个参数：

```js
const mapStatetoProps(state){
    return {num:state}
}
```

返回一个store中state映射/抽取到此组件需要的state的的对象，作为props属性传入

2. 第二个参数：

```js
const actionCreators = {addGun,removeGun,addGunAsynv}
App = connect(mapStatetoProps,actionCreators)(App)
```

一个包裹所有要传递给该组件的派发函数的对象，派发函数作为props的属性传入

3. 此函数传进组件的函数不需要subscribe
4. 装饰器模式需要安装`babel-plugin-transform-decorators-legacy`并在webpack的babel中配置

```json
"babel":{
    "plugin":["tranform-decorators-legacy"]
}
```