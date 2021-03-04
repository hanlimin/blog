---
title: mapping
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
# org.apache.ibatis.mapping

### SqlSource
代表从xml文件或注解中获取的sql

### BoundSql
对Configuration、sql、ParamerterMapping、paramterObject进行封装，对内部additionalParameters添加key-value或者获取key对应的值。
能过getter获取paramterMapping、paramterObject、sql
### CacheBuidler
一个builder用于创建Cache。如果未指定Cache实现类就默认使用```PrepetualCache```，并对cache嵌套指定的装饰器和配置属性的对应装饰器，否则就仅仅嵌套一个LoggingCache装饰器就返回了。
### DatabaseIdProvider
对应数据库类型进行表示
### Discriminator
封装了ResultMapping和一个string-string的Map，还提供了一个构建器。
### Enviroment
包含一个字符串id、TransactionFactory、DataSource，提供了一个构建器。
### ParameterMap
封装了3个属性，分别为一个字符串id、type、ParamterMapping列表，提供了一个构建器。
### ParameterMapping
参数映射
javaType、jdbcType、typeHandler，封装了java到jdbc的类型转化相关的几个元素。
### ParameterMode
枚举IN、OU、INOUT
### ResultFlag
枚举ID、CONSTRUCTOR
### ResultMap
结果映射，一个简单类，封装了很多属性。resultMappings、idResultMappings、constructorResultMappings、propertyResultMappings等4种ResultMapping列表，mappedColumns、mappedProperties等两个字符串集合、字符串id、类型字段type、3个hasNestedResultMaps、hasNestedQueries、autoMappings布尔标识、最后一个Discriminator。有个方便构建的内部类Builder。

### ResultMapping
结果映射，与ParaameterMapping相似封装了javaType、jdbcType、typeHandler，提供了一个构建器。
### ResultSetType
封装了jdbc的ResultSet类型
### SqlCommandTYpe
sql命令枚举
### SqlSource
一个接口只有一个方法```getBoundSql```，指定参数对应获取BoundSql
### StatementType
一个Statement类型枚举
### VendorDatabaseIdProvider
实现了DatabaseIdProvider接口，默认返回数据库的产品名字。当指定了Properties，则用数据库产品名字作为key查询对应的值并返回，若没找到侧返回null。
### MappedStatement
没有提供公共的构造方法，只提供了一个内部静态类builder。build构造方法入参有Configuration、id、SqlSource、SqlCommandType，同时提供了其余10多个属性配置的便捷方法。
