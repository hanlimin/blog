# org.apache.ibatis.binding

### MapperMethod
封装了SqlCommand和MethodSignature两个属性。只有两个公共方法，一个入参为class、method、configuration的构造方法，一个入参为SqlSession、Object[]的execute方法。根据SqlCommand的不同，通过MethodSignature完成数据库查询。
#### SqlCommand
statementId=className+methodName

