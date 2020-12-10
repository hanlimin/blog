

### 开源框架源码剖析

持久层框架设计与实现及MyBatis源码剖析

- 从查询结果集Utils到ORM思想升级
- ORM框架设计步骤推导，掌握框架设计思想
- MyBatis源码分析，探秘底层实现原理及框架设计思想
- 纯手写持久层框架，设计属于你自己的持久层框架

MVC框架设计与实现及SpringMVC源码剖析

- MVC设计模式及前端控制器模型分析
- 通过原始BaseServlet，推导MVC框架实现步骤
- SpringMVC源码分析，探秘底层实现原理及框架设计思想
- 纯手写MVC注解版框架，设计属于你自己的MVC框架

通用持久层规范及Spring Data源码剖析

- 持久层复用演进：从继承父类到实现接口再到JPA规范
- 掌握通用持久层规范设计思想
- Spring Data源码分析，探秘底层实现原理及框架设计思想
- Spring Data JPA & Spring Data Redis实现分析

IoC容器设计与实现及Spring-Core源码剖析

- 从分析代码耦合到IoC思想演进
- 从功能代码抽取到面向切面AOP思想演进
- Spring源码分析，探秘底层实现原理及框架设计思想
- 纯手写IoC和AOP框架，设计属于你自己的Spring框架

约定优于配置设计范式及Spring Boot源码剖析

- 解放双手：约定优于配置（Convention over Configuration）设计范式
- SpringBoot自动装配实现原理分析
- SpringBoot源码剖析，探秘底层实现原理及框架设计思想

###  Web服务器深度解析及调优 

Tomcat深度剖析及性能调优

- Tomcat工作原理及架构剖析
- Jasper等核心引擎运行机制探究
- Tomcat高级配置技巧
- Tomcat多实例集群架构
- Tomcat漏洞防护与安全加固策略
- Tomcat性能监控机制与调优方案

Cluster模式潜在问题及解决方案

- 一致性Hash和Session共享解决方案
- 时钟同步和分布式调度解决方案
- 唯一性ID生成方案及SnowFlake算法

Nginx深度剖析及性能调优

- Nginx场景化配置方案
- Nginx日志策略及切割处理应用
- Nginx Cache策略及Gzip压缩机制
- Nginx进程模型及产线配置
- LVS+Nginx+keepalived实现高可用
- Nginx惊群效应内核级剖析

Web服务综合解决方案

- 动静分离思想及架构设计
- 页面动态模块化渲染（Nginx+lua）
- 内容分发网络CDN加速实现原理
- SEO搜索引擎优化

### 分布式架构设计&微服务深入剖析

分布式理论及架构设计

- 分布式理论（CAP、Paxos、Raft、Lease、脑裂）
- 分布式架构设计策略（心跳、HA、容错、负载均衡）
- 分布式架构网络通信（NIO&Netty、RMI、自定义RPC）

高性能RPC框架Apache Dubbo

- 分布式协调服务 Zookeeper
- Dubbo深度配置与高可用
- Dubbo服务治理（权重、降级、容错、路由等）
- Dubbo原理分析与源码深度剖析

分布式服务治理

- 分布式服务削峰、降级、熔断、限流等
- 分布式事务&分布式锁
- 分布式安全&链路追踪

SpringCloud 微服务框架

- 注册中心底层原理及Eureka&Consul实战
- 熔断器设计原理及Hystrix实战
- 配置中心设计原理及Spring Cloud Config实战
- 负载均衡算法剖析及Ribbon&服务消费Feign实战
- 服务网关设计原理Zuul&Gateway实战
- 消息总线设计原理及Bus实战
- 链路追踪设计原理及Sleuth+Zipkin实战
- 消息驱动服务设计原理及Stream实战
- Spring Cloud Alibaba最佳实践

### 大型分布式存储系统架构进阶 

MySQL海量数据存储与优化

- MySQL存储引擎InnoDB&MyISAM
- MySQL架构设计及性能优化方案
- MySQL基准测试工具MysqlSlap，Sysbench
- MySQL读写分离、分库分表策略
- MySQL生产级数据库监控方案
- MyCat高可用架构方案（单点故障、HAProxy、故障转移）
- Sharding-JDBC & Sharding-Proxy & Sharding-UI
- ShardingSphere深入（分片、编排治理、SPI、测试引擎）

海量列式存储数据库HBase

- HBase架构设计及集群部署
- HBase RowKey设计原则及生产实践
- HBase 性能提升策略与读写速率优化案例

轻量级分布式文件系统FastDFS

- FastDFS集群架构与原理剖析
- FastDFS+Nginx高吞吐文件服务器

阿里云OSS云存储平台

- OSS云存储开放接口规范
- OSS云存储的权限控制
- 基于Java的OSS云存储编程操作

分布式文档存储独角兽MongoDB

- MongoDB数据模型和聚合管道
- replica sets & Sharded Cluster
- MongoDB水平扩展架构实战

知识图谱存储数据库Neo4j

- Neo4j数据模型及图形理论
- Neo4j的CQL高级查询语言

Hadoop分布式文件系统HDFS

- HDFS设计原理和运行机制
- HDFS HA方案
- HDFS Data Stream操作
- HDFS相关运维工具



