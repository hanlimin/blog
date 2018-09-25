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
### ParameterMapping
参数映射
javaType、jdbcType、typeHandler，封装了java到jdbc的类型转化相关的几个元素。
