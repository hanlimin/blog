---
title: unix IO 模型
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---

# unix IO 模型

#### blocking IO

在 linux 中，默认情况下所有的 socket 都是 blocking，一个典型的读操作流程大概是这样：

<img src="https://i.loli.net/2020/08/27/sKc1kFfQePT2AZi.jpg"/>

当用户进程调用了 recvfrom 这个系统调用，kernel 就开始了 IO 的第一个阶段：准备数据。对于 network io 来说，很多时候数据在一开始还没有到达（比如，还没有收到一个完整的 UDP 包），这个时候 kernel 就要等待足够的数据到来。而在用户进程这边，整个进程会被阻塞。当 kernel 一直等到数据准备好了，它就会将数据从 kernel 中拷贝到用户内存，然后 kernel 返回结果，用户进程才解除 block 的状态，重新运行起来。
所以，blocking IO 的特点就是在 IO 执行的两个阶段都被 block 了。

#### non-blocking IO

linux 下，可以通过设置 socket 使其变为 non-blocking。当对一个 non-blocking socket 执行读操作时，流程是这个样子：

<img src="https://i.loli.net/2020/08/27/6rtNeYka1nxLFcj.jpg"/>

从图中可以看出，当用户进程发出 read 操作时，如果 kernel 中的数据还没有准备好，那么它并不会 block 用户进程，而是立刻返回一个 error。从用户进程角度讲 ，它发起一个 read 操作后，并不需要等待，而是马上就得到了一个结果。用户进程判断结果是一个 error 时，它就知道数据还没有准备好，于是它可以再次发送 read 操作。一旦 kernel 中的数据准备好了，并且又再次收到了用户进程的 system call，那么它马上就将数据拷贝到了用户内存，然后返回。所以，用户进程其实是需要不断的主动询问 kernel 数据好了没有。

#### IO multiplexing

IO multiplexing 这个词可能有点陌生，但是如果我说 select，epoll，大概就都能明白了。有些地方也称这种 IO 方式为 event driven IO。我们都知道，select/epoll 的好处就在于单个 process 就可以同时处理多个网络连接的 IO。它的基本原理就是 select/epoll 这个 function 会不断的轮询所负责的所有 socket，当某个 socket 有数据到达了，就通知用户进程。它的流程如图：

<img src="https://i.loli.net/2020/08/27/oaDxygbRWVEKh4Y.jpg">

当用户进程调用了 select，那么整个进程会被 block，而同时，kernel 会“监视”所有 select 负责的 socket，当任何一个 socket 中的数据准备好了，select 就会返回。这个时候用户进程再调用 read 操作，将数据从 kernel 拷贝到用户进程。
这个图和 blocking IO 的图其实并没有太大的不同，事实上，还更差一些。因为这里需要使用两个 system call (select 和 recvfrom)，而 blocking IO 只调用了一个 system call (recvfrom)。但是，用 select 的优势在于它可以同时处理多个 connection。（多说一句。所以，如果处理的连接数不是很高的话，使用 select/epoll 的 web server 不一定比使用 multi-threading + blocking IO 的 web server 性能更好，可能延迟还更大。select/epoll 的优势并不是对于单个连接能处理得更快，而是在于能处理更多的连接。）
在 IO multiplexing Model 中，实际中，对于每一个 socket，一般都设置成为 non-blocking，但是，如上图所示，整个用户的 process 其实是一直被 block 的。只不过 process 是被 select 这个函数 block，而不是被 socket IO 给 block。

#### 信号驱动 I/O

信号驱动 I/O 模型使用信号量来告知内核通过`SIGIO`信号通知我们数据准备好了，它的流程如图：

![Signal-Driven I/O Model](/static/figure_6.4.png)

进程先创建一个信号处理 handler，然后内核立刻返回，进程可以去处理其他事情，等到数据报就绪，内核通过发送信号给之前的 handler 通知进程，然后进程在拷贝数据报期间阻塞。

#### Asynchronous I/O

linux 下的 asynchronous IO 其实用得很少。先看一下它的流程：

<img src="https://i.loli.net/2020/08/27/qaWgeovF9QZJM6t.jpg">

用户进程发起 read 操作之后，立刻就可以开始去做其它的事。而另一方面，从 kernel 的角度，当它受到一个 asynchronous read 之后，首先它会立刻返回，所以不会对用户进程产生任何 block。然后，kernel 会等待数据准备完成，然后将数据拷贝到用户内存，当这一切都完成之后，kernel 会给用户进程发送一个 signal，告诉它 read 操作完成了。

各个 IO Model 的比较如图所示：

<img src="https://i.loli.net/2020/08/27/eIBv37YG8rwH5os.jpg">

## 应用场景

很容易产生一种错觉认为只要用 epoll 就可以了，select 和 poll 都已经过时了，其实它们都有各自的使用场景。

### 1. select 应用场景

select 的 timeout 参数精度为 1ns，而 poll 和 epoll 为 1ms，因此 select 更加适用于实时要求更高的场景，比如核反应堆的控制。 select 可移植性更好，几乎被所有主流平台所支持。

### 2. poll 应用场景

poll 没有最大描述符数量的限制，如果平台支持并且对实时性要求不高，应该使用 poll 而不是 select。 需要同时监控小于 1000 个描述符，就没有必要使用 epoll，因为这个应用场景下并不能体现 epoll 的优势。 需要监控的描述符状态变化多，而且都是非常短暂的，也没有必要使用 epoll。因为 epoll 中的所有描述符都存储在内核中，造成每次需要对描述符的状态改变都需要通过 epoll_ctl() 进行系统调用，频繁系统调用降低效率。并且 epoll 的描述符存储在内核，不容易调试。

### 3. epoll 应用场景

只需要运行在 Linux 平台上，并且有非常大量的描述符需要同时轮询，而且这些连接最好是长连接。

## 参考文献

《UNIX 网络编程》
[IO - 同步，异步，阻塞，非阻塞 （亡羊补牢篇](https://blog.csdn.net/historyasamirror/article/details/5778378)
