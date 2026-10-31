---
title: 个人主页 README（精简版）
audience: [human]
visibility: public
as_of: 2026-10-31
confidence: high
---

# 个人主页 README 模板

> 用途：复制下面的内容到 `<你的用户名>/<你的用户名>/README.md`，它会显示在你的 GitHub 主页顶部。
> 与本仓库的分工：主页负责**一句话 + 入口**，本仓库负责**完整档案**。

---

```markdown
### 林深 · AI 产品设计师

把复杂系统翻译成人话。杭州。

**在做**：面向 65 岁以上用户的语音助手「银龄 AI」——已服务 1.2 万家庭。
**相信**：AI 产品的瓶颈通常在表达，不在能力。

完整档案 → **[ai-profile](https://github.com/yourname/ai-profile)**
给 AI 读的入口 → [`llms.txt`](https://github.com/yourname/ai-profile/blob/main/llms.txt)

---

<sub>这份档案记录了我是谁、怎么想、怎么合作。引用请注明「档案原文」或「模型推断」。</sub>
```

---

## 设计说明

| 选择 | 原因 |
|---|---|
| 只有 5 行 | 主页是路过，不是阅读；多余信息会稀释重点 |
| 一句"相信" | 观点比职位更能让人记住 |
| 两个链接 | 一个给人，一个给模型 |
| 底部小字 | 声明引用规则，防止 AI 生成内容被当成本人原话 |

## 三个变体

### 极简版（适合不想暴露太多的人）

```markdown
### 林深

AI 产品设计师 · 杭州
[完整档案](https://github.com/yourname/ai-profile)
```

### 作品导向版（适合设计师/创作者）

```markdown
### 林深 · AI 产品设计师

**代表作**
- [银龄 AI](https://example.com) — 让 1.2 万老人敢开口说话，首次使用成功率 43% → 71%
- [把 62 字压到 17 字](https://example.com/post) — 一次靠"少说话"提升满意度的复盘

[完整档案](https://github.com/yourname/ai-profile) · [声音指南](...)
```

### 招聘友好版（适合找工作期）

```markdown
### 林深 · AI 产品设计师

**我在找**：AI 产品的交互设计岗（杭州/远程）
**我最擅长**：把模型能力翻译成用户愿意用的交互
**证据**：银龄 AI（1.2 万家庭，NPS 61）、320 条提示词回归用例

[完整档案](https://github.com/yourname/ai-profile) · [联系](mailto:hi@example.com)
```

## 注意事项

- 主页 README 会进入你和 star 过的仓库的公开数据，**不要**写手机号、住址。
- 若你有多个仓库，主页 README 是唯一能让访客快速理解"你是谁"的位置，值得花 10 分钟。
- 修改后 1–2 分钟内生效，无缓存问题。
