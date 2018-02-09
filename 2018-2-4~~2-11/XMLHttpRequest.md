# XMLHttpRequest

[参考文献1](http://www.ruanyifeng.com/blog/2012/09/xmlhttprequest_level_2.html)  
[参考文献2](https://segmentfault.com/a/1190000004322487)

首先是XMLHttpRequest老版本的用法

```js
var xhr = new XMLHttpRequest();

xhr.open('GET', 'example.php');

xhr.send();

xhr.onreadystatechange = function(){

　　　　if ( xhr.readyState == 4 && xhr.status == 200 ) {

　　　　　　alert( xhr.responseText );

　　　　} else {

　　　　　　alert( xhr.statusText );

　　　　}

　　};
```

* xhr.readyState：XMLHttpRequest对象的状态，等于4表示数据已经接收完毕。

* xhr.status：服务器返回的状态码，等于200表示一切正常。

* xhr.responseText：服务器返回的文本数据

* xhr.responseXML：服务器返回的XML格式的数据

* xhr.statusText：服务器返回的状态文本。

## 老版本的缺点

* 只支持文本数据传输，无法读取和上传二进制文件

* 传送接受数据时候，无进度信息

* 受到同源策略限制

## 新版本的XMLHttpRequest

1. 可设置http请求的时限
2. 可用formdata对象管理表单数据
3. 可以上传文件
4. ***支持跨域***
5. 可以获取服务器端的二进制数据
6. 可获取数据传输的进度信息

~~其中第四条我觉得还挺有意思，详细记录一下，其他的我八成记不住，就先放在这边，有遇到过需求再来补上吧。~~

### 跨域CORS(cross-origin resource sharing)

*前提是浏览器必须支持这个功能*</br>
*目前除了ie8和ie9,其他主流浏览器都支持*</br>
然后写法和普通版本的一样，但是服务器端要进行配置

#### CORS两种请求

简单请求和不简单请求  ~~这名字真蠢~~</br>
满足以下两大条件，就属于简单请求：

1. 请求方法是以下之一：
* HEAD
* GET
* POST
2. HTTP的头信息不超过以下几种字段
* Accept
* Accept-Language
* Content-Language
* Last-Event-ID
* Content-Type(只限三个值:application/x-www-form-urlencoded、multipart/form-data、text/plain)

不是简单请求的就是不简单请求(逃。</br>
浏览器对于这两种请求的处理不同

#### 简单请求

浏览器直接发出CORS请求，即在头信息中，增加一个Origin字段。服务器根据这个值，决定是否同意这次请求。  
若Origin字段中的值，不在服务器许可范围内，***服务器会返回一个正常的http响应***，但这个响应头中没有Access-Control-Allow-Origin，浏览器发现没有这个字段，就会抛出一个错误，被XMLHttpRequest的onerror回调函数捕获
>这种错误无法通过状态码识别，因为HTTP回应的状态码有可能是200

若在服务器允许的范围内，服务器返回的响应，会多几个头信息片段

1. Access-Control-Allow-Origin

* 必须，可能是*，表示接受任意域名请求

2. Access-Control-Allow-Credentials

* 可选，Bool值，true表示允许发送cookie。同时前端开发者也要在ajax中打开withCredentials属性。 默认情况下cookie不包含在CORS请求中。若发送cookie，则Access-Control-Allow-Origin不能设置为*，必须指定明确的，与请求网页一致的域名。同时，Cookie依然遵循同源政策，只有用服务器域名设置的Cookie才会上传，其他域名的Cookie并不会上传，且（跨源）原网页代码中的document.cookie也无法读取服务器域名下的Cookie。

```js
var xhr = new XMLHttpRequest();
xhr.withCredentials = true;
```

3. Access-Control-Expose-Headers  

* 可选，CORS请求时，XMLHttpRequest对象的getResponseHeader()方法只能拿到6个基本字段：Cache-Control、Content-Language、Content-Type、Expires、Last-Modified、Pragma。如果想拿到其他字段，就必须在Access-Control-Expose-Headers里面指定。

##### 不简单请求

这个有点烦躁，怕是记不住，先不记。

## XMLHttpRequest的事件

| 事件 | 触发条件 |
| --- | ---|
|onreadystatechange| 每当xhr.readyState改变时触发，由非0值变为0时不触发|
|onloadstart|xhr.send()执行之后立即触发|
|onprogress|xhr.upload.onprogress在上传阶段(即xhr.send()之后，xhr.readystate=2之前)触发，每50ms触发一次；xhr.onprogress在下载阶段（即xhr.readystate=3时）触发，每50ms触发一次。|
|onload|xhr.readtstate=4时触发|
|onloadend|当请求结束（包括请求成功和请求失败）时触发|
|onabort|当调用xhr.abort()后触发|
|ontimeout|xhr.timeout不等于0，由请求开始即onloadstart开始算起，当到达xhr.timeout所设置时间请求还未结束即onloadend，则触发此事件|
|onerror|在请求过程中，若发生Network error则会触发此事件（若发生Network error时，上传还没有结束，则会先触发xhr.upload.onerror，再触发xhr.onerror；若发生Network error时，上传已经结束，则只会触发xhr.onerror）。注意，只有发生了网络层级别的异常才会触发此事件，对于应用层级别的异常，如响应返回的xhr.statusCode是4xx时，并不属于Network error，所以不会触发onerror事件，而是会触发onload事件|

***成功回调函注册在onload函数中，别问为什么***

### 事件触发顺序

一切正常时：

1. 触发xhr.onreadystatechange(之后每次readyState变化时，都会触发一次)

2. 触发xhr.onloadstart

    //上传阶段开始：

3. 触发xhr.upload.onloadstart

4. 触发xhr.upload.onprogress

5. 触发xhr.upload.onload

6. 触发xhr.upload.onloadend

    //上传结束，下载阶段开始：

7. 触发xhr.onprogress

8. 触发xhr.onload

9. 触发xhr.onloadend
