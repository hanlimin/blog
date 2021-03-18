---
title: Java 8 新特性
date: "2021-03-18 22:14:20"
modifyDate: "2021-03-18 22:14:20"
draft: true
---

# Java 8 新特性

## 函数编程

面向对象编程是对数据进行抽象；函数式编程是对行为进行抽象。

核心思想: 使用不可变值和函数，函数对一个值进行处理，映射成另一个值。

对核心类库的改进主要包括集合类的 API 和新引入的流 Stream。流使程序员可以站在更高的抽象层次上对集合进行操作。

- lambda 表达式仅能放入如下代码: 预定义使用了 @Functional 注释的函数式接口，自带一个抽象函数的方法，或者 SAM(Single Abstract Method 单个抽象方法)类型。这些称为 lambda 表达式的目标类型，可以用作返回类型，或 lambda 目标代码的参数。例如，若一个方法接收 Runnable、Comparable 或者 Callable 接口，都有单个抽象方法，可以传入 lambda 表达式。类似的，如果一个方法接受声明于 java.util.function 包内的接口，例如 Predicate、Function、Consumer 或 Supplier，那么可以向其传 lambda 表达式。
- lambda 表达式内可以使用`方法引用`，仅当该方法不修改 lambda 表达式提供的参数。本例中的 lambda 表达式可以换为方法引用，因为这仅是一个参数相同的简单方法调用。

```java
list.forEach(n -> System.out.println(n));
list.forEach(System.out::println);
```

然而，若对参数有任何修改，则不能使用方法引用，而需键入完整地 lambda 表达式，如下所示:

```java
list.forEach((String s) -> System.out.println("*" + s + "*"));
```

事实上，可以省略这里的 lambda 参数的类型声明，编译器可以从列表的类属性推测出来。

- lambda 内部可以使用静态、非静态和局部变量，这称为 lambda 内的变量捕获。
- Lambda 表达式在 Java 中又称为闭包或匿名函数，所以如果有同事把它叫闭包的时候，不用惊讶。
- Lambda 方法在编译器内部被翻译成私有方法，并派发 invokedynamic 字节码指令来进行调用。可以使用 JDK 中的 javap 工具来反编译 class 文件。使用 javap -p 或 javap -c -v 命令来看一看 lambda 表达式生成的字节码。大致应该长这样:

```java
private static java.lang.Object lambda$0(java.lang.String);
```

- lambda 表达式有个限制，那就是只能引用 final 或 final 局部变量，这就是说不能在 lambda 内部修改定义在域外的变量。

```java
List<Integer> primes = Arrays.asList(new Integer[]{2, 3,5,7});
int factor = 2;
primes.forEach(element -> { factor++; });
```

Compile time error : "local variables referenced from a lambda expression must be final or effectively final" 另外，只是访问它而不作修改是可以的，如下所示:

```java
List<Integer> primes = Arrays.asList(new Integer[]{2, 3,5,7});
int factor = 2;
primes.forEach(element -> { System.out.println(factor*element); });
```

### 分类

#### 惰性求值方法

```java
lists.stream().filter(f -> f.getName().equals("p1"))
```

这行代码并未做什么实际性的工作，filter 只是描述了 Stream，没有产生新的集合。

如果是多个条件组合，可以通过代码块{}

#### 及早求值方法

```java
List<Person> list2 = lists.stream().filter(f -> f.getName().equals("p1")).collect(Collectors.toList());
```

如上示例，collect 最终会从 Stream 产生新值，拥有终止操作。 理想方式是形成一个惰性求值的链，最后用一个及早求值的操作返回想要的结果。与建造者模式相似，建造者模式先是使用一系列操作设置属性和配置，最后调用 build 方法，创建对象。

#### stream & parallelStream

每个 Stream 都有两种模式: 顺序执行和并行执行。

顺序流:

```java
List <Person> people = list.getStream.collect(Collectors.toList());
```

并行流:

```java
List <Person> people = list.getStream.parallel().collect(Collectors.toList());
```

顾名思义，当使用顺序方式去遍历时，每个 item 读完后再读下一个 item。而使用并行去遍历时，数组会被分成多个段，其中每一个都在不同的线程中处理，然后将结果一起输出。

### Stream 中常用方法如下:

