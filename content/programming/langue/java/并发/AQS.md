---
title: AQS
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
> 注意：本文代码基于java 5版本，已落后于当前最新版本
#### 大致原理

AQS核心思想是，如果被请求的共享资源空闲，则将当前请求资源的线程设置为有效的工作线程，并且将共享资源设置为锁定状态。如果被请求的共享资源被占用，那么就需要一套线程阻塞等待以及被唤醒时锁分配的机制，这个机制AQS是用CLH队列锁实现的，即将暂时获取不到锁的线程加入到队列中。

CLH(Craig,Landin,and Hagersten)队列是一个双向链表。AQS是将每条请求共享资源的线程封装成一个CLH锁队列的一个结点（Node）来实现锁的分配 。

AQS使用一个int成员变量来表示同步状态，通过内置的FIFO队列来完成获取资源线程的排队工作。AQS使用CAS对该同步状态进行原子操作实现对其值的修改。 

#### CLH队列

```java
private transient volatile Node head;
private transient volatile Node tail;
//The synchronization state.
//在互斥锁中它表示着线程是否已经获取了锁，0未获取，1已经获取了，大于1表示重入数。
private volatile int state;
```

AQS维护了一个volatile int state（代表共享资源）和一个FIFO线程等待队列（多线程争用资源被阻塞时会进入此队列） 

AQS对于CLH锁的改进主要有两个方面：

- AQS中每个节点需要有个指针指向后继节点(单链表变为双链表)，在自旋锁中，每个节点只需要改变自己的状态，后续的节点在下一次自旋时就会感知到，所以不需要链接后继节点。但是在阻塞同步器中，一个节点需要唤醒(wake up/unpark)她的后继节点。这里有一个地方需要注意，因为我们目前没有相关技术实现原子的无锁的插入双链表节点，所以后继节点的操作不是原子的，只是简单的`pred.next = node;`，next 链接只是作为优化路径，当我们通过一个节点的next拿不到后继节点时，我们可以在双链表的链尾通过prev指针向前循环来确定是不是该节点的确不存在后继节点
- 第二个主要的改进在于，在AQS队列的node中保存的状态status是为了控制blocking而不是spinning。在队列中，只有处于队首的active状态的线程才允许调用 tryAcquire 方法，但是这不需要额外的状态来判断，只需要判断当前节点的前驱节点是不是head即可。取消状态则必须依赖该status。同时节点的status状态可以用来避免不必要的park和unpark操作，在调用park操作前，线程会设置(prodecessor)“signal me”bit，然后在真正调用park操作前，重新检查同步状态和节点status状态；在线程释放锁时，可以根据successor是否设置了 signal bit 来确定对哪个Node节点进行unpark操作；推荐去阅读 AQS 源码中Node的定义和文档，部分重要的数据结构如下：

#### Node节点

AQS中使用Node来表示CLH队列的每个节点，源码如下： 

```java
  static final class Node {
        //表示共享模式（共享锁）
        static final Node SHARED = new Node();
        //表示独占模式（独占锁）
        static final Node EXCLUSIVE = null;

        //表示线程已取消
        static final int CANCELLED =  1;
        //表示当前结点的后继节点需要被唤醒
        static final int SIGNAL    = -1;
        //线程(处在Condition休眠状态)在等待Condition唤醒
        static final int CONDITION = -2;
        //表示锁的下一次获取可以无条件传播，在共享模式头结点有可能处于这种状态
        static final int PROPAGATE = -3;

        //线程等待状态
        volatile int waitStatus;

        //当前节点的前一个节点
        volatile Node prev;

        //当前节点的下一个节点
        volatile Node next;

        //当前节点所代表的的线程
        volatile Thread thread;

        //可以理解为当前是独占模式还是共享模式
        Node nextWaiter;

        //如果节点在共享模式下等待，则返回true。
        final boolean isShared() {
            return nextWaiter == SHARED;
        }
        //获取前一个节点
        final Node predecessor() throws NullPointerException {
            Node p = prev;
            if (p == null)
                throw new NullPointerException();
            else
                return p;
        }
        ...
    }

```

 下面解释下waitStatus五个的得含义:

