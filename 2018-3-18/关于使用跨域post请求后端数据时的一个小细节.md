# 关于使用跨域post请求后端数据时的一个小细节

今天用fetch进行跨域POST请求的时候遇到一个小问题，fetch的第二个参数对象里面的body属性已经赋值了，但是后端里的`req.body`一直都是空，一直都不知道为什么

首先是在后端的express路由里加了`bodyparser`中间件以获得`req.body`，接着前段的参数对象里增加`mode:cors`,修改body属性值的类型，各种都不行

后来抗抗说他实现了，我就看了一下，发现是这个玩意儿出了问题

首先前端要用`Content-Type`说明自己传输的数据的类型，我接触到的有这么两种：

`application/json`，还有一种很复杂的大概长这个样子的类型`application/xxxx-form-urlencode`

相对应的传输的body属性类型是不同的

同样，在后端使用`body-parser`时也是不同的

第一种对应`bodyparser.json()`,，第二种对应`bodyparser.urlencode()`，这样才能在`req.body`中获得我们POST传过去的值



可能还有别的需要注意的点，以后遇到再补充吧。