- `stream()`, `parallelStream()`
- `filter()`
- `findAny()` `findFirst()`
- `sort`
- `forEach` void
- `map(), reduce()`
- `flatMap()` - 将多个 Stream 连接成一个 Stream
- `collect(Collectors.toList())`
- `distinct`, `limit`
- `count`
- `min`, `max`, `summaryStatistics`

## Optional 类

```java
public static<T> Optional<T> empty()
// 为非null的值创建一个Optional。
public static <T> Optional<T> of(T value)
// 为指定的值创建一个Optional，如果指定的值为null，则返回一个空的Optional。
public static <T> Optional<T> ofNullable(T value)
// 如果Optional有值则将其返回，否则抛出NoSuchElementException。
public T get()
// 如果值存在返回true，否则返回false。
public boolean isPresent()
// 如果Optional实例有值则为其调用consumer，否则不做处理
public void ifPresent(Consumer<? super T> consumer)
// 如果有值并且满足断言条件返回包含该值的Optional，否则返回空Optional。
public Optional<T> filter(Predicate<? super T> predicate)
// 如果有值，则对其执行调用mapping函数得到返回值。如果返回值不为null，则创建包含mapping返回值的Optional作为map方法返回值，否则返回空Optional。
public<U> Optional<U> map(Function<? super T, ? extends U> mapper)
// 如果有值，为其执行mapping函数返回Optional类型返回值，否则返回空Optional。flatMap与map(Funtion)方法类似，区别在于flatMap中的mapper返回值必须是Optional。调用结束时，flatMap不会对结果用Optional封装。
public<U> Optional<U> flatMap(Function<? super T, Optional<U>> mapper)
// 如果有值则将其返回，否则返回指定的其它值。
public T orElse(T other)
// orElseGet与orElse方法类似，区别在于得到的默认值。orElse方法将传入的字符串作为默认值，orElseGet方法可以接受Supplier接口的实现用来生成默认值。示例如下:
public T orElseGet(Supplier<? extends T> other)
// 如果有值则将其返回，否则抛出supplier接口创建的异常。
public <X extends Throwable> T orElseThrow(Supplier<? extends X> exceptionSupplier) throws X
public boolean equals(Object obj)
public int hashCode()
public String toString()
```

## default 方法

接口可以有实现方法，而且不需要实现类去实现其方法。只需在方法名前面加个 default 关键字即可。

默认方法给予我们修改接口而不破坏原来的实现类的结构提供了便利，目前 java 8 的集合框架已经大量使用了默认方法来改进了，当我们最终开始使用 Java 8 的 lambdas 表达式时，提供给我们一个平滑的过渡体验。

之前的接口是个双刃剑，好处是面向抽象而不是面向具体编程，缺陷是，当需要修改接口时候，需要修改全部实现该接口的类，目前的 java 8 之前的集合框架没有 foreach 方法，通常能想到的解决办法是在 JDK 里给相关的接口添加新的方法及实现。然而，对于已经发布的版本，是没法在给接口添加新方法的同时不影响已有的实现。所以引进的默认方法。他们的目的是为了解决接口的修改与现有的实现不兼容的问题

**多重继承的冲突**

由于同一个方法可以从不同接口引入，自然而然的会有冲突的现象，默认方法判断冲突的规则如下:

- 1.一个声明在类里面的方法优先于任何默认方法(classes always win)
- 2.否则，则会优先选取路径最短的

### 类型注解

那充满争议的类型注解究竟是什么? 复杂还是便捷?

在 java 8 之前，注解只能是在声明的地方所使用，比如类，方法，属性； java 8 里面，注解可以应用在任何地方，比如:

创建类实例

```java
new @Interned MyObject();
```

类型映射

```java
myString = (@NonNull String) str;
```

implements 语句中

```java
 class UnmodifiableList<T> implements @Readonly List<@Readonly T> { … }
```

throw exception 声明

```java
 void monitorTemperature() throws @Critical TemperatureException { … }
```

需要注意的是，类型注解只是语法而不是语义，并不会影响 java 的编译时间，加载时间，以及运行时间，也就是说，编译成 class 文件的时候并不包含类型注解。

类型注解被用来支持在 Java 的程序中做强类型检查。配合插件式的 check framework，可以在编译的时候检测出 runtime error，以提高代码质量。这就是类型注解的作用了。check framework 是第三方工具，配合 Java 的类型注解效果就是 1+1>2。它可以嵌入到 javac 编译器里面，可以配合 ant 和 maven 使用。

