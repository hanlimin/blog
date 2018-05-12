# org.apache.ibatis.io

工具包，主要提供获取资源的方法

## ClassLoaderWrapper
对ClassLoader的封装，构造方法为package作用域。该类的主要作用是通过遍历一个私有方法```getClassLoaders```返回的ClassLoader数组，查找资源路径对应URL或InputStream，找到即返回。

## Resources
一个工具类，内部使用```ClassLoaderWrapper```查找资源。可通过资源路径获取对应URL、InputStream、Properties、Reader、File，可使用```setCharset(Charset charset)```指定Reader的字符集。

## VFS
主要方法是```public List<String> list(String path) throws IOException```获取指定路径下所有资源名字。默认有两个实现```JBoss6VFS```和```DefaultVFS```,但是可以添加用户实现，内部是优先使用用户实现的。

这里看下DefaultVFS，这个类有意思的地方有几个。第一个呢，它查找的时候，先找到资源所在的jar文件，而判断一个文件是不是jar文件，是同zip文件一样判断文件头4个字节是不是```['P', 'K', 3, 4]```(\x50\x4b\x03\x04)字节数组签名为依据。第二点，把jar文件打开输入流转成JarInputStream，再简单粗暴的遍历所有条目，只要该条目对应的路径以```path```开头就是符合条件的资源并把名字放入返回集合中。因为DefaultVFS要兼顾多个平台，资源查找逻辑出了开始的找jar文件这种普通情况，还在失败后以进行其它方式的进行尝试，因为不了解考虑的因素就不写了。

## ResolverUtil
首先通过```VFS```找出指定二进制名下所有以```.class```为后缀名的资源，再将这些资源当成类文件加载，若加载成功则将该类根据指定条件判断，最后将符合条件的类放入内部的集合中。判断条件就是只有一个方法的内部类接口```Test```，默认提供了```IsA```(是指定类的子类)和```AnnotatedWith```(带有指定的注解)，对应的方法为```findImplementations(Class<?> parent, String... packageNames)```和```findAnnotated(Class<? extends Annotation> annotation, String... packageNames)```。筛选出来的类可通过```getClasses()```获取。


