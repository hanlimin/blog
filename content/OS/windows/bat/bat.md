---
title: bat
date: "2021-02-19 15:26:40"
modifyDate: "2021-02-19 15:26:40"
draft: true
---
# bat脚本总结

## 回显

### @echo off

通常放在头部，用来关闭命名回显

### cls

清屏

### setlocal 和 endlocal

设置”命令扩展名”和”延缓环境变量扩充”

### errorlevel

获取上个命令运行返回值

### title

设置cmd标题

#### pause

暂停命令

### prompt

设置提示符

```bat
prompt $p$g 以当前目录名和>号为提示符，这是最常用的提示符
prompt $t 表示时间
prompt $d 表示日期
prompt $$ 表示$
prompt $q 表示=
prompt $v 表示当前版本
prompt $l 表示<
prompt $b 表示|
prompt $h 表示退位符
prompt $e 表示Esc代表的字符 　
prompt $_ 表示回车换行
```

## 目录与文件

### dir

获取当前目录中的文件和子目录信息

### cd

用于切换目录

### md

新建目录

### rd

删除当前目录下子目录

### del

删除目标子文件

### copy

复制文件

### ren

重命名

### type

显示文件内容

### pushd 和 popd

切换当前目录

## 命令

### rem和::

注释命令

### date和time

获取日期和时间

#### goto和：

跳转和标签命令

### find

查找

### more

逐屏显示

### tree

显示指定目标文件目录结构

#### &

顺序执行多条命令，不管命令是否成功执行

### &&

顺序执行多条命令，当碰到执行出错的命令后将不执行后面的命令

### ||

顺序执行多条命令，当碰到正确的命令后将不执行后面的命令

### |

管道命令：先执行前置命令，后对前置命令作为后置命令的目标

### > 和 >> 输出重定向命令

\> 清除文件内容中的原有内容后再写入

\>> 追加内容到文件末尾，而不会清除原有的内容

### < 重定向输入指令

从文件中获得输入信息，而不是从屏幕中，一般用于 date、time、label 等需要等待屏幕输入的指令

### %n 批参数

命令行传递给批处理的参数

```bat
# 批处理文件本身
%0
# 第一个参数
%1
# 第九个参数
%9
#从第一个参数开始的所有参数
%*
#删除引号，扩充%1
%~1
# 将 %1 扩充到一个完全合格的路径名
%~f1
# 仅将 %1 扩充到一个驱动器号
%~d1
# 仅将 %1 扩充到一个路径
%~p1
# 仅将 %1 扩充到一个文件名
%~n1
# 仅将 %1 扩充到一个文件扩展名
%~x1
# 扩充的路径指含有短名
%~s1
# 将 %1 扩充到文件属性
%~a1
# 将 %1 扩充到文件的日期/时间
%~t1
# 将 %1 扩充到文件的大小
%~z1
# 查找列在 PATH 环境变量的目录，并将 %1 扩充到找到的第一个完全合格的名称。如果环境变量名未被定义，或者没有找到文件，此组合键会扩充到空字符串
%~$PATH:1
```

### set

设置变量

### %var%

获取变量的值

```bat
echo %p%
# 字符串变量操作
echo %p:~6%
```

### call

调用调用标签

### if

```bat
# 文件检测
if exist filename commmand
# 字符串检测
if str1 == str2 command
# 变量是否定义检测
if defined variable command
# 是否有参数检测
if [%1] == [] command
```

### for

循环命令

```bat
# 依次调用小括号里的每个字符串，执行 do 后面的命令
for %%i in (c: d: e: f:) do echo %%i
# 在当前目录和子目录里所有的.txt文件中搜索包含 abc 字符串的行
for /r . %%i in (*.txt) do find \"abc\" %%i
# 显示当前目录名和所有子目录名，包括路径，不包括盘符
for /r . %%i in (.) do echo %%~pni
# 把 d:\mp3 及其子目录里的mp3文件的文件名都存到 d:\mp3.txt 里去
for /r d:\mp3 %%i in (*.mp3) do echo %%i>>d:\mp3.txt
# 生成2345678的一串数字，2是数字序列的开头，8是结尾，1表示每次加1
for /l %%i in (2,1,8) do echo %%i
# 对 set 命令的输出结果循环调用，每行一个
for /f %%i in ('set') do echo %%i
# 取 set 命令的输出结果，忽略以 P 开头的那几行
for /f \"eol=P\" %%i in ('set') do echo %%i
# 显示 d:\mp3.txt 里的每个文件名，每行一个，不支持带空格的名称
for /f %%i in (d:\mp3.txt) do echo %%i
# 显示 d:\mp3.txt 里的每个文件名，每行一个，支持带空格的名称
for /f \"delims=\" %%i in (d:\mp3.txt) do echo %%i
# 对dir命令的结果，跳过前面5行，余下的每行取第4列
for /f \"skip=5 tokens=4\" %%a in ('dir') do echo %%a
```

## 编码

### chcp

用来声明编码

```bat
# 声明为UTF-8
chcp 65001
```

其它语言代码
　　1258 越南语
　　1257 波罗的语
　　1256 阿拉伯语
　　1255 希伯来语
　　1254 土耳其语
　　1253 希腊语
　　1252 拉丁 1 字符 (ANSI)
　　1251 西里尔语
　　1250 中欧语言
　　950 繁体中文
　　949 朝鲜语
　　936 简体中文（默认）
　　932 日语
　　874 泰国语
　　850 多语种 (MS-DOS Latin1)
　　437 MS-DOS 美国英语

## REG

REG  QUERY [REG PATH] /v [KEY]

```bat
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Microsoft SQL Server\110\Tools\ClientSetup" /v "Path"
```