### 重复注解

允许在同一申明类型(类，属性，或方法)的多次使用同一个注解。

java 8 之前也有重复使用注解的解决方案，是通过另一个注解来存储重复注解，但可读性不是很好。

现在，加上@Repeatable，指向存储注解，在使用时候，直接可以重复使用元素注解，这样的注解更适合常规的思维，可读性强一点。

### 类型推断

**泛型**

泛型是 Java SE 1.5 的新特性，泛型的本质是参数化类型，也就是说所操作的数据类型被指定为一个参数。通俗点将就是“类型的变量”。这种类型变量可以用在类、接口和方法的创建中。

理解 Java 泛型最简单的方法是把它看成一种便捷语法，能节省你某些 Java 类型转换(casting)上的操作:

```java
List<Apple> box = new ArrayList<Apple>();
box.add(new Apple());
Apple apple =box.get(0);
```

上面的代码自身已表达的很清楚: box 是一个装有 Apple 对象的 List。get 方法返回一个 Apple 对象实例，这个过程不需要进行类型转换。没有泛型，上面的代码需要写成这样:

```java
Apple apple = (Apple)box.get(0);
```

泛型的最大优点是提供了程序的类型安全同时可以向后兼容，但也有尴尬的地方，就是每次定义时都要写明泛型的类型，这样显示指定不仅感觉有些冗长，最主要是很多程序员不熟悉泛型，因此很多时候不能够给出正确的类型参数，现在通过编译器自动推断泛型的参数类型，能够减少这样的情况，并提高代码可读性。

**java7 的泛型类型推断改进**

在以前的版本中使用泛型类型，需要在声明并赋值的时候，两侧都加上泛型类型。例如:

```java
Map<String, String> myMap = new HashMap<String, String>();
```

在声明变量的的时候已经指明了参数类型，为什么还要在初始化对象时再指定? 幸好，在 Java SE 7 中，这种方式得以改进，现在你可以使用如下语句进行声明并赋值:

```java
Map<String, String> myMap = new HashMap<>(); //注意后面的"<>"
```

在这条语句中，编译器会根据变量声明时的泛型类型自动推断出实例化 HashMap 时的泛型类型。再次提醒一定要注意 new HashMap 后面的“<>”，只有加上这个“<>”才表示是自动类型推断，否则就是非泛型类型的 HashMap，并且在使用编译器编译源代码时会给出一个警告提示。

但是: Java SE 7 在创建泛型实例时的类型推断是有限制的: 只有构造器的参数化类型在上下文中被显著的声明了，才可以使用类型推断，否则不行。例如: 下面的例子在 java 7 无法正确编译(但现在在 java8 里面可以编译，因为根据方法参数来自动推断泛型的类型):

```java
List<String> list = new ArrayList<>();
list.add("A");// 由于addAll期望获得Collection<? extends String>类型的参数，因此下面的语句无法通过
list.addAll(new ArrayList<>());
```

**Java8 的泛型类型推断改进**

java8 里面泛型的目标类型推断主要 2 个:

1.支持通过方法上下文推断泛型目标类型

2.支持在方法调用链路当中，泛型类型推断传递到最后一个方法

```java
class List<E> {
   static <Z> List<Z> nil() { ... };
   static <Z> List<Z> cons(Z head, List<Z> tail) { ... };
   E head() { ... }
}
```

根据 JEP101 的特性，我们在调用上面方法的时候可以这样写

```java
//通过方法赋值的目标参数来自动推断泛型的类型
List<String> l = List.nil();
//而不是显示的指定类型
//List<String> l = List.<String>nil();
//通过前面方法参数类型推断泛型的类型
List.cons(42, List.nil());
//而不是显示的指定类型
//List.cons(42, List.<Integer>nil());
```

### JRE 精简

模块化特性是 javaer 所期待的特性, 一个占用资源少的 JRE 运行环境，紧凑的 JRE 特性的出现，能带来以后的物联网的发展，甚至还是会有大量的 java 应用程序出现在物联网上面。

**JRE 精简好处**

- 更小的 Java 环境需要更少的计算资源。
- 一个较小的运行时环境可以更好的优化性能和启动时间。
- 消除未使用的代码从安全的角度总是好的。
- 这些打包的应用程序可以下载速度更快

