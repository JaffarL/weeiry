# Http缓存机制

## http报文中与缓存相关的首部字段

1. 通用首部字段

|字段名|说明|
|:--------:|:--------:|
|Cache-control|控制缓存的行为|
|Pragma|http1.0的遗产，值为‘no-cache’时禁用缓存|

2. 请求首部字段

|字段名|说明|
|:--:|:-:|
|If-Match|比较ETag是否一致|
|If-None-Match|比较ETag是否不一致|
|If-Modified-Since|比较资源最后更新时间是否一致|
|If-Unmodified-Since|比较资源最后更新时间是否不一致|

3. 响应首部字段

|字段名|说明|
|:--:|:-:|
|ETag|资源的匹配信息|

4. 实体首部字段

|字段名|说明|
|:--:|:-:|
|Expires|http1.0的遗产，实体主体过期的时间|
|Last-Modified|资源的最后一次修改时间|

## Pargma

当该字段值为‘no-cache’时，通知客户端不对该资源进行缓存。
Pragma是通用首部字段，在客户端使用时得这样
`<meta http-equiv="Pragma" content="no-cache">`
但这种禁用缓存的方式有比较大的局限性
- 只有IE认得这段Meta标签含义
- IE中识别到该meta标签时，并不一定会在请求字段上加Pragma，但的确会让当前页面每次都发新请求（仅限页面，页面上的资源不受影响）。也就是IE浏览器看到页面有这个属性就会禁用缓存，但是并不会在Http消息报头中增加这个属性。

## Expires

Pragma用来禁用缓存，Expires是用来启用缓存，定义缓存时间的字段。同样也只有IE认得这个字段。
`<meta http-equiv="expires" content="mon, 18 apr 2016 14:30:00 GMT">`
也可以把content里的内容改为-1或者0来使每次刷新页面都发新请求。
如果在服务端返回的报头中返回expires字段，那么在任何浏览器中都能正确设置资源缓存的时间。
如果Pragma和Expires都设置并且冲突的话，则以Pragma为准。并且Expires是以服务器上的时间为准，与服务器端时间不统一，会出现问题。

## Cache-Control

http1.1新增Cache-Control来定义缓存

