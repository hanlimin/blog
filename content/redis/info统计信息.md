### info Persistence

| 属性名                      | 属性值                              |
| --------------------------- | ----------------------------------- |
| rdb_bgsave_in_progress      | bgsave子进程是否正在运行            |
| rdb_current_bgsave_time_sec | 当前运行bgsave的时间，-1表示未运行  |
| aof_enable                  | 是否开启AOF功能                     |
| aof_rewrite_in_progress     | AOF重写子进程是否正在运行           |
| aof_rewrite_scheduled       | 在bgsave结束后是否运行AOF重写       |
| aof_current_rewrite_sec     | 当前运行AOF重写的时间，-1表示未运行 |
| aof_current_size            | AOF文件当前字节数                   |
| aof_base_size               | AOF上次重写rewrite的字节数          |

### info memory

| 属性名                  | 属性说明                                                    |
| :---------------------- | :---------------------------------------------------------- |
| used_memory             | Redis分配器分的内存总量，也就是内部储存的所有数据内存占用量 |
| used_menory_human       | 以可读的格式返回used_memory                                 |
| used_menory_rss         | 以操作系统的角度显示Redis进程占用的物理内存总量             |
| used_memory_peak        | 内存使用的最大值，表示used_memory的峰值                     |
| used_menory_peak_human  | 以可读的格式返回used_memory_peak                            |
| used_memory_lua         | Lua引擎所消耗的内存大小                                     |
| mem_fragmentation_ratio | used_menory_rss/used_memory比值，表示内存碎片率             |
| mem_allocator           | Redis所使用的内存分配器。默认为jemalloc                     |

