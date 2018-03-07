# webpack打包原理

webpack是如何在内部实现对js文件的模块化的，这里尝试做一些分析，仅限js文件

## 入口文件代码

首先是写两个测试文件

m.js文件

```js
// m.js
'use strict';
export default function bar () {
    return 1;
};
export function foo () {
    return 2;
}
```

index.js文件

```js
// index.js
'use strict';
import bar, {foo} from './m';
bar();
foo();
```

然后简单配置一下webpack

```js
var path = require("path");
module.exports = {
    entry: path.join(__dirname, 'index.js'),
    output: {
        path: path.join(__dirname, 'outs'),
        filename: 'index.js'
    },
};
```

## 打包完成的代码

执行webpack之后得到的代码如下，这里去掉了一些没用的注释(不同webpack版本可能有细微的差异)

```js
(function(modules) { // webpackBootstrap
    // The module cache
    var installedModules = {};
    // The require function
    function __webpack_require__(moduleId) {
        // Check if module is in cache
        if(installedModules[moduleId]) {
            return installedModules[moduleId].exports;
        }
        // Create a new module (and put it into the cache)
        var module = installedModules[moduleId] = {
            i: moduleId,
            l: false,
            exports: {}
        };
        // Execute the module function
        modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
        // Flag the module as loaded
        module.l = true;
        // Return the exports of the module
        return module.exports;
    }
    // expose the modules object (__webpack_modules__)
    __webpack_require__.m = modules;
    // expose the module cache
    __webpack_require__.c = installedModules;
    // define getter function for harmony exports
    __webpack_require__.d = function(exports, name, getter) {
        if(!__webpack_require__.o(exports, name)) {
            Object.defineProperty(exports, name, {
                configurable: false,
                enumerable: true,
                get: getter
            });
        }
    };
    // getDefaultExport function for compatibility with non-harmony modules
    __webpack_require__.n = function(module) {
        var getter = module && module.__esModule ?
            function getDefault() { return module['default']; } :
            function getModuleExports() { return module; };
        __webpack_require__.d(getter, 'a', getter);
        return getter;
    };
    // Object.prototype.hasOwnProperty.call
    __webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
    // __webpack_public_path__
    __webpack_require__.p = "";
    // Load entry module and return exports
    return __webpack_require__(__webpack_require__.s = 0);
})
([
(function(module, __webpack_exports__, __webpack_require__) {

    "use strict";
    Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
    /* harmony import */
    var __WEBPACK_IMPORTED_MODULE_0__m__ = __webpack_require__(1);

    Object(__WEBPACK_IMPORTED_MODULE_0__m__["a" /* default */])();
    Object(__WEBPACK_IMPORTED_MODULE_0__m__["b" /* foo */])();

}),
(function(module, __webpack_exports__, __webpack_require__) {

    "use strict";
    /* harmony export (immutable) */
    __webpack_exports__["a"] = bar;
    /* harmony export (immutable) */
    __webpack_exports__["b"] = foo;

    function bar () {
        return 1;
    };
    function foo () {
        return 2;
    }

})
]);
```

### 结构分析

首先这是一个匿名的立即执行函数(IIFE)，将函数体去掉后大概长这个样子：

```js
(function(modules) {
    //TODO
}([fn1,fn2])
```

而代码中的`fn1,fn2`则是将入口文件的代码封装在其中的匿名函数，并将其中的模块化`require`或者`import`方法重写了

`fn`的形式一般为

```js
function(module, __webpack_exports__, __webpack_require__){
    //模块文件源代码
}
```

### IIFE主要逻辑

这个立即执行函数中最重要的就是`__webpack_require__`了，IIFE执行之后第一件事是创建了一个对象

`var installedModules = {};`

用来缓存模块标记，接着直接定义了`__webpack_require__`函数

然后在`__webpack_require__`函数对象上增加了许多属性，就我们这个项目来看这些属性好像没派上用场

紧接着IIFE就返回了

```js
return __webpack_require__(__webpack_require__.s = 0)
```

返回的是`__webpack_require__`的函数运行返回值，传递的参数是0，那么我们来看一下这个函数的运行逻辑

### `__webpack_require__`实现分析

这个函数不长，所有代码可以直观地看到

```js
function __webpack_require__(moduleId) {
        // Check if module is in cache
        if(installedModules[moduleId]) {
            return installedModules[moduleId].exports;
        }
        // Create a new module (and put it into the cache)
        var module = installedModules[moduleId] = {
            i: moduleId,
            l: false,
            exports: {}
        };
        // Execute the module function
        modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
        // Flag the module as loaded
        module.l = true;
        // Return the exports of the module
        return module.exports;
    }
```

1. 随着我们第一次调用，传入的参数`moduleId`是0，对IIFE入口的对象变量进行条件判断，很显然结果为false，不返回，向下走
2. 初始化`installedModules`的`moduleId`属性，这里即0属性，`i`大概代表`id`，`l`代表`load`，`exports`初始化为空，是为了实现模块化的`exports`属性，并将此属性值赋值给一个新创建的对象变量`module`
3. 这时候要记得我们IIFE执行时候传入的参数名是`modules`，而实参是一个函数对象数组，所以语句`modules[moduleId].call(module.exports, module, module.exports, __webpack_require__)`(`moduleId`为0)就是调用传入的第一个函数，而参数就是，就是刚才定义的一系列变量，现在再去看第一个参数函数是什么样子

```js
(function(module, __webpack_exports__, __webpack_require__) {

    "use strict";
    Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
    /* harmony import */
    var __WEBPACK_IMPORTED_MODULE_0__m__ = __webpack_require__(1);

    Object(__WEBPACK_IMPORTED_MODULE_0__m__["a" /* default */])();
    Object(__WEBPACK_IMPORTED_MODULE_0__m__["b" /* foo */])();

})
```

4. 这个函数执行首先在`__webpack_exports__`上定义了一个属性，貌似是为了区分commonjs的模块化和es6的模块化用的，我们这里么作用，然后给一个变量赋值，值是`__webpack_require__(1)`，又回头调用`__webpack_require__`了，只不过这次传的值是1
5. 和之前一样，一直到`modules[moduleId].call(module.exports, module, module.exports, __webpack_require__)`，调用函数数组里第二个参数函数，看一下是什么

```js
(function(module, __webpack_exports__, __webpack_require__) {
    "use strict";
    /* harmony export (immutable) */
    __webpack_exports__["a"] = bar;
    /* harmony export (immutable) */
    __webpack_exports__["b"] = foo;

    function bar () {
        return 1;
    };
    function foo () {
        return 2;
    }
})
```

函数逻辑就是将内部定义的两个导出函数挂在函数入参`__webpack_exports__`上，这个入参在函数外部是什么？回头看一下其实就是`module.exports`

6. 接着`moduleId`为1的`__webpack_require__`函数返回一个带有两个属性的对象，第一个参数函数，执行其中的两个函数，函数退出
7. 将`module`的加载标记置为true，并返回此模块文件的导出属性

至此，这个很简单的模块打包原理就分析完了。

### 后记

我看文章说还有commonjs模块实现，以及混合使用时候的模块化方案，但`__webpack_require__`这个函数的实现方法是一样的

我比较迷的是什么时候是使用commonjs规范，我看我即使使用的全是require，不用import，打包出来的源文件依然是es6的样子，这里不太懂了

[参考资料](https://segmentfault.com/a/1190000010955254)