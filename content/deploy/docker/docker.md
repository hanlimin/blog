---
title: docker
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
## Docker网络

当Docker启动时，会自动在主机上创建一个`docker0`虚拟网桥。同时Docker随机分配一个本地未占用的私有网段的一个地址给`docker0`接口。

### 网络驱动

- `bridge`：默认网络驱动。容器连接到`docker0`，与外界通信使用NAT。
- `host`：对于独立的容器，移除了容器与主机之间的网络隔离，可直接使用主机网络。
- `overlay`：覆盖网络将多个Docker守护进程连接在一起，并且开启了使得集群服务能够在彼此之间通信。
- `macvlan`：Mac网络能够允许你分配MAC地址给容器，使得容器像是在网络中的一个物理设备。Dokcer守护进程能够通过MAC地址路由通信。
- `none`：对于容器而言，关闭所有网络。通常用于自定义网络驱动。

总结：

1. brige网络适用于同个主机上多个容器之间的通信。
2. host网络适用于不需要网络与主机隔离，但是在容器的其它方面需要隔离时。
3. overlay网络适用于运行于不同主机的容器间通信，或者使用集群服务的多个应用工作中。
4. Macvlan适用于需要容器在网络上像个物理主机时
5. 第三方网络插件能够给予更多定制化。

### 网路配置

可通过查看网络列表

```shell
# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
4ddb2e5d7097        bridge              bridge              local
16d2c65785f2        host                host                local
3c2f6880a87c        none                null                local
```

docker容器默认情况下连接bridge网络，容器之间可以通过容器ip来互相访问。但是在ip可能会变化的情况下，使用ip访问并不方便。Docker Deamon实现了一个内嵌的DNS server，使容器可以直接使用容器名通信。使用自定义bridge网络可以做到通过容器名互相通信。在`docker run`时使用`--network`指定网络。

skip-host-cache

skip-name-resolve

**# Docker**



**### 优点**

\+   使用应用自身携带依赖环境

\+   与虚拟虚拟机相比更加轻量的容器

### docker-compose 

#### linux安装

```
 curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```



### 命令

#### logs 

指定容器名称查看对应日志

- `-since` 指定开始时间
- `-f` 实时日志
- `-t` 显示日志产生日期
- `-tail`指定从尾部数指定条数日志



