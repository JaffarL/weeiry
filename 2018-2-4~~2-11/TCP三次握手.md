[参考文献](https://juejin.im/post/5a7835a46fb9a063606eb801?utm_source=gold_browser_extension)
</br>
# TCP三次握手
~~这玩意儿好无聊,计算机网络课时候就说过,我总记不住,因为太无聊了,留个印象,需要解决问题的时候别忘掉,然后用到的时候直接百度一下不就好了么,然而面试貌似总会考,我ca,好吧我还是详细记一下吧~~


### 细节
1.  client发送同步信息给server,携带信息syn(seq=j),本身进入syn-sent状态
2.  server收到之后返回确认包,携带信息ack(seq=j+1),syn(seq=k).server进入syn-received状态
3.  client收到ack(seq=j+1)后,进入established状态,然后因为收到syn(seq=k),所以再返回一个ack(seq=k+1)包.server收到此信息后再把自己的状态设置为established状态.结束 
***

### 为什么要三次握手 
1. 第一次握手,server确认client的发信能力正常
2. 第二次握手,client确认server的收发能力正常
3. 第三次握手,server确认client的收信能力正常
***

