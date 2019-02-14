##HashMap
hash计算 (h = (key == null) ? 0 : key.hashCode()) ^ (h >>> 16)
索引计算 hash & (length - 1)
允许key为null，
## put
-   调用hash方法计算出可以的hash值，而后调用putVal
-   若table为null，则说明是首次添加，调用resize方法完成table数组初始化。
-   计算出hash对应的桶索引，若桶为空直接赋值
-   若桶不为空，桶内节点与欲添加值hash和key都相等，进入旧值替换判断
-   若桶内节点为TreeNode实例，向红黑树添加节点
-   若桶内是链表，若无相同hash和key则创建节点添加到尾部，当链表长度超过8个则替换成红黑树。 若存在相同的，进入旧值替换判断，
-   旧值替换判断，若允许旧值替换或旧值为null，则替换旧值且返回旧值
-   最后，判断节点数量是否超出阈值，若超出则调用resize进行扩容。
##LinkedHashMap
继承自HashMap，使用双向链表储存了所有节点，重写了newNode、newTreeNode、replacementNode、replacementTreeNode方法创建的新节点会添加到链表尾部。重写了afterNodeRemoval方法，在删除节点时也从链表中删除。重写了afterNodeInsertion方法，留下了removeEldestEntry方法hook用于判断是否删除最老节点。重写了afterNodeAccess方法了，如果表示accessOrder为true，就会将刚访问过的节点放在链表尾部。这个map的节点迭代方法forEach和entrySet迭代都是通过链表完成的
也就是说迭代是有序的，默认下就是节点添加顺序，如果启用了accessOrder那就一个LRU排序。
##HashTable
不允许key为null
hash计算 key.hashCode()
索引计算 (hash & 0x7FFFFFFF) % length
所有公共方法都加了synchronized
### put
-   计算出索引值，若对应桶内有节点，遍历这个节点若hash和key相等则替换旧值并返回旧值
-   调用addEntry添加新节点
-   判断节点数量是否超出阈值，超出则调用rehash扩容
-   创建节点添加

## TreeMap
不允许key为空，使用构造方法注入comparator来进行比较，如果没有comparator就要求key实现了Comparable接口没有则抛出转型失败异常。
就是一个红黑树。实现了NavigableMap接口，基于Tree的有序的原因，提供了获取极值、获取大于或小于指定key值的节点有序集合的方法。
## WeakHashMap
hash计算 h = k.hashCode(); h ^= (h >>> 20 ) ^ (h >>> 12); h ^= (h >>> 7) ^ (h >>> 4);
索引计算 h & (length - 1)
### put
-   调用getTable，这个方法内部会调用expungeStaleEntries方法，清理ReferenceQueue队列queue内所有key失效的节点在table对应的节点。
-   根据计算出索引查找是否存在旧值，有就直接替换返回。
-   没有旧值则创建新节点添加。
-   阈值判断，超出则扩容2倍
所有公共都会导致调用expungeStaleEntries达成无效节点清理。

## IdentityHashMap
hash计算 h = System.identityHashCode(x); h = (h << 1) - (h << 8) 
索引计算 h & (length -1)
冲突解决 开放寻址法
计算出的索引数字必为偶数，这个map使用偶数索引储存key值，使用key值后一位索引储存对应的value
### put
-   计算出索引值，查询是否存在旧值，有就进行value的替换，没有就检查下一个索引位置，直到查到旧值替换返回或查到空桶跳出循环
-   判断节点数量是否超出长度1/3的阈值，超出则扩容2倍，并使用标签跳到第一步循环开始处
-   在偶空桶放key，后一位放value

## EnumMap
利用枚举数量固定且枚举自身就有一个序号，构建一个数组存值。

