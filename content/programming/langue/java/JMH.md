---
title: JMH
date: "2021-03-24 16:00:38"
modifyDate: "2021-03-24 16:00:38"
draft: true
---

# JMH

是 openjdk 内用于代码基准测试工具。

pom 文件中引入 JMH 的依赖：

```xml
<dependency>
    <groupId>org.openjdk.jmh</groupId>
    <artifactId>jmh-core</artifactId>
    <version>1.28</version>
</dependency>
<dependency>
    <groupId>org.openjdk.jmh</groupId>
    <artifactId>jmh-generator-annprocess</artifactId>
    <version>1.28</version>
</dependency
```

- `@Warmup`,进行预热

iterations：预热的次数。

time：每次预热的时间。

timeUnit：时间单位，默认是 s。

batchSize：批处理大小，每次操作调用几次方法。（后面用到

因为 JVM 的 JIT 机制的存在，如果某个函数被调用多次之后，JVM 会尝试将其编译成为机器码从而提高执行速度。为了让 benchmark 的结果更加接近真实情况就需要进行预热。

- `@Measurement`，用来控制实际执行的内容

@BenchmarkMode
@BenchmarkMode 主要是表示测量的纬度，有以下这些纬度可供选择：

Mode.Throughput 吞吐量纬度

Mode.AverageTime 平均时间

Mode.SampleTime 抽样检测

Mode.SingleShotTime 检测一次调用

Mode.All 运用所有的检测模式 在方法级别指定@BenchmarkMode 的时候可以一定指定多个纬度，例如： @BenchmarkMode({Mode.Throughput, Mode.AverageTime, Mode.SampleTime, Mode.SingleShotTime})，代表同时在多个纬度对目标方法进行测量。

@State
在很多时候我们需要维护一些状态内容，比如在多线程的时候我们会维护一个共享的状态，这个状态值可能会在每隔线程中都一样，也有可能是每个线程都有自己的状态，JMH 为我们提供了状态的支持。该注解只能用来标注在类上，因为类作为一个属性的载体。 @State 的状态值主要有以下几种：

Scope.Benchmark 该状态的意思是会在所有的 Benchmark 的工作线程中共享变量内容。
Scope.Group 同一个 Group 的线程可以享有同样的变量
Scope.Thread 每隔线程都享有一份变量的副本，线程之间对于变量的修改不会相互影响。 下面看两个常见的@State 的写法
