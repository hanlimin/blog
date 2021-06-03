---
title: SPI机制
date: "2021-03-19 13:15:32"
modifyDate: "2021-03-19 13:15:32"
draft: true
---

# SPI 机制

SPI（Service Provider Interface），是 JDK 内置的一种 服务提供发现机制，可以用来启用框架扩展和替换组件，主要是被框架的开发人员使用，比如 java.sql.Driver 接口，其他不同厂商可以针对同一接口做出不同的实现，MySQL 和 PostgreSQL 都有不同的实现提供给用户，而 Java 的 SPI 机制可以为某个接口寻找服务实现。Java 中 SPI 机制主要思想是将装配的控制权移到程序之外，在模块化设计中这个机制尤其重要，其核心思想就是 **解耦**。

![SPI 机制](/static/java-advanced-spi-8.jpg)

当服务的提供者提供了一种接口的实现之后，需要在 classpath 下的 `META-INF/services/` 目录里创建一个以服务接口命名的文件，这个文件里的内容就是这个接口的具体的实现类。当其他的程序需要这个服务的时候，就可以通过查找这个 jar 包（一般都是以 jar 包做依赖）的 `META-INF/services/` 中的配置文件，配置文件中有接口的具体实现类名，可以根据这个类名进行加载实例化，就可以使用该服务了。JDK 中查找服务的实现的工具类是：`java.util.ServiceLoader`。

## 使用

使用流程了：

- 有关组织或者公司定义标准。
- 具体厂商或者框架开发者实现。
- 程序猿使用。

### 定义标准

定义标准，就是定义接口。比如接口`java.sql.Driver`

### 具体厂商或者框架开发者实现

厂商或者框架开发者开发具体的实现：

在`META-INF/services`目录下定义一个名字为接口全限定名的文件，比如`java.sql.Driver`文件，文件内容是具体的实现名字，比如`me.cxis.sql.MyDriver`。

写具体的实现`me.cxis.sql.MyDriver`，都是对接口 Driver 的实现。

## SPI 机制的广泛应用

### JDBC DriverManager

在 JDBC4.0 之前，我们开发有连接数据库的时候，通常会用 Class.forName("com.mysql.jdbc.Driver")这句先加载数据库相关的驱动，然后再进行获取连接等的操作。而 JDBC4.0 之后不需要用 Class.forName("com.mysql.jdbc.Driver")来加载驱动，直接获取连接就可以了，现在这种方式就是使用了 Java 的 SPI 扩展机制来实现

#### JDBC 接口定义

首先在 java 中定义了接口`java.sql.Driver`，并没有具体的实现，具体的实现都是由不同厂商来提供的。

#### mysql 实现

在 mysql 的 jar 包`mysql-connector-java-6.0.6.jar`中，可以找到`META-INF/services`目录，该目录下会有一个名字为`java.sql.Driver`的文件，文件内容是`com.mysql.cj.jdbc.Driver`，这里面的内容就是针对 Java 中定义的接口的实现。

#### postgresql 实现

同样在 postgresql 的 jar 包`postgresql-42.0.0.jar`中，也可以找到同样的配置文件，文件内容是`org.postgresql.Driver`，这是 postgresql 对 Java 的`java.sql.Driver`的实现。

### Common-Logging

首先，日志实例是通过 LogFactory 的 getLog(String)方法创建的：

```java
public static getLog(Class clazz) throws LogConfigurationException {
    return getFactory().getInstance(clazz);
}
```

`getFactory()`加载具体实现的步骤如下：

- 首先获取系统环境变量`org.apache.commons.logging.LogFactory`，然后尝试加载环境变量指定的类。
- 上步成功，读取文件`META-INF/services/org.apache.commons.logging.LogFactory`，加载文件内指定的具体类。
- 上步未成功，读取配置文件 `commons-logging.properties`，从中获取 `org.apache.commons.logging.LogFactory"`属性对应的配置，加载配置信息指定的具体类。
- 上布未成功，直接尝试加载 `org.apache.commons.logging.impl.LogFactoryImpl`。

### 插件体系

Eclipse 使用 OSGi 作为插件系统的基础，动态添加新插件和停止现有插件，以动态的方式管理组件生命周期。

一般来说，插件的文件结构必须在指定目录下包含以下三个文件：

- `META-INF/MANIFEST.MF`: 项目基本配置信息，版本、名称、启动器等
- `build.properties`: 项目的编译配置信息，包括，源代码路径、输出路径
- `plugin.xml`：插件的操作配置信息，包含弹出菜单及点击菜单后对应的操作执行类等

当 eclipse 启动时，会遍历 plugins 文件夹中的目录，扫描每个插件的清单文件`MANIFEST.MF`，并建立一个内部模型来记录它所找到的每个插件的信息，就实现了动态添加新的插件。

这也意味着是 eclipse 制定了一系列的规则，像是文件结构、类型、参数等。插件开发者遵循这些规则去开发自己的插件，eclipse 并不需要知道插件具体是怎样开发的，只需要在启动的时候根据配置文件解析、加载到系统里就好了，是 spi 思想的一种体现。

### Spring 中 SPI 机制

在 springboot 的自动装配过程中，最终会加载`META-INF/spring.factories`文件，而加载的过程是由`SpringFactoriesLoader`加载的。从 CLASSPATH 下的每个 Jar 包中搜寻所有`META-INF/spring.factories`配置文件，然后将解析 properties 文件，找到指定名称的配置后返回。需要注意的是，其实这里不仅仅是会去 ClassPath 路径下查找，会扫描所有路径下的 Jar 包，只不过这个文件只会在 Classpath 下的 jar 包中。

## SPI机制的缺陷

- 不能按需加载，需要遍历所有的实现，并实例化，然后在循环中才能找到我们需要的实现。如果不想用某些实现类，或者某些类实例化很耗时，它也被载入并实例化了，这就造成了浪费。
- 获取某个实现类的方式不够灵活，只能通过 Iterator 形式获取，不能根据某个参数来获取对应的实现类。
- 多个并发多线程使用 ServiceLoader 类的实例是不安全的
