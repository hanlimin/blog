---
title: Java中的IO
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---

# Java 中的 IO

## 本地 IO

### BIO

BIO 就是传统的 java.io 包，它是基于流模型实现的，交互的方式是同步、阻塞方式，也就是说在读入输入流或者输出流时，在读写动作完成之前，线程会一直阻塞在那里，它们之间的调用时可靠的线性顺序。它的有点就是代码比较简单、直观；缺点就是 IO 的效率和扩展性很低，容易成为应用性能瓶颈。

- TCP
  - ServerSocket
  - Socket
- UDP
  - DatagramSocket
  - DatagramPacket

### NIO

NIO 是 Java 1.4 引入的 java.nio 包，提供了 Channel、Selector、Buffer 等新的抽象，可以构建多路复用的、同步非阻塞 IO 程序，同时提供了更接近操作系统底层高性能的数据操作方式。

核心的组件：

- ServerSocketChannel
- SocketChannel

- Channel(通道)
- Buffer(缓冲区)
  - ByteBuffer
  - CharBuffer
  - ShortBuffer
  - IntBuffer
  - LongBuffer
  - FloatBuffer
- Selector(选择器)

- 首先，通过 Selector.open() 创建一个 Selector，作为类似调度员的角色；
- 然后，创建一个 ServerSocketChannel，并且向 Selector 注册，通过指定 SelectionKey.OP_ACCEPT，告诉调度员，它关注的是新的连接请求；
- 为什么我们要明确配置非阻塞模式呢？这是因为阻塞模式下，注册操作是不允许的，会抛出 IllegalBlockingModeException 异常；
- Selector 阻塞在 select 操作，当有 Channel 发生接入请求，就会被唤醒

### AIO

AIO 是 Java 1.7 之后引入的包，是 NIO 的升级版本，提供了异步非堵塞的 IO 操作方式，所以人们叫它 AIO（Asynchronous IO），异步 IO 是基于事件和回调机制实现的，也就是应用操作之后会直接返回，不会堵塞在那里，当后台处理完成，操作系统会通知相应的线程进行后续的操作。

### 事件分发器模型

#### 在 Reactor 中实现读

- 注册读就绪事件和相应的事件处理器。
- 事件分发器等待事件。
- 事件到来，激活分发器，分发器调用事件对应的处理器。
- 事件处理器完成实际的读操作，处理读到的数据，注册新的事件，然后返还控制权。

#### 在 Proactor 中实现读：

- 处理器发起异步读操作（注意：操作系统必须支持异步 IO）。在这种情况下，处理器无视 IO 就绪事件，它关注的是完成事件。
- 事件分发器等待操作完成事件。
- 在分发器等待过程中，操作系统利用并行的内核线程执行实际的读操作，并将结果数据存入用户自定义缓冲区，最后通知事件分发器读操作完成。
- 事件分发器呼唤处理器。
- 事件处理器处理用户自定义缓冲区中的数据，然后启动一个新的异步操作，并将控制权返回事件分发器。

## 字节流

- InputStream
  - ByteArrayINputStream
  - PipedInputStream
  - FilterInputStream
    - BufferedInputStream
    - DataInputStream
  - FileInputStream
  - DataInputStream
  - ObjectInputStream
- OutputStream
  - ByteArrayOutputStream
  - PipedOutputStream
  - FilterOutputStream
    - BufferedOutputStream
    - DataOutputStream
    - PrintStream
  - FileOutputStream
  - ObjectOutputStream

## 字符流

- Reader
  - CharArrayReader
  - PipedReader
  - FilterReader
  - BufferedReader
  - InputStreamReader
    - FileReader
- Writer
  - CharArrayWrite
  - PipedWriter
  - FilterWriter
  - BufferedWriter
  - OutputStreamWriter
    - FileWrite
  - PrintWriter

按数据来源和操作对象分类

- 文件
  - FileInputStream
  - FileOuputStream
  - FileReader
  - FileWriter
- 数组
  - ByteArrayInputStream
  - ByteArrayOutputStream
  - CharArrayReader
  - CharArrayWriter
- 管道操作
  - PipedInputStream
  - PipedOutputStream
  - PipedReader
  - PipedWriter
- 基本数据类型
  - DataInputStream
  - DataOutputStream
- 缓冲操作
  - BufferedInputStream
  - BufferedOutputStream
  - BufferReader
  - BufferedWriter
- 打印
  - PrintStraem
  - PrintWriter
- 对象的序列化反序列化
  - ObjectInputStream
  - ObjectOutputStream
- 转换
  - InputStreamReader
  - OutputStreamWriter

**字节流和字符流的区别**

- 字节流读取单个字节，字符流读取单个字符(一个字符根据编码的不同，对应的字节也不同，如 UTF-8 编码是 3 个字节，中文编码是 2 个字节。)
- 字节流用来处理二进制文件(图片、MP3、视频文件)，字符流用来处理文本文件(可以看做是特殊的二进制文件，使用了某种编码，人可以阅读)。

## 字节转字符 Input/OutputStreamReader/Writer

