---
title: 工具
date: "2020-12-10 23:10:25"
modifyDate: "2020-12-10 23:10:25"
draft: true
---
### Git

#### .gitignore

配置使得Git忽略某些文件

#### .gitattributes 

`.gitattributes`文件允许你指定当执行 `git commit` 等 git 动作时，应该被 git 使用的文件和路径的属性。这样一来就可以使得，跨仓库使用不同机器、操作系统的每一位开发者都能使用到同样的值。

属性之一是 **eol** (end of line) ，其用于配置文件的行尾。

```properties
# 行尾自动转换
* text=auto
# 非文本文件，不进行任何的行尾转换。
*.png binary
*.jpg binary
```

#### pre-commit

Git工具提供的hooks，在commit 之前会被触发。用于代码的自动格式化和代码规范检测。使用的hook通过项目目录下`.pre-commit-config.yam`文件来配置。

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.5.0
    hooks:
      - id: check-byte-order-marker
      - id: trailing-whitespace
      - id: end-of-file-fixer
        exclude: "^tests/.*.http$"
```

#### 常用命令

删除已跟踪文件夹

`git rm -r --cached <>`

### 文档

#### sphinx
