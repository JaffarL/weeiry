# 神奇的THIS

今天看了班主任发的一篇关于this的周报。。嗯。。~~废话太多太啰嗦，100个字能说完的事非要用1000个字~~我觉得写的很好，但我看完还是很懵，就自己再整理了一波。  
先摆结论：

1. 函数内部的this是函数运行时调用它的对象
2. 匿名函数，异步队列中的函数，直接调用的函数都属于裸奔的函数
3. 裸奔的函数调用里的this在浏览器中是window对象，在node下是global对象
4. 可以通过apply,call,bind,箭头函数等方式改变函数运行时里面的this  
5. bind绑定的this对象在后期调用时不可改变

直接看代码：

```js
var test = {
    xx : 'xx',
	 fu:function(){
	 	console.log(this)    
	 	var fu3 = function(){
	 		console.log(this==global)
	 		function f4(){
	 	            console.log(this==global)  
	 		}
	 		f4()
	 	}
	 	fu3()
	 },
	 fu2:function(){
	 	this.fu()
	 }
}
test.fu2()
var test2 = test.fu
test2()
```

输出内容是

```js
test
true
true
global
true
true
```

fu3,fu4函数虽然是在对象内部被调用，但是依然属于裸奔函数，所以this指向global
fu第一被调用时this指的是test对象，因为外部是由test对象调用的
fu第二次被调用时因为被暴露到全局环境下，所以this指向global对象


再看第二段代码：

```js
var test={
	t1:{
		t2:function(){
			console.log(this)
		},
		t3:this
	},
	}
}

test.t1.t2();
console.log(test.t1.t3)
```

输出：

```js
t1
t3
```

感觉这个挺好理解
再看一段代码

```js
new Promise((res,rej)=>{
	console.log('before then',this)   //{}
	res()
}).then(res=>{
	console.log('then',this) 	//{}
})


new Promise(function(res,rej){
	console.log(this==global)   //global
	res()
}).then(function(res){
	console.log(this==global) 	//global
})

setTimeout(()=>{
	console.log(this)       //{}
},0)

```

在浏览器中输出全部都是window
而在node环境下则输出注释中的内容
箭头函数绑定了一个空对象，这个空对象就是当前文件作用域下的全局对象，可参考[这篇文章](关于Node的global变量.md)。

```js
setTimeout(function(){
	console.log(this)       //Timeout
},0)

```

这行代码输出的是一个Timeout对象，有点奇怪，改一下。

```js
this.x = setTimeout(function(){
	console.log(this)
},0)
console.log(this)
```

此时全局下输出的this中有一个x对象，x对象中还有一个timeout对象。
我认为应该是setTimeout函数会自己创建一个Timeout对象并复制给匿名函数中的this，而箭头函数中则直接绑定文件作用域对象。
