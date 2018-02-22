# CSS知识1

## 元素

* 常见块级元素：div，p，form，ul，ol，li


* 常见行内元素：span，em，strong


特点：
1. 块级元素独占一行且占满父元素宽度；行内元素不独占一行，相邻行内元素排在同一行
2. 块级元素可以设置宽高，但依然独占一行；行内元素设置width,height无效
3. 块级元素可以设置margin,padding；行内元素水平方向的margin,padding可以设置，垂直无效
4. 可以使用`display:block`或者`display:inline`来手动设置标签为块状元素或者行内元素，还有`display:inline-block`来使元素同时具有块状和行内元素的特性，又可设置宽高又可与其他元素并排

*置换元素：img，可以为其设置宽高，marging属性起作用*

## 定位

1. 相对定位`position:relative`
  是普通流定位模型的一部分，定位元素的位置相对于他在普通流中的位置移动，使用相对定位的元素无论它是否移动，仍要占据原来的位置，移动此元素会导致它覆盖其他框
2. 绝对定位`position:absolute`
  相对已定位的最近的祖先元素，若没有，就相对最初的包含块(如body)。脱离普通流，可覆盖页面上其他元素，设置z-index来控制此框的堆放次序
3. 固定定位`position:fixed`
  相对于浏览器窗口的绝对定位
4. 静态定位`position:static`
  默认位置属性
5. 浮动`float` 
  将元素排除在普通流之外，将其放在包含框的左边或者右边，但依旧在包含框之内

> *已定位：即position值不为static*

## 浮动以及如何清除浮动

* 元素浮动之后不会影响块级元素布局，只影响内联元素布局(???)
* 问题：当包含框的高度小于浮动框的时候，会出现高度塌陷

解决方案：

1. 在塌陷父元素的尾部添加冗余元素并设置其clear:both；缺点是页面中添加许多冗余元素，此方案不优美
2. 伪元素，添加类

```css
.clearfix: after{
    display:block;
    clear:both;
    content:'';
    overflow:hidden;
    height:0
}
```

3. 将父元素变为BFC

> clear属性：规定元素那一侧不允许出现浮动元素



## BFC

> Block Formatting Contexts(块级格式化上下文)，属于普通流范围

### 如何触发BFC

1. body根元素(没懂)
2. 浮动，即float值不为none
3. 对元素进行绝对定位：position:absolute/fixed
4. overflow值不为visible(hidden,auto,scroll)  ***建议使用`overflow:hidden`来触发BFC***
5. display值为inline-block,table-cells,flex中任意一个

### 应用

1. 避免外边距重叠，将发生外边距重叠的两个元素分别设置为两个不同的BFC
2. 清除浮动，将发生高度塌陷的父元素设置为BFC
3. 阻止元素被浮动元素覆盖，可以实现左边固定一个浮动元素，右边自适应宽度的两栏布局

### BFC特点总结

1. BFC内部的box会在垂直方向一个接一个的放置
2. box垂直方向的距离由margin决定，属于同一个BFC的两个相邻box的margin还是会重叠
3. BFC区域不会与浮动元素重叠
4. BFC是一个独立的容器，其中的内部元素与外部元素相互之间会有影响
5. BFC计算高度时，浮动元素也会计算在内



## CSS盒模型

1. content:内容
2. padding:填充/内边距，框内容与边框之间的空间
3. margin:边距/外边距，边框与相邻边框之间的距离
4. border:边框

CSS盒模型还分了两种：标准模型和IE模型

* 标准模型中，css属性的宽高指的是content的宽高
* ie模型中css属性宽高包括了content,border和padding的宽高

*可以通过设置`box-sizing:content`(标准模型)，或者`box-sizing:boder-box`(IE模型)来手动指定该元素是哪种模型，浏览器默认是标准模型*