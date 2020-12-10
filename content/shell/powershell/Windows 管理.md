# PowerShell管理Windwos

## 文件系统

### 驱动器信息

`Get-PSDrive` 来列出系统中有那些驱动器：

```powershell
PS D:\blog> Get-PSDrive
Name           Used (GB)     Free (GB) Provider      Root                                               CurrentLocation
----           ---------     --------- --------      ----                                               ---------------
Alias                                  Alias
C                  63.87          6.81 FileSystem    C:\                                                    Users\mioon
Cert                                   Certificate   \
D                  23.53         16.46 FileSystem    D:\
E                   6.20        193.80 FileSystem    E:\
Env                                    Environment
F                  48.58        151.43 FileSystem    F:\
Function                               Function
G                  16.31        515.07 FileSystem    G:\
HKCU                                   Registry      HKEY_CURRENT_USER
HKLM                                   Registry      HKEY_LOCAL_MACHINE
I                2504.98       1221.03 FileSystem    I:\
K                                      FileSystem    K:\
Variable                               Variable
WSMan                                  WSMan
```

### 列出当前目录（Get-ChildItem，Alias：ls，dir）

这个命令列出了当前文件夹下的所有子内容。Powershell 对这个命令由多个别名，保证不管是 Linux 还是 Windows 管理员都能顺利上手。

```powershell
PS D:\blog> ls

    目录: D:\blog

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         2020/9/18     22:11                archetypes
d-----         2020/9/18     22:50                content
d-----         2020/9/18     22:08                data
d-----         2020/9/18     22:08                layouts
d-----         2020/9/18     22:41                public
d-----         2020/9/18     22:15                resources
d-----         2020/9/18     22:08                static
d-----         2020/9/18     22:14                themes
-a----         2020/8/27      7:44             64 .gitattributes
-a----         2020/9/18     22:52             90 .gitignore
-a----         2020/9/18     22:41             97 config.toml
```

### 查看当前位置（Get-Location，Alias： pwd）和修改当前位置（Set-Location，Alias：cd）

这是一对对偶命令，使用 Get-Location 命令来查询当前位置，以及使用 Set-Location 来改变位置。我通常情况下习惯使用 pwd 和 cd 别名。值得注意的是，Linux 常用的 “.” , “..” , “~” 等标记依然可用。

### 查看文件内容（Get-Item 和 Get-Content，Alias：cat，和 more）

Get-Item 命令用于获取单个文件的信息，比如：Get-Item test.txt 等。另外有 Get-Content 命令可以查看文件的内容。他有一个别名叫做 cat。

```powershell
PS D:\blog> cat .\.gitignore
*.swp
/imgs
### Hugo ###
# Generated files by hugo
# /public/
/resources/_gen/
# /themes/
```

PowerShell 中也有 more 命令，可以查看较长的文本。

### 新建文件和文件夹（New-Item 和 mkdir）

新建文件和文件夹都是使用命令 New-Item。 其中，当使用参数 -Type Directory 时候，会新建文件夹。但是这样比较麻烦，因此 PowerShell 提供了 mkdir 来直接新建文件夹。

### 删除文件和文件夹（Remove-Item，alias：rm）

删除文件和文件夹都是使用 Remove-Item 命令，也可以使用别名 rm。当文件夹有内容时，windows 会给出进一步操作提示：

### 拷贝（Copy-Item，alias：copy，cp，ci）和移动（Move-Item，alias：mv，move，mi）

这两个命令使用基本上没有什么太大区别。因此不再介绍具体使用。只是要提示一句，Windows 的文件权限机制和 Linux 的并不相同，在移动文件和拷贝文件时，可能会产生权限的变化，

## 用户、组

### 查看本地用户和组

Winodws 本地用户的相关信息，是存在与本地安全账户数据库（SAM）之中的，由此实现对登陆实体身份对鉴别。我们可以使用 Get-LocalUser 命令来查询本地用户信息：

