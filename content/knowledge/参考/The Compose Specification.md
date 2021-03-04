---
title: The Compose Specification
date: "2021-02-19 15:26:40"
modifyDate: "2021-02-19 15:26:40"
draft: true
---
# The Compose Specification

Table of Contents
Status of this document
The Compose application model
Compose file
Version top-level element
Services top-level element
Networks top-level element
Volumes top-level element
Configs top-level element
Secrets top-level element
Fragments
Extension
Interpolation

## 文档状态

本文档规范了用于定义多容器应用的 Compose 文件格式。本文档的分发是无限制的。

在本文档中的关键词“**必须**”、“**必须不**”、“**要求**”、“**不要求**”、“**应该**”、“**不应该**”，“**推荐**”、“**可能**”和“**可选**”可在[RFC 2199](https://tools.ietf.org/html/rfc2119)的描述中得到解释。

## 要求和可选属性

Compose 规范包含了以本地[OCI]容器运行时为目的设计的属性，暴漏了 Linux 内核特定的配置选项，而且还有一些 Windows 容器的特定属性，也可以能是在集群中云平台特性相关的资源放置，再部署的应用的分发和可伸缩性。
