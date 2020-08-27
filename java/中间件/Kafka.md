> 本文由 JavaGuide 读者推荐，JavaGuide 对文章进行了整理排版！原文地址：https://www.wmyskxz.com/2019/07/17/kafka-ru-men-jiu-zhe-yi-pian/ ， 作者：我没有三颗心脏。

# 一、Kafka 简介

------

## Kafka 创建背景

**Kafka** 是一个消息系统，原本开发自 LinkedIn，用作 LinkedIn 的活动流（Activity Stream）和运营数据处理管道（Pipeline）的基础。现在它已被[多家不同类型的公司](https://cwiki.apache.org/confluence/display/KAFKA/Powered+By) 作为多种类型的数据管道和消息系统使用。

**活动流数据**是几乎所有站点在对其网站使用情况做报表时都要用到的数据中最常规的部分。活动数据包括页面访问量（Page View）、被查看内容方面的信息以及搜索情况等内容。这种数据通常的处理方式是先把各种活动以日志的形式写入某种文件，然后周期性地对这些文件进行统计分析。**运营数据**指的是服务器的性能数据（CPU、IO 使用率、请求时间、服务日志等等数据)。运营数据的统计方法种类繁多。

近年来，活动和运营数据处理已经成为了网站软件产品特性中一个至关重要的组成部分，这就需要一套稍微更加复杂的基础设施对其提供支持。

## Kafka 简介

**Kafka 是一种分布式的，基于发布 / 订阅的消息系统。** 

主要设计目标如下：

- 以时间复杂度为 O(1) 的方式提供消息持久化能力，即使对 TB 级以上数据也能保证常数时间复杂度的访问性能。
- 高吞吐率。即使在非常廉价的商用机器上也能做到单机支持每秒 100K 条以上消息的传输。
- 支持 Kafka Server 间的消息分区，及分布式消费，同时保证每个 Partition 内的消息顺序传输。
- 同时支持离线数据处理和实时数据处理。
- Scale out：支持在线水平扩展。

## Kafka 基础概念

### 概念一：生产者与消费者

![生产者与消费者](../../../JavaGuide/media/pictures/kafka/生产者和消费者.png)

对于 Kafka 来说客户端有两种基本类型：

1. **生产者（Producer）**
2. **消费者（Consumer）**。

除此之外，还有用来做数据集成的 Kafka Connect API 和流式处理的 Kafka Streams 等高阶客户端，但这些高阶客户端底层仍然是生产者和消费者API，它们只不过是在上层做了封装。

这很容易理解，生产者（也称为发布者）创建消息，而消费者（也称为订阅者）负责消费or读取消息。

### 概念二：主题（Topic）与分区（Partition）

![主题（Topic）与分区（Partition）](../../../JavaGuide/media/pictures/kafka/主题与分区.png)

在 Kafka 中，消息以**主题（Topic）**来分类，每一个主题都对应一个 **「消息队列」**，这有点儿类似于数据库中的表。但是如果我们把所有同类的消息都塞入到一个“中心”队列中，势必缺少可伸缩性，无论是生产者/消费者数目的增加，还是消息数量的增加，都可能耗尽系统的性能或存储。

我们使用一个生活中的例子来说明：现在 A 城市生产的某商品需要运输到 B 城市，走的是公路，那么单通道的高速公路不论是在「A 城市商品增多」还是「现在 C 城市也要往 B 城市运输东西」这样的情况下都会出现「吞吐量不足」的问题。所以我们现在引入**分区（Partition）**的概念，类似“允许多修几条道”的方式对我们的主题完成了水平扩展。

### 概念三：Broker 和集群（Cluster）

一个 Kafka 服务器也称为 Broker，它接受生产者发送的消息并存入磁盘；Broker 同时服务消费者拉取分区消息的请求，返回目前已经提交的消息。使用特定的机器硬件，一个 Broker 每秒可以处理成千上万的分区和百万量级的消息。（现在动不动就百万量级..我特地去查了一把，好像确实集群的情况下吞吐量挺高的..嗯..）

若干个 Broker 组成一个集群（Cluster），其中集群内某个 Broker 会成为集群控制器（Cluster Controller），它负责管理集群，包括分配分区到 Broker、监控 Broker 故障等。在集群内，一个分区由一个 Broker 负责，这个 Broker 也称为这个分区的 Leader；当然一个分区可以被复制到多个 Broker 上来实现冗余，这样当存在 Broker 故障时可以将其分区重新分配到其他 Broker 来负责。下图是一个样例：

![Broker和集群](../../../JavaGuide/media/pictures/kafka/Broker和集群.png)

Kafka 的一个关键性质是日志保留（retention），我们可以配置主题的消息保留策略，譬如只保留一段时间的日志或者只保留特定大小的日志。当超过这些限制时，老的消息会被删除。我们也可以针对某个主题单独设置消息过期策略，这样对于不同应用可以实现个性化。

### 概念四：多集群

随着业务发展，我们往往需要多集群，通常处于下面几个原因：

- 基于数据的隔离；
- 基于安全的隔离；
- 多数据中心（容灾）

