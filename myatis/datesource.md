### DataSourceFactory

一个接口只有配置属性和获取```DataSource```的两个方法。

### JndiDataSourceFactory

实现了```DataSourceFactory```接口，通过JNDI获取```DataSource```。

### UnpooledDataSourceFactory

实现了```DataSourceFactory```接口，在构造方法中直接创建出```UnpooledDataSource```实例并赋值到类属性上```dataSource```。```setProperties```方法会将入参分为驱动器属性和```DataSource```属性赋值到```dataSource```上。

### UnpooledDataSource

实现了```DataSource```接口，内部封装了连接数据库的相关属性，简单地通过```DriverManager```获取数据库连接```Connect```。

### PooledDataSourceFactory

直接继承了```UnpooledDataSourceFacotry```，只是在构造方法中创建赋值到```datgaSource```的是```PooledDataSource```。

### PooledDataSource

实现了```DataSource```接口，

- ``pushConnection``方法，使用类属性``state``作为同步对象进入同步块，先从``state``的活跃列表中移除入参``conn``，如果入参连接有效则进入if块。如果空闲列表数量小于指定最大值且入参``conn``的``connectionTypeCode``和类属性``expectedConnnectionTypeCode``相同，则累加``state`` 的``acculatedCheckoutTime``，如果实际连接为非自动提交则事务回滚，接下来创建新的``PooledConnection`` ``newConn`` 赋值原来的连接的属性，将原来的连接无效化，新连接添加到空闲列表中，通知同步对象。而在不成立时则直接关闭内部实际连接，无效化连接。
- ``popConnection``方法，获取``PooledConnnection``连接，声明一个``PooledConnection`` 变量``conn``，以``conn``不为null为条件进入while循环，进入``state``为锁对象的同步块。首先判断空闲列表不为空则直接从空闲列表中获取连接；如果活跃列表中连接数量未超过允许的最大值则创建新的连接；如果活跃列表已满则取表中第一个连接，判断该链接的检查时间是否超出最大值，若超出则非自动提交的事务回滚且使用对应实际内部连接创建新连接，无效化原连接；剩余情况则是无法获取连接，在锁对象上``state``等待``poolTimeToWait``时间，若等待时线程被中断爆出``InterruptedException``异常则直接跳出循环；如果``conn``不为``null``，若``conn``有效则更新相关属性并添加到活跃列表中，若``conn``无效则添加坏连接计数，将``conn``置``null``，如果本次方法调用中坏链接计数超出允许的最大值则抛出``SQLException``。跳出循环后，检查``conn``是否为``null``，为``null``则抛出``SQLException``异常，最后返回``conn``的值。
- ``pingConnection``方法，第一步检查``conn``内实际连接是否已经关闭，如果上一步检查为真则继续检查，如果``poolPingEnabled``已经开启则执行指定的PING sql语句，若执行正常则通过测试，若执行爆出异常则关闭连接，最后返回测试结果。

### PooledConnection

实现了```InvocationHandler```接口。构造方法入参包含了```Connection``` ```connection```和```PooledDataSource```。

- ```invoke```方法，如果是调的``close``方法则调用``dataSource``的``pushConnection``方法；如果不是```Object```声明的方法会调用一次```checkConnection```方法，最后会以```connection```为调用方执行方法。

- ``checkConnection``方法，如果``valid``为``false``则包抛出异常。

### PoolState

封装了``PooledDataSource``和其它多个属性，构造方法只有``PooledDataSource``一个参数，其它方法都是同步方法，其中``toStirng``输出了大量属性信息，是个封装了多个属性和获取状态信息的类。属性中有两个``PooledConnection``列表，分别为空闲列表和活跃列表。









