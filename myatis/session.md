# org.apache.ibaties.session

### AutoMappingBehavior
枚举定义了3种自动映射行为。
-   NONE 不自动映射
-   PARITAL 无嵌套的才映射
-   FULL 都映射
### AutoMappingUnknownColumnBehavior 
枚举定义对未知列或未知属性的处理行为
-   NONE 什么都不做
-   WARNING 只打印warn日志
-   FAILING 抛出SqlSessionExecption异常
### Congiguration
mybaits配置项都在里面、大量的类型别名注册。
buildAllStatement
### ExecutorType
枚举，SIMPLE、REUSE、BATCH
### LocalCacheScope
枚举，本地缓存作用域，SESSION、STATEMENT
### ResultContext
一个接口，定义4个方法，getResultObject获取结果对象，getResultCount获取结果数量、isStopped判断是否停止、stop停止
### ResultHandler
一个接口，就一个方法handleResult，入参是ResultContext
### SqlSession
一个接口定义了增删改查、游标查询事务、获取连接、配置信息、会话缓存、获取指定类的映射等方法。

### SqlSessionFactory
一个sql会话工厂接口，定义了可通过指定是否自动提交、连接、事务隔离级别、执行器来获取```SqlSession```方法，也提供了获取配置信息```Congiguration```的方法。

### DefaultSqlSession
接口```SqlSession```的默认实现。创建一个DefaultSqlSession需要指定三个参数，分别为```Configuration```、```Executor```、```autoCommint```。```Configuration```即mybaties配置项，```Executor```即执行器，```DefaultSqlSession```内的数据库调用都是通这个执行器完成的。```autoCommint```指定是否自动提交。

### DefaultSqlSeesionFactory
实现了``SqlSessionFactory```接口的会话工厂。

### SqlSessionFactoryBuilder
为SqlSessionFactory提供构建器。可以指定配置文件输入流、环境信息、properties信息，内部通过```XMLConfigBuilder```生成```Configuration```，也可以直接指定```Configuration```。有了配置信息后，通过```DefaultSqlSessionFactory```建立会话工厂并返回。

### SqlSessionManager
内部只有三个常量字段：分别为```sqlSessionFactory```、```sqlSessionProxy```、使用```ThreadLocal```储存会话的```localSqlSession```，很简单的通过组合模式实现了```SqlSession```接口和```SqlSessionFactory```接口。```sqlSessionProxy```是```SqlSession```的代理对象，内部私有类```SqlSessionInterceptor```是它的```InvocationHandler```。```SqlSessionInterceptor```的调用处理逻辑为：若```localSqlSession```中有储存着的会话，则直接调用它完成数据库调用，出现异常就直接抛出不做其它处理。反之，则通过```sqlSessionFactory```重新创建会话，完成数据库调用，无异常则提交事务、有异常则回滚，最后关闭会话。默认```localSqlSession```为空。

### RowBounds
用于逻辑分页

### ResultContext
结果上下文。

### ResultHandler
只有一个方法，方法参数为```ResultContext```，对结果进行处理。

### LocalCacheScope
一个枚举类，值分别为```SESSION```、```STATEMENT```表示两个缓存范围。

### ExecutorType

执行器类型，一个枚举，只有三个值，分别为:```SIMPLE```，```REUSE```，```BATCH```。
