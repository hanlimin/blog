---
title: Untitled
date: "2020-12-10 23:10:25"
modifyDate: "2021-01-01 18:07:30"
draft: true
---
Resources 资源 the client provided
Exploration for inspiration, 灵感
Process 设计过程文件
Deliverables 可交付文件
Design a Sketch file, images, resources, etc.
Dev
Prototypes
Developer
archive
config
resources
side
uni
working
archive
Conclusion
Examples
Sites
Bench.sh
秋水逸冰大佬的写的 Bench.sh 脚本

特点
显示当前测试的各种系统信息；
取自世界多处的知名数据中心的测试点，下载测试比较全面；
支持 IPv6 下载测速；
IO 测试三次，并显示平均值

wget -qO- bench.sh | bash #或者
curl -Lso- bench.sh | bash #或者
wget -qO- 86.re/bench.sh | bash #或者
curl -so- 86.re/bench.sh | bash

SuperBench.sh
老鬼大佬的 SuperBench 测试脚本

特点
改进了显示的模式，基本参数添加了颜色，方面区分与查找。
I/O 测试，更改了原来默认的测试的内容，采用小文件，中等文件，大文件，分别测试 IO 性能，然后取平均值。
速度测试替换成了 Superspeed 里面的测试，第一个默认节点是，Speedtest 默认，其他分别测试到中国电信，联通，移动，各三个不同地区的速度。
wget -qO- --no-check-certificate <https://raw.githubusercontent.com/oooldking/script/master/superbench.sh> | bash

# 或者

curl -Lso- -no-check-certificate <https://raw.githubusercontent.com/oooldking/script/master/sup>

UnixBench.sh
秋水逸冰大佬的作品，UnixBench 是一个类 unix 系（Unix，BSD，Linux）统下的性能测试工具，一个开源工具，被广泛用与测试 Linux 系统主机的性能。Unixbench 的主要测试项目有：系统调用、读写、进程、图形化测试、2D、3D、管道、运算、C 库等系统基准性能提供测试数据。

特点
自动安装 UnixBench 和测试脚本
系统调用、读写、进程、图形化测试、2D、3D、管道、运算、C 库等系统基准性能
使用
wget --no-check-certificate <https://github.com/teddysun/across/raw/master/unixbench.sh>
chmod +x unixbench.sh
./unixbench.sh

LemonBench.sh
LemonBench 工具(别名 LBench、柠檬 Bench)，是一款针对 Linux 服务器设计的服务器性能测试工具。通过综合测试，可以快速评估服务器的综合性能，为使用者提供服务器硬件配置信息。

特点
服务器基础信息(CPU 信息/内存信息/Swap 信息/磁盘空间信息等)
Speedtest 网速测试 (本地到最近源及国内各地域不同线路的网速)
磁盘测试(4K 块/1M 块 直接写入测试)
路由追踪测试(追踪到国内和海外不同线路的路由信息)
Spoofer 测试(获取详细网络信息，快速判断服务器接入线路)
使用
curl -fsL <https://ilemonra.in/LemonBenchIntl> | bash -s fast

内存检测脚本
FunctionClub 大佬作品，本程序检测的可分配内存指的是用户使用时最大能占用的内存量。

特点
检测 VPS 真实可分配内存，适用于检测 VPS 超售情况
使用

# CentOS / RHEL

yum install wget -y
yum groupinstall "Development Tools" -y
wget <https://raw.githubusercontent.com/FunctionClub/Memtester/master/memtester.cpp>
gcc -l stdc++ memtester.cpp
./a.out

# Ubuntu / Debian

apt-get update
apt-get install wget build-essential -y
wget <https://raw.githubusercontent.com/FunctionClub/Memtester/master/memtester.cpp>
gcc -l stdc++ memtester.cpp
./a.out

Besttrace4Linux
回程路由测试<http://-IPIP.net>出品

特点
Linux(X86/ARM)/Mac/BSD 系统环境下发起 traceroute 请求
附带链路可视化
兼容性强
支持 JSON 格式
使用

# 下载

wget <http://cdn.ipip.net/17mon/besttrace4linux.zip>

# 解压

unzip besttrace4linux.zip

# 授权

chmod +x besttrace

# 使用

./besttrace -q 1 这里是目标 IP
如果是 64 位系统则直接 besttrace 替换 besttrace32

mPing.sh
Mr.zou 大佬写的脚本

特点
方便测试回程 Ping 值
目前支持众多区域和各大运营商
使用
wget <https://raw.githubusercontent.com/helloxz/mping/master/mping.sh>
bash mping.sh

Superspeed.sh
老鬼大佬的 Superspeed 测试脚本

特点
一键全面测速功能
测试服务器到全国北方南方，电信，联通，移动的速度
使用
wget <https://raw.githubusercontent.com/oooldking/script/master/superspeed.sh> && chmod +x super
