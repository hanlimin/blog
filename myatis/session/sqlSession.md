# org.apache.ibaties.session

### Congiguration
mybaits配置项都在里面、大量的类型别名注册

### SqlSession
一个接口定义了增删改查、事务、获取连接、配置信息、会话缓存、获取指定类的映射等方法。

### DefaultSqlSession
接口```SqlSession```的默认实现。内部数据的调用方式待探索。

### SqlSessionFactory
一个sql会话工厂接口，定义了可通过指定是否自动提交、连接、事务隔离级别、执行器来获取```SqlSession```方法，也提供了获取配置信息```Congiguration```的方法。

### DefaultSqlSeesionFactory
实现了``SqlSessionFactory```接口的会话工厂。

### SqlSessionFactoryBuilder
为SqlSessionFactory提供构建器。可以指定配置文件输入流、环境信息、properties信息，内部通过```XMLConfigBuilder```生成```Configuration```，也可以直接指定```Configuration```。有了配置信息后，通过```DefaultSqlSessionFactory```建立会话工厂并返回。


### SqlSessionManager
组合模式。实现了```SqlSession```接口和```SqlSessionFactory```接口。对这两个接口的封装。内部使用```TheadLocal```保存```SqlSession```。
