# Grid布局

网格布局，和flex布局结合使用是最好的布局解决方案。

## 基本概念

### 网格容器(grid container)

```css
.anycontainer{
    display:grid
}
```

通过以上属性将任意容易定义为一个网格容器

### 网格项(grid item)

>网格容器内部的所有子元素都是网格项，但是网格项的子元素不属于网格项

### 网格线(grid line)

>就是分割网格的线，包围网格容器的也叫网格线

### 网格轨道(grid track)

>两条相邻平行网格线之间的空间，可能包含多个网格单元格，就是网格轨道

### 网格单元格 (grid cell)

>就是一个不可再分割的方块，我不想再用形式化语言描述了

### 网格区域(grid area)

>四条网格包围的总空间，一个四边形，可能包含多个网格单元格

## 网格属性

1. display  grid||inline-grid||subgrid 定义网格容器的属性
2. grid-template-columns/rows 定义网格容器的列行细节

```html

<div style="
    display: grid;
    grid-template-columns: 100px 50px 150px;
    grid-template-rows: 50px 80px 100px;
">


    <div style="background-color:black"></div>
    <div style="background-color:orange"></div>
    <div style="background-color:green"></div>
    <div style="background-color:red"></div>
    <div style="background-color:yellow"></div>
    <div style="background-color:blue"></div>
</div>

```

***md好像不支持gird属性啊，这里展示不了，先放着吧，看样子恐怕这个玩意儿普及率不高***
