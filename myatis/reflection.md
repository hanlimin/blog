# org.apache.ibatis.reflection

### Reflector
反射器。反射一个类，获取所有getter、setter方法和对应属性名字、类型。也将其它字段反射出来保存名字对应Invoer。

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
通过ReflectorFactory获取指定类的Reflector，还提供一个工厂方法获取MetaClass。添加了查询属性名对应类型、
