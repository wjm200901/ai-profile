---
title: 上手：三步把示例变成你自己
audience: [human]
visibility: public
as_of: 2026-10-31
confidence: high
---

# 上手：三步走

当前仓库里的人物「林深」是**虚构示例**，用来展示"填到什么颗粒度才算够"。你的任务是把示例替换成你自己——不是重写，是替换。

## 10 分钟版（最小可用）

1. **改三个地方**：`profile.json` 的 `name` / `jobTitle` / `description`；`identity/00-core.md` 的"一句话"与"30 秒"；`README.md` 开头那段。
2. **跑一次校验**：`python scripts/validate.py`，把报错改到全绿。
3. **发布**：按 [`docs/PUBLISH.md`](docs/PUBLISH.md) 推到 GitHub。

做完这三步，你就有了一个"模型能读懂、别人能看懂"的最小版本。剩下的文件可以逐步填。

## 30 分钟版（推荐）

按这个顺序填，每一步都能独立使用：

| 顺序 | 文件 | 回答的问题 | 最少写多少 |
|---|---|---|---|
| 1 | `identity/00-core.md` | 一句话、现在在做什么 | 150 字 |
| 2 | `identity/06-boundaries.md` | 什么不能公开、AI 能代表我说什么 | 80 字 |
| 3 | `identity/05-voice.md` | 我说话什么样 | 100 字 + 2 组对照 |
| 4 | `identity/04-principles.md` | 我怎么做决定 | 5 条 |
| 5 | `identity/02-capabilities.md` | 我能做什么、证据是什么 | 6 行 |
| 6 | `identity/03-taste.md` | 我判断好坏的标尺 | 3 条 + 3 个反例 |
| 7 | `identity/01-timeline.md` | 我怎么变成现在这样 | 5 行 |
| 8 | `memory/projects/` | 代表作档案 | 1 张卡 |

**先填 1、2 两个**，因为一个决定"你是谁"，另一个决定"什么不能写"——顺序反了容易写出一堆不能公开的内容。

## 不想自己写？让 AI 访谈你

把 [`INTAKE.md`](INTAKE.md) 连同 [`prompts/interview-me.md`](prompts/interview-me.md) 一起粘给任意模型（Claude / GPT / DeepSeek 都行），它会分 5 轮访谈你，最后直接输出符合本仓库格式的 Markdown。全程约 25 分钟。

## 每周 15 分钟（让它活着）

见 [`ops/update-ritual.md`](ops/update-ritual.md)。最短版本：问自己三个问题——**这周我改变了什么看法？做了什么新东西？哪个旧事实过期了？**

## 发布前检查清单

- [ ] `python scripts/validate.py` 全部通过（0 error）
- [ ] 全文搜索过：手机号、身份证、住址、客户名、同事真名、未公开项目
- [ ] `identity/06-boundaries.md` 里的授权范围写清楚了
- [ ] `profile.json` 里的 `sameAs` 链接都对
- [ ] 决定了仓库是 public 还是 private（建议：public 骨架 + private 细节）
- [ ] 想清楚是否要开启 GitHub Pages / 自定义域名

## 常见的三个坑

1. **一次写完**。写档案像写代码，一次写完必然假。先写 60 分，每周加 5 分。
2. **只写优点**。没有失败、犹豫、拒绝的档案，模型会把你写成宣传册。
3. **忘了删示例**。发布前搜一遍「林深」，确认没漏。命令见 [`docs/PUBLISH.md`](docs/PUBLISH.md)。
