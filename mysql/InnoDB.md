### InnoDB

InnoDB架构图

<img src="https://i.loli.net/2020/08/27/ZDnYpebSyN35HGU.png" />

### 储存逻辑划分

| 类型 | 作用 |
| ------ | ----------------------------------------------------------- |
| 表空间 | 表空间是InnoDB中的最高抽象层次。 |
| 段     | 表空间又是由段组成的，段通常又分为数据段、索引段、回滚段等等。对于数据段它就对应于 B+ 树上的的叶子节点、索引段对应于 B+ 树上的非叶子节点。 |
| 区     | 区是由连续页组成的空间，任何情况下区的大小均为1MB,默认情况下InnDB 引擎页的大小为16KB，因此一个区默认情况下一共有 64 个页。 |
| 页     | InnDB 磁盘管理的最小单位，默认为16KB。                       |
| 行     | 数据库中的数据最终是以行的形式存放在页中。                   |

### 缓冲池

内容包括：索引、行的数据、自适应哈希索引、插入缓冲、锁以及其它内部数据。使用缓冲可以延迟写入，这样就可以合并多个写入操作，然后一起顺序的写回。大的缓冲池会导致预热和关闭都会话费很长时间。如果事先知道什么时候关闭InnoDB，可以在运行时修改`innodb_max_dirty_pages_pct`变量，将值变小，等待刷新线程清理缓冲池，然后在脏页数量较少时关闭。在启动时，预热缓冲池也可能会花费很长时间，可以通过立刻进行全表扫描或者索引扫描等方法直接加快预热过程。可以使用`init_file`设置来达到加快的目的。

- `innodb_max_dirty_pages_pct` InnoDB中缓冲池脏页占比。
- `innodb_buffer_pool_size` InnoDB缓冲池大小

### read-ahead

如果`InnoDB`可以确定很可能很快就需要数据，它会执行 read-ahead 操作以将该数据放入缓冲池，以便在 memory 中可用。对连续数据进行一些大的读取请求比发出几个小的 spread-out 请求更有效。 `InnoDB`中有两个 read-ahead 启发式：

- 在顺序 read-ahead 中，如果`InnoDB`注意到表空间中某个段的访问 pattern 是顺序的，它会事先将一批数据库页面读取到 I/O 系统。
- 在随机 read-ahead 中，如果`InnoDB`注意到表空间中的某些区域似乎处于完全读入缓冲池的 process 中，则会将剩余的读取发布到 I/O 系统

```properties
# 顺序页面访问模式时检测的敏感程度
innodb_read_ahead_threshold
# 开启随机读
innodb_random_read_ahead
```

### Redo事务日志

InnoDB使用日志来减少提交事务时的开销。因为日志中已经记录了事务，就无需在每个事务提交时把缓冲池的脏块刷新到磁盘中。事务修改的数据和索引通常会映射到表空间的随机位置，所以刷新这些变更到磁盘需要很多随机I/O。InnoDB使用日志把随机I/O变成顺序I/O。一旦日志安全写到磁盘，事务就持久化了，即使变更还没写到数据文件。InnoDB的日志时环形方式写的：当写到文件的尾部，会重新跳转到开头继续写，但不会覆盖到还未应用到数据文件的日志记录。

InnoDB使用一个后台线程智能地刷新这些变更到数据文件。这个线程可以批量组合写入，使得数据写入更顺序，以提高效率。整体日志文件大小受控于`innodb_log_file_size`和`innodb_log_files_in_group`两个参数，这对写性能非常重要。InnoDB使用多个文件作为一组循环日志。通常不需要修改默认日志数量，只修改每个日志文件的大小即可。如果有大事务，可以增加日志缓冲区大小可以帮助减少I/O。变量`innodb_log_buffer_size`可以控制日志缓冲区的大小。

可以通过`SHOW INNODB STATUS`的输出中LOG部分来监控InnoDB的日志和日志缓冲区的I/O性能。

作为经验法则，日志文件的全部大小，应该足够容纳服务器一个小时的活动内容。

- `innodb_log_file_size`：每个日志文件大小
- `innodb_log_files_in_group`：在每组日志文件中的日志文件数量。
- `innodb_log_buffer_size` 日志缓冲大小。
- `innodb_flush_log_at_trx_commit`：日志缓冲的刷新时间控制。

### InnoDB表空间

InnoDB把数据保存在表空间内，本质上是有一个或多个磁盘文件组成的虚拟文件系统。InnoDB使用表空间实现很多功能，并不只是储存表和索引，它保存了回滚日志、插入缓冲、双写缓冲以及其它内部数据结构。通过`innodb_date_file_path`配置项可以定制表空间文件。这些文件放在`innodb_data_home_dir`指定的目录下。开启`innodb_file_per_table`选项可以是每个表对应一个表空间。即使打开了`innodb_file_per_table`选项，依然需要为回滚日志和其他系统数据创建共享表空间。

