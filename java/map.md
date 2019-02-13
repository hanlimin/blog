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
##LinkedHashMap
继承自HashMap，使用双向链表储存了所有节点，重写了newNode、newTreeNode、replacementNode、replacementTreeNode方法创建的新节点会添加到链表尾部。重写了afterNodeRemoval方法，在删除节点时也从链表中删除。重写了afterNodeInsertion方法，留下了removeEldestEntry方法hook用于判断是否删除最老节点。重写了afterNodeAccess方法了，如果表示accessOrder为true，就会将刚访问过的节点放在链表尾部。这个map的节点迭代方法forEach和entrySet迭代都是通过链表完成的
也就是说迭代是有序的，默认下就是节点添加顺序，如果启用了accessOrder那就一个LRU排序。
##HashTable
hash计算 key.hashCode()
索引计算 (hash & 0x7FFFFFFF) % length
所有公共方法都加了synchronized
### put
-   计算出索引值，若对应桶内有节点，遍历这个节点若hash和key相等则替换旧值并返回旧值
-   调用addEntry添加新节点
-   判断节点数量是否超出阈值，超出则调用rehash扩容
-   创建节点添加

## TreeMap
就是一个红黑树。实现了NavigableMap接口，基于Tree的有序的原因，提供了获取极值、获取大于或小于指定key值的节点有序集合
## WeakHashMap


