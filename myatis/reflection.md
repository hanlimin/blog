# org.apache.ibatis.reflection

### Reflector
一个工具类，通过反射获取了一个类的属性信息。
-   无参构造方法
-   通过反射所有方法，通过分析方法的名字获取getter、setter方法及对方法名字解析出属性名字、类型，setter、getter方法封装成Invoker和类型以属性名字为key分别保存在map中。
-   通过反射获取所有字段。如果字段非静态常量字段且字段名字未在上步形成的propName-setter的map中，则封装成Invoker保存在这个map中。若字段名字未在上步形成的propName-getter的map中，则也封装成Invoker保存在其中。对应的类型也同样保存下来。
-   把上述两步形成的方法map的key值也就是属性名分别保存在数组。将上述两个数组的值将值转成大写作为key值作为value保存在另一个map中。

### ReflectorFactory
Reflector的创建工厂，可配置是否缓存。

### DefaultReflectorFactory
RefectoryFactory的一个实现，默认开启了缓存

### CustomReflectorFactory
继承自DefaultReflectoryFactory

### ArrayUtil
提供针对数组的工具类，提供了hashCode，equals，toString等方法。

### ExceptionUtil
一个工具类，若是异常是InvocationTargetException或UndeclaredThrowableException，则取出封装的异常对象。

### JDK
一个工具类，检测java环境是否支持java8的价格特性。

### MetaClass
通过ReflectorFactory获取指定类的Reflector，还提供一个工厂方法获取MetaClass。获取
