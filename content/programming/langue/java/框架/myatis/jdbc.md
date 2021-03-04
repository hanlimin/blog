---
title: jdbc
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### AbstractSQL

一个抽象类，主要用来对SQL语句做词法分析。

### SQL 

继承自```AbstractSQL```，就实现了一个方法```getSelf```，方法是直接返回```this```。泛型也是使用的```SQL```。

### SqlRunner

直接通过原始jdbc执行sql语句，只有返回结果处理上使用了```TypeHandler```。

### ScriptRunner

执行SQL脚本

### Null

一个枚举类，只在```SqlRunner```和几个测试类中使用过。



