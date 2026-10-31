# Changelog

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- 初始化档案结构：`identity/`、`memory/`、`prompts/`、`agent/`、`privacy/`、`ops/`
- 机器可读层：`llms.txt`、`profile.json`、`agent/agent-card.json`
- 工具：`scripts/validate.py`、`scripts/build.py`、`scripts/publish.ps1`
- CI：`.github/workflows/validate.yml`

## [0.2.0] - 2026-11-01

### Changed
- 档案从虚构示例（林深）替换为王嘉铭的真实内容
- 新增 `identity/07-academics.md`（学业现状与目标）与 `plan/study-plan.md`（周计划 / 打卡表）
- 重写：00 核心、01 时间线、02 能力、03 品味、04 原则、05 声音、06 边界、记忆/项目、`llms.txt`、`profile.json`、agent card、系统提示词

### Notes
- 部分小节标注「待补」，等下一轮访谈补齐（分班考细节、书法年限、影响我的人）

## [0.1.0] - 2026-10-31

### Added
- 首版示例档案（人物「林深」为虚构示例）
- 十条设计原则（`docs/DESIGN.md`）
- 42 题自省问卷（`INTAKE.md`）
- 三套提示词：访谈、系统提示、每周复盘

### Notes
- 示例内容用于展示"填到什么颗粒度才算够"，替换时请整体重写，不要半改。
