---
title: firewall-cmd
date: "2021-02-19 15:26:40"
modifyDate: "2021-02-19 15:26:40"
draft: true
---
服务

```csharp
firewall-cmd --zone=public --add-service=https //临时

firewall-cmd --permanent --zone=public --add-service=https //永久
```

端口

```csharp
firewall-cmd --permanent --zone=public --add-port=8080-8081/tcp //永久

firewall-cmd --zone=public --add-port=8080-8081/tcp //临时
```

查看

```cpp
firewall-cmd --permanent --zone=public --list-services //服务空格隔开 例如 dhcpv6-client https ss

firewall-cmd --permanent --zone=public --list-ports //端口空格隔开 例如 8080-8081/tcp 8388/tcp 80/tcp
```

设置某个ip 访问某个服务



```csharp
firewall-cmd --permanent --zone=public --add-rich-rule="rule family="ipv4" source address="192.168.0.4/24" service name="http" accept"

ip 192.168.0.4/24 访问 http
```





删除上面设置的规则



```csharp
firewall-cmd --permanent --zone=public --remove-rich-rule="rule family="ipv4" source address="192.168.0.4/24" service name="http" accept"
```

检查设定是否生效



```php
 iptables -L -n | grep 21
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:21 ctstate NEW
```

执行命令`firewall-cmd --list-all`
 显示：



```cpp
public (default)
  interfaces:
  sources:
  services: dhcpv6-client ftp ssh
  ports:
  masquerade: no
  forward-ports:
  icmp-blocks:
  rich rules:
```

查询服务的启动状态



```undefined
firewall-cmd --query-service ftp
yes
firewall-cmd --query-service ssh
yes
firewall-cmd --query-service samba
no
firewall-cmd --query-service http
no
```

自行加入要开放的 Port



```cpp
firewall-cmd --add-port=3128/tcp
firewall-cmd --list-all
public (default)
  interfaces:
  sources:
  services: dhcpv6-client ftp ssh
  ports: 3128/tcp
  masquerade: no
  forward-ports:
  icmp-blocks:
  rich rules:
```
