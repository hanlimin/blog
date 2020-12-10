### Servlet

总共5个方法、init初始化、destroy容器销毁servlet的方法、getServletConfig获取ServletConfig配置信息、getServletInfo获取相应说明信息、service被容器调用处理请求的核心方法。

### GenericServlet

实现了`Servlet`和`ServletConfig`接口的抽象类。

### HttpServlet

继承了`GenericServlet`的抽象类，主要根据请求方法的类型提供了相对应的处理方法。

### ServletContext

定义了和servlet容器通信的方法

### ServletConfig

能够获取servlet名字、对应ServletContext、配置参数信息

