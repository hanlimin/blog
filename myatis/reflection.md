# org.apache.ibatis.reflection

### ObejctFactory
对象工厂，用于创建对象。

### DefaultObjectFactory
对象工厂默认实现。只能创建对象，不能设置属性。

### Invoker
一个接口提供一个方法调用指定对象的方法并返回返回值。

### MenthodInvoker、SetFieldInvoker、GetFieldInvoker
Invoker的实现，针对普通方法和对字段的复制与获取。

### PropertyCopier
工具类。通过反射将所有字段的值从原对象复制到目标对象。

### PropertyNamer
工具类。获取setter、getter等方法对应的属性名字。

### PropertyTokenizer
解析属性表达式。

### ObjectWrapper
对象进行封装，能够获取或设置属性、对象信息。如果该对象是集合对象也可添加元素。

### BaseWrapper
ObjectWrapper的抽象实现。添加了针对集合的protected方法。

### BeanWrapper
继承自BaseWrapper，使用MateObect和MateClass对对象进行操作。

### CollectionWrapper
集合封装。只能添加元素。

### MapWrapper
map封装。

### ObjectWrapperFactory
对象封装器工厂，获取指定对象的封装器。

### Reflector
一个工具类，通过反射获取了一个类的属性信息。
-   无参构造方法
-   通过反射所有方法，通过分析方法的名字获取getter、setter方法及对方法名字解析出属性名字、类型，setter、getter方法封装成Invoker和类型以属性名字为key分别保存在map中。
-   通过反射获取所有字段。如果字段是非静态常量字段且字段名字未在上步形成的propName-setter的map中，则封装成Invoker保存在这个map中。若字段名字未在上步形成的propName-getter的map中，则也封装成Invoker保存在其中。对应的类型也同样保存下来。
-   把上述两步形成的方法map的key值也就是属性名分别保存在数组。将上述两个数组的值将值转成大写作为key值作为value保存在另一个```caseInsensitivePropertyMap```中。
特别的方法```findPropertyName```是现将要查找的属性名转成大写，然后再```caseInsensitivePropertyMap```中查找。

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
一个工具类，检测java环境是否支持java8的指定特性。

### MetaClass
封装了Reflector、ReflectorFactory。通过ReflectorFactory获取指定类的Reflector，还提供一个工厂方法获取MetaClass。

### MetaObject
封装了对象的所有属性信息。

### ParamNameResolver
用于处理方法参数的```@param```注解。内部一个map储存参数序号对参数名字。参数名字由构造方法解析。
-   参数类型为RowRounds或ResultHandler及它们子类则跳过。
-   取出参数上第一个```@param```注解，获取注解的value，即映射的参数名字name。
-   当name为空时，如果配置了可取参数实际名字，这需要java8环境支持，如果那么仍为空，则取参数序号。
```getNamedParams```根据上步解析出来的参数名字取出对应参数，并生成对应通用名字param1,param2,param3...

### ParamNameUtil
工具类。需要java8环境，获取指定方法或Executable的所有参数名字。

### SystemMetaObject
包含三个公共静态常量```DEFAULT_OBJECT_FACTORY```、```DEFAULT_OBJECT_WRAPPER_FACTORY```、```NULL_META_OBJEC```T和一个静态方法```forObejct```使用```DEFAULT_OBJECT_FACTORY```、```DEFAULT_OBJECT_WRAPPER_FACTORY```和新创建的DefaultReflectorFactory获取指定对象的```MeteObject```。

### TypeParameterResolver
工具类，包含多个静态方法。解析字段类型、方法返回值类型、方法参数类型信息。内部实现了ParameterizedType、WildcardType。