当构建多个数据中心时，往往需要实现消息互通。举个例子，假如用户修改了个人资料，那么后续的请求无论被哪个数据中心处理，这个更新需要反映出来。又或者，多个数据中心的数据需要汇总到一个总控中心来做数据分析。

上面说的分区复制冗余机制只适用于同一个 Kafka 集群内部，对于多个 Kafka 集群消息同步可以使用 Kafka 提供的 MirrorMaker 工具。本质上来说，MirrorMaker 只是一个 Kafka 消费者和生产者，并使用一个队列连接起来而已。它从一个集群中消费消息，然后往另一个集群生产消息。


# 二、Kafka 的设计与实现

------

上面我们知道了 Kafka 中的一些基本概念，但作为一个成熟的「消息队列」中间件，其中有许多有意思的设计值得我们思考，下面我们简单列举一些。

## 讨论一：Kafka 存储在文件系统上

是的，**您首先应该知道 Kafka 的消息是存在于文件系统之上的**。Kafka 高度依赖文件系统来存储和缓存消息，一般的人认为 “磁盘是缓慢的”，所以对这样的设计持有怀疑态度。实际上，磁盘比人们预想的快很多也慢很多，这取决于它们如何被使用；一个好的磁盘结构设计可以使之跟网络速度一样快。

现代的操作系统针对磁盘的读写已经做了一些优化方案来加快磁盘的访问速度。比如，**预读**会提前将一个比较大的磁盘快读入内存。**后写**会将很多小的逻辑写操作合并起来组合成一个大的物理写操作。并且，操作系统还会将主内存剩余的所有空闲内存空间都用作**磁盘缓存**，所有的磁盘读写操作都会经过统一的磁盘缓存（除了直接 I/O 会绕过磁盘缓存）。综合这几点优化特点，**如果是针对磁盘的顺序访问，某些情况下它可能比随机的内存访问都要快，甚至可以和网络的速度相差无几。**

**上述的 Topic 其实是逻辑上的概念，面相消费者和生产者，物理上存储的其实是 Partition**，每一个 Partition 最终对应一个目录，里面存储所有的消息和索引文件。默认情况下，每一个 Topic 在创建时如果不指定 Partition 数量时只会创建 1 个 Partition。比如，我创建了一个 Topic 名字为 test ，没有指定 Partition 的数量，那么会默认创建一个 test-0 的文件夹，这里的命名规则是：`<topic_name>-<partition_id>`。

![主题（Topic）与分区（Partition）](../../../JavaGuide/media/pictures/kafka/kafka存在文件系统上.png)

任何发布到 Partition 的消息都会被追加到 Partition 数据文件的尾部，这样的顺序写磁盘操作让 Kafka 的效率非常高（经验证，顺序写磁盘效率比随机写内存还要高，这是 Kafka 高吞吐率的一个很重要的保证）。

每一条消息被发送到 Broker 中，会根据 Partition 规则选择被存储到哪一个 Partition。如果 Partition 规则设置的合理，所有消息可以均匀分布到不同的 Partition中。

## 讨论二：Kafka 中的底层存储设计

假设我们现在 Kafka 集群只有一个 Broker，我们创建 2 个 Topic 名称分别为：「topic1」和「topic2」，Partition 数量分别为 1、2，那么我们的根目录下就会创建如下三个文件夹：

```shell
    | --topic1-0
    | --topic2-0
    | --topic2-1
```

在 Kafka 的文件存储中，同一个 Topic 下有多个不同的 Partition，每个 Partition 都为一个目录，而每一个目录又被平均分配成多个大小相等的 **Segment File** 中，Segment File 又由 index file 和 data file 组成，他们总是成对出现，后缀 “.index” 和 “.log” 分表表示 Segment 索引文件和数据文件。

现在假设我们设置每个 Segment 大小为 500 MB，并启动生产者向 topic1 中写入大量数据，topic1-0 文件夹中就会产生类似如下的一些文件：

```shell
   | --topic1-0 
       | --00000000000000000000.index 
       | --00000000000000000000.log 
       | --00000000000000368769.index 
       | --00000000000000368769.log 
       | --00000000000000737337.index 
       | --00000000000000737337.log 
       | --00000000000001105814.index | --00000000000001105814.log 
   | --topic2-0 
   | --topic2-1

```

**Segment 是 Kafka 文件存储的最小单位。**Segment 文件命名规则：Partition 全局的第一个 Segment 从 0 开始，后续每个 Segment 文件名为上一个 Segment 文件最后一条消息的 offset 值。数值最大为 64 位 long 大小，19 位数字字符长度，没有数字用0填充。如 00000000000000368769.index 和 00000000000000368769.log。

以上面的一对 Segment File 为例，说明一下索引文件和数据文件对应关系：

![索引文件和数据文件](../../../JavaGuide/media/pictures/kafka/segment是kafka文件存储的最小单位.png)



其中以索引文件中元数据 `<3, 497>` 为例，依次在数据文件中表示第 3 个 message（在全局 Partition 表示第 368769 + 3 = 368772 个 message）以及该消息的物理偏移地址为 497。