编码就是把字符转换为字节，而解码是把字节重新组合成字符。如果编码和解码过程使用不同的编码方式那么就出现了乱码。 GBK 编码中，中文字符占 2 个字节，英文字符占 1 个字节； UTF-8 编码中，中文字符占 3 个字节，英文字符占 1 个字节； UTF-16be 编码中，中文字符和英文字符都占 2 个字节。 UTF-16be 中的 be 指的是 Big Endian，也就是大端。相应地也有 UTF-16le，le 指的是 Little Endian，也就是小端。 Java 使用双字节编码 UTF-16be，这不是指 Java 只支持这一种编码方式，而是说 char 这种类型使用 UTF-16be 进行编码。char 类型占 16 位，也就是两个字节，Java 使用这种双字节编码是为了让一个中文或者一个英文都能使用一个 char 来存储。

## 输入流

### `InputStream`

```java
// 读取数据
public abstract int read()
// 读取数据至 byte 数组中，该方法实际上是根据下面的方法实现的，off 为 0，len 为数组的长度
public int read(byte b[])
// 从第 off 位置读取 len 长度字节的数据放到 byte 数组中，流是以 -1 来判断是否读取结束的
public int read(byte b[], int off, int len)
// 跳过指定个数的字节不读取
public long skip(long n)
// 返回可读的字节数量
public int available()
// 关闭流，释放资源
public void close()
// 标记读取位置，下次还可以从这里开始读取，使用前要看当前流是否支持，可以使用 markSupport() 方法判断
public synchronized void mark(int readlimit)
// 重置读取位置为上次 mark 标记的位置
public synchronized void reset()
// 判断当前流是否支持标记流，和上面两个方法配套使用
public boolean markSupported()
```

抽象类，定义了字节输入流操作方法。

### `FilterInputStream`

继承自 `InputStream`，是一个装饰器，操作都是直接调用内部 `InputStream`。

### `ByteArrayInputStream`

继承自 `InputStream`，实现了以一个 byte 数组为数据源的输入流。其中，只有 `mark()` 和 `markSupported()` 未被 `synchronized`装饰。

### `BufferedInputStream`

继承自 `FilterInputStream`，内部的缓冲一次性读取指定大小的数据，这样可以减少 IO 次数，达到提高 IO 效率的目的。

### `PipedInputStream`

```java
public void connect(PipedOutputStream src)
```

继承自 `InputStream`，实现了两个线程之间的 IO 流。

### `FileInputStream`

```java
public final FileDescriptor getFD()
public FileChannel getChannel()
protected void finalize()
```

继承自 `InputStream`，实现了本地文件的字节输入流。

## 输出流

### `OutputStream`

```java
// 写入一个字节，可以看到这里的参数是一个 int 类型，对应上面的读方法，int 类型的 32 位，只有低 8 位才写入，高 24 位将舍弃。
public abstract void write(int b)
// 将数组中的所有字节写入，和上面对应的 read() 方法类似，实际调用的也是下面的方法。
public void write(byte b[])
// 将 byte 数组从 off 位置开始，len 长度的字节写入
public void write(byte b[], int off, int len)
// 强制刷新，将缓冲中的数据写入
public void flush()
// 关闭输出流，释放资源
public void close()
```

抽象类，定义了字节输出流操作方法。

### `FilterOutputStream`

继承自 `OutputStream`，是一个装饰器，操作都是直接调用内部 `OutputStream`。

### `ByteArrayOutputStream`

```java
public synchronized void writeTo(OutputStream out)
public synchronized void reset()
public synchronized byte toByteArray()[]
public int size()
public String toString(String enc)
```

继承自 `InputStream`，实现了以一个 byte 数组为数据源的输出流。并添加了多个操作内部 byte 数组的方法，导出至其它输出流、导出数据新数组、获取长度、指定编码输出字符串。

### `BufferedOutputStream`

继承自 `FilterOutputStream`，写时将数据保存至内部缓冲中，调用 `flush()` 才会调用内部封装的输入流写入并刷新，减少 IO 次数，达到提高 IO 效率的目的。

### `PipedOutputStream`

```java
public synchronized void connect(PipedInputStream snk)
```

继承自 `OutputStream`，实现了两个线程之间的 IO 流。

## 序列化 & Serializable & transient

- 序列化就是将一个对象转换成字节序列，方便存储和传输。 序列化: ObjectOutputStream.writeObject()
- 反序列化: ObjectInputStream.readObject() 不会对静态变量进行序列化，因为序列化只是保存对象的状态，静态变量属于类的状态。

序列化的类需要实现 `Serializable`s 接口，它只是一个标准，没有任何方法需要实现，但是如果不去实现它的话而进行序列化，会抛出异常。

`transient` 关键字可以使一些属性不会被序列化。 ArrayList 中存储数据的数组 elementData 是用 transient 修饰的，因为这个数组是动态扩展的，并不是所有的空间都被使用，因此就不需要所有的内容都被序列化。通过重写序列化和反序列化方法，使得可以只序列化数组中有内容的那部分数据。

## 网络 IO

- InetAddress: 用于表示网络上的硬件资源，即 IP 地址；
- URL: 统一资源定位符；
- Sockets: 使用 TCP 协议实现网络通信；
- Datagram: 使用 UDP 协议实现网络通信。

### Sockets

- ServerSocket: 服务器端类
- Socket: 客户端类
- 服务器和客户端通过 InputStream 和 OutputStream 进行输入输出。

### Datagram

- DatagramSocket: 通信类
- DatagramPacket: 数据包类
