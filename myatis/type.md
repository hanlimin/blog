# org.apache.ibatis.type

### Alias
别名注解
### JdbcType
封装了jdbc数据类型的枚举
### TypeHandler
类型处理接口,```setParameter```用于配置PreparedStatement参数，```getResult```从Result获取结果。
### TypeReference
一个抽象类，只有一个字段，在构造方法中调用一个方法完成赋值。该方法一直向上获取父类，直到父类为TypeRerence，获取TypeReference的泛型实际类型参数，如果获取的类型还是参数化类型则返回这个类型的原始类型。
### BaseTypeHandler
继承自TypeReference,实现了TypeHandler的抽象类,对null值进行了处理，其余情况都留了抽象方法。