紧凑的 JRE 分 3 种，分别是 compact1、compact2、compact3，他们的关系是 compact1<compact2<compact3,他们包含的 API 如下图所示

![java8-jre](/static/java8-jre-1.png)

**JPEDS 工具使用**
java8 新增一个工具，用来分析应用程序所依赖的 profile，有三个参数比较常用 -p，-v，-r

### LocalDate/LocalDateTime

Java 8 仍然延用了 ISO 的日历体系，并且与它的前辈们不同，java.time 包中的类是不可变且线程安全的。新的时间及日期 API 位于 java.time 包中，下面是里面的一些关键的类:

- Instant——它代表的是时间戳
- LocalDate——不包含具体时间的日期，比如 2014-01-14。它可以用来存储生日，周年纪念日，入职日期等。
- LocalTime——它代表的是不含日期的时间
- LocalDateTime——它包含了日期及时间，不过还是没有偏移信息或者说时区。
- ZonedDateTime——这是一个包含时区的完整的日期时间，偏移量是以 UTC/格林威治时间为基准的。

新的库还增加了 ZoneOffset 及 Zoned，可以为时区提供更好的支持。有了新的 DateTimeFormatter 之后日期的解析及格式化也变得焕然一新了

### JavaFX

JavaFX 主要致力于富客户端开发，以弥补 swing 的缺陷，主要提供图形库与 media 库，支持 audio,video,graphics,animation,3D 等，同时采用现代化的 css 方式支持界面设计。同时又采用 XUI 方式以 XML 方式设计 UI 界面，达到显示与逻辑的分离。

- javaFX 发展历程?
- Java8 对其增加了哪些特性?

- 全新现代主题: Modena

新的 Modena 主题来替换原来的 Caspian 主题。不过在 Application 的 start()方法中，可以通过 setUserAgentStylesheet(STYLESHEET_CASPIAN)来继续使用 Caspian 主题。

- JavaFX 3D

在 JavaFX8 中提供了 3D 图像处理 API，包括 Shape3D (Box, Cylinder, MeshView, Sphere 子类),SubScene, Material, PickResult, LightBase (AmbientLight 和 PointLight 子类),SceneAntialiasing 等。Camera 类也得到了更新。从 JavaDoc 中可以找到更多信息。

- 富文本

强化了富文本的支持,TreeTableView

- 日期控件

DatePicker 增加日期控件

- 用于 CSS 结构的公共 API

```
CSS 样式设置是 JavaFX 的一项主要特性
CSS 已专门在私有 API 中实现(com.sun.javafx.css 软件包)
多种工具(例如 Scene Builder)需要 CSS 公共 API
开发人员将能够定义自定义 CSS 样式
```

- WebView 增强功能

Nashorn JavaScript 引擎 https://blogs.oracle.com/nashorn/entry/open_for_business

WebSocket http://javafx-jira.kenai.com/browse/RT-14947

Web Workers http://javafx-jira.kenai.com/browse/RT-9782

- JavaFX Scene Builder 2.0

可视化工具，加速 JavaFX 图形界面的开发，下载地址

JavaFX Scene Builder 如同 NetBeans 一般，通过拖拽的方式配置界面，待完成界面之後，保存为 FXML 格式文件，此文件以 XML 描述物件配置，再交由 JavaFX 程式处理，因此可減少直接以 JavaFX 编写界面的困難度。

JavaFX Scene Builder 2.0 新增 JavaFX Theme 预览功能，菜单「Preview」→「JavaFX Theme」选择不同的主題，包括:

### PermGen 移除

PermGen space 的全称是 Permanent Generation space,是指内存的永久保存区域。PermGen space 是 Oracle-Sun Hotspot 才有，JRockit 以及 J9 是没有这个区域。

- Java8 之前 “java.lang.OutOfMemoryError: PermGen space”是怎么引起的，怎么解决的?
- 新增加的元空间(Metaspace)包含哪些东西，画出图
- 元空间(Metaspace)和 PermGen 对比

PermGen space 的全称是 Permanent Generation space,是指内存的永久保存区域，说说为什么会内存益出: 这一部分用于存放 Class 和 Meta 的信息,Class 在被 Load 的时候被放入 PermGen space 区域，它和和存放 Instance 的 Heap 区域不同,所以如果你的 APP 会 LOAD 很多 CLASS 的话,就很可能出现 PermGen space 错误。这种错误常见在 web 服务器对 JSP 进行 pre compile 的时候。

