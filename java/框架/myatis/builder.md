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
-   parse
    这个方法是惟一的公共方法，首先会判断指定的resource是否已经处理过，未处理则处理。最后会调用parsePendingMethods方法，对Configuration的incompleteMethods再次进行解析。
    处理过程为：
    调用loadXmlResource，解析mapper xml 文件
    将resource添加到Configuration中。
    为MapperBuilderAssistant设置namespace。
    调用parseCache解析可能有的缓存信息。
    调用parseCacheRef解析缓存应用
    迭代调用parseStatement处理类型所有非bridge方法，如果处理过程中抛出IncompleteElementException，则创建出MethodResolver添加到Configuration的incompleteMethods中。
-   loadXmlResource
    根据指定resource获取对应的InputStream，构造XMLMapperBuilder，再调用XMLMapperBuilder.parse完成mapper xml的解析。
-   parseCache
    如果指定类型上有CacheNamespace注解，获取相关属性，调用MapperBuilderAssistant的userNewCache方法完成对应缓存的创建。
-   parseCacheRef
    如果指定类型上有CacheNamespaceRef,获取相关属性，通过MapperBuilderAssistant的userCacheRef完成引用缓存的获取。如果获取过程中抛出IncompleteElementException，则添加到Configuration的incompleteCacheRef中。
-   parseStatement
    通过getSqlSourceFromAnnotations获取SqlSource。如果上步获取sqlSource不为null，则开始为创建MappedStatement获取去各个参数。首先获取方法上的Options注解，这个注解包含了大量配置信息，方法上注解分析出SqlCommandType枚举值，KeyGenerator、ResultMap等属性值而后调用MappedBuilderAssistant的addMappedStatement方法创建MappedStatement。
-   getParameterType
    获取指定方法参数中第一个非RowBounds和非ResultHandler的类的参数类型，若无参数则返回ParaMap类型。
-   getLanguage
    获取方法上的Lang注解，若存在注解则返回注解指定的LangDriver类型，若不存在则返回默认LanguageDriver类型。
-   getSqlSourceFromAnnotations
    从方法上获取第一个找到在SQL_ANNOTATION_TYPES、SQL_PRIVIDER_ANNOTATION_TYPES的两个注解。两个注解同时存在，存在则抛出BindingException，同时为空则返回null。如果存在的是sqlAnnotation(SELECT/UPDATE/INSERT/DELETE等注解)，则调用buildSqlSourceFromStrings返回SqlSource。如果存在的sqlPrioviderAnnotationType，则创建ProviderSqlSource返回。
-   buildSqlSourceFromStrings
    通过Language的createSqlSource方法将sql语句构建出SqlSource并返回。

## xml
### XMLConfigBuilder
继承自BaseBuilder，只有一个公共方法parse，方法内部通过parseConfiguration来完成config.xml配置文件的解析，通过一个布尔值parsed只允许解析一次。
### XMLMapperEntityResolver
实现了EntityResolver接口，用来获取mapper和config的dtd文件输入流InputSource。
### XMLMapperBuilder
继承自BaseBuilder。主要完成了mapper.xml文件的解析，文件格式定义见mybatis-3-mapper.dtd
-   构造方法
    入参包含XpathParser、Configuration、String类型的resource、Map类型的sqlFragments、可选的String类型的namespace。除了通过configuration、resource构造出MapperBuilderAssistant外，其余都是字段赋值。resource指的是文件的完整路径。
-   parse
    唯一有在使用的公共方法，方法逻辑如下：
    先判断指定的resource是否处理过，若还未处理则调用configurationElement进行处理，将resource添加到configuration的loadedResources中。
    下一步对之前解析失败抛出IncompleteException的在Configuration保存的incompleteResultMaps、incompleteCacheRefs、incompleteStatements再次进行解析，再次进行解析，若成功则从map中移除，若失败再次抛出IncompleteElementException则直接忽略该异常异常。
-  configurationElement 
    namespace必须有，并配置到builderAssistant。解析处理cache、cache、parameterMap、resultMap、sql、select、insert、update、delete等节点。
- cacheRefElement
    处理cache-ref节点
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
    首先从节点的所有子节点解析出ResultMapping，构造出ResultMapResolver，通过ResultMapResolver.resolve返回ResultMap，若出现异常则将ResultMapResolver添加到Configuration中并抛出异常。
-   sqlElment
    sql节点对应id，会先转成带有当前namespace的完整id。如果id作为key未在sqlFragments中，则将该sql节点放入sqlFragments中。
-   buildStatementFormContext
    将每个节点作为入参，构建XMLStatementBuilder，再调用XMLStatementBuilder.parseStatementNode方法完成解析，如果抛出IncompleteElementException，则调用configuration.addIncompleteStatement方法。

### XMLStatementBuilder
    处理select/update/delte/insert节点
-   parseStatementNode
    从节点中获取所有属性
    通过XMLIncludeTransfer完成include节点的替换。
    通过parseSlectKeyNodes完成selectKey节点的处理。
    通过LangDriver创建出SqlSource。
    拼出keyStatementid，从Configuration中获取对应KeyGenerator，如果没有对应的值就取用默认值。
    通过MapperBuilderAssistent.addMappedStatement创建MappedStatement
-   parseSelectKeyNodes
    处理selectkey节点，迭代所有节点调用parseSelectKeyNode处理，最后移除这些节点。
-   parseSelectkeyNode
   解析处理节点的属性，通过LangDriver.createSqlSource构建出SqlSource。 通过MapperBuilderAssistant.addMapperStatement构建出MappedStatement，通过id从Configuration取出这个MappedStatement名为keyStatement，将keyStatment和executeBefore作为入参构建SelectKeyGenerator并添加到Configuration的keyGenerators中。
### XMLIncludeTransformer
    处理include节点
-   applyIncludes
    这个方法通过节点的不同状态递归调用完成指定节点的处理。
    从include节点取出refid和子节点对用properties，通过refid从configuration的sqlFragments中获取对应Node toInclude，对toinClude应用properties，使用toInclude替换source节点

### ResultMapResolver
    封装了MapperBuilderAssistant和它的addResultMap方法入参。主要用于addResultMap的再次调用。
