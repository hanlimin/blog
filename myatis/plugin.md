### Interceptor
一个接口，有三个方法。intercept执行处理代码，plugin向指定对象插入本插件？setProperties设置配置信息。
### InterceptorChain
封装了一个Interceptor列表，其它是添加、获取列表、插入插件的方法。
### Intercepts
一个注解，属性是一个注解Signature数组。
### Invocation
封装了targe、method、args。proceed方法为代理后处理方法。
### Plugin
封装了target、interceptor、一个类类型对泛型为Method的Set的Map signatureMap。 实现了InvocationHandler接口，invoke方法为首先判断入参method是否在signatureMap中，若存在则构建Invocation为入参调用interceptor的intercept方法实现织入逻辑，若不存在则简单调用method。此外一个公共静态方法warp，通过getSignatureMap获取signatureMap，通过getAllInterface方法获取target类及其父类是在signatureMap的key值的接口类型组成数组，最后通过Proxy返回JDK代理对象。
### Signature
    用来标记被拦截的类类型、方法、入参。
