### Guard
只有一个方法checkGurad(Object),判断事是否允许访问被守护对象，如果不允许则会抛出SecurityException异常。
### Permission
Guard的唯一实现类，是个抽象类。权限被表示成一个字符串，getActions()获取行为
## BasicPermission

### AccessController
基于安全测试判断是否允许系统资源
使代码获取特权
获取上下文快照
主要方法为doPrivilieged的多个重载方法和getContext

### AccessControlContext
基于涵盖的上下文来判断对系统资源的访问权限。
### ProtectionDomain 
封装来加载器、代码源、被赋予的权限

### Principal
代表一个实体

### Subject
代表单一实体的关系信息，封装了principal、credential

### CodeSource
封装代码库地址、证书链、签名器。
#### implies
##### matchCerts
-   先判断certs和signers是否都为null，非严格下返回true。严格条件下that的也都为null才返回true
-   当俩个对象都有signers时，如果this中signers中的signer都能在that.signers找到返回true，严格条件两个signers长度不等就会返回false。
-   都有certs时，判断this.certs中的cert都能在that.certs中找到，能则返回true，严格条件下两个certs长度不等就返回false。
### matchLocation
对比过程中，已当前对象为基准。
-   如果当前对象location为null直接返回true
-   如果对方为null或对方的location为null返回false
-   两个location相等返回true 
-   如果location的端口不为-1，就会比较两个location的端口，如果不同就会返回false
-   如果location的getFile返回的字符串已```/-```结尾，那么that的对应值必须以前值的去掉```-```的字符串开始，否则返回false。也就是说that可有下级目录
-   如果location的getFile返回的字符串已```/*```结尾，那么that的对应值取最后一个```/```的位置的字符串，这个字符串要与前值的去掉```*```的字符串相等，否则返回false。也就说that不能有下级目录。
-   如果location的file值与that的对应值和这个对应值+```/```的字符串都不相等则返回false
-   如果location的reference不为null，则要求that的对应值与前者相等，否则返回false
-   如果location的host不为null，当连个为空或为localhost，则跳过。分别为两个location的host构造SocketPermission，若this的SocketPermission不能涵盖that的权限，则返回false
-   最后默认返回true。
### CodeSigner
封装代码签名器信息
### CertPath
抽象类封装了证书类型和一个有序证书类表。
### Certificate
证书抽象类。封装了证书类型、证书数据，提供了使用公钥验签的verify方法

### SecurityConstants

静态类封装了大量代表权限的静态常量