```powershell
PS D:\blog> Get-LocalUser

Name               Enabled Description
----               ------- -----------
Administrator      False   管理计算机(域)的内置帐户
DefaultAccount     False   系统管理的用户帐户。
defaultuser1       True
Guest              False   供来宾访问计算机或访问域的内置帐户
mioon              True
WDAGUtilityAccount False   系统为 Windows Defender 应用程序防护方案管理和使用的用户帐户。
```

同样的道理，我们可以使用 Get-LocalGroup Comlet 来查询当前有那些本地组：

```powershell
PS D:\blog> Get-LocalGroup

Name                                Description
----                                -----------
Access Control Assistance Operators 此组的成员可以远程查询此计算机上资源的授权属性和权限。
Administrators                      管理员对计算机/域有不受限制的完全访问权
Backup Operators                    备份操作员为了备份或还原文件可以替代安全限制
Cryptographic Operators             授权成员执行加密操作。
Distributed COM Users               成员允许启动、激活和使用此计算机上的分布式 COM 对象。
Event Log Readers                   此组的成员可以从本地计算机中读取事件日志
Guests                              按默认值，来宾跟用户组的成员有同等访问权，但来宾帐户的限制更多
Hyper-V Administrators              此组的成员拥有对 Hyper-V 所有功能的完全且不受限制的访问权限。
IIS_IUSRS                           Internet 信息服务使用的内置组。
Network Configuration Operators     此组中的成员有部分管理权限来管理网络功能的配置
Performance Log Users               该组中的成员可以计划进行性能计数器日志记录、启用跟踪记录提供程序，以及在本地或通...
Performance Monitor Users           此组的成员可以从本地和远程访问性能计数器数据
Power Users                         包括高级用户以向下兼容，高级用户拥有有限的管理权限
Remote Desktop Users                此组中的成员被授予远程登录的权限
Remote Management Users             此组的成员可以通过管理协议(例如，通过 Windows 远程管理服务实现的 WS-Management)...
Replicator                          支持域中的文件复制
System Managed Accounts Group       此组的成员由系统管理。
Users                               防止用户进行有意或无意的系统范围的更改，但是可以运行大部分应用程序
```

### 新建用户和组

使用 New-LocalUser 和 New-LocalGroup 来新建新的用户和组。
先使用 Read-Host 读取控制台输入，使用 -AsSecureString 参数，指定输入密码。新建带有密码的用户的例子：

```powershell
PS D:\blog> $Password = Read-Host -AsSecureString
PS D:\blog> New-LocalUser "Blog" -Password $Password -FullName "Blog User" -Description "新建用户与组测试例子用户"

Name Enabled Description
---- ------- -----------
Blog True    新建用户与组测试例子用户
```

新建不带密码的用户：

```powershell
PS D:\blog> New-LocalUser -Name "BlogNoPwd" -Description "新建用户与组测试例子用户没有密码" -NoPassword

Name      Enabled   Description
----      -------   -----------
BlogNoPwd True      新建用户与组测试例子用户没有密码
```

使用 New-LocalGroup 新建用户组：

```powershell
PS D:\blog> New-LocalGroup -Name BlogGroup -Description 新建用户与组测试例子用户组

Name      Description
----      -----------
BlogGroup 新建用户与组测试例子用户组
```

### 修改用户和用户组

使用 Set-LocalUser 和 Set-LocalGroup 来修改组权限，具体的 “-Password”, “-Name”, “-Description” 等参数使用于上面的命令用法一样。

### 删除用户和用户组

使用命令 Remove-LocalUser 和 Remove-LocalGroup 来删除本地组和用户。我们可以使用 名称、SID以及用户对象来指定具体删除的用户或者用户组。使用下面命令来删除本地的用户和用户组：Blog以及BlogGroup：

```powershell
PS D:\blog> Remove-LocalUser -Name Blog
PS D:\blog>Remove-LocalGroup -Name BlogGroup
```

## 本地访问控制

### 安全标识符（SID）

Windows 对于所有的主体（包括用户、组、计算机等）都分配一个安全标识符，这类似于 Linux 中的 uid， gid， pid 等相关概念。 每一个安全标识符都对应了一个安全主体。

