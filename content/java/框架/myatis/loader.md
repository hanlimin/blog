### ProxyFactory
一个接口，就只有两个方法。
setProperties方法入参就是Properties用来配置属性。
createProxy用来创建指定对象的代理对象，入参有：
-   targe Object原对象
-   lazyLoader ResultLoaderMap 包含延迟加载信息对象
-   configuration Configuration 配置对象
-   objectFactory ObjectFactory对象工厂
-   constructorArgTypes List<Class<?>> 构造方法参数类型列表
-   constructorArgs List<Object> 构造方法参数列表

### CglibProxyProxyFactory
借助cglib实现了ProxyFactory接口。
-   createProxy
    一个静态方法，根据入参创建Enhancer对象，如果父类中没有```writeReplace```会在enhance中添加WriteReplaceInterface接口，之后根据构造参数情况调用Enhance.create方法返回增强后的子类实例。
### EnhancedResultObjectProxyImpl
在CglibProxyProxyFactory内的一个内部类，实现了MethodInterceptor接口。
-   intercept
    如果执行的方法是```writeReplace```，会通过objectFactory创建出新的original对象，复制原对象属性到新对象上，若lazyLoader有加载内容则创建CglibSerialStateHolder返回，否则直接返回original。其它若lazyLoader有加载内容且方法名不是finalize则进入下个逻辑内，若开启了aggressive或是lazyLoaderTriggerMethods方法则加载所有内容，若是个setter方法则从lazyloader中删除这个属性不再加载，若是getter方法是待加载属性则直接加载。
第一步判断，用于序列化的，和clone方法相似，创建出新的对象而不影响原对象，存疑？
第二判断中，加载完成的属性不会再次加载，对象中若首次调用某一属性的setter方法也会删除对应的加载信息。
- createProxy
    一个静态方法，负责实例化EnhancedResultObjectProxyImpl，调用CglibProxyFactory的静态方法获取enhanced增强对象，将原对象属性复制到enhanced上，最后返回这个enhanced对象。

### CglibSerialStateHolder
继承自AbstractSerialStateHolder，重写了createDeserializatonProxy，直接构建一个CglibProxyFactory实例并调用它的createDeserializationProxy创建出代理对象并返回。

### AbstractSerialStateHolder
实现了Externalizable接口，实现了对类内属性userBean、unloaderProperties、objectFactory、constructorArgTypes、constructorArgs序列化和反序列化处理。

### JavassistProxyFactory
继承自ProxyFactory，使用javassist实现的代理增强，延迟加载的逻辑是和CglibProxyFactory一样的。

### ResultLoader
封装了延迟执行的query。