- CANCELLED(1)：该节点的线程可能由于超时或被中断而处于被取消(作废)状态,一旦处于这个状态,节点状态将一直处于CANCELLED(作废),因此应该从队列中移除.
- SIGNAL(-1)：当前节点为SIGNAL时,后继节点会被挂起,因此在当前节点释放锁或被取消之后必须被唤醒(unparking)其后继结点.
- CONDITION(-2)：该节点的线程处于等待条件状态,不会被当作是同步队列上的节点,直到被唤醒(signal),设置其值为0,重新进入阻塞状态.
- PROPAGATE(-3)：共享模式下的释放操作应该被传播到其他节点。该状态值在doReleaseShared方法中被设置的。 
- 0:新加入的节点

#### 入队

如果当前线程通过CAS获取锁失败，AQS会将该线程以及等待状态等信息打包成一个Node节点，并将其加入同步队列的尾部，同时将当前线程挂起。 

```java
public final void acquire(int arg) {
    //tryAcquire是子类重写的方法
    if (!tryAcquire(arg) &&
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
        selfInterrupt();
}
```

代码逻辑为：

1. 首先tryAcquire获取同步状态，成功则直接返回；否则，进入下一环节。
2. 此时，获取同步状态失败，构造独占式同步结点，通过addWatiter将此结点添加到同步队列的尾部。
3. 加入队列中的结点线程进入自旋状态， 若获取不到，则阻塞结点线程，直到被前驱结点唤醒或者被中断。


```java
private Node addWaiter(Node mode) {
     //把当前线程包装为node,设为独占模式
    Node node = new Node(Thread.currentThread(), mode);
    // Try the fast path of enq; backup to full enq on failure
    Node pred = tail;
    if (pred != null) {
        node.prev = pred;
         //快速的将节点插入队列尾部
        if (compareAndSetTail(pred, node)) {
            pred.next = node;
            return node;
        }
    }
    //快速插入失败，通过轮询来插入尾部，性能比快速插入消耗要大一些
    enq(node);
    return node;
}
 //节点的初始化，通过轮询方式将节点插入队列尾部
private Node enq(final Node node) {
    for (;;) {
        Node t = tail;
        if (t == null) {
            // head、tail节点初始化
            if (compareAndSetHead(new Node()))
                tail = head;
        } else {
            node.prev = t;
            if (compareAndSetTail(t, node)) {
                t.next = node;
                return t;
            }
        }
    }
}
```

先CAS快速设置，若失败，进入enq方法。在enq方法内， 通过循环和CAS保证线程安全的初始化头尾节点并添加新节点 。 最外层死循环保证了在多线程进行操作时，如果CAS操作失败，线程会不断自旋直到操作入队成功。

```java
final boolean acquireQueued(final Node node, int arg) {
    boolean failed = true;
    try {
        boolean interrupted = false;
        for (;;) {
            final Node p = node.predecessor();
            if (p == head && tryAcquire(arg)) {
                setHead(node);
                p.next = null;
                failed = false;
                return interrupted;
            }
            if (shouldParkAfterFailedAcquire(p, node) &&
                parkAndCheckInterrupt())
                interrupted = true;
        }
    } finally {
        if (failed)
            cancelAcquire(node);
    }
}

private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
    int ws = pred.waitStatus;
    if (ws == Node.SIGNAL)
        ///若前驱结点的状态是SIGNAL，意味着当前结点可以被安全地park
        return true;
    if (ws > 0) {
        //ws>0，只有CANCEL状态ws才大于0。若前驱结点处于CANCEL状态，也就是此结点线程已经无效，从后往前遍历，找到一个非CANCEL状态的结点，将自己设置为它的后继结点
        do {
            node.prev = pred = pred.prev;
        } while (pred.waitStatus > 0);
        pred.next = node;
    } else {
        // 若前驱结点为其它状态，将其设置为SIGNAL状态
        compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
    }
    return false;
}
```