Windows 的 SID 由字母 S 开头，而后紧跟多个数字。分别代表了修订级别、颁发机构、子颁发机构、其余颁发机构以及相对标识符构成。

### NTFS 文件权限

NTFS 和 ReFS 的文件权限基本类似，主要分为标准访问权限和特殊访问权限。简单的来说，标注访问权限的细粒度较粗，是多个特殊访问权限的结合， 在一般情况下使用标准访问权限就能够很好的对文件进行访问控制。特殊访问权限的划分非常细致，当有特殊需求的时候，可以使用特殊访问权限加以控制。 由于篇幅原因，我们只重点记录标准访问权限。

在 Windows 中，对于文件的标准访问控制权限主要有以下五种：

读取：读取文件内容、属性、扩展属性、权限。
写入：写入或者附加内容，写入属性和扩展属性。
读取和执行：比写入多了执行文件权限。
修改：除了读取、写入、执行权限之外，还能够删除该文件。
完全控制：上述所有权限，外加修改权限和获得所有权。
对于文件夹的标准访问控制权限主要有一下六种：

读取：列出该文件夹、读取属性、扩展属性以及权限。
写入：在文件夹内创建新的文件和文件夹，写入属性和扩展属性。
列出文件夹内容：比读取多一个列出该文件夹中内容的权限。
读取和执行：具有的权限与“列出文件夹内容”权限一样。但是在继承时有区别，所有文件夹都能继承该属性，而只有子文件夹才能继承“列出文件夹内容”属性。
修改：具有读取和写入的权限，外加删除该文件夹的权限。（但是没有删除子文件夹和文件的权限）
完全控制： 具有上述所有权限以及删除子文件夹、文件，更改权限、获得所有权

### 文件权限的运算规则

权限最小化原则：尽量给用户分配最小的权限，而不分配过多权限。
累加原则：将用户以及用户所在的所用组的权限叠加，作为用户的权限。
拒绝有限：当用户某一个组具有拒绝权限时，则直接拒绝该权限。
继承原则：一个文件夹中的权限默认继承自该文件夹。当然，我们也可以设置权限不继承。注意之前有提到文件夹继承的特殊性。
另外，当使用 SMB 分享文件时，文件同时具有分享权限和NTFS权限。此时对权限取交集。

### Windows 访问控制列表（ACL）

回顾 Linux 的文件权限控制。传统的 Linux 的访问控制，主要是划分为 属主、属组、其他人 三类来进行权限管理，当然还有其他机制在这里暂且不提。 在最近的发行版之中，开始加入了对于访问控制列表（ACL）的更加细致的文件访问控制方法。

Windows 原生使用访问控制列表（ACL）来对文件进行控制。这个列表主要记录了某一个主体（SID）对于这个客体（文件等）的具体访问权限。每一种权限都有允许、拒绝、空三种状态。
我们使用 Get-ACL 来获取某一个文件的访问控制列表，从其中可以看到具体的文件名、拥有者以及具体的访问控制列表。

```powershell
PS D:\blog> Get-ACL .\.gitignore

    目录: D:\blog

Path       Owner         Access
----       -----         ------
.gitignore MIDZOON\mioon BUILTIN\Administrators Allow  FullControl...
```

注意到其中的 Access 是一个 Powershell 列表对象，我们来详细列出其中的内容：

```powershell
PS D:\blog> (Get-ACL .\.gitignore).Access

FileSystemRights  : FullControl
AccessControlType : Allow
IdentityReference : BUILTIN\Administrators
IsInherited       : True
InheritanceFlags  : None
PropagationFlags  : None

FileSystemRights  : FullControl
AccessControlType : Allow
IdentityReference : NT AUTHORITY\SYSTEM
IsInherited       : True
InheritanceFlags  : None
PropagationFlags  : None

FileSystemRights  : Modify, Synchronize
AccessControlType : Allow
IdentityReference : NT AUTHORITY\Authenticated Users
IsInherited       : True
InheritanceFlags  : None
PropagationFlags  : None

FileSystemRights  : ReadAndExecute, Synchronize
AccessControlType : Allow
IdentityReference : BUILTIN\Users
IsInherited       : True
InheritanceFlags  : None
PropagationFlags  : None
```