JVM 种类有很多，比如 Oralce-Sun Hotspot, Oralce JRockit, IBM J9, Taobao JVM(淘宝好样的！)等等。当然最受广泛使用的是 Hotspot 了，这个毫无争议。需要注意的是，PermGen space 是 Oracle-Sun Hotspot 才有，JRockit 以及 J9 是没有这个区域。

JDK8 HotSpot JVM 将移除永久区，使用本地内存来存储类元数据信息并称之为: 元空间(Metaspace)；这与 Oracle JRockit 和 IBM JVM’s 很相似，如下图所示

java8 中 metaspace 总结如下:

- PermGen 空间的状况

这部分内存空间将全部移除。
JVM 的参数: PermSize 和 MaxPermSize 会被忽略并给出警告(如果在启用时设置了这两个参数)。

- Metaspace 内存分配模型

大部分类元数据都在本地内存中分配。
用于描述类元数据的“klasses”已经被移除。

- Metaspace 容量

默认情况下，类元数据只受可用的本地内存限制(容量取决于是 32 位或是 64 位操作系统的可用虚拟内存大小)。

新参数(MaxMetaspaceSize)用于限制本地内存分配给类元数据的大小。如果没有指定这个参数，元空间会在运行时根据需要动态调整。

- Metaspace 垃圾回收

对于僵死的类及类加载器的垃圾回收将在元数据使用达到“MaxMetaspaceSize”参数的设定值时进行。

适时地监控和调整元空间对于减小垃圾回收频率和减少延时是很有必要的。持续的元空间垃圾回收说明，可能存在类、类加载器导致的内存泄漏或是大小设置不合适。

- Java 堆内存的影响

一些杂项数据已经移到 Java 堆空间中。升级到 JDK8 之后，会发现 Java 堆 空间有所增长。

- Metaspace 监控

元空间的使用情况可以从 HotSpot1.8 的详细 GC 日志输出中得到。

Jstat 和 JVisualVM 两个工具，在使用 b75 版本进行测试时，已经更新了，但是还是能看到老的 PermGen 空间的出现。

### StampedLock

- 为什么会引入 StampedLock
- 用 Lock 写悲观锁和乐观锁举例
- 用 StampedLock 写悲观锁和乐观锁举例
- 性能对比

它是 java8 在 java.util.concurrent.locks 新增的一个 API。

ReentrantReadWriteLock 在沒有任何读写锁时，才可以取得写入锁，这可用于实现了悲观读取(Pessimistic Reading)，即如果执行中进行读取时，经常可能有另一执行要写入的需求，为了保持同步，ReentrantReadWriteLock 的读取锁定就可派上用场。

然而，如果读取执行情况很多，写入很少的情况下，使用 ReentrantReadWriteLock 可能会使写入线程遭遇饥饿(Starvation)问题，也就是写入线程迟迟无法竞争到锁定而一直处于等待状态。

StampedLock 控制锁有三种模式(写，读，乐观读)，一个 StampedLock 状态是由版本和模式两个部分组成，锁获取方法返回一个数字作为票据 stamp，它用相应的锁状态表示并控制访问，数字 0 表示没有写锁被授权访问。在读锁上分为悲观锁和乐观锁。

所谓的乐观读模式，也就是若读的操作很多，写的操作很少的情况下，你可以乐观地认为，写入与读取同时发生几率很少，因此不悲观地使用完全的读取锁定，程序可以查看读取资料之后，是否遭到写入执行的变更，再采取后续的措施(重新读取变更信息，或者抛出异常) ，这一个小小改进，可大幅度提高程序的吞吐量

### 其它更新

#### 处理文件

Files 工具类首次在 Java7 中引入，作为 NIO 的一部分。JDK8 API 添加了一些额外的方法，它们可以将文件用于函数式数据流。

#### java.util.Random

在 Java8 中 java.util.Random 类的一个非常明显的变化就是新增了返回随机数流(random Stream of numbers)的一些方法。

#### java.util.Base64

Java8 中 java.util.Base64 性能比较高。

#### 处理数值

Java8 添加了对无符号数的额外支持。

- Java8 还有哪些其它更新
  - 字符串
  - Base64
  - Random
  - Nashorn