注意该 index 文件并不是从0开始，也不是每次递增1的，这是因为 Kafka 采取稀疏索引存储的方式，每隔一定字节的数据建立一条索引，它减少了索引文件大小，使得能够把 index 映射到内存，降低了查询时的磁盘 IO 开销，同时也并没有给查询带来太多的时间消耗。

因为其文件名为上一个 Segment 最后一条消息的 offset ，所以当需要查找一个指定 offset 的 message 时，通过在所有 segment 的文件名中进行二分查找就能找到它归属的 segment ，再在其 index 文件中找到其对应到文件上的物理位置，就能拿出该 message 。

由于消息在 Partition 的 Segment 数据文件中是顺序读写的，且消息消费后不会删除（删除策略是针对过期的 Segment 文件），这种顺序磁盘 IO 存储设计师 Kafka 高性能很重要的原因。

> Kafka 是如何准确的知道 message 的偏移的呢？这是因为在 Kafka 定义了标准的数据存储结构，在 Partition 中的每一条 message 都包含了以下三个属性：
>
> - offset：表示 message 在当前 Partition 中的偏移量，是一个逻辑上的值，唯一确定了 Partition 中的一条 message，可以简单的认为是一个 id；
> - MessageSize：表示 message 内容 data 的大小；
> - data：message 的具体内容

## 讨论三：生产者设计概要

当我们发送消息之前，先问几个问题：每条消息都是很关键且不能容忍丢失么？偶尔重复消息可以么？我们关注的是消息延迟还是写入消息的吞吐量？

举个例子，有一个信用卡交易处理系统，当交易发生时会发送一条消息到 Kafka，另一个服务来读取消息并根据规则引擎来检查交易是否通过，将结果通过 Kafka 返回。对于这样的业务，消息既不能丢失也不能重复，由于交易量大因此吞吐量需要尽可能大，延迟可以稍微高一点。

再举个例子，假如我们需要收集用户在网页上的点击数据，对于这样的场景，少量消息丢失或者重复是可以容忍的，延迟多大都不重要只要不影响用户体验，吞吐则根据实时用户数来决定。

不同的业务需要使用不同的写入方式和配置。具体的方式我们在这里不做讨论，现在先看下生产者写消息的基本流程：

![生产者设计概要](../../../JavaGuide/media/pictures/kafka/生产者设计概要.png)

