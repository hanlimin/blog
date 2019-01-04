### Guard
只有一个方法checkGurad(Object),判断事是否允许访问被守护对象，如果不允许则会抛出SecurityException异常。
### Permission
Guard的唯一实现类，是个抽象类。权限被表示成一个字符串，
## BasicPermission

### AccessController
-   checkPermission(Permission)

### AccessControlContext
基于涵盖的上下文来判断对系统资源的访问权限。
### ProtectionDomain 
封装一些类及这些类赋予的权限。
### CodeSource
封装代码库地址、证书链、签名器。
### CodeSigner
分装代码签名器信息
