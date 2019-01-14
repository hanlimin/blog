# org.apache.ibatis.builder
### BaseBuilder
一个抽象类。封装了Configuration、TypeAliasRegistry、TypehandlerRegistry。构造方法入参就一个Configuration，其余两个字段值都是从Configuration获取的。剩下都是protected方法。
### CacheRefResolver
封装了MapperBuilderResolver、一个字符串cacheRefNameSpace，主要方法就一个resolveCacheRef通过cacheNameRefNamespace从MapperBuilderAssistant中获取对应Cache。
### InitializiongObject
表明初始化对象，就一个方法。
### MapperBuilderAssistant
继承自BaseBuilder。封装了4个属性，分别为2个字符串currentNamespace、resource、一个布尔值unresolvedCacheRef、一个缓存Cache，其中resource不可变。
-   get/setCurrentNamespace 如果当前的currentNamespace不为null或与设定值相等则抛出BuildException。
-   applyCurrentNamespace 判断指定的名字是否正确，返回名字
-   userCacheRef 从Configuration中获取指定namespace对应的Cache
-   userNewCache 依据入参和当前currentNamespace创建新的Cache并添加到Configuration中且返回
-   addParameterMap 依据入参构造ParameterMap添加到Configuration中并返回
-   buildParameterMapping 返回依据入参构造ParamterMapping
-   addResultMap 依据入参构造ResultMap添加到Configuration并返回
-   buildDisriminator 返回依据入参构造Discriminator
-   addMapperStatement 依据入参构造MappedStatement添加到Configuration并返回
-   buildResultMapping 返回依据入参构造的ResultMapping
-   getLanguageDriver 从Configuration中获取指定类型的LanguageDriver
## annotation
注解处理
### MapperAnnotationBuilder
Mapper类注解处理。

