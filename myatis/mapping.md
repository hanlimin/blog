# org.apache.ibatis.mapping

### SqlSource
代表从xml文件或注解中获取的sql

### BoundSql
对Configuration、sql、ParamerterMapping、paramterObject进行封装，对内部additionalParameters添加key-value或者获取key对应的值。
能过getter获取paramterMapping、paramterObject、sql
### CacheBuidler
一个builder用于Cache
### DatabaseIdProvider
对应数据库类型进行表示
### ParameterMapping
参数映射
javaType、jdbcType、typeHandler，封装了java到jdbc的类型转化相关的几个元素。
