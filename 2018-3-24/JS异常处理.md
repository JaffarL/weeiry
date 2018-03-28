# JS异常处理

[TOC]

## JS运行时错误

包括语法错误，`window`对象会触发一个`ErrorEvent`接口的`error`事件，并执行`window.onerror()`

## 资源加载时错误

例如<img>和<script>标签加载失败时，加载资源的标签元素会触发一个`event`接口的`error`事件，并执行其上的`onerror()`处理函数，并且这个事件不会冒泡到`window`上

## 错误捕捉方法

```js
window.onerror = function(message,source,lineNo,colNo,error){...}
```

- `message`:：误信息，是字符串
- `source`：发生错误的脚本url
- `lineNo`：错误行号
- `colNo`：错误列号
- `error`：`error`对象

*若该函数返回`true`，则阻止执行默认事件处理函数*？？ 没懂



```js
window.addEventListener('error',function(event){
    ...
})
```



```js
element.onerror = function(event){
    ...
}
```



## 跨域脚本错误

当跨域加载来的脚本发生运行错误(语法错误)时，为了避免信息泄露，浏览器不会报告错误的细节，取而代之的是一个简单的字符串“Script error”，但我们需要知道这条错误信息怎办

1. 前端`script`标签中增加`crossorigin属性`，值为`anonymously`
2. 提供脚本的服务器中添加允许跨域的http头`Access-Control-Allow-Origin:*`

### 可替代方案

使用`try/catch`测试我们调用的外部脚本里的函数