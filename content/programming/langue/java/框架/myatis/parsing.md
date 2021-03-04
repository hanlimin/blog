---
title: parsing
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### TokenHandler
接口，只有一个方法handleToken，处理文本。
### GenericTokenParser

构造方法三个入参，2个字符串openToken、closeToken，一个TokenHandler实例，只是简单字段赋值。此外只有一个公共方法parse，主要作用是将入参字符串中，openToken和closeToken和它们之间的字符串作为key使用TokenHandler替换成对应的值，其它部分不变转换另一个字符串返回。

### PropertyParser
声明了几个公共静态常量和一个公共静态方法parse，入参为一个字符串string和一个Properties variables，构建内部类VariableTokenHandler handler，已"${"，"}",handler为入参构建出GenericTokenParser，将string内包含的标识替换成variables中包含的值，VariableTokenHandler可配置成可使用默认值模式，开在variables放入对应标志开启。默认值表示成标识:值，":"之前为标识，之后的即为设置的默认值。

### XPathParser
封装了SAX接口，提供了XML文档解析功能。主要获取节点和节点数值。

### XNode
封装了XpathParser和Node，主要用来对指定的一个节点解析，可以获取子节点、节点数值、节点属性

-   getValueBasedIdentifier
    nodeName([(@id|@value|@property])?，已指定节点为起点，向上至根节点为止，获取节点名字、按顺序获取id、value、property每个节点之间使用"_"相连，

