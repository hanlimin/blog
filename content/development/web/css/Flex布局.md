---
title: Flex布局
date: "2021-2-28 00:37:22"
modifyDate:
draft: true
---

# Flex布局

在传统的方式中，我们通常会设置盒模型的 display、position、float 等属性来进行布局，对于一些特殊布局运用起来不是很方便，比如垂直居中水平居中，如果运用了浮动特性的话，就需要清除浮动，不但比较麻烦，一不小心还会出现意料之外的布局，最后呈现的结果往往不尽人意。
Flexbox（全称 Flexible Box）布局，也叫 Flex 布局，意为“弹性布局”，顾名思义，Flex 布局中的元素具有可伸缩性，是的，通过设置父元素的 display 属性为 display: flex | inline-flex; 其子元素便有了伸缩性，即使在子元素的宽高不确定的情况下，也能通过设置相关 css 属性来决定子元素的对齐方式、所占比例和空间分布

## 一些概念

在开始学习Flex 布局前，我们先来熟悉下有关 Flex 布局的几个概念，这些概念可以帮助对后文的理解。

![基本概念预览，图来源于网络](/static/1542896341060-89f557f2-6905-48c6-bf07-81a5f7a1adb0.png)

上图便是一个 Flex 布局的大致架构了，图中的囊括概念有几点：
• Flex 布局是一整个模块，其中父元素称为 flex container，意为容器；子元素称为 flex item，意为项目；
• Flex 布局中有两条看不见的轴线：主轴（main axis）和交叉轴（cross axis）。默认的主轴是平行的，交叉轴是垂直于主轴的；
• 主轴的开始位置叫 main start，结束位置叫 main end；交叉轴的开始位置叫 cross start，结束位置叫 cross end；
• 子元素在主轴方向上的大小称为 main size，在交叉轴方向上的大小称为 cross size。
在上面的相关概念中，比较重要的是主轴、交叉轴，和它们的开始位置、结束位置。子元素在父元素中会沿着主轴从 main start 到 main end 排列，沿着交叉轴从 cross start 到 cross end 排列。在常规的布局中，浏览器是从左到右排列，挤不下了就换行，在这种情况下，主轴是水平方向，交叉轴是垂直方向，主轴是从左到右，交叉轴是从上到下。
在 Flex 布局中，默认的主轴方向也是水平的，交叉轴是垂直的，通过改变  flex-direction 和 flex-wrap 的属性值可以分别改变两个轴的方向和它们的开始位置、起始位置，这就让布局更加灵活多变了。
了解完 Flex 布局相关的抽象概念，接下来我们来看看有关 Flex 布局的属性部分，这里分为两部分介绍，一是作用于父元素（容器）的，二是作用于子元素（项目）的。

## 容器属性

display 属性用来将父元素定义为 Flex 布局的容器，设置 display 值为 display: flex; 容器对外表现为块级元素；display: inline-flex; 容器对外表现为行内元素，对内两者表现是一样的。

```html
<div class="container"></div>
```

```css
.container {
    display: flex | inline-flex;
}
```

上面的代码就定义了一个 Flex 布局的容器，我们有以下六个属性可以设置的容器上：
• flex-direction
• flex-wrap
• flex-flow
• justify-content
• align-items
• align-content

### flex-direction

flex-direction 定义了主轴的方向，即项目的排列方向。

```html
<div class="container">
    <div class="item">1</div>
    <div class="item">2</div>
    <div class="item">3</div>
    <div class="item">4</div>
</div>
```

```css
.container {
    flex-direction: row | row-reverse | column | column-reverse;
}
```

• row（默认值）：主轴在水平方向，起点在左侧，也就是我们常见的从左到右；
• row-reverse：主轴在水平方向，起点在右侧；
• column：主轴在垂直方向，起点在上沿；
• column-reverse: 主轴在垂直方向，起点在下沿

![flex-direction 为 row](/static/1543373286494-97561c2b-b7ea-430b-8acd-0d07ae6b8920.png)

![flex-direction 为 row-reverse](/static/1543373420639-a8219196-de22-4378-bf88-f1ba9cfbdcc3.png)

![flex-direction 为 column](/static/1543373536749-6724b195-03f2-4330-a2e3-31612a480fe7.png)

![flex-direction 为 column-reverse](/static/1543373594472-d4733be8-285f-4452-a30c-4e4bacd27315.png)

