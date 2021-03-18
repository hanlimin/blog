---
title: AIO
date: "2021-03-18 20:29:24"
modifyDate: "2021-03-18 20:29:24"
draft: true
---

# AIO

![java-io-aio](/static/java-io-aio-2.png)

异步 IO 则是采用“订阅-通知”模式: 即应用程序向操作系统注册 IO 监听，然后继续做自己的事情。当操作系统发生 IO 事件，并且准备好数据后，在主动通知应用程序，触发相应的函数。

异步 IO 也是由操作系统进行支持的。微软的 windows 系统提供了一种异步 IO 技术: IOCP(I/O Completion Port，I/O 完成端口)； Linux 下由于没有这种异步 IO 技术，所以使用的是 epoll 对异步 IO 进行模拟。

JAVA AIO 框架中，只实现了两种网络 IO 通道“AsynchronousServerSocketChannel”(服务器监听通道)、“AsynchronousSocketChannel”(socket 套接字通道)。但是无论哪种通道他们都有独立的 fileDescriptor(文件标识符)、attachment(附件，附件可以使任意对象，类似“通道上下文”)，并被独立的 SocketChannelReadHandle 类实例引用。

- AsynchronousServerSocketChannel

服务端 Socket 通道类，负责服务端 Socket 的创建和监听；AsynchronousServerSocketChannel 的使用需要经过三个步骤：创建/打开通道、绑定地址和端口和监听客户端连接请求。

AsynchronousServerSocketChannel 提供了设置通道分组(AsynchronousChannelGroup)的功能，以实现组内通道资源共享。可以调用 open(AsynchronousChannelGroup)重载方法创建指定分组的通道

AsynchronousChannelGroup 封装了处理由绑定到组的异步通道所触发的 I/O 操作完成所需的机制。每个 AsynchronousChannelGroup 关联了一个被用于提交处理 I/O 事件和分发消费在组内通道上执行的异步操作结果的 completion-handlers 的线程池。除了处理 I/O 事件，该线程池还有可能处理其他一些用于支持完成异步 I/O 操作的任务。如果不指定 AsynchronousChannelGroup，则 AsynchronousServerSocketChannel 会归类到一个默认的分组中。

- AsynchronousSocketChannel

客户端 Socket 通道类，负责客户端消息读写；AsynchronousSocketChannel 表示服务端与客户端之间的连接通道。客户端可以通过调用 AsynchronousSocketChannel 静态方法 open()创建，而服务端则通过调用 AsynchronousServerSocketChannel.accept()方法后由 AIO 内部在合适的时候创建。

客户端可以通过调用 AsynchronousSocketChannel 静态方法 open()创建，而服务端则通过调用 AsynchronousServerSocketChannel.accept()方法后由 AIO 内部在合适的时候创建。

可以构建一个 ByteBuffer 对象并调用 socketChannel.write(ByteBuffer)方法异步发送消息，并通过 CompletionHandler 回调接收处理发送结果。

- CompletionHandler<A,V>

消息处理回调接口，是一个负责消费异步 IO 操作结果的消息处理器；

AIO 中定义的异步通道允许指定一个 CompletionHandler 处理器消费一个异步操作的结果。从上文中也可以看到，AIO 中大部分的异步 I/O 操作接口都封装了一个带 CompletionHandler 类型参数的重载方法，使用 CompletionHandler 可以很方便地处理 AIO 中的异步 I/O 操作结果。CompletionHandler 是一个具有两个泛型类型参数的接口,声明了两个接口方法：

```java
public interface CompletionHandler<V,A> {
    void completed(V result, A attachment);
    void failed(Throwable exc, A attachment);
}
```

其中，泛型 V 表示 I/O 操作的结果类型，通过该类型参数消费 I/O 操作的结果；泛型 A 为附加到 I/O 操作中的对象类型，可以通过该类型参数将需要的变量传入到 CompletionHandler 实现中使用。

当 I/O 操作成功完成时，会回调到 completed 方法，failed 方法则在 I/O 操作失败时被回调。需要注意的是：在 CompletionHandler 的实现中应当即使处理操作结果，以避免一直占用调用线程而不能分发其他的 CompletionHandler 处理器。

- ByteBuffer
  负责承载通信过程中需要读、写的消息。

- AsynchronousChannelGroup

异步通道资源共享
