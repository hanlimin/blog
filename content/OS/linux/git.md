---
title: git
date: "2021-02-19 15:26:40"
modifyDate: "2021-02-19 15:26:40"
draft: true
---
### 标签

#### 基本操作

```bash
# 查看所有标签
git tag
# 查看指定标签信息
git show <tag-name>
# 删除本地的标签：
git tag -d <tag-name>
# 以指定标签创建分支
git branch <new-branch-name> <tag-name> 
# 提交标签到远程仓库
git push origin v1.4
# 一次提交本地的所有标签：
git push origin --tags
```

#### 删除远程标签

```bash
# 1. 使用参数 `--delete`:
git push origin --delete tag <tag-name>
# 2. 相当于推送一个空分支到远程分支:
git push origin :<tag-name>

# 3. 先删除本地 tag，在推送一个空的 tag 到远程仓库：
git tag -d <tag-name>
git push origin :refs/tags/<tag-name>
```

### 检出

#### 检出分支

```bash
git checkout <branch-name>
```

#### 检出文件

```bash
git checkout <commit> <file>
```

#### 检出提交

```bash
git checkout <commit>
```

### 历史

#### 重新提交

合并缓存的修改和上一次的提交，用新的快照替换上一个提交

```bash
git commit --amend
# 不修改提交信息
git commit --amend --no-edit
```

#### rebase

将次分支移动到指定分支的末端产生快速向前合并，实现完美的线性分支。

```bash
git rebase <branch>
# 交互式rebase，能够修改单个提交，可以移除、分割提交、更改提交顺序
git rebase -i <branch>
```

reset



```bash
git reset <commit>
```

