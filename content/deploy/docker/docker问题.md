---
title: docker问题
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### dns无法工作

#### 开机防火墙IP地址伪装（IP地址转发）功能

如果使用的是Centos(RHEL)，并且没有关闭`Firewalld`防火墙，你需要留意是否开启了IP转发功能。

`sudo firewall-cmd --query-masquerade`返回的结果为no，则没有开启。yes则为已经开启了IP地址转发，如果问题没有解决，请继续往下看。

`sudo firewall-cmd --add-masquerade --permanent && sudo firewall-cmd --reload`开启IP地址转发并生效。开启后请再次尝试容器内是否可以正常解析域名。

#### 开启内核IP地址转发

`cat /proc/sys/net/ipv4/ip_forward`查看是否已经开启，0为关闭状态，1为开启状态。如果已经开启请尝试其他解决方案。

如果返回值为0，则为关闭状态。切换到root用户执行`echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf`，继续执行`sysctl -p /etc/sysctl.conf`使之永久生效。

之后需要重新启动网络服务来使IP地址转发功能生效：

如果你是Centos(RHEL)系，需要重新启动`network`服务。执行`systemctl restart network`重启服务后生效。

如果是Debian/Ubuntu系列的发行版，执行`/etc/init.d/procps restart`或`/etc/init.d/procps.sh restart`生效