同理，我们使用 Set-ACL 来设置某一文件的访问控制列表。
添加一个用户：

```powershell
PS D:\blog> $identity ='MIDZOON\BlogNoPwd'
PS D:\blog> $fileSystemRights = "Read,Write"
PS D:\blog> $type = 'Allow'
PS D:\blog> $fileSystemAccessRuleArgumentList = $identity, $fileSystemRights, $type
PS D:\blog> $fileSystemAccessRule = New-Object -TypeName System.Security.AccessControl.FileSystemAccessRule -ArgumentList $fileSystemAccessRuleArgumentList
PS D:\blog> $acl = Get-Acl .\.gitignore
PS D:\blog> $acl.AddAccessRule($fileSystemAccessRule)
PS D:\blog> Set-Acl -Path .\.gitignore -AclObject $acl
PS D:\blog> (Get-ACL .\.gitignore).Access

FileSystemRights  : Write, Read, Synchronize
AccessControlType : Allow
IdentityReference : MIDZOON\BlogNoPwd
IsInherited       : False
InheritanceFlags  : None
PropagationFlags  : None

...
```

修改
// TODO 修改例子没有作用

```powershell
⚡ mioon@MIDZOON  D:\blog   master ↑21 +5 ~1 -193 !  $true
True
⚡ mioon@MIDZOON  D:\blog   master ↑21 +5 ~1 -193 !  $isProtected = $true
⚡ mioon@MIDZOON  D:\blog   master ↑21 +5 ~1 -193 !  $isPreserveInheritance = $true
⚡ mioon@MIDZOON  D:\blog   master ↑21 +5 ~1 -193 !  $acl.SetAccessRuleProtection($isProtected, $isPreserveInheritance)
⚡ mioon@MIDZOON  D:\blog   master ↑21 +5 ~1 -193 !  $acl.Access
```

对于 ACL 对象来说，还有 RemoveAccessRule 函数可以用来删除一项内容。其接受的参数可以是 Access 列表中的具体某一个元素。

## 组策略和本地安全策略

当计算机没有加入域时，其主要策略由“本地组策略”进行设置。当计算机加入域时，域控制器可以对域内的计算机设置多个组，可以为每一个组单独建立“组策略”。

而“本地安全策略”则是“组策略”中非常重要的一部分，主要控制计算机的访问控制等相关设置。我们使用 “gpedit.msc” 来打开 “组策略编辑器”， 而后在“计算机配置” -> “安全设置” 即可查看本地安全策略相关设置。其中的主要设置有：

安全策略经常配置等项目有：

账户策略
密码策略：设置密码长度，使用期限等。
账户锁定策略：登陆失败时的锁定策略。
本地策略：
审核策略：各种审计功能是否打开
用户权限分配：对于特殊任务（关机、远程登录等），指定其所能执行的组和用户
安全选项：对于各种安全选项是否允许（未登录时关闭计算机等）
高级Windows Definder： 防火墙配置
软件限制策略、应用程序限制策略
高级审核策略：高级等审计是否打开
此外，在组策略的 “Windows 策略” 中，可以修改 DNS 服务器、启动和关机时脚本、打印机等配置。在组策略的“管理模版”中可以配置“控制面板“、“桌面”、“开始菜单”等系统组建的设置。

在 Windows Server Core 中，没有 gpedit.msc 因此我们只能够通过直接修改注册表，或者使用 secedit 命令行工具等，来修改本地安全策略

## 磁盘管理

### Windows Server 磁盘模型

Windows 使用了最多四层结构来构建磁盘模型和文件系统。这个模型非常类似于 Linux 的 lvm 的概念。五层结构是：

