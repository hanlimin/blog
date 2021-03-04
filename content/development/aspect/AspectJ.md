---
title: AspectJ
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### AspectJ使用



#### 源代码织入

使用ajcjava源代码和AspectJ代码一起编译



​    ajc Demo.java  Trace.aj



也可以将相关的代码文件名写入一个文本文件



​    //lib.lst

​    Demo.java

​    Trace.aj

再使用



​    ajc -argfile lib.lst



最后输出成jar



​    ajc -argfile lib.lst -outjar demo.jar



#### 编译后织入
