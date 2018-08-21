# org.apache.ibaties.executor

### Executor
执行器。包含更新、查询、事务、缓存处理、延迟加载。

### ResultExtractor
只有一个公共方式```Object extractObjectFromList(List<Object> list, Class<?> targetType)```作用为将```list```转化为```targetType```指定类型。判断过程如下：
-   `list`不为`null`。若`targeType`为`list`同类或其子类则直接返回`list`
-    `list`不为`null`。使用`ObjectFactory`的`isCollection`判断`targetType`是否为集合，若是则使用`ObjectFactory`创建这个集合类型的对象并把`list`加入进去，返回这集合对象
-    `list`不为`null`。若`targetType`是个数组类型，当这个数组的元素类型是基本类型时，就创建这个基本类型的数组迭代存入`list`的每个值，然后返回这个基本类型数组；当这个数组的元素类型不是是基本类型时则直接将`list`转成数组返回。这里第一个情况隐含了`list`的泛型类型是`targetType`的元素类型的包装类，反则返回在`Array.set()`时出现异常。
-    `list`不为`null`。若`list`为`null`或长度对于1则抛出异常，若`list`不为空且长度为1则返回唯一的一个元素。
-   若都不符合上述条件则返回`null`
## 其它

### ResultSet
有几个常量
-   3个常量声明了```ResultSet```处理顺序
-   3个常量声明了游标是否数据变化敏感
-   2个常量声明并发模式
-   2个常量事务关闭后```ResultSet```是否可用
