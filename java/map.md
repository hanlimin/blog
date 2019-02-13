##HashMap
hash计算 (h = (key == null) ? 0 : key.hashCode()) ^ (h >>> 16)
索引计算 hash & (length - 1)
## put调用hash方法计算出了key的hash值而后调用putVal方法完成添加。
-   若table为null，则说明是首次添加，调用resize方法完成table数组初始化。
-   计算出hash对应的桶索引，若桶为空直接赋值
-   若桶不为空，桶内节点与欲添加值hash和key都相等，进入旧值替换判断
-   若桶内节点为TreeNode实例，向红黑树添加节点
-   若桶内是链表，若无相同hash和key则创建节点添加到尾部，当链表长度超过8个则替换成红黑树。 若存在相同的，进入旧值替换判断，
-   旧值替换判断，若允许旧值替换或旧值为null，则替换旧值且返回旧值
-   最后，判断节点数量是否超出阈值，若超出则调用resize进行扩容。
##HashTable
hash计算 key.hashCode()
索引计算 (hash & 0x7FFFFFFF) % length
### put
-   计算出索引值，若对应桶内有节点，遍历这个节点若hash和key相等则替换旧值并返回旧值
-   调用addEntry添加新节点
-   判断节点数量是否超出阈值，超出则调用rehash扩容
-   创建节点添加

