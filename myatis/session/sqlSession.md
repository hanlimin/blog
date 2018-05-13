# org.apache.ibaties.session

### Congiguration
mybaits配置项都在里面、大量的类型别名注册

### SqlSession
一个接口定义了增删改查、事务、获取连接、配置信息、会话缓存、获取指定类的映射等方法。

### SqlSessionFactory
一个sql会话工厂接口，定义了可通过指定是否自动提交、连接、事务隔离级别、执行器来获取```SqlSession```方法，也能够获取配置信息```Congiguration``的方法。

### SqlSessionFactoryBuilder
为SqlSessionFactory提供多种构建方式


### SqlSessionManager
实现了```SqlSession```接口和```SqlSessionFactory```接口。内部使用```TheadLocal```保存```SqlSession```。
