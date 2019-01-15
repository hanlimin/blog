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
### ResultMapperResolver
主要方法就一个resolve，方法逻辑只是调用MapperBuilderAssistant.addResultMap并返回调用结果。
### SqlSourceBuilder
继承自BaseBuilder。完成mapper.xml中的sql语句的解析
-   parse 
    构建出ParameterMappingTokenHandler handler
    构建出GenericTokenParse parser
    调用parser.parse解析出sql
    返回使用configgration、sql，handler.getParameterMappings构建出StaticSqlSource
#### ParameterMappingTokenHandler 
继承自BaseBuider、实现了TokenHandler接口。
构造入参Configuration、一个Class对象parameterType、一个string对Object的Map对象additionalParameters。
-   getParametermappings 返回属性parameterMappings
-   handleToken
    调用buidParameterMapping，并将返回值放入属性parameterMappings中，返回字符串"?"
-   buildParameterMapping
    调用parseParameterMapping获取一个propertiesMap
    从propertiesMap中获取property对应的value
    通过判断获取property对应的类型propertyType
    根据configuration、property、propertyType构建ParameterMapping.Builder builder
    递归propertiesMap配置builder对应属性
    返回builder构建出的ParameterMapping
-   parseParameterMapping 一个私有方法，通过创建ParamterExpression返回一个Map<String, String>
### StaticSqlSource
实现了SqlSource接口。getBoundSql入参为参数对象，构建BoundSql并返回。
    
## annotation
注解处理
### MapperAnnotationBuilder
Mapper类注解处理。

