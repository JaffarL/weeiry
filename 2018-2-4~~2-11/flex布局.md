# FLEX布局

~~一直对CSS布局不熟悉，在这里就认真学习一波~~  
flex中文名弹性布局，任何容器都可以通过指定CSS标签中的display属性而将其设置为弹性布局

```css
.anycontaniner{
    display:flex
}
```

>*设置为flex布局以后，子元素的floar,clear,vertical-align属性将失效*

## 基本概念

采用flex布局的元素被称为flex容器(flex container)，它的所有子元素自动成为容器成员，称为flex项目(flex item)，简称'*项目*'~~真难听~~  
flex容器存在两根轴，水平的主轴(**main axis**)和垂直的交叉轴(**cross axis**)。主轴的开始位置，即与边框的相交点称作**main start**，结束位置叫做**main end**。同理，交叉轴有**cross start**，和**cross end**。
*项目*默认是沿主轴排列。单个项目占据的主轴空间叫**main size**，占据的交叉轴空间叫**cross size**

## 容器属性

1. flex-direction 决定主轴的方向
2. flex-wrap 定义若轴线排不下如何换行
3. flex-flow 是1和2的简写形式
4. justify-content 定义项目在主轴上的对齐方式
5. align-items 定义项目在交叉轴上如何对齐
6. align-contetn 定义多根轴线的对齐方式(黑人问号)

## 项目属性

1. order 项目排列顺序的权重值，数值越小越靠前，默认0
2. flex-grow 项目的放大比例，默认0即不放大
3. flex-shrink 项目的缩小比例，默认1即若容器空间不足将缩小
4. flex-basis 分配多余空间之前，项目占据的主轴空间，默认auto，即项目的本来大小(?黑人问号)
5. flex 是2,3,4的合并简写，默认 0 1 auto,快捷设置auto(1 1 auto),以及none(0 0 auto)。后两个属性可选
6. align-self 允许单个项目与其他项目不同的对齐方式，可覆盖align-items属性，默认auto，表继承父元素的align-items，若无父元素则等同于*stretch*

## 简单实例

* 以下代码实现两边固定，中间弹性伸缩的块级布局

```html
<div style='display:flex;width:100%;height:100px;'>

<div style="width:30px;background-color:red"></div>
<div style="flex:auto;background-color:blue"></div>
<div style="width:30px;background-color:yellow"></div>

</div>

```

<div style='display:flex;width:100%;height:100px;'>

<div style="width:30px;background-color:red"></div>
<div style="flex:auto;background-color:blue"></div>
<div style="width:30px;background-color:yellow"></div>

</div>


* 以下代码实现一个内容居中的div元素

```html
<div style="width:150px;
    height:150px;
    background-color:black;    
    display:flex;
    justify-content:center;
    align-items:center;">
<div style="
    background-color:white;
    width:50%;
    height:50%;">
    </div>
</div>

```



<div style="width:150px;
    height:150px;
    background-color:black;    
    display:flex;
    justify-content:center;
    align-items:center;">
<div style="
    background-color:white;
    width:50%;
    height:50%;">
    </div>
</div>

[参考资料](http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html)



