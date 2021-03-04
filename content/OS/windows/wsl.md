---
title: wsl
date: "2021-02-19 15:26:40"
modifyDate: "2021-02-19 15:26:40"
draft: true
---
# wsl常见问题

## systemd无法使用

WSL2的启动方式和WSL1似乎是一致的，都是通过微软自定义的init启动。进程树的root pid不是0，而是1，原来不能使用的systemctl依旧不能使用。会直接提示：

```error
System has not been booted with systemd as init system (PID 1). Can't operate.
```

而这直接导致了我通过apt安装的docker.io不能使用(因为需要通过systemctl来启动)。

解决办法

1. 可以让 Windows 执行开机脚本，通过脚本启动 WSL2 中的 Docker，参见<https://blog.csdn.net/XhyEax/article/details/105560377>，这种方案在 WSL1 时代就有，我自己使用过没碰到过问题。
2. 第二种方案是使用第三方工具运行 systemd，参见 <https://github.com/arkane-systems/genie>，原理是提供了一个单独的 namespace 跑 systemd。
3. 第三种方案是使用 Docker Desktop，2.3.0.2 以上版本已经支持 WSL2 和 Hyper-V，免去一些折腾。

## 
