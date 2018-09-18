# java.lang.ref.Reference

引用对象有4种状态
-   Active
-   Pending
-   Enqueued
-   Inactive
在Reference创建时就是Active状态。实例会受到垃圾回收器的特殊处理，有时在可达性性分析后会改变实例的状态为Pending或Inactive。如果Referce创建时指定了ReferenceQueue会进入Pending状态，反之进入Inactive状态。
