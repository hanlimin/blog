---
title: keygen
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### KeyGenerator
一个接口，有两个方法processBefore、processAfter用来处理自增主键的获取。

### NoKeyGenerator
实现了KeyGenerator接口，两个方法都是空的，代表了没有主键获取处理。

### Jdbc3KeyGenerator
从MappedStatement中获取配置的keyProperties数组，从Statement获取GeneratedKeys结果集ResultSet rs，遍历rs的每一行，以参数对象parameter为参数，获取对应MetaObject和对应属性的各个TypeHandler。依据参数序号，取出每个keyProperty对应的值，通过typeHandler转换类型，通过MetaObject把值配置到对象的属性上。

### SelectKeyGenerator
构建方法两个入参一个是用于执行获取key值的select语句的MappedStatement keyStatement，另一个是executeBefore一个标记key值查询是在主语句之前还是之后执行。主要就是通过以parameter为参数，执行keyStatemnet，再把查询出的值配置到参数上。
