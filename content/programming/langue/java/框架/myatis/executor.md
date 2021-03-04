---
title: executor
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### Executor

一个`ResultHandler`字段。包含更新、查询、事务、缓存处理、延迟加载。

### CachingExecutor

实现了```Executor```接口，类内部封装了一个```Executor``` ```delegate```和```TransactionalCacheManager``` ```tcm```。实现的接口方法都加入了缓存的处理，最终都会调用```delegate```方法。```tcm```缓存了查询返回的数据，在所实现的接口方法中都调用了```flushCacheIfRequired```方法来判断是否清空相应缓存。```flushCacheIfRequired```方法判断入参```MappedStatement```中```Cache```不为空且```MappedStatement```中```flushCacheRequired```返回为空，判断通过则清空```cache```在```tcm```中的缓存。

### BaseExecutor
接口Executor的抽象实现,封装了Transaction、Executor、ConcurrentLinkedQueue、PerpetualCache localCache和localOutputParameterCache、Configuration。实现了延迟加载等所有逻辑留下具体执行的抽象方法，doUpdate、doFlushStatement、doQuery、doQueryCursor。大部分字段是protected。
该接口共有4个实现，分别为

-   SimpleExecutor
-   BatchExecutor
-   ReuseExecutor
-   ClosedExecutor
### SimpleExecutor
继承自BaseExecutor。

- ```prepareStatement```方法，通过方法```getConnection```获取```Connect```，通过入参```StatementHandler``` ```handler```的```prepare```方法获取```Statement``` ```stmt```，再次通过```handler```的```paramterize```对```stmt```配置相关参数，最后返回```stmt```。
- ```doUpdate```、```doQuery```、```doQueryCursor```、```doFlushStatements```方法，前三个方法都是先从```MappedStatement```中获取```Configuration```，通过```Configuration```的```newStatementHandler```创建出```StatementHandler ``` ```handler```，调用私有方法```prepareStatement```获取到```Statement``` ```stmt```。```doUpdate```、```doQuery```等方法分别调用```handler```的```update```、```query```方法并返回方法返回值，最后调用```closeStatement```。```doQueryCursor```方法会调用```stmt```的```closeOnCompletion```方法，最后返回```handler```的```queryCursor```方法的返回值。```doFlushStatement```方法直接返回一个空列表。

### BatchExecutor

继承自```BaseExecutor```，实现了```doUpdate```、```doQuery```、```doQueryCursor```、```doFlushStatements```等接口方法。

