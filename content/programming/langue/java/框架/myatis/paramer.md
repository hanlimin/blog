---
title: paramer
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### ParameterHandler
一个接口只有两个方法，一个getParameterObject获取参数对象？setParameters方法入参是PreparedStatement作用是为入参PreparedStatement配置参数。
###  DefaultParameterHandler
实现了ParameterHandler接口，封装了TypeHandlerResgistry、MappedStatement、一个Obejct paraameterObejct、BoundSql、Configuration。构造参数只有MappedStatement、parameterObject、BoundSql。多个的属性是从MappedStatement中获取的。