###  大型分布式系统缓存架构进阶 

高性能分布式缓存 Redis

- Redis持久化方案（RDB & AOF）
- Redis删除策略和IO多路复用模型
- Redis集群模式（主从、哨兵、Cluster）
- Redis缓存预热、雪崩、击穿、穿透
- Redis多级缓存和性能指标监控
- 基于Redis实现的分布式锁、Session分离和消息队列

Google开源Java工具库Guava Cache

- Guava Cache数据缓存方案
- Guava Cache高并发场景调优实践

Alibaba开源K-V数据存储系统 Tair

- Tair弹性可伸缩缓存架构
- Tair存储引擎（MDB引擎&LDB引擎）

Twitter开源缓存代理Twemproxy

- Twemproxy实现原理剖析
- Redis+Twemproxy+HAProxy集群方案
- Twemproxy+keepalived高可用方案

Netflix开源分布式缓存系统 EVCache

- EVCache高可靠低延迟解决方案
- EVCache分布式复制架构

SSD-Based 高性能企业级K-V存储数据库Aerospike

- Aerospike架构和Cluster实现
- Aerospike与Redis的对比分析
- Aerospike实现个性化广告推荐和实时竞价广告

###  分布式消息服务中间件进阶 

从生产者消费者模型到消息中间件

- 生产者消费者模型到消息中间件的诞生
- 消息中间件在大型分布式架构的使用场景分析
- 剖析消息中间件的核心部件与关键技术

Apache开源消息中间件 RabbitMQ

- AMQP和JMS
- RabbitMQ高级特性（ACK、限流、TTL、死信、延迟）
- RabbitMQ消息可靠性分析与追踪
- 消息可靠性保证和幂等性处理
- RabbitMQ集群部署方案和HA Proxy

Apache消息传递引擎 RocketMQ

- RocketMQ消息存储结构
- RocketMQ刷盘机制
- RocketMQ路由中心NameServer等源码分析

高吞吐消息中间件Kafka

- Kafka集群原理和消息流处理流程
- Kafka消费者组机制探究
- Kafka数据管道Connect
- Kafka流处理基础
- 三种消息中间件性能对比
- Kafka监控工具 Kafka Eagle

###  分布式搜索引擎进阶 

Apache全文检索引擎工具包Lucene

- Lucene倒排索引机制和底层存储结构
- Lucene词典排序算法（TF-IDF）
- Lucene亿级搜索实践调优方案

分布式搜索和分析引擎Elasticsearch

- 数据模型分析、构建和算法扩展
- Query DSL、Filter DSL高级应用与机制剖析
- 非法搜索定位及问题追踪
- 指标聚合、桶聚合及下钻分析
- ES零停机索引重建
- ES Suggester智能搜索建议方案
- 拉勾网亿级数据量搜索实战
- ES深度应用及原理剖析
- 拉勾网高并发亿级场景Es 7.x分布式集群调优策略

企业级搜索应用服务器Solr

- Solr高级特性
- SolrCloud+Zookeeper集群化解决方案
- Solr性能监控

海量日志分析平台Elastic Stack（ELK）

- 轻量级数据采集器Beats
- 开源服务器端数据处理管道Logstash
- 可视化日志分析平台Kibana

### 分布式实时流式计算引擎Flink

分布式实时流式计算引擎Flink

- 无界流和有界流模型分析
- 流处理与mini-batch的区别
- Flink流处理特性
- Flink编程模型及实践
- 基于Flink的物联网数据实时监控系统

###  容器技术&CI/CD、DevOps 

容器虚拟化技术

- 容器引擎Docker & K8s容器编排系统
- 开源PaaS云平台Cloud Foundry
- 动态资源调度Mesos+Marathon
- 虚拟化容器弹性扩缩容方案

服务质量治理

- APM管理工具Skywalking
- 性能监控工具Pinpoint

CI/CD、DevOps

- 持续集成工具Jenkins
- 代码质量管理工具Sonar
- DevOps开发运维一体化方案

###  底层调优与算法深入 

数据结构与算法

- 高级数据结构
- 排序、递归与回溯
- 深度与广度优先搜索
- 动态规划
- 二分搜索与贪婪算法

JVM分析与调优

- JVM内存模型
- JVM内存泄漏检查
- GC机制及算法分析
- JVM优化实战

高并发编程核心

- 线程6种状态机制分析与线程池实现原理
- 悲观锁与乐观锁
- JDK锁机制（Synchronized、Lock、ReadWriteLock）
- 死锁的产生与避免
- 阻塞队列与线程协作机制
- 抽象队列化同步器AQS

Linux性能监控与调优

- CPU监控与调优
- 内存监控与调优
- 磁盘监控与调优
- 网络监控与调优

###  大型互联网项目实战和业务解决方案 

主流业务解决方案

- 秒杀系统解决方案
- 单点登录SSO+第三方登录解决方案
- 即时通信IM解决方案
- 服务推送解决方案
- 第三方支付解决方案
- 架构安全解决方案
- 基于位置服务LBS解决方案
- 分布式任务调度解决方案
- 规则引擎解决方案
- BI报表解决方案

实战项目

- 细节以具体《详细设计说明书》为主