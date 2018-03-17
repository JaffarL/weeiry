# Fetch API 学习

[TOC]

本周对工作中的项目代码的一部分进行重构，其中很重要的一部分是合并请求次数，用到了fetch() API，用起来发现和想象中的稍微有点不一样，在这里做点笔记

## 首先

第一眼看到的fetch大概是长这个样子：

```js
fetch('https://www.baidu.com/search/error.html') // 返回一个Promise对象
  .then((res)=>{		
    return res.text() // res.text()是一个Promise对象
  })
  .then((res)=>{		
    console.log(res) // res是最终的结果
  })
```

我在使用的时候以为第二个then是有什么业务逻辑操作的时候才会使用的，但实际上发现并非如此，fetch使用连续两个then是必须的

* fetch函数返回一个promise，所以连着直接使用then
* 这返回的第一个promise中的resolve值，即$1处的值，是一个response对象

这个response对象中，挂载了许多解析服务器传回来的数据的函数，而服务器传回来的数据类型，也可以由fetch API来指定

## 数据类型

官网上有多种数据类型，包括

1. `ArrayBuffer`
2. `ArrayBufferView`
3. `Blob/File`
4. `string`
5. `URLSearchParams`
6. `FormData`

每种数据都有对应的函数将其格式化出来

1. `arrayBuffer()`
2. `blob()`
3. `json()`
4. `text()`
5. `formData()`

string类型对应的格式化函数毫无疑问应该是`text()`，而除了`json()`以外的其他函数我都没看出来是什么应用场景，所以以后遇到的话再来补充吧

## 使用

```js
fetch(url,{
            method: 'GET',   
            headers: new Headers({
                Accept: 'application/json'
            })
        }
    )
        .then((reso1,rej1)=>{   //#1
            return reso1.json()
        })
        .then((reso2,rej2)=>{   //#2
        	console.log(reso2)
        })
```



`fetch()`第二个参数指定了此次请求的option，方法是`GET`，数据头中指示了接受的数据类型是json，后端对应的路由代码就可以可以直接返回一个对象

```js
app.get(url,(req,resp)=>{
    resp.send({
        data:'hello you idot'
    })
})
```

到了前端，#1处将返回的promise拿出来并做json处理并返回给下一个promise，#2处再将一返回的值取出来，此时这个reso2就是后端返回的对象，非常好用。



***未完待续***