acquireQueued方法，外层是一个死循环，先判断当前节点的前驱节点是不是头节点，如果是的话，尝试获取锁，如果成功，则把当前node节点设置为头节点，把原来头节点的后继指针断开，如果失败，调用`shouldParkAfterFailedAcquire`方法，根据当前节点的前驱节点判断是否需要挂起当前节点的线程。如果判断成功，则执行`parkAndCheckInterrupt`方法，对当前线程调用park方法。最外层的for循环保证了该节点的线程最终会获取到锁。

#### 出队

当释放锁时，执行出队操作及唤醒后继节点。 

```java
public final boolean release(int arg) {
    if (tryRelease(arg)) {//调用使用者重写的tryRelease方法，若成功，唤醒其后继结点，失败则返回false
        Node h = head;
        if (h != null && h.waitStatus != 0)
            //线程唤醒
            unparkSuccessor(h);
        return true;
    }
    return false;
}
private void unparkSuccessor(Node node) {
    //获取wait状态
    int ws = node.waitStatus;
    if (ws < 0)
        compareAndSetWaitStatus(node, ws, 0);// 将等待状态waitStatus设置为初始值0
    
    Node s = node.next;
    //若后继结点为空，或状态为CANCEL（已失效），则从后尾部往前遍历找到一个处于正常阻塞状态的结点进行唤醒
    if (s == null || s.waitStatus > 0) {
        s = null;
        for (Node t = tail; t != null && t != node; t = t.prev)
            if (t.waitStatus <= 0)
                s = t;
    }
    if (s != null)
        LockSupport.unpark(s.thread);
}
```

首先调用重写tryRelease()方法释放锁，若返回成功说明已无重入锁，接下来唤醒后继节点。如果后继节点不为空且不是失效状态，则唤醒这个后继节点，否则从tail节点向前寻找合适的节点，如果找到则唤醒。

从后向前寻找，是因为在enq方法中，新节点prev指向tail，tail指向新节点，这里后继指向前驱的指针是由CAS操作保证线程安全的。而cas操作之后t.next=node之前，可能会有其他线程进来。所以出现了问题，从尾部向前遍历是一定能遍历到所有的节点。 

#### 自定义独占锁及共享锁

AQS非常强大，只需要重写`tryAcquire`、`tryRelease`这两个方法就可以实现一个独占锁。

#### 惊群效应

在使用`wait/notify/notifyAll`时，唤醒线程都是使用`notifyAll`来唤醒线程，因为`notify`无法唤醒指定线程，从而可能导致死锁。但使用`notifyAll`也有一个问题，那就是当大量线程来获取锁时，就会产生[惊群效应](https://zh.wikipedia.org/wiki/惊群问题)，大量的竞争必然造成资源的剧增和浪费，因此终究只能有一个线程竞争成功，其他线程还是要老老实实的回去等待。而AQS的FIFO的等待队列给解决在锁竞争方面的惊群效应问题提供了一个思路：保持一个FIFO队列，队列每个节点只关心其前一个节点的状态，线程唤醒也只唤醒队头等待线程。

#### 可重写方法

- protected boolean tryAcquire(int arg) : 独占式获取同步状态，试着获取，成功返回true，反之为false

- protected boolean tryRelease(int arg) ：独占式释放同步状态，等待中的其他线程此时将有机会获取到同步状态；

- protected int tryAcquireShared(int arg) ：共享式获取同步状态，返回值大于等于0，代表获取成功；反之获取失败；

- protected boolean tryReleaseShared(int arg) ：共享式释放同步状态，成功为true，失败为false

- protected boolean isHeldExclusively() ： 是否在独占模式下被线程占用

## 参考文献

- Doug Lea. The java.util.concurrent synchronizer framework[J]. Science of Computer Programming, 2005, 58(3): 293-309.
- [Java魔法类：Unsafe应用解析](https://tech.meituan.com/2019/02/14/talk-about-java-magic-class-unsafe.html)