- PhysicalDisk 物理磁盘：表征一个具有物理实体的磁盘对象。
- StoragePool 存储池：可以将多个物理磁盘聚合成一个大的存储池。
- VirtualDIsk 虚拟磁盘：在存储池中，可以分割成多个虚拟磁盘。可以指定多种 raid 级别。
- Partition 分区。可以在物理磁盘和虚拟磁盘的基础上，划分多个分区并格式化成各种文件格式。
- Volume 卷。在分区中安装文件系统构成卷。

### 通用磁盘管理命令

命令 Get-Disk 将会列出所有的物理磁盘和虚拟磁盘。而 Get-PhysicalDisk 将只列出所有的物理磁盘。

```powershell
PS D:\blog> Get-Disk

Number Friendly Name                 Serial Number                    HealthStatus         OperationalStatus      Total Size PartitionStyle
------ -------------                 -------------                    ------------         -----------------      ---------- ----------
2      Samsung SSD 750 EVO 120GB     S3HZNB0HC66607Z                  Healthy              Online                  111.79 GB GPT
0      WDC WD40EZRZ-22GXCB0          WD-WCC7K1AZXCRC                  Healthy              Online                    3.64 TB GPT
```

```powershell
PS D:\blog> Get-PhysicalDisk

Number FriendlyName              SerialNumber    MediaType CanPool OperationalStatus HealthStatus Usage            Size
------ ------------              ------------    --------- ------- ----------------- ------------ -----            ----
0      WDC WD40EZRZ-22GXCB0      WD-WCC7K1AZXCRC HDD       False   OK                Healthy      Auto-Select   3.64 TB
2      Samsung SSD 750 EVO 120GB S3HZNB0HC66607Z SSD       False   OK                Healthy      Auto-Select 111.79 GB
1      WDC WD10EZEX-21WN4A0      WCC6Y7RLP546    HDD       False   OK                Healthy      Auto-Select 931.51 GB
```

使用命令 Set-Disk 来设置磁盘的属性，比如是否可读、是否离线,文档中给出了一个例子：

```powershell
PS D:\blog> Set-Disk –Number 5 -IsReadonly $False
```

命令 Initialize-Disk命令来初始化磁盘，并建立分区表。参数 -VirtualDisk 指明该磁盘是虚拟磁盘，参数 -PartitionStyle 明确分区表（比如 MBR，GPT）。而 Clear-Disk 用于删除所有分区，抹除数据和分区表。

### 物理磁盘管理命令

与上面类似，我们使用 Get-PhysicalDisk 来获取磁盘列表和磁盘属性。使用 Set-PhysicalDisk 来设置磁盘属性。一个常见的磁盘属性是 -FriendlyName 类似磁盘名。Reset-PhysicalDisk 命令可以用来重置磁盘属性。

下面这个命令查询了所有不健康的物理磁盘。

```powershell
Get-PhysicalDisk | where {$_.HealthStatus -Ne "Healthy"} | ft
```

### 存储池相关命令

使用 Get-StoragePool 来列出存储池及其属性。通过 Set-StoragePool 来设置存储池的属性（只读等）

命令 New-StoragePool 用于新建存储池。必须使用 -StorageSubSystemFriendlyName 一般写 “Windows Storage*” 。可以使用 -FriendlyName 来制定名称。使用 -PhysicalDisks 来制定所有加入存储池的磁盘。

命令 Remove-StoragePool 来取消一个存储池，需要使用 -FriendlyName 参数来制定存储池名称。

命令 Update-StoragePool 来将一个 Windows Server 2012 之前版本的存储池升级成最新版。

命令 Optimize-StoragePool 来优化存储池。

### 将物理磁盘加入和移除存储池

命令 Add-PhysicalDisk 可以将一个物理磁盘加入一个存储池。添加时可以使用存储池对象，也可以使用 -StoragePoolFriendlyName 参数来制定存储卷的名称。另外需要 -PhysicalDisks 参数来传入物理磁盘对象。

而 Remove-PhysicalDisk 可以从存储池中移除一个物理磁盘。和添加类似，我们也需要指定物理磁盘和存储池的名称。

Remove-PhysicalDisk -StoragePoolFriendlyName "npn" -PhysicalDisks $PDToAdd

### 虚拟磁盘命令