### flex-wrap

默认情况下，项目是排成一行显示的，flex-wrap 用来定义当一行放不下时，项目如何换行。

```css
.container {
    flex-wrap: nowrap | wrap | wrap-reverse;
}
```

假设此时主轴是从左到右的水平方向：
• nowrap（默认）：不换行；
• wrap：换行，第一行在上面；
• wrap-reverse：换行，第一行在下面

![默认情况，flex-wrap 为 nowrap，不换行，即使设置了项目的宽度，项目也会根据屏幕的大小被压缩](/static/1543373755165-d771966b-ee52-4c75-8db3-65fd2fd7c1d0.png)

![flex-wrap 为 wrap](/static/1543375750858-e77c117d-c71e-4233-b8da-c7cf3ecbd09d.png)

![flex-wrap 为 wrap-reverse](/static/1543375789385-e5231a20-6d43-4e02-b91a-a453242ccadd.png)

将 flex-wrap 设置为 wrap-reverse 可以看做是调换了交叉轴的开始位置（cross start）和结束位置（cross end）

### flex-flow

flex-flow 是 flex-direction 和 flex-wrap 的简写，默认值是 row no-wrap。

```css
.container {
    flex-flow: <flex-direction> || <flex-wrap>;
}
```

### justify-content

justify-content 定义了项目在主轴上的对齐方式。

```css
.container {
    justify-content: flex-start | flex-end | center | space-between | space-around;
}
```

• flex-start（默认）：与主轴的起点对齐；
• flex-end：与主轴的终点对齐；
• center：项目居中；
• space-between：两端对齐，项目之间的距离都相等；
• space-around：每个项目的两侧间隔相等，所以项目与项目之间的间隔是项目与边框之间间隔的两倍。
假设此时主轴是从左到右的水平方向，下面给出了不同属性值的效果图

![justify-content 为 flex-start](/static/1542960779643-ec7a0051-565c-455e-b787-234f9fc2840d.png)

![justify-content 为 flex-end](/static/1542960596421-cb3abd60-a88f-4196-b246-d5179c6d9f6b.png)

![justify-content 为 center](/static/1542960697106-d12a9643-68d5-47b9-9547-3948e8600c12.png)

![justify-content 为 space-between](/static/1542960834327-5f1a516f-de69-4f0e-b0e0-038aa4f958a8.png)

![justify-content 为 space-around](/static/1542960936141-9565287f-3efd-47e4-a76b-3aa3c5a313b7.png)

### align-items

align-items 定义了项目在交叉轴上如何对齐。

```css
.container {
    align-items: flex-start | flex-end | center | baseline | stretch;
}
```

• flex-start：与交叉轴的起点对齐；
• flex-end：与交叉轴的终点对齐；
• center：居中对齐；
• baseline：项目第一行文字的基线对齐；
• stretch（默认值）：如果项目未设置高度或者为 auto，项目将占满整个容器的高度。
假设交叉轴是从上到下的垂直方向，下面给出了不同属性值的效果图。

![align-items 为 flex-start](/static/1542967996970-07c8aec3-f794-423f-9c92-b10f9687d234.png)

![align-items 为 flex-end](/static/1542968183016-8c6ebe68-e6f5-4209-845c-3c8f36771d83.png)

![align-items 为 center](/static/1542968239022-3760da71-29b7-4757-9297-591f311f5fd1.png)

![align-items 为 baselin](/static/1542967161754-8202543f-949e-4f35-9054-79a3473a4178.png)

![align-items 为 stretch](/static/1542968524410-b3a5001f-e02b-48e7-a297-1f2391fb0812.png)

### align-content

align-content 定义了多根轴线的对齐方式，若此时主轴在水平方向，交叉轴在垂直方向，align-content 就可以理解为多行在垂直方向的对齐方式。项目排列只有一行时，该属性不起作用。

```css
.container {
    align-content: flex-start | flex-end | center | space-between | space-around | stretch;
}
```

- flex-start：与交叉轴的起点对齐；
- flex-end： 与交叉轴的终点对齐；
- center：居中对齐；
- space-between：与交叉轴两端对齐，轴线之间的距离相等；
- space-around：每根轴线两侧的间隔都相等，所以轴线与轴线之间的间隔是轴线与边框之间间隔的两倍；
- stretch（默认值）：如果项目未设置高度或者为 auto，项目将占满整个容器的高度。