图片来源：[http://www.dengshenyu.com/%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F/2017/11/12/kafka-producer.html](http://www.dengshenyu.com/分布式系统/2017/11/12/kafka-producer.html)

流程如下：

1. 首先，我们需要创建一个ProducerRecord，这个对象需要包含消息的主题（topic）和值（value），可以选择性指定一个键值（key）或者分区（partition）。
2. 发送消息时，生产者会对键值和值序列化成字节数组，然后发送到分配器（partitioner）。
3. 如果我们指定了分区，那么分配器返回该分区即可；否则，分配器将会基于键值来选择一个分区并返回。
4. 选择完分区后，生产者知道了消息所属的主题和分区，它将这条记录添加到相同主题和分区的批量消息中，另一个线程负责发送这些批量消息到对应的Kafka broker。
5. 当broker接收到消息后，如果成功写入则返回一个包含消息的主题、分区及位移的RecordMetadata对象，否则返回异常。
6. 生产者接收到结果后，对于异常可能会进行重试。



## 讨论四：消费者设计概要

### 消费者与消费组

假设这么个场景：我们从Kafka中读取消息，并且进行检查，最后产生结果数据。我们可以创建一个消费者实例去做这件事情，但如果生产者写入消息的速度比消费者读取的速度快怎么办呢？这样随着时间增长，消息堆积越来越严重。对于这种场景，我们需要增加多个消费者来进行水平扩展。

Kafka消费者是**消费组**的一部分，当多个消费者形成一个消费组来消费主题时，每个消费者会收到不同分区的消息。假设有一个T1主题，该主题有4个分区；同时我们有一个消费组G1，这个消费组只有一个消费者C1。那么消费者C1将会收到这4个分区的消息，如下所示：

![生产者设计概要](../../../JavaGuide/media/pictures/kafka/消费者设计概要1.png)
如果我们增加新的消费者C2到消费组G1，那么每个消费者将会分别收到两个分区的消息，如下所示：

![生产者设计概要](../../../JavaGuide/media/pictures/kafka/消费者设计概要2.png)

如果增加到4个消费者，那么每个消费者将会分别收到一个分区的消息，如下所示：

![生产者设计概要](../../../JavaGuide/media/pictures/kafka/消费者设计概要3.png)

但如果我们继续增加消费者到这个消费组，剩余的消费者将会空闲，不会收到任何消息：

![生产者设计概要](../../../JavaGuide/media/pictures/kafka/消费者设计概要4.png)

总而言之，我们可以通过增加消费组的消费者来进行水平扩展提升消费能力。这也是为什么建议创建主题时使用比较多的分区数，这样可以在消费负载高的情况下增加消费者来提升性能。另外，消费者的数量不应该比分区数多，因为多出来的消费者是空闲的，没有任何帮助。

**Kafka一个很重要的特性就是，只需写入一次消息，可以支持任意多的应用读取这个消息。**换句话说，每个应用都可以读到全量的消息。为了使得每个应用都能读到全量消息，应用需要有不同的消费组。对于上面的例子，假如我们新增了一个新的消费组G2，而这个消费组有两个消费者，那么会是这样的：

![生产者设计概要](../../../JavaGuide/media/pictures/kafka/消费者设计概要5.png)

在这个场景中，消费组G1和消费组G2都能收到T1主题的全量消息，在逻辑意义上来说它们属于不同的应用。

最后，总结起来就是：如果应用需要读取全量消息，那么请为该应用设置一个消费组；如果该应用消费能力不足，那么可以考虑在这个消费组里增加消费者。

### 消费组与分区重平衡

可以看到，当新的消费者加入消费组，它会消费一个或多个分区，而这些分区之前是由其他消费者负责的；另外，当消费者离开消费组（比如重启、宕机等）时，它所消费的分区会分配给其他分区。这种现象称为**重平衡（rebalance）**。重平衡是 Kafka 一个很重要的性质，这个性质保证了高可用和水平扩展。**不过也需要注意到，在重平衡期间，所有消费者都不能消费消息，因此会造成整个消费组短暂的不可用。**而且，将分区进行重平衡也会导致原来的消费者状态过期，从而导致消费者需要重新更新状态，这段期间也会降低消费性能。后面我们会讨论如何安全的进行重平衡以及如何尽可能避免。

消费者通过定期发送心跳（hearbeat）到一个作为组协调者（group coordinator）的 broker 来保持在消费组内存活。这个 broker 不是固定的，每个消费组都可能不同。当消费者拉取消息或者提交时，便会发送心跳。

如果消费者超过一定时间没有发送心跳，那么它的会话（session）就会过期，组协调者会认为该消费者已经宕机，然后触发重平衡。可以看到，从消费者宕机到会话过期是有一定时间的，这段时间内该消费者的分区都不能进行消息消费；通常情况下，我们可以进行优雅关闭，这样消费者会发送离开的消息到组协调者，这样组协调者可以立即进行重平衡而不需要等待会话过期。

在 0.10.1 版本，Kafka 对心跳机制进行了修改，将发送心跳与拉取消息进行分离，这样使得发送心跳的频率不受拉取的频率影响。另外更高版本的 Kafka 支持配置一个消费者多长时间不拉取消息但仍然保持存活，这个配置可以避免活锁（livelock）。活锁，是指应用没有故障但是由于某些原因不能进一步消费。

### Partition 与消费模型

上面提到，Kafka 中一个 topic 中的消息是被打散分配在多个 Partition(分区) 中存储的， Consumer Group 在消费时需要从不同的 Partition 获取消息，那最终如何重建出 Topic 中消息的顺序呢？

答案是：没有办法。Kafka 只会保证在 Partition 内消息是有序的，而不管全局的情况。

下一个问题是：Partition 中的消息可以被（不同的 Consumer Group）多次消费，那 Partition中被消费的消息是何时删除的？ Partition 又是如何知道一个 Consumer Group 当前消费的位置呢？

无论消息是否被消费，除非消息到期 Partition 从不删除消息。例如设置保留时间为 2 天，则消息发布 2 天内任何 Group 都可以消费，2 天后，消息自动被删除。
Partition 会为每个 Consumer Group 保存一个偏移量，记录 Group 消费到的位置。 如下图：
![生产者设计概要](../../../JavaGuide/media/pictures/kafka/Partition与消费模型.png)




### 为什么 Kafka 是 pull 模型

消费者应该向 Broker 要数据（pull）还是 Broker 向消费者推送数据（push）？作为一个消息系统，Kafka 遵循了传统的方式，选择由 Producer 向 broker push 消息并由 Consumer 从 broker pull 消息。一些 logging-centric system，比如 Facebook 的[Scribe](https://github.com/facebookarchive/scribe)和 Cloudera 的[Flume](https://flume.apache.org/)，采用 push 模式。事实上，push 模式和 pull 模式各有优劣。

**push 模式很难适应消费速率不同的消费者，因为消息发送速率是由 broker 决定的。**push 模式的目标是尽可能以最快速度传递消息，但是这样很容易造成 Consumer 来不及处理消息，典型的表现就是拒绝服务以及网络拥塞。**而 pull 模式则可以根据 Consumer 的消费能力以适当的速率消费消息。**

**对于 Kafka 而言，pull 模式更合适。**pull 模式可简化 broker 的设计，Consumer 可自主控制消费消息的速率，同时 Consumer 可以自己控制消费方式——即可批量消费也可逐条消费，同时还能选择不同的提交方式从而实现不同的传输语义。

## 讨论五：Kafka 如何保证可靠性

当我们讨论**可靠性**的时候，我们总会提到*保证**这个词语。可靠性保证是基础，我们基于这些基础之上构建我们的应用。比如关系型数据库的可靠性保证是ACID，也就是原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）和持久性（Durability）。

Kafka 中的可靠性保证有如下四点：

- 对于一个分区来说，它的消息是有序的。如果一个生产者向一个分区先写入消息A，然后写入消息B，那么消费者会先读取消息A再读取消息B。
- 当消息写入所有in-sync状态的副本后，消息才会认为**已提交（committed）**。这里的写入有可能只是写入到文件系统的缓存，不一定刷新到磁盘。生产者可以等待不同时机的确认，比如等待分区主副本写入即返回，后者等待所有in-sync状态副本写入才返回。
- 一旦消息已提交，那么只要有一个副本存活，数据不会丢失。
- 消费者只能读取到已提交的消息。

使用这些基础保证，我们构建一个可靠的系统，这时候需要考虑一个问题：究竟我们的应用需要多大程度的可靠性？可靠性不是无偿的，它与系统可用性、吞吐量、延迟和硬件价格息息相关，得此失彼。因此，我们往往需要做权衡，一味的追求可靠性并不实际。

> 想了解更多戳这里：http://www.dengshenyu.com/%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F/2017/11/21/kafka-data-delivery.html

# 三、动手搭一个 Kafka

通过上面的描述，我们已经大致了解到了「Kafka」是何方神圣了，现在我们开始尝试自己动手本地搭一个来实际体验一把。

## 第一步：下载 Kafka

这里以 Mac OS 为例，在安装了 Homebrew 的情况下执行下列代码：

```shell
brew install kafka
```

由于 Kafka 依赖了 Zookeeper，所以在下载的时候会自动下载。

## 第二步：启动服务

我们在启动之前首先需要修改 Kafka 的监听地址和端口为 `localhost:9092`：

```shell
vi /usr/local/etc/kafka/server.properties
```


然后修改成下图的样子：

![启动服务](../../../JavaGuide/media/pictures/kafka/启动服务.png)
依次启动 Zookeeper 和 Kafka：

```shell
brew services start zookeeper
brew services start kafka
```

然后执行下列语句来创建一个名字为 “test” 的 Topic：

```shell
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```

我们可以通过下列的命令查看我们的 Topic 列表：

```shell
kafka-topics --list --zookeeper localhost:2181
```

## 第三步：发送消息

然后我们新建一个控制台，运行下列命令创建一个消费者关注刚才创建的 Topic：

```shell
kafka-console-consumer --bootstrap-server localhost:9092 --topic test --from-beginning
```

用控制台往刚才创建的 Topic 中添加消息，并观察刚才创建的消费者窗口：

```shel
kafka-console-producer --broker-list localhost:9092 --topic test
```

能通过消费者窗口观察到正确的消息：

![发送消息](../../../JavaGuide/media/pictures/kafka/发送消息.png)

# 参考资料

------

1. https://www.infoq.cn/article/kafka-analysis-part-1 - Kafka 设计解析（一）：Kafka 背景及架构介绍
2. [http://www.dengshenyu.com/%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F/2017/11/06/kafka-Meet-Kafka.html](http://www.dengshenyu.com/分布式系统/2017/11/06/kafka-Meet-Kafka.html) - Kafka系列（一）初识Kafka
3. https://lotabout.me/2018/kafka-introduction/ - Kafka 入门介绍
4. https://www.zhihu.com/question/28925721 - Kafka 中的 Topic 为什么要进行分区? - 知乎
5. https://blog.joway.io/posts/kafka-design-practice/ - Kafka 的设计与实践思考
6. [http://www.dengshenyu.com/%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F/2017/11/21/kafka-data-delivery.html](http://www.dengshenyu.com/分布式系统/2017/11/21/kafka-data-delivery.html) - Kafka系列（六）可靠的数据传输



----

> 原文链接：https://mp.weixin.qq.com/s/zxPz_aFEMrshApZQ727h4g 

## 引言

MQ（消息队列）是跨进程通信的方式之一，可理解为异步rpc，上游系统对调用结果的态度往往是重要不紧急。使用消息队列有以下好处：业务解耦、流量削峰、灵活扩展。接下来介绍消息中间件Kafka。

## Kafka是什么？

Kafka是一个分布式的消息引擎。具有以下特征

能够发布和订阅消息流（类似于消息队列）
以容错的、持久的方式存储消息流
多分区概念，提高了并行能力

## Kafka架构总览

![Kafka系统架构](https://i.loli.net/2020/08/27/oxLakTrFCPUmn5f.png)

## Topic

消息的主题、队列，每一个消息都有它的topic，Kafka通过topic对消息进行归类。Kafka中可以将Topic从物理上划分成一个或多个分区（Partition），每个分区在物理上对应一个文件夹，以”topicName_partitionIndex”的命名方式命名，该dir包含了这个分区的所有消息(.log)和索引文件(.index)，这使得Kafka的吞吐率可以水平扩展。

## Partition

每个分区都是一个 顺序的、不可变的消息队列， 并且可以持续的添加;分区中的消息都被分了一个序列号，称之为偏移量(offset)，在每个分区中此偏移量都是唯一的。
producer在发布消息的时候，可以为每条消息指定Key，这样消息被发送到broker时，会根据分区算法把消息存储到对应的分区中（一个分区存储多个消息），如果分区规则设置的合理，那么所有的消息将会被均匀的分布到不同的分区中，这样就实现了负载均衡。
![partition_info](https://i.loli.net/2020/08/27/rQWdD6vBNPMfE1k.jpg)

## Broker

Kafka server，用来存储消息，Kafka集群中的每一个服务器都是一个Broker，消费者将从broker拉取订阅的消息
Producer
向Kafka发送消息，生产者会根据topic分发消息。生产者也负责把消息关联到Topic上的哪一个分区。最简单的方式从分区列表中轮流选择。也可以根据某种算法依照权重选择分区。算法可由开发者定义。

## Cousumer

Consermer实例可以是独立的进程，负责订阅和消费消息。消费者用consumerGroup来标识自己。同一个消费组可以并发地消费多个分区的消息，同一个partition也可以由多个consumerGroup并发消费，但是在consumerGroup中一个partition只能由一个consumer消费

## CousumerGroup

Consumer Group：同一个Consumer Group中的Consumers，Kafka将相应Topic中的每个消息只发送给其中一个Consumer

# Kafka producer 设计原理

## 发送消息的流程

![partition_info](https://i.loli.net/2020/08/27/tkf5u2PCneEpdMW.jpg)
**1.序列化消息&&.计算partition**
根据key和value的配置对消息进行序列化,然后计算partition：
ProducerRecord对象中如果指定了partition，就使用这个partition。否则根据key和topic的partition数目取余，如果key也没有的话就随机生成一个counter，使用这个counter来和partition数目取余。这个counter每次使用的时候递增。

**2发送到batch&&唤醒Sender 线程**
根据topic-partition获取对应的batchs（Dueue<ProducerBatch>），然后将消息append到batch中.如果有batch满了则唤醒Sender 线程。队列的操作是加锁执行，所以batch内消息时有序的。后续的Sender操作当前方法异步操作。
![send_msg](https://blog-article-resource.oss-cn-beijing.aliyuncs.com/kafka/send2Batch1.png)![send_msg2](https://blog-article-resource.oss-cn-beijing.aliyuncs.com/kafka/send2Batch2.png)



**3.Sender把消息有序发到 broker（tp replia leader）**
**3.1 确定tp relica leader 所在的broker**

Kafka中 每台broker都保存了kafka集群的metadata信息，metadata信息里包括了每个topic的所有partition的信息: leader, leader_epoch, controller_epoch, isr, replicas等;Kafka客户端从任一broker都可以获取到需要的metadata信息;sender线程通过metadata信息可以知道tp leader的brokerId
producer也保存了metada信息，同时根据metadata更新策略（定期更新metadata.max.age.ms、失效检测，强制更新：检查到metadata失效以后，调用metadata.requestUpdate()强制更新

```
public class PartitionInfo { 
    private final String topic; private final int partition; 
    private final Node leader; private final Node[] replicas; 
    private final Node[] inSyncReplicas; private final Node[] offlineReplicas; 
} 
```

**3.2 幂等性发送**

为实现Producer的幂等性，Kafka引入了Producer ID（即PID）和Sequence Number。对于每个PID，该Producer发送消息的每个<Topic, Partition>都对应一个单调递增的Sequence Number。同样，Broker端也会为每个<PID, Topic, Partition>维护一个序号，并且每Commit一条消息时将其对应序号递增。对于接收的每条消息，如果其序号比Broker维护的序号）大一，则Broker会接受它，否则将其丢弃：

如果消息序号比Broker维护的序号差值比一大，说明中间有数据尚未写入，即乱序，此时Broker拒绝该消息，Producer抛出InvalidSequenceNumber
如果消息序号小于等于Broker维护的序号，说明该消息已被保存，即为重复消息，Broker直接丢弃该消息，Producer抛出DuplicateSequenceNumber
Sender发送失败后会重试，这样可以保证每个消息都被发送到broker

**4. Sender处理broker发来的produce response**
一旦broker处理完Sender的produce请求，就会发送produce response给Sender，此时producer将执行我们为send（）设置的回调函数。至此producer的send执行完毕。

## 吞吐性&&延时：

buffer.memory：buffer设置大了有助于提升吞吐性，但是batch太大会增大延迟，可搭配linger_ms参数使用
linger_ms：如果batch太大，或者producer qps不高，batch添加的会很慢，我们可以强制在linger_ms时间后发送batch数据
ack：producer收到多少broker的答复才算真的发送成功
0表示producer无需等待leader的确认(吞吐最高、数据可靠性最差)
1代表需要leader确认写入它的本地log并立即确认
-1/all 代表所有的ISR都完成后确认(吞吐最低、数据可靠性最高)

## Sender线程和长连接

每初始化一个producer实例，都会初始化一个Sender实例，新增到broker的长连接。
代码角度：每初始化一次KafkaProducer，都赋一个空的client

```
public KafkaProducer(final Map<String, Object> configs) { 
	this(configs, null, null, null, null, null, Time.SYSTEM);
}
```

![Sender_io](https://i.loli.net/2020/08/27/L45uigckvOXf7DY.jpg)

终端查看TCP连接数：
lsof -p portNum -np | grep TCP

# Consumer设计原理

## poll消息

![consumer-pool](https://i.loli.net/2020/08/27/6yhNuMifHxqsTzF.jpg)

- 消费者通过fetch线程拉消息（单线程）
- 消费者通过心跳线程来与broker发送心跳。超时会认为挂掉
- 每个consumer
    group在broker上都有一个coordnator来管理，消费者加入和退出，以及消费消息的位移都由coordnator处理。

## 位移管理

consumer的消息位移代表了当前group对topic-partition的消费进度，consumer宕机重启后可以继续从该offset开始消费。
在kafka0.8之前，位移信息存放在zookeeper上，由于zookeeper不适合高并发的读写，新版本Kafka把位移信息当成消息，发往__consumers_offsets 这个topic所在的broker，__consumers_offsets默认有50个分区。
消息的key 是groupId+topic_partition,value 是offset.

![consumerOffsetDat](https://i.loli.net/2020/08/27/T5k1dburtNjaBpG.jpg)![consumerOffsetView](https://i.loli.net/2020/08/27/Tz34Ebm2jynJpXi.jpg)



## Kafka Group 状态

![groupState](https://i.loli.net/2020/08/27/qsgEmYxA1dp948z.jpg)

- Empty：初始状态，Group 没有任何成员，如果所有的 offsets 都过期的话就会变成 Dead
- PreparingRebalance：Group 正在准备进行 Rebalance
- AwaitingSync：Group 正在等待来 group leader 的 分配方案
- Stable：稳定的状态（Group is stable）；
- Dead：Group 内已经没有成员，并且它的 Metadata 已经被移除

## 重平衡reblance

当一些原因导致consumer对partition消费不再均匀时，kafka会自动执行reblance，使得consumer对partition的消费再次平衡。
什么时候发生rebalance？：

- 组订阅topic数变更
- topic partition数变更
- consumer成员变更
- consumer 加入群组或者离开群组的时候
- consumer被检测为崩溃的时候

## reblance过程

举例1 consumer被检测为崩溃引起的reblance
比如心跳线程在timeout时间内没和broker发送心跳，此时coordnator认为该group应该进行reblance。接下来其他consumer发来fetch请求后，coordnator将回复他们进行reblance通知。当consumer成员收到请求后，只有leader会根据分配策略进行分配，然后把各自的分配结果返回给coordnator。这个时候只有consumer leader返回的是实质数据，其他返回的都为空。收到分配方法后，consumer将会把分配策略同步给各consumer

举例2 consumer加入引起的reblance

使用join协议，表示有consumer 要加入到group中
使用sync 协议，根据分配规则进行分配
![reblance-join](https://i.loli.net/2020/08/27/FERGIStc4ygqsiX.jpg)![reblance-sync](https://i.loli.net/2020/08/27/B3N9Mkl1WaOqL5c.jpg)

(上图图片摘自网络)

## 引申：以上reblance机制存在的问题

在大型系统中，一个topic可能对应数百个consumer实例。这些consumer陆续加入到一个空消费组将导致多次的rebalance；此外consumer 实例启动的时间不可控，很有可能超出coordinator确定的rebalance timeout(即max.poll.interval.ms)，将会再次触发rebalance，而每次rebalance的代价又相当地大，因为很多状态都需要在rebalance前被持久化，而在rebalance后被重新初始化。

## 新版本改进

**通过延迟进入PreparingRebalance状态减少reblance次数**

![groupStateOfNewVersion](https://i.loli.net/2020/08/27/tIeKJdoRDMPCBQj.jpg)

新版本新增了group.initial.rebalance.delay.ms参数。空消费组接受到成员加入请求时，不立即转化到PreparingRebalance状态来开启reblance。当时间超过group.initial.rebalance.delay.ms后，再把group状态改为PreparingRebalance（开启reblance）。实现机制是在coordinator底层新增一个group状态：InitialReblance。假设此时有多个consumer陆续启动，那么group状态先转化为InitialReblance，待group.initial.rebalance.delay.ms时间后，再转换为PreparingRebalance（开启reblance）



# Broker设计原理

Broker 是Kafka 集群中的节点。负责处理生产者发送过来的消息，消费者消费的请求。以及集群节点的管理等。由于涉及内容较多，先简单介绍，后续专门抽出一篇文章分享

## broker zk注册

![brokersInZk](https://i.loli.net/2020/08/27/KHusb9dIBSqg4AY.jpg)

## broker消息存储

Kafka的消息以二进制的方式紧凑地存储，节省了很大空间
此外消息存在ByteBuffer而不是堆，这样broker进程挂掉时，数据不会丢失，同时避免了gc问题
通过零拷贝和顺序寻址，让消息存储和读取速度都非常快
处理fetch请求的时候通过zero-copy 加快速度

## broker状态数据

broker设计中，每台机器都保存了相同的状态数据。主要包括以下：

controller所在的broker ID，即保存了当前集群中controller是哪台broker
集群中所有broker的信息：比如每台broker的ID、机架信息以及配置的若干组连接信息
集群中所有节点的信息：严格来说，它和上一个有些重复，不过此项是按照broker ID和***类型进行分组的。对于超大集群来说，使用这一项缓存可以快速地定位和查找给定节点信息，而无需遍历上一项中的内容，算是一个优化吧
集群中所有分区的信息：所谓分区信息指的是分区的leader、ISR和AR信息以及当前处于offline状态的副本集合。这部分数据按照topic-partitionID进行分组，可以快速地查找到每个分区的当前状态。（注：AR表示assigned replicas，即创建topic时为该分区分配的副本集合）

## broker负载均衡

**分区数量负载**：各台broker的partition数量应该均匀
partition Replica分配算法如下：

将所有Broker（假设共n个Broker）和待分配的Partition排序
将第i个Partition分配到第（i mod n）个Broker上
将第i个Partition的第j个Replica分配到第（(i + j) mod n）个Broker上

**容量大小负载：**每台broker的硬盘占用大小应该均匀
在kafka1.1之前，Kafka能够保证各台broker上partition数量均匀，但由于每个partition内的消息数不同，可能存在不同硬盘之间内存占用差异大的情况。在Kafka1.1中增加了副本跨路径迁移功能kafka-reassign-partitions.sh，我们可以结合它和监控系统，实现自动化的负载均衡

# Kafka高可用

在介绍kafka高可用之前先介绍几个概念

同步复制：要求所有能工作的Follower都复制完，这条消息才会被认为commit，这种复制方式极大的影响了吞吐率
异步复制：Follower异步的从Leader pull数据，data只要被Leader写入log认为已经commit，这种情况下如果Follower落后于Leader的比较多，如果Leader突然宕机，会丢失数据

## Isr

Kafka结合同步复制和异步复制，使用ISR（与Partition Leader保持同步的Replica列表）的方式在确保数据不丢失和吞吐率之间做了平衡。Producer只需把消息发送到Partition Leader，Leader将消息写入本地Log。Follower则从Leader pull数据。Follower在收到该消息向Leader发送ACK。一旦Leader收到了ISR中所有Replica的ACK，该消息就被认为已经commit了，Leader将增加HW并且向Producer发送ACK。这样如果leader挂了，只要Isr中有一个replica存活，就不会丢数据。

## Isr动态更新

Leader会跟踪ISR，如果ISR中一个Follower宕机，或者落后太多，Leader将把它从ISR中移除。这里所描述的“落后太多”指Follower复制的消息落后于Leader后的条数超过预定值（replica.lag.max.messages）或者Follower超过一定时间（replica.lag.time.max.ms）未向Leader发送fetch请求。

broker Nodes In Zookeeper
/brokers/topics/[topic]/partitions/[partition]/state 保存了topic-partition的leader和Isr等信息

![partitionStateInZk](https://i.loli.net/2020/08/27/I3vkWjgdxstcfNF.jpg)

## Controller负责broker故障检查&&故障转移（fail/recover）

1. Controller在Zookeeper上注册Watch，一旦有Broker宕机，其在Zookeeper对应的znode会自动被删除，Zookeeper会触发
    Controller注册的watch，Controller读取最新的Broker信息
2. Controller确定set_p，该集合包含了宕机的所有Broker上的所有Partition
3. 对set_p中的每一个Partition，选举出新的leader、Isr，并更新结果。

3.1 从/brokers/topics/[topic]/partitions/[partition]/state读取该Partition当前的ISR

3.2 决定该Partition的新Leader和Isr。如果当前ISR中有至少一个Replica还幸存，则选择其中一个作为新Leader，新的ISR则包含当前ISR中所有幸存的Replica。否则选择该Partition中任意一个幸存的Replica作为新的Leader以及ISR（该场景下可能会有潜在的数据丢失）

![electLeader](https://i.loli.net/2020/08/27/CUgY8RScjdFObIx.jpg)
3.3 更新Leader、ISR、leader_epoch、controller_epoch：写入/brokers/topics/[topic]/partitions/[partition]/state

4. 直接通过RPC向set_p相关的Broker发送LeaderAndISRRequest命令。Controller可以在一个RPC操作中发送多个命令从而提高效率。

## Controller挂掉

每个 broker 都会在 zookeeper 的临时节点 "/controller" 注册 watcher，当 controller 宕机时 "/controller" 会消失，触发broker的watch，每个 broker 都尝试创建新的 controller path，只有一个竞选成功并当选为 controller。

# 使用Kafka如何保证幂等性

不丢消息

首先kafka保证了对已提交消息的at least保证
Sender有重试机制
producer业务方在使用producer发送消息时，注册回调函数。在onError方法中重发消息
consumer 拉取到消息后，处理完毕再commit，保证commit的消息一定被处理完毕

不重复

consumer拉取到消息先保存，commit成功后删除缓存数据

# Kafka高性能

partition提升了并发
zero-copy
顺序写入
消息聚集batch
页缓存
业务方对 Kafka producer的优化

增大producer数量
ack配置
batch