使用 Get-VirtualDisk 和 Set-VirtualDisk 来读取和设置虚拟磁盘的属性。

使用命令 New-VirtualDisk 来新建虚拟磁盘，主要参数有：

- StoragePoolFriendlyName 存储池名称
- FriendlyName 虚拟磁盘名称
- Size 大小
- ProvisioningType Thin 指定了精简（而非固定大小，最大使用指定 Size 的大小）。可选。
- ResiliencySettingName 有 “Mirror” ““Parity” 和 “Single” 选项，给出了可靠性级别。具体参见文档。可选。

命令 Remove-VirtualDisk 来删除一个虚拟磁盘，需要指定虚拟磁盘名称。

其他命令具体使用请参见文档。具体主要有如下这些：

- New-VirtualDiskClone 建立虚拟磁盘的克隆
- New-VirtualDiskSnapShot 建立快照
- Hide-VirtualDisk 隐藏虚拟磁盘
- Show-VirtualDisk 现实虚拟磁盘
- Repair-VirtualDisk 修复虚拟磁盘
- Resize-VirtualDisk 重新指定大小

### 分区和创建文件系统

当我们创建虚拟磁盘或者直接从磁盘上创建分区（卷）时，将会需要如下命令：

查看和修改分区属性： Get-Partition 和 Set-Partition。例如：

```powershell
PS D:\blog> Get-Partition

   DiskPath:\\?\scsi#disk&ven_samsung&prod_ssd_750_evo_120g#4&38fbd192&0&030000#{53f56307-b6bf-11d0-94f2-00a0c91efb8b}

PartitionNumber  DriveLetter Offset                                                                        Size Type
---------------  ----------- ------                                                                        ---- ----
1                           1048576                                                                     450 MB Recovery
2                           472907776                                                                   100 MB System
3                           577765376                                                                    16 MB Reserved
4                C           594542592                                                                 70.67 GB Basic
5                           76478939136                                                                 577 MB Recovery
6                D           77085016064                                                                  40 GB Basic


   DiskPath:\\?\scsi#disk&ven_wdc&prod_wd40ezrz-22gxcb0#4&38fbd192&0&010000#{53f56307-b6bf-11d0-94f2-00a0c91efb8b}

PartitionNumber  DriveLetter Offset                                                                        Size Type
---------------  ----------- ------                                                                        ---- ----
1                           17408                                                                     15.98 MB Reserved
2                I           16777216                                                                   3.64 TB Basic
```

通常会使用命令 Get-PartitionSupportedSize 来获取当前分区可以获得的最大和最小大小，比如

使用命令 New-Partition 来新建分区，使用 -DiskNumber 来指定磁盘编号；使用 -UseMaximumSize 指定使用最大大小，使用 -AssignDriveLetter 来分配磁盘分卷号。使用命令 Remove-Partition 来删除一个分区。例如：