![align-content 为 flex-start](/static/1543073620720-e08de47d-6052-419a-8f7b-7d6b929f7531.png)

![align-contet 为 flex-end](/static/1543073660448-eece6c2b-f2a3-4908-8ebc-253805ee91c6.png)

![align-content 为 center](/static/1543073567989-2555fbc5-6683-42cb-9396-be5cc4ad7a81.png)

![align-content 为 space-between](/static/1543073493812-8f402b4c-cb45-4de2-83f1-1e6af22dfaed.png)

![align-content 为 space-around](/static/1543073713850-45e4df08-53a3-4c41-b4ea-8159b91952c9.png)

![align-content 为 stretch](/static/1543074213853-b645c59d-5462-4b02-b97a-85e76e1997e0.png)

## 项目属性

对项目设置属性，可以更灵活地控制 Flex 布局。以下六种属性可以设置在项目上：

- order
- flex-grow
- flex-shrink
- flex-basis
- flex
- align-self

### order

order 定义了项目的排列顺序，默认值为 0，数值越小，排列越靠前。

```css
.item {
    order: <integer>;
}
```

![给第三个项目设置了 order: -1; 后，该项目排到了最前面](/static/1543129295187-2d1b848e-07e8-4bb5-b40e-d5971dc6ad92.png)

### flex-grow

flex-grow 定义了项目的放大比例，默认为 0，也就是即使存在剩余空间，也不会放大。

如果所有项目的 flex-grow 都为 1，则所有项目平分剩余空间；如果其中某个项目的 flex-grow 为 2，其余项目的 flex-grow 为 1，则前者占据的剩余空间比其他项目多一倍。

```css
.item {
    flex-grow: <number>;  
}
```

![所有项目的 flex-grow 都为 1，平分剩余空间](/static/1543129904362-310d8908-2458-4fb7-abb8-157a45920db2.png)

![flex-grow 属性值越大，所占剩余空间越大](/static/1543130592755-f510736d-815d-46b9-b452-c73a93a79781.png)

### flex-shrink

flex-shrink 定义了项目的缩小比例，默认为 1，即当空间不足时，项目会自动缩小。

如果所有项目的 flex-shrink 都为 1，当空间不足时，所有项目都将等比缩小；如果其中一个项目的 flex-shrink 为 0，其余都为 1，当空间不足时，flex-shrink 为 0 的不缩小。

负值对该属性无效。

```css
.item {
    flex-shrink: <number>；
}
```

![空间不足时，默认等比缩小](/static/1543132006935-09ab4bb7-732f-4092-ad10-e3bcefd86ce9.png)

![flex-shrink 为 0 的不缩小](/static/1543132178629-ec75d3a2-1955-4cbc-9da0-54fe0e2f3f4d.png)

### flex-basis

flex-basis 定义了在分配多余的空间之前，项目占据的主轴空间，默认值为 auto，即项目原来的大小。浏览器会根据这个属性来计算主轴是否有多余的空间。

flex-basis 的设置跟 width 或 height 一样，可以是像素，也可以是百分比。设置了 flex-basis 之后，它的优先级比 width 或 height 高。

```css
.item {
    flex-basis: <length> | auto;
}
```

![不同的 flex-basis 值效果展示](/static/1543133040010-941a4e3b-5aad-429a-888f-b0ed4da2e460.png)

### flex

flex 属性是 flex-grow、flex-shrink、flex-basis 的缩写，默认值是 0 1 auto，后两个属性可选。

该属性有两个快捷值：auto（1 1 auto）和 none（0 0 auto）。auto 代表在需要的时候可以拉伸也可以收缩，none 表示既不能拉伸也不能收缩。

```css
.item {
    flex: auto | none | [ <'flex-grow'> <'flex-shrink'>? || <'flex-basis'> ]
}
```

### align-self

align-self 用来定义单个项目与其他项目不一样的对齐方式，可以覆盖 align-items 属性。默认属性值是 auto，即继承父元素的 align-items 属性值。当没有父元素时，它的表现等同于 stretch。

align-self 的六个可能属性值，除了 auto 之外，其他的表现和 align-items 一样。

```css
.item {
    align-self: auto | flex-start | flex-end | center | baseline | stretch;
}
```

![第三个项目的对齐方式与其他不同](/static/1543135456654-b7f06914-077a-4067-bef4-42ab141d7069.png)