- `innodb_date_file_path`： 定义了InnoDB表空间数据文件的名字、大小等属性。`autoextend`允许表空间在超过了分配的空间是还能增长，可以配置最后一个文件自动扩展。可以再使用`max`配置自动扩展文件大小上限。
- `innodb_data_home_dir`：指定了InnoDB表空间数据文件所在目录。
- `innodb_file_per_table`：一个开关选项，是否让InnoDB为每张表使用一个文件。即一个表对应一个表空间。

### InnoDB数据字典（Date Dictionary）

InnoDB自己的表缓存。当InnoDB打开一张表，就增加了一个对应的对象到数据字典。每张表可能占用4KB或者更多的内存，当表关闭时也不会从数据字典中移除它们。因此，随着时间推移，导致数据字典中的元素不断地增长。相比MyISAM，InnoDB没有将统计信息持久化，而是每次打开表时重新计算，这需要很多I/O操作，所以代价很高。在打开之后，每隔一段时间或者遇到触发事件，也会重新计算统计信息。可以开启` innodb_stats_persistent`选项来持久化统计信息以解决这个问题。即使开启之后，InnoDB统计操作还可能对服务器和一些特定的查询产生冲击，可以关闭`innodb_stats_on_metadata`选项来避免耗时的表统计信息刷新。

- ` innodb_stats_persistent` 持久化统计信息到磁盘。
- `innodb_stats_on_metadata` 表统计信息刷新开关。

### Undo事务日志

undo log有两个作用：提供回滚和多个行版本控制(MVCC)。在数据修改的时候，备份了原始数据，如果因为某些原因导致事务失败或回滚了，可以借助该undo进行回滚。

在写压力大的环境下，InnoDB的表空间可能增长得非常大。如果事务保持打开状态很久，并且使用默认的REPEATABLE READ事务隔离级别，InnoDB将不能删除旧的行版本。InnoDB把旧版本存在共享表空间，所以如果有更多的数据在更新，共享表空间会持续增长。没有清理的行版本会对所有的查询产生影响，因为它们事实上使得表和索引更大了。

MySQL使用一个线程来清理事务，如果工作负载过高可能导致清理线程处理速度跟不上旧版本行数增加的速度。可以使用`SHOW ENGINE INNODB STATUS`命令可以观察历史链表的长度来定位问题。可以配置`innodb_max_purge_lag`强制MySQL减速来使InnoDB的清理线程可以跟得上。

- `innodb_max_purge_lag`：定义了清理线程可以等待被清理的最大事务数量。

### 双写缓冲

InnoDB使用双写缓冲来避免页没写完整所导致的数据损坏。当InnoDB从缓冲池刷新页面到磁盘时，首先把它们写到双写缓冲，然后再把它们写到其所属的数据区域中。如果有一个不完整的页写到了双写缓冲，原始的页依然会在磁盘上它的真实位置。当InnoDB恢复时，它将用原始页面替换掉双写缓冲中的损失页面。然而，如果双写缓冲成功写入，而写到页真实位置失败了，InnoDB在恢复时将使用双写缓冲中的拷贝来替换。有些场景下，双写缓冲确实没有必要。可以通过设置`innodb_doublewrite`为0来关闭双写缓冲。

- `innodb_doublewrite`：一个开关选项，是否开启双写缓冲。

### 行格式

| Row Format   | Compact Storage Characteristics | Enhanced Variable-Length Column Storage | Large Index Key Prefix Support | Compression Support | Supported Tablespace            | Required File Format  |
| ------------ | ------------------------------- | --------------------------------------- | ------------------------------ | ------------------- | ------------------------------- | --------------------- |
| `REDUNDANT`  | No                              | No                                      | No                             | No                  | system, file-per-table, general | Antelope or Barracuda |
| `COMPACT`    | Yes                             | No                                      | No                             | No                  | system, file-per-table, general | Antelope or Barracuda |
| `DYNAMIC`    | Yes                             | Yes                                     | Yes                            | No                  | system, file-per-table, general | Barracuda             |
| `COMPRESSED` | Yes                             | Yes                                     | Yes                            | Yes                 | file-per-table, general         | Barracuda             |

一个表的行格式决定了行是如何物理储存，这会影响查询和DML操作的性能。如果更多的行储存进一个硬盘页中，查询和索引查找会工作更快，减少在Buffer Pool的内存占用，减少写入更新数值时的I/O。