```powershell
New-Partition -DiskNumber 1 -UseMaximumSize -AssignDriveLetter`
```

命令 Format-Volume 用来格式化分卷。-DriveLetter 指定卷号； -FileSystem 指定文件系统。

命令 Add-PartitionAccessPath 来为分区分配卷号。而使用 Remove-PartitionAccessPath 来移除卷号。

```powershell
PS C:\>Add-PartitionAccessPath -DiskNumber 1 -PartitionNumber 2 -AccessPath F:
PS C:\>Remove-PartitionAccessPath -DiskNumber 1 -PartitionNumber 2 -AccessPath F:
```

Resize-Partition 用来压缩或者扩展分区。用 -Size 参数指定大小。

Volume 的相关命令主要有：

- Get-Volume 获取卷信息（可以查看卷的使用情况）
- Set-Volume 修改卷信息
- Get-VolumeCorruptionCount 获取卷错误数
- Repair-Volume 修复卷
- Optimize-Volume 优化卷
- New-Volume 新建分区，并在此之上创建卷
等。

### 挂载和取消挂载磁盘镜像（ISO等）

命令 Mount-DiskImage 来挂载一个磁盘镜像文件。例如：

PS C:\>Mount-DiskImage -ImagePath "E:\ISO-Files\My US Visit Fall 2010 Pictures.iso"
命令 DisMount-DiskImage 来卸载一个磁盘镜像文件。可以使用 -ImagePath 来制定镜像文件。或者使用 -DevicePath 指定挂载位置。

```powershell
PS C:\>Dismount-DiskImage -ImagePath "E:\ISO-Files\My US Visit Fall 2010 Pictures.iso"
```

### 内存虚拟文件系统

内存虚拟文件系统的相关命令有：

Cmdlet          Get-PmemDisk                                       1.0.0.0    PersistentMemory
Cmdlet          Get-PmemPhysicalDevice                             1.0.0.0    PersistentMemory
Cmdlet          Get-PmemUnusedRegion                               1.0.0.0    PersistentMemory
Cmdlet          Initialize-PmemPhysicalDevice                      1.0.0.0    PersistentMemory
Cmdlet          New-PmemDisk                                       1.0.0.0    PersistentMemory
Cmdlet          Remove-PmemDisk                                    1.0.0.0    PersistentMemory

## 文件共享

//todo https://www.laytonchen.com/post/tech/ps6/

### 关机和重启

关机的命令是 `Stop-Computer` ,而重启的命令是 `Restart-Computer`。如果需要查看计算机的属性可以通过 `Get-ComputerInfo` 来获取，不过这个命令输出太多参数，所以一般需要使用其他命令来获取具体细节。

### 设置计算机名称以及加入域

通过命令 `Restart-Computer <computer name>` 来设置计算机名称，通过`Add-Computer` 来加入网络中的某一个域。关于域和活动目录的管理，将在之后说明

### 信息查询

我们通常需要有一个命令来查询计算机的软硬件信息，包括内存、CPU、OS 等相关信息。PowerShell 提供了一个 `Get-ComputerInfo` 命令来查询这些基本信息。但是这个命令输出的条目过多，往往不能够很好的找到我们所需要的信息。因此需要在这个命令的基础上加以筛选来现实我们所需要的系统信息：

```powershell
Get-ComputerInfo *process* # 获取处理器信息
Get-ComputerInfo *memory* # 获取内存用量信息
Get-ComputerInfo *OS* # 获取操作系统信息
Get-ComputerInfo *Bios* # BIOS 信息
Get-ComputerInfo *Timezone* # 时区
Get-COmputerInfo *Domain* # 加入的域名
```

PowerShell 支持完整的正则表达式支持，因此可以灵活地设置匹配字符串。

### 进程管理

`Get-Process`

`Get-Process` 可以用来获取当前的所有进程对象。在此基础上，我们可以加以搜索或者筛选，以此来查看我们所需要的进程对象：

```
PS C:\Windows\system32> Get-Process explorer

Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
   1531      58    31076      99056       3.45   4948   1 explorer
