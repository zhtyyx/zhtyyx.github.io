---
layout:     post
title:      "git 核心操作手册"
subtitle:   "安装 git"
date:       2021-01-01
author:     "Hunter"
header-img: "img/post-bg-js-version.jpg"
tags:
    - git
    - 技术
    - 后端
---

## 安装 git
- Linux:
  - sudo apt-get install git
- Mac OS X:
  - homebrew 安装
  - Appstore 安装Xcode 运行后——>preference——>Download——>Command Line Tools——>install
- Windows:
  - git 官网下载，在项目目录右键Git bash

- Config:
  - git config --global user.name "输入用户名"
  - git config --global user.email "输入邮箱"
    
---
    
***如需搭建 git server, 参考以下：***
## 搭建 git 服务器
### 在运行Linux的服务器中安装 git
 - `sudo apt-get install git`
### 创建 git 用户运行 git 服务
   - `sudo adduser git`
### 创建证书登录
 - 收集所有需要登录的用户的公钥(id_rsa.pub)
- 将所有公钥导入/home/git/.ssh/authorized_keys文件中，一行一个
### 初始化git仓库
- `sudo git init --bare sample.git`
- Git就会创建一个裸仓库，裸仓库没有工作区，因为服务器上的Git仓库纯粹是为了共享，所以不让用户直接登录到服务器上去改工作区，并且服务器上的Git仓库通常都以.git结尾。然后，把owner改为git：
	- `sudo chown -R git:git sample.git`
- 禁止使用shell登录
	- 编辑/etc/passwd
	- 将`git:x:1001:1001:,,,:/home/git:/bin/bash`改为`git:x:1001:1001:,,,:/home/git:/usr/bin/git-shell`
### 克隆远程仓库：
- `git clone git@server:/srv/sample.git`

---
# Github 和码云的使用
### Github参与开源项目：
1. 找到开源项目，在项目主页点Fork，克隆一个仓库到自己的账号
2. 到自己的账号下 clone
3. 推送 pull request到官方
## 码云使用：
1. 码云上注册账号并上传SSH公钥（ 修改资料）
2. 在码云上的控制面板中创建项目
3. 本地库关联码云上的远程库
  - `git remote add origin git@gitee.com:码云个人路径/项目名称`
4. 注意：可以同时关联码云和github，只要远程库名称不同