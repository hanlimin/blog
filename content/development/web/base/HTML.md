---
title: HTML基础
date: "2021-2-28 19:44:00"
modifyDate: 
draft: true
---

# HTML基础

## DOM

### 获取元素

```javascript
getElementByClassName
```

### 元素操作

```javascript
children
childElementCount
previousElementSibling
nextElementChild
firstElementChild
lastElementChild
```

## 事件

- contextmenu
- click
- readystatechange
- hashchange

## 表单

input/texttarea增加的`autuFocus()`字段,使用`checkValidate()`检验`required`、`pattern="\d+"`实现表单校验。

## 脚本

- 跨文档消息传输(XDM)，核心是`postMessage`

## 储存

1. sessionStorage：大小上限为2.5Mb(不同游览器会有差异)，页面关闭时便清空。
2. localStorage：大小上限为2.5Mb(不同游览器会有差异)，页面关闭时不会清空。
3. cookie：存放在客户端，可以有客户端也可由服务端生成，大小上限为4kb。
4. IndexedDB：大小上限为5Mb
5. cacheStorage：由服务端提供

1、2的api有如下几个：

- `setItem(key, value)`
- `getItem(key)`
- `removeItem(key)`
- `clear()`

## JavaScript API

- `requestAnimationFrame(callback)`: 表示在重绘前执行指定的回调函数。
