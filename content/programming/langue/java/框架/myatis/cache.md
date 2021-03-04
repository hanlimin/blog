---
title: cache
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### Cache

缓存接口有获取缓存编号、添加移除清空键值方法、获取键值数量、获取读写锁等方法。

### PerpertualCache

实现了``Cache``接口，内部使用``HashMap``实现的缓存功能。

### 装饰器

其它类都是提供独功能的装饰器类

- BlockingCache 使用``ReentrantLock``实现了若获取``key``值时，若对应值不存在则阻塞线程到值被添加
- ``FifoCache``  使用双向链表储存key，储存的key数量受类属性``size``限制。
- ``LoggingCache`` 记录了获取key对应值的请求次数和命中次数，在开启DEBUG日志等级下会在``getObject``方法中日志输出命中率。
- ``LruCache`` 使用``LinkedHashMap``实现的LRU最近最少使用。
- ``ScheduledCache`` 根据指定时长，定时清空缓存。
- ``SerializedCache`` 在储存对象时会序列化为字节数组，取出对象时又会反序列化。
- ``SoftCache`` 使用SoftEntry以值作为软引用当内存不足而被GC清理时自动从缓存中清理对应键值对。在``getObject``方法中当获取到值时添加到另一个双端链表中，这个链表使用固定容量，超出则移除尾部元素，每次都是在头部添加元素，目的是留下命中键值对的强引用避免GC时被清理。
- ``SynchronizedCache`` 大部分方法都加上了``synchronized`` 
- ``TransactionalCache`` 在原缓存基础上使用``HashMap`` 实现了二层缓存，``Cache``接口中部分都是在这个二层缓存上处理不直接作用于封装缓存，另提供了``commint`` 方法将二层缓存中的值添加到封装缓存中并重置缓存，``rollback``方法则将封装缓存中将未命中的键值对移除。
- ``WeakCache`` 和``SoftCache``相似使用的弱引用。

### TransactionalCacheManager

内部使用``HashMap``保存了``Cache``对``TransactionalCache``键值对，提供了对缓存操作的方法。

