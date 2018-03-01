# Redux 基本原理/简单实现

---

[TOC]



## createStore

```js
export function createStore(reducer){
    let currentState = {}  //当前状态
    let currentListeners = [] //当前的监听器
    
    function getState(){
        return currentState
    }
    function subscribe(listener){
        currentListeners.push(listener)
    }
    function dispatch(action){
        currentState = reducer(currentState,action)
        currentListeners.forEach(v=>v())	//监听函数都运行一遍
        return action
    }
    dispatch({type:'@LYZ/REDUX'})//触发一次，给一个初始状态
    return {getState,subscribe,dispatch}
}
```

## Context

```jsx
import React from 'React'
import PropTypes from 'prop-types'//Context对数据类型是强校验的
class Sidebar extends React.Component{
    render(){
        return (
        <div>
            <p>Sidearbar</p>
        	<Navbar></Navbar>
        </div>
            	)
    }
}
class Navbar extends React.Component{
    static contextTypes = {   //声明数据类型
        'user':PropTypes.string
    }
    render(){
        return (
            <div>{this.context.user}'NavBar</div>   //从context获取数据
        )
    }
}
class Page extends React.Component{
    static childContextTypes = {    //在父元素也要声明子元素获取的数据类型
        'user':PropTypes.string
    }
    constructor(props){
        super(props)
        this.state = {user:'lyz'}
    }
    getChildContext(){			//将数据用context传出去
        return this.state
    }
    render(){
        return(
            <div>
                <p>I'm {this.state.user}</p>
                <Sidebar></Sidebar>
            </div>
        )
    }
}

```

若子元素是无状态组件，则函数声明是

```jsx
function Navbar(props,context){
    //todo
}
```

函数第一个参数是props，第二个参数是context

## react-redux基本原理/简单实现

### Provider

```jsx
class Provider extends React.Component{
    static childContextTypes = {
        store:ProtoTypes.object
    }
    getChildContext(){   //将store传进context
		return {store:this.store}
    }
	constructor(props,context){
    	super(props,context)
        this.store = props.store
	}
	render(){
    	return this.props.children
	}
}
```

### Connect

1. 负责接收一个组件，把state数据放进去并返回一个组件
2. 数据变化的时候，通知组件

```jsx
//辅助函数
function bindActionCreator(creator,dispatch){
    return (...args)=>dispatch(creator(...args))
}
//每个actionCreator外面包一层store.dispatch函数
function bindActionCreators(creators,dispatch){
    let bound = {}
    Object.keys(creators).forEach(v=>{
        let creator = creators[v]
        bound[v] = bindActionCreator(creator,dispatch)
    })
    return bound
}


export const connect = (mapStateToProps=>state,mapDispatchToProps={})=>(WrapComponent)=>{  //
    return class ConnectComponent extends React.Component{
        static contextTypes = {
            store:PropTypes.object
        }
        constructor(props,context){
			super(props)
            this.state={
                props:{}
            }
        }
        componentDidMount(){
            const {store} = this.context
            store.subscribe(()=>this.update())
            this.update()
        }
        update(){
			const {store} = this.context
            const stateProps = mapStateToProps(store.getState())
            //方法不能直接塞进去，因为需要diapatch
            const dispatchProps = bindActionCreators(mapDispatchToProps,store.dispatch)
            this.setState({
                props:{
                ...this.state.props		//原本的状态
                ...stateProps,   //状态
                ...dispatchProps,  //函数
                }
            })
        }
        render(){
			return <WrapComponent>{...this.state.props}</WrapComponent>
        }
    }
}
/**   
export function connect(mapStateToProps,mapDispatchToProps){
    return function(WrapComponent){
        return class ConnectComponent extends React.Component{
            
        }
    }
}**/
```



## 中间件

### applyMiddleware

先扩展creatStore

```js
export function createStore(reducer,enhancer){//第二个参数是中间件
    if(enhancer){
        return enhancer(createStore)(reducer)
    }
    let currentState = {}  //当前状态
    let currentListeners = [] //当前的监听器
    
    function getState(){
        return currentState
    }
    function subscribe(listener){
        currentListeners.push(listener)
    }
    function dispatch(action){
        currentState = reducer(currentState,action)
        currentListeners.forEach(v=>v())	//监听函数都运行一遍
        return action
    }
    dispatch({type:'@LYZ/REDUX'})//触发一次，给一个初始状态
    return {getState,subscribe,dispatch}
}

export function applyMiddleware(middleware){
    return createStore=>(...args)=>{
        const store = createStore(...args)
        let dispatch = store.dispatch
        const midApi = {					//科里化
            getState:store.getState,
            dispatch:{...args}=>dispatch(...args)
        }
        dispatch = middleware(midApi)(store.dispatch)
        return {
            ...store,
            dispatch
        }
    }
}
```

### Middleware

#### thunk中间件实现

```js
//此中间件即applyMiddleware函数的参数middleware
const thunk = ({dispatch,getState})=>next=>action=>{
    //如果是函数，则执行并将参数传入
    if(typeof action=='function'){
        return action(dispatch,getState)
    }
    //若是对象，则什么都不干...
    return next(action)
}
```

### 中间件合并 compose函数

```js
export function applyMiddleware(middlewares){  //参数名加了一个s
    return createStore=>(...args)=>{			//科里化
        const store = createStore(...args)
        let dispatch = store.dispatch
        const midApi = {					
            getState:store.getState,
            dispatch:{...args}=>dispatch(...args)
        }
        //dispatch = middleware(midApi)(store.dispatch)
        const middlewareChain = middlewares.map(middleware=>middleware(midApi))
        dispatch = compose(...middlewareChain)(store.dispatch)
        return {
            ...store,
            dispatch
        }
    }
}
export function compose(...args){
    if(args.length==0){
        return arg=>arg
    }
    if(args.length==1){
        return args[0]
    }
    return args.reduce(
        (ret,item)=>
        (...args)=>
        ret(item(args))				//f1(f2(f3()))
    )
}
```