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
-   构造方法
    构造入参为Confinguration和一个类类型对象type。
    获取type的二进制名字并转为以'.java (best guess)'为后缀的文件名resource。
    以configuraiton、resource为入参构造出MapperBuilderAssistant.
    向sqlAnnotationTypes、sqlPrioviderAnnotationTypes添加相应的注解类型。
-

## xml
### XMLMapperBuilder
继承自BaseBuilder。主要完成了mapper.xml文件的解析，文件格式定义见mybatis-3-mapper.dtd
-   构造方法
    入参包含XpathParser、Configuration、String类型的resource、Map类型的sqlFragments、可选的String类型的namespace。除了通过configuration、resource构造出MapperBuilderAssistant外，其余都是字段赋值。resource指的是文件的完整路径。
-   parse
    唯一有在使用的公共方法，方法逻辑如下：
-  configurationElement 
    namespace必须有，并配置到builderAssistant
    处理cache-ref和cache
- cacheRefElement 处理cache-ref
    向configuration添加mapper@namespace对cache@namespace
     构建CacheRefResolver,调用resolveCacheRef方法，作用是调用MapperBuildAssisant的userCacheRef验证Configuration中对应Cache是存在的且把对应的Cache引用保存下来。如果未查找到对应Cache、查找过程中抛出异常，最后都会封装成IncompleteElementException抛出。
        如果上步抛出IncompleteElementException，那么会把CacheRefResolver保存到Configuration的incompleteCacheRefs中。
-   cacheElement
    获取mapper/cache的所有属性和子节点，所有属性都有对应的默认值。使用这些属性和子节点通过MapperBuidlerAssistant.useNewCache保存引用和添加到Configuration.caches。
-   parameterMapElement
    处理所有/mapper/parameterMap节点。迭代所有节点，迭代单个节点下的所有parameter节点，通过MapperBuilderAssistant构建出ParameterMapping，将所有构建出的ParameterMapping添加到集合parameterMappings中，再把这个parameterMappings通过MapperBuilderAssistant的addParameterMap构建出ParameterMap。
-   resultMapElements
    处理所有/mapper/resultMap节点。迭代调用resultMapElement
-   resultMapElement
    

