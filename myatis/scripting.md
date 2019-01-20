### XMLScriptBuilder
    继承自BaseBuilder，封装XNode、一个布尔值isDynamic、类型parameterType、一个string对NodeHandler的nodeHandlerMap。
    构造方法中调用了initNodeHandlerMap完成了对nodeHandlerMap的包括trim、where、set、foreach、if、choose、when、otherwise、bind等NodeHandler的添加。NodeHandler是一个内部私有接口，这些实现了mapper.xml中sql动态的语句处理。