- 在```doUpdate```方法内，首先获取从入参```MappedStatement``` ```ms```中获取```Configuration``` ```configuration```，通过```configuration```创建出```StatementHandler``` ```handler```,从```handler```中获取```BoundSql``` ``` boundSql```，从```boundSql```中获取```sql```，接下来进入一个if判断，判断条件是上述sql变量是否与类属性```currentSql```相等和入参```ms```与类属性```currentStatement```相等，如果上述判断条件则进入第一个处理分支，获取```statementList```的size记为```last```,在第一个分支中首先从```statementList```中获取```last```-1位即最后一个元素赋值到```stmt```，调用```applytansactionTimeout```方法，以```stmt```为入参调用```handler```的```parameterize```方法，从```batchResultList```获取```last```索引对应元素记为```batchResult```，以方法入参```parameterObject```为入参调用```batchResult```的```addParameterObject```方法。若判断条件为假则进入第二个处理分支，首先调用```getConnect```获取````Connect``` ```connect```，调用```handler```的```prepare```方法入参为```connect```和从```transaction```获取的timeout返回值赋值到```stmt```上，以```stmt```为入参调用```handler```的```parameterize```方法，将```sql```赋值到```currentSql```、将```ms```赋值到```currentStatement```、将```stmt```添加到```statementList```列表中、以```ms```、```sql```、```parameterObject```为入参构建出```BatchResult```实例到```batchresultList```列表中去。最后以```stmt```为入参调用```handler```的```batch```方法，方法返回类静态常量```BATCH_UPDATE_RETURN_VALUE```。
- ```doQuery```方法，首先调用```flushStatements```方法，从入参```ms```中获取```configuration```，通过```configuration```创建出```StatementHandler```记为```handler```，调用```getConnect```获取```connection```，以```connection```和```tansaction```的timeout为入参调用```handler```的```prepare```方法返回值赋值到```stmt```上，以```stmt```为入参调用```handler```的```parameter```方法，以```stmt```和```resultHandler```为入参调用```handler```的```query```方法并返回方法返回值。最后在finally块以```stmt```为入参调用```closeStatement```方法。
- ```doQueryCursor```方法，调用```flushStatements```，获取```configuration```,构建出```StatementHandler``` ```handler```，通过```handler```的```prepare```构建出```Statement``` ```stmt```，调用```stmt```的```closeOnCompletion```方法，以```stmt```为入参调用```handler```的```parameterize```方法，以```stmt```为入参调用```handler```的```queryCursor```方法并返回方法返回值。
- ```doFlushStatements```方法，首先创建出```BatchResult```的列表```results```。如果入参```isRollback```则直接返回一个空列表。接下来会迭代处理类属性```statementList```列表中的每一个元素，获取单个```Statement``` ```stmt```,以```stmt```为入参调用```applyTransactionTimeout```方法，从```batchResultList```获取对应```BatchResult``` ```batchResult```。进入一个try块，调用```stmt```的```executeBatch```并将返回值作为入参调用```batchResult```的```setUpdateCounts```方法，调用```batchResult```的```getMapppedStatement```方法返回值记为```ms```,再调用```getParameterObjects```返回值记为```parameterObjects```,从```ms```获取```keyGenerator``` ```keyGenerator```。如果```keyGenerator``` 是```Jdbc3KeyGenerator```类型则强转类型为```Jdbc3KeyGenerator```并调用```processBatch```方法，反之若不是```NoKeyGenerator```则迭代```parameterObjects```将每个元素都作为入参调用一个```keyGenerator```的```processAfter```方法。调用```closeStatement```方法。在最近一个```cache```块会拼接说明字符串并再抛出```BatchExecutorExeception```异常。迭代处理的最后一步是将```batchResult```添加到```results```中去。方法最后会返回```results```。在最终的finally块中迭代```statementList```对每个元素调用```closeStatement```。将```currentSql```赋值为```null```，将```statementList```、```batcheResultList```列表清空。

### ReuseExecutor

继承自```BaseExecutor```，实现了```doUpdate```、```doQuery```、```doQueryCursor```、```doFlushStatements```等接口方法。类内部封装了一个```String```对```Statement```的Map ```statementMap```。

- ```doUpdate```方法，从入参```MapppedStatement``` ```ms```获取```Configuration``` ```configuration```，通过```configuration```构建出```StatementHandler``` ```handler```，以```handler```和从```ms```获取的StatementLog为入参调用私有方法```prepareStatement```返回值记为```stmt```，最后以```stmt```为入参调用```handler```的```update```并返回方法返回值。
- ```doQuery```方法，直到获取```Statement``` ```stmt```的步骤与```doUpdate```相同，最后以```stmt```和```resultHandler```为入参调用```handler```的```query```并返回方法返回值。
- ```doQueryCursor```方法，和```doQuery```相比，不同点只是最后调的是```handler```的```queryCursor```方法。
- ```doFlushStatements```方法，迭代```statementMap```的values值，对每个元素调用```closeStatement```方法。清空```statementMap```。最后返回一个空列表。
- ```prepareStatement```方法，一个私有方法入参是```StatementHandler```和```Log```。首先从```handler```中获取```BoundSql```记为```boundSql```，从```boundSql```中获取字符串```sql```。调用```hasStatementFor```方法根据返回的真假，有着不同处理，若为真从```statementMa```获取```sql```对应```Statement``` ，而后调用```applyTransactionTimeout```；若为假，调用```getConnection``` 返回值记为```connnect```，而后以```connection```和timout为入参调用```handler```的```prepare```方法返回值记为```stmt```，将```sql```对```stmt```放入```statementMap```中。跳出判断处理后，以```stmt```为入参调用```handler```的```parameterize```方法，最后返回```stmt```的值。
- ```hasStatementFor```方法，主要作用是判断入参```sql```在```statementMap```中以及对应的```Statement```内的```Connection```还未关闭，如果上述条件成立则返回真反之返回假，若出现异常也返回假。

