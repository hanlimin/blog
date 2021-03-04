---
title: transaction
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
# org.apache.ibaties.transaction

### Transaction
事务接口。获取连接、提交、回滚、关闭连接、获取事务超时时间

### TransactionFactory
```Transaction```创建工厂。设置Properties、获取```Transaction```

### JdbcTransactino
通过封装jdbc实现了```Transaction```接口

### JdbcTransactionFactory
```TransactionFactory```接口实现

### ManagedTransaction
```Transaction```实现

### ManagedTransactionFactory
```ManagedTransaction```创建工厂
