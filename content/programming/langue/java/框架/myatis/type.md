---
title: type
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### Alias

别名注解
### JdbcType
封装了jdbc数据类型的枚举
### TypeHandler
类型处理接口,```setParameter```用于配置PreparedStatement参数，```getResult```从Result获取结果。set、get的过程就表现出了jdbcType到javaType、javaType到jdbcType的转换。可以使用```MappedJdbcTypes```标注jdbcType。
一个抽象类，只有一个字段，在构造方法中调用一个方法完成赋值。该方法一直向上获取父类，直到父类为TypeRerence，获取TypeReference的泛型实际类型参数，如果获取的类型还是参数化类型则返回这个类型的原始类型。
### BaseTypeHandler
继承自TypeReference,实现了TypeHandler的抽象类,对null值进行了处理，其余情况都留了抽象方法。
### JdbcType
枚举，对Types内使用数据定义的数据类型进行了封装，并额外定义了几个类型。
### MappedJdbcTypes
注解，封装了JdbcType数组
### MappedTyps
注解，封装了Class数组。
### TypeAliasRegistry
java类型别名注册，一个类型可能有多个别名。在构造方法中注册了多个常用类型，同时也提供公共方法根据包名注册。
### TypeHandlerRegistry
管理类型和对应TypeHandler,javaType对应多个jdbcType-TypeHandler。
