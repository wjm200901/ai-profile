---
title: 发布到 GitHub 的三种方式
audience: [human]
visibility: public
as_of: 2026-10-31
confidence: high
---

# 发布到 GitHub

> 三种方式，从"最快"到"最可控"。若本机尚未安装 Git / gh，直接看方式 B / C 的替代路径。

## 方式 A：有 Git + gh（最快）

```powershell
# 1. 安装（一次）
winget install --id Git.Git -e
winget install --id GitHub.cli -e
gh auth login          # 选 GitHub.com → HTTPS → 浏览器登录

# 2. 一条命令建仓并推送
powershell -ExecutionPolicy Bypass -File scripts\publish.ps1 -Repo ai-profile -Visibility public
```

脚本会做：初始化仓库 → 生成首次提交 → 创建远端 → 推送 → 设置描述与 topics。

## 方式 B：只有 Git（无 gh）

```powershell
winget install --id Git.Git -e
cd D:\deepseek\ai-profile
git init -b main
git add .
git commit -m "docs: 初始化 AI 时代个人档案 v0.1"
# 先在网页上手动创建空仓库，再：
git remote add origin https://github.com/<你的用户名>/ai-profile.git
git push -u origin main
```

> 推送时会要求凭证。推荐用 [Personal Access Token](https://github.com/settings/tokens)（勾选 `repo`），
> 用户名填 GitHub 用户名，密码填 token。

## 方式 C：完全没有 Git（网页上传）

1. 打开 <https://github.com/new>，创建仓库 `ai-profile`，**不要**勾选 "Add a README"。
2. 打开仓库页 → **Add file → Upload files**。
3. 把 `D:\deepseek\ai-profile\` **里面的所有文件和文件夹**拖进去（支持文件夹拖拽）。
4. 提交信息填 `docs: 初始化 AI 时代个人档案 v0.1`。

> 注意：网页上传不会保留 `.github/` 等隐藏目录的可用性，CI 需要在网页上重新添加文件（Create new file → 输入路径 `.github/workflows/validate.yml`）。

## 发布后必做（5 分钟）

1. **改占位符**：全局搜索 `yourname`、`example.com`、`林深`，替换成你的。
2. **设 About**：右侧齿轮 → Description 填一句话 → Website 填你的主页。
3. **加 Topics**：`personal-profile`、`ai-native`、`llms-txt`、`digital-twin`、`knowledge-base`。
4. **确认 Action 通过**：Actions 标签页应显示 `validate` 绿色。第一次运行需要启用 Actions。

## 进阶：让它在个人主页出现

GitHub 有一个特殊约定：**仓库名与用户名相同的仓库**（`<username>/<username>`），其 `README.md` 会显示在你的 GitHub 主页顶部。

两种用法：

- **A. 主页仓库只放精简版**：复制 [`docs/PROFILE-README.md`](PROFILE-README.md) 到 `<username>/<username>/README.md`，并在其中链接到 `ai-profile` 仓库。
- **B. 主页仓库只做跳转**：一句话 + 指向 `ai-profile` 的链接（更简单，适合保持主页干净）。

## 进阶：GitHub Pages

想让档案有个好看的网页版：

1. Settings → Pages → Source 选 `Deploy from a branch` → `main` / `/docs`。
2. 但本仓库的 `docs/` 是说明文档，不适合直接做站点。推荐另建 `site/` 或使用 [GitHub Pages + Jekyll](https://docs.github.com/pages)。

> 建议：**先不要做网页**。档案的价值在文本的可解析性，不在视觉。等有人主动来读，再做站点。

## 进阶：私有仓库 + 有限公开

- 仓库设为 **private**：内容不公开，但你可以把链接发给特定的人（对方需登录且有权限）。
- **双仓库方案**：public 骨架（`ai-profile`）+ private 细节（`ai-profile-private`），详见 [`privacy/layers.md`](../privacy/layers.md)。

## 安全提醒

- **不要**把 token 写进任何文件或提交历史。若误提交，立刻在 GitHub 上吊销该 token。
- 公开前跑一遍：`python scripts/validate.py`（会扫描手机号、身份证、密钥模式）。
- 提交历史是永久的。**删掉文件 ≠ 删掉记录**，敏感信息一旦推送，需要重写历史（`git filter-repo`）并强推。
