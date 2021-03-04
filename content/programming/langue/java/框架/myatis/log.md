---
title: log
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### Log

一个接口含有不同等级的日志输出方法和判断当前设置等级方法。

### LogFactory

自动查询可用日志实现并实例化返回。

### ErrorContext

类使用```ThreadLocal```的私有静态常量储存实例，其它方法都是配置相关属性的方法。