```

`Start-Process` 用于启动一个新的进程。主要可选参数有：

- -FilePath 指定可执行文件位置
- -WorkingDirectory 指定工作目录
- -RedirectStandardInput 重定向标准输入
- -RedirectStandardOutput 重定向标准输出
- -RedirectStandardError 重定向标准错误
- -UseNewEnvironment 使用自己的环境变量，而不是从父进程继承。
- -WindowStyle 窗口情况，例如 Maximized
- -Verb 打开方式，比如 Powershell 有 open（新建窗口）、runas（以管理员身份打开）

### 服务管理

####  查询和修改服务

命令 `Get-Service` 和 `Set-Service` 可以用来查询和修改服务对象。进程对象的常见属性有：

- Name名称
- RequiredServices 要求的服务
- DisplayName 显示的名称
- DependentServices 依赖的服务
- MachineName 计算机
- ServiceName 服务名
- ServicesDependedOn 依赖于
- Status 状态
- StartType 启动类型

#### 新建和删除服务

`New-Service` 用于新建服务。

- -Name 指定名称
- -BinaryPathName 指定运行程序
- -DependsOn 指定依赖
- -DisplayName 指定显示名称
- -StartupType 启动类型 Boot, System, Automatic, Manual, Disabled
- -Description 描述

例如：

```
New-Service -Name "TestService" -BinaryPathName "C:\WINDOWS\System32\svchost.exe -k netsvcs"
```

目前没有删除服务的命令，只能使用 sc.exe 命令行工具来删除。使用格式是:

```
sc.exe delete <服务名>
```

#### 修改服务状态

`Start-Service` 用于启动服务，`Stop-Service` 用于关闭服务，`Restart-Service` 用于重启服务。 `Suspend-Service` 用于暂停服务，`Resume-Service` 用于继续服务。

这些命令都是用于改变某一个或者某一些服务的状态。我们可以使用 -Name 参数指定名称，或使用 -DisplayName 来指定展示名称，或直接利用管道符“|”来传递服务对象。

### 日志管理

Windows 提供了统一的日志模块。各个应用在统一的日志管理中注册。命令 `Get-EventLog -List` 来列出当前有哪些日志：

```
PS C:\Windows\system32> get-eventlog -List

  Max(K) Retain OverflowAction        Entries Log
  ------ ------ --------------        ------- ---
  20,480      0 OverwriteAsNeeded         474 Application
  20,480      0 OverwriteAsNeeded           0 HardwareEvents
     512      7 OverwriteOlder              0 Internet Explorer
  20,480      0 OverwriteAsNeeded           0 Key Management Service
     512      7 OverwriteOlder                Parameters
  20,480      0 OverwriteAsNeeded       2,114 Security
     512      7 OverwriteOlder                State
  20,480      0 OverwriteAsNeeded       2,513 System
  15,360      0 OverwriteAsNeeded         204 Windows PowerShell
```

#### 新建日志和移除日志

命令 `New-EventLog` 用于新建一个日志。使用参数 -LogName 指定日志名称；-Source 指定源程序；MessageResourceFile 指定消息源的程序。

命令 `Remove-EventLog` 用来删除一个日志。可以使用 -LogName 来指定名称或者使用 -Source 来制定程序。

#### 移除日志条目和限制日志大小。

命令 `Clear-EventLog` 用来清除日志中的所有条目。需要使用 -Logname 指定清除的日志名称。

```
PS C:\Windows\system32> Clear-EventLog 'Windows PowerShell'
```

命令 `Limit-EventLog` 用来限制一个日志的大小。 -LogName 来指定日志名称，而 -MaximumSize 指定了日志最大的容量。

#### 获取日志条目和写日志条目

命令 `Get-EventLog` 用来获取某一个日志中具体的条目。具有以下参数：

- -LogName 日志名
- -Newest 数字，最近的几个条目
- -EntryType 条目的类型，比如 Error
- -InstanceID 实例 ID
- -Source 数据源
- -Message 正则表达式匹配日志条目
- -UserName 用户名
- -After 该日期之后
- -before 该日期之前

例如：

```
PS C:\>$May31 = Get-Date 5/31/08
PS C:\>$July1 = Get-Date 7/01/08
PS C:\>Get-EventLog -Log "Windows PowerShell" -EntryType Error -After $May31 -before $July1

PS C:\> Get-EventLog -LogName System -EntryType Error
```

命令 `Show-EventLog`， 打开 GUI 的事件查看器。

命令 `Write-EventLog` 用来写一个新的日志条目。有一下参数可以设置：

- -LogName 日志名
- -Source 数据源
- -EventId 事件 ID
- -EntryType 有 Error, Information, FailureAudit, SuccessAudit, Warning 几个等级。
- -Message 消息内容
- -Category Int16 类型分类ID

例如：

```
Write-EventLog -LogName "Application" -Source "MyApp" -EventID 3001 -EntryType Information -Message "MyApp added a user-requested feature to the display." -Category 1 -RawData 10,20

Write-EventLog -LogName Application -Source "MyApp" -EventID 3001 -Message "MyApp added a user-requested feature to the display."
```

### 清空回收站

`Clear-RecycleBin` 用于清空回收站。

> https://www.laytonchen.com/tags/powershell/
