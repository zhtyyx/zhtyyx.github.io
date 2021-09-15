---
layout:     post
title:      "git 核心操作手册（四）"
subtitle:   "git 分支管理 & debug流程"
date:       2021-03-01
author:     "Hunter"
header-img: "img/git.jpg"
tags:
    - git
---

## 如何进行代码分支管理？
#### 创建分支：创建一个新的分支并将该分支指向master相同的提交
- `git checkout -b dev`
#### 合并分支：将HEAD指向的分支指向想要合并的分支（不显示合并历史，fast-forward）
- `git merge 分支名（别人的）`
#### 删除分支：
- `git branch -d 分支名`
#### 强行删除分支（忽略提示）：            
- `git branch -D 分支名`
#### 查看分支：   
- `git branch`
#### 切换分支：            
- `git checkout 分支名`
#### 不使用Fast Forward模式合并（显示合并历史，no-fast-forward）：            
- `git merge-no-ff -m "instruction" 分支名（别人的）`
---
## debug 的通用步骤：            
1. 先确定在哪个分支上修改bug（以master举例）：
    - `git checkout master ` ——>切换到master分支
    - `git stash 保存工作现场` ——>保存此时分支上的工作现场
2. 从master分支上创建临时分支:
    - `git checkout -b 临时分支名` ——>准备在临时分支上修改bug
3. 修复bug
4. 切换到master分支并合并分支
    - `git checkout 分支名` ——>切换回master分支并将临时分支上修改后的代码合并到master上
5. 删除临时分支
    - `git branch -d 分支名`
6. 回到之前的工作现场所在分支dev
    - `git checkout dev`
7. 恢复工作现场：
    - `git stash apply` ——>恢复工作现场并不删除stash，要用git stash drop来删除               
    -  `git stash pop` ——>恢复工作现场并删除stash
    - 将本地未push的分叉提交历史整理成直线 
      - `git rebase`