在早期的InnoDB版本中，由于文件格式只有一种，因此不需要为此文件格式命名。随着InnoDB引擎的发展，开发出了不兼容早期版本的新文件格式，用于支持新的功能。为了在升级和降级情况下帮助管理系统的兼容性，以及运行不同的MySQL版本，InnoDB开始使用命名的文件格式。

目前，InnoDB只支持两种文件格式：Antelope 和 Barracuda。

- Antelope: 先前未命名的，原始的InnoDB文件格式。它支持两种行格式：COMPACT 和 REDUNDANT。MySQL 5.6的默认文件格式。可以与早期的版本保持最大的兼容性。不支持 Barracuda 文件格式。
- Barracuda: 新的文件格式。它支持InnoDB的所有行格式，包括新的行格式：COMPRESSED 和 DYNAMIC。与这两个新的行格式相关的功能包括：InnoDB表的压缩，长列数据的页外存储和索引建前缀最大长度为3072字节

在MySQL 5.7.9 及以后版本，默认行格式由`innodb_default_row_format`变量决定，它的默认值是`DYNAMIC`，也可以在 create table 的时候指定`ROW_FORMAT=DYNAMIC`。用户可以通过命令 `SHOW TABLE STATUS LIKE table_name` 来查看当前表使用的行格式，其中 row_format 列表示当前所使用的行记录结构类型。

#### REDUNDANT

`REDUNDANT`行格式提供与旧版MySQL(5.0以前)的兼容性。 

`REDUNDANT`行格式保存可变长度列（`VARCHAR`、`VARBINARY`、`BLOB`、`TEXT`）的头部768字节数据在B-tree节点的索引记录中，而其余数据在溢出页中。对于定长列的长度大于等于768字节是也会当作可变长度列处理。

#### COMPACT

与`REDUNDANT`行格式相比，`COMPACT`行格式减少了大约 20％的行存储空间，代价是增加了某些操作的 CPU 使用。如果您的工作负载是受缓存命中率和磁盘速度限制的典型工作负载，则`COMPACT`格式可能会更快。如果工作负载受 CPU 速度限制，则紧凑格式可能会变慢。在`VARCHAR`、`VARBINARY`、`BLOB`、`TEXT`这些类型的处理与REDUNDANT相同。 MySQL 5.6版本的默认行格式。

#### DYNAMIC

`DYNAMIC`行格式提供与`COMPACT`行格式相同的存储特性，但添加了增强的存储功能，并支持大型索引前缀。

`DYNAMIC`行格式在保存可变长度列（`VARCHAR`、`VARBINARY`、`BLOB`、`TEXT`)时使用完全溢出页，在索引中只保存20字节指向溢出页的指针。对于定长列的长度大于等于768字节是也会当作可变长度列处理。

`DYNAMIC`行格式支持索引前缀，最多 3072 个字节。此 特性由`innodb_large_prefix`变量控制，该变量默认启用。 

#### COMPRESSED

`DYNAMIC`行格式提供与`DYNAMIC`行格式相同的存储特性，但增加了对 表和索引数据压缩的支持。

### Checkpoint机制

 InnoDB出于性能的考虑，所有的更改操作都是在内存上进行的，之后通过批量处理的方式将脏页刷新回磁盘。 当数据库宕机恢复时，不需要依据所有的redo log 进行恢复，只需要找到上一个检查点，从这个检查点开始进行数据恢复。

### Adaptive Hash Index 

 InnoDB 内部会对表上的所有索引页的查询使用情况进行监控统计，如果观察到某些数据访问非常频繁，InnoDB会对这些数据建立哈希索引来提升性能，这种技术叫做自适应哈希索引。这个过程外界是完全透明的并且不可干预。 

### Flush Neighbor Page

InnoDB 在刷新一个脏页的时候，会检测该页所在区的所有页，如果是脏页那么一并刷新回磁盘。这样做的好处是多个写入操作合并成一个写入操作，这个功能对于传统机械硬盘有着显著的好处，但是目前SSD 固态硬盘已经开始普及，当硬盘IOPS较高的时候，该特性效果并不明显，且效率不高——在如果该区所在的页的数据变化并不大的情况下，比如某个页只更新一个数据，这个时候进行了合并写入，之后很可能更新了该页的其他行，这个页又变成了脏页。这个时候该页需要不停的重复刷入磁盘。因此在 IOPS 较高的硬件下，可以考虑关闭该功能，以避免不必要的开销。

### InnoDB刷新方法

使用`innodb_flush_method`选项可以配置InnoDB如何跟系统文件系统相互作用。Windows和非Windows的操作系统对这个选项的值是互斥的。