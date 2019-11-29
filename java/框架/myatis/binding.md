# org.apache.ibatis.binding

### MapperMethod
封装了SqlCommand和MethodSignature两个属性。只有两个公共方法，一个入参为class、method、configuration的构造方法，一个入参为SqlSession、Object[]的execute方法。根据SqlCommand的不同，通过MethodSignature完成数据库查询。
-   execute
    -   对INSERT、UPDATE、DELETE都是相同的处理，使用converArgsToSqlCommandParam处理入参，使用SqlSession对应方法执行sql命令，使用rowCountResult处理返回值。 
    -   对SELECT会根据方法返回值的类型的不同而有不同处理方法。
        -   方法返回值类型为void且有ResultHandler参数。首先依据command.name获取MappedStatement，接下来判断MappedStatement的StatementType为CALLABLE且返回值类型为void，条件不成立则抛出BindingException。
        -   方法返回值是个集合。使用converArgsToSqlCommandParam处理入参，使用SqlSession执行SELECT命令，根据方法返回值类型将查询结果转成数组或Collection
返回。
        -   方法返回值是Map的子类型且方法注有MapKey注解。使用converArgsToSqlCommandParam处理入参，使用SqlSession.selectMap执行SELECT命令，返回结果为Map。MapKey的值作为Key。
        -   方法返回值是Cursor。使用converArgsToSqlCommandParam处理入参，使用SqlSession.selectCursor执行SELECT命令，返回Cursor对象。
        -   默认处理。使用converArgsToSqlCommandParam处理入参，使用SqlSession.selectOne执行SELECT命令。如果method的返回值类型为Optioal，则会结果使用Optional封装返回。
    -   FLUSH，直接调用SqlSession.flushStatements完成SQL命令。
    -   switch默认抛出BindingException
    -   在方法返回之前，还会对结果做个判断。当方法返回值是基本类型且不为void，若结果为null则抛出BindingException。
-   rowCountResult
    对只返回影响行数的结果进行处理
    -   如果方法返回值为void则返回null
    -   如果方法返回值类型为Integer、Long则返回rowCount
    -   如果方法返回值类型为布尔类型，则根据rowCount是否大于0返回
    -   其它情况皆抛出BindException
#### SqlCommand
封装了name和type
statementId=className+'.'+methodName
先根据statementId在Configuration里查找MappedStatement，如果Configuration里不存在statementId对应MappedStatement，这时若类类型和方法的所属类型相同则直接返回null，反之则说明这个方法属于父类，接下来会已父类为入参递归调用到找到MappedStatement为止，最终找到则返回仍未找到则返回null。这里前提是Configuration中已经存在了MappendStatement，也就是说MappeerMethod创建之前Configuration中就完成MappedStatement的加载。
### MethodSignature
封装了多个关于返回值的属性信息、在方法参数中Bound索引、ResultHandler索引、ParamNameResolver。设定了参数中有且只有一个ResultHandler参数。主要方法是converArgsToSqlcommandParam，这个方法通过调用ParamNameResolver的getNameParams方法获取参数名字和参数的映射关系。如果参数上没有Param注解且只有一个参数就返回第一个参数，返回值就是一个对象；其它情况，根据注解设定名或默认名字对参数对象、通用名字对参数对象构成map返回。
### MapperProxy
实现了InvocationHandler的JDK代理
-   如果方法的声明类是Object则以当前对象为Targe调用方法
-   如果方法是默认方法，则通过MethodHandle以入参proxy为Targe调用方法
-   默认则从methodCache中获取method对应MapperMethod，如果没有则创建MapperMethod放入缓存并返回，最后调用MapperMethod.execute返回结果。
### MapperProxyFactory
MapperProxy的创建工厂，封装了MapperInterface、methodCacche。每次创建MapperProxy时mapperInterface和methodCache都是同样的。创建的MapperProxy实例使用的mapperInterface和methodCache所指向的对象都是相同的。
### MapperRegistry
封装了Configuration和一个Class对MapperProxyFactory的Map。管理Mapper类和对应MapperProxyFactory。
-   getMapper
    使用入参type找出对应的MapperProxyFactory并通过它创建MapperProxy返回。未找到MapperProxyFactory或工厂方法创建实例都可能抛出BindingException。
-   hasMapper
    判断指定Mapper类型是否在map中。
-   addMapper
    若指定的类型是接口且不在map的keys中时，创建MapperProxyFactory并添加到map中，通过MapperAnnnotationBuilder对type完成解析，如果解析失败则从map中移除type。
-   getMappers
    获取map的keyset
-   addMappers
    类中有两个重载方法。一个是两个参数的，入参packageName和type，获取指定包下所有type的子类，迭代子类集合调用addMapper。另一个方法入参就一个packageName，该方法只是调用第一个方法，第二入参为Object.class，也就是说添加包下所有类。
