---
title: jmx
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### 探测器

标准MBean实现仍然要求被管理的Bean实现一个MBean接口，spring提供MBeanExporter来探测需要纳入JMX管理范围的Bean。
以下是一个简单的jmx配置文件的实现，被管理的bean的命名规范为 域名:name=MBean名称。

```xml
<bean name="domain:name=hello" class="com.wch.base.jmx.Hello"/>

<!-- 配置MBean探测器 -->
<bean id="exporter" class="org.springframework.jmx.export.MBeanExporter">
    <!-- MBean探测模式默认为AUTODETECT_ALL：所有注册的MBean -->
    <property name="autodetectModeName" value="AUTODETECT_ALL"/>
</bean>
```

MBeanExporter的属性autodetectModeName表示探测的方式，包括：

- AUTODETECT_NONE：不启用自动探测，需要手动在MBeanServer注册，即通过MBeanExporter的beans属性进行注册。
- AUTODETECT_MBEAN：在当前IOC容器中进行查找MBean组件。
- AUTODETECT_ASSEMBLER：根据MBeanInfoAssembler策略进行探测。
- AUTODETECT_ALL：启用自动探测，包含AUTODETECT_MBEAN和AUTODETECT_ASSEMBLER的情况。
     此外，MBeanExporter还可设置autodetect属性，当该属性为true时，采用AUTODETECT_ALL模式，否则采用AUTODETECT_NONE模式。

#### 手动

```xml
<!-- 配置MBean探测器 -->
<bean id="exporter" class="org.springframework.jmx.export.MBeanExporter">
    <!-- 配置纳入JMX管理的bean -->
    <property name="beans">
        <map>
            <entry key="com.wch.base.jmx:name=Hello" value-ref="hello"/>
        </map>
    </property>
</bean>
```

#### 注解

```xml
<!-- 配置MBean探测器 -->
<bean id="exporter" class="org.springframework.jmx.export.MBeanExporter">
    <!-- 设置被管理bean的暴露方式 -->
    <property name="assembler" ref="assembler"/>
    <!-- 被管理bean的命名策略 -->
    <property name="namingStrategy" ref="namingStrategy"/>
</bean>
<!-- 使用注解的简化配置 -->
<bean id="jmxAttributeSource" class="org.springframework.jmx.export.annotation.AnnotationMBeanExporter"/>
<!-- 使用注解获取命名策略（objectName）-->
<bean id="namingStrategy" class="org.springframework.jmx.export.naming.MetadataNamingStrategy">
    <property name="attributeSource" ref="jmxAttributeSource"/>
</bean>
```



### 暴露方式

```xml
<bean id="exporter" class="org.springframework.jmx.export.MBeanExporter">
    <!-- MBean探测模式默认为AUTODETECT_ALL：所有注册的MBean -->
    <property name="autodetectModeName" value="AUTODETECT_ALL"/>
    <!-- 设置被管理bean的暴露方式 -->
    <property name="assembler" ref="assembler"/>
</bean>
```

- 通过方法集合进行暴露

```jsx
<bean id="assembler" class="org.springframework.jmx.export.assembler.MethodNameBasedMBeanInfoAssembler">
    <property name="managedMethods" value="setName,setAge"/>
</bean>
```

- 通过接口进行暴露

```jsx
<bean id="assembler" class="org.springframework.jmx.export.assembler.InterfaceBasedMBeanInfoAssembler">
    <property name="managedInterfaces" value="com.wch.base.jmx.HelloMBean"/>
</bean>
```

- 通过注解进行暴露

```xml
 <!-- 基于注解的暴露方式 -->
<bean id="assembler" class="org.springframework.jmx.export.assembler.MetadataMBeanInfoAssembler">
    <property name="attributeSource" ref="jmxAttributeSource"/>
</bean>
```

