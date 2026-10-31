#!/usr/bin/env python3
"""校验个人档案仓库：front matter / JSON 结构 / 死链 / 敏感信息 / 时效。

零依赖，Python 3.9+。
用法：python scripts/validate.py [--strict]
退出码：0 = 通过（可有警告），1 = 存在错误。
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today()

REQUIRED_FM = ("title", "audience", "visibility", "as_of", "confidence")
VISIBILITY = {"public", "semi-public", "private"}
CONFIDENCE = {"high", "medium", "low"}
JSON_REQUIRED = {
    "profile.json": ("version", "as_of", "canonicalUrl", "person", "summary30s"),
    "agent/agent-card.json": ("name", "description", "skills", "authorization"),
}
STALE_DAYS = 120
LLMS_BUDGET = 2000
SKIP_DIRS = {".git", "dist", "private", "__pycache__", ".venv", "node_modules"}

SENSITIVE = [
    ("手机号", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("身份证号", re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")),
    ("API Key", re.compile(r"\b(?:sk|ghp|gho|github_pat)[-_][A-Za-z0-9]{16,}")),
    ("私钥", re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY")),
]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CJK_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")
WORD_RE = re.compile(r"[A-Za-z0-9_]+")

errors: list[str] = []
warnings: list[str] = []
checks = 0


def err(msg: str) -> None:
    errors.append(msg)
    print(f"  x {msg}")


def warn(msg: str) -> None:
    warnings.append(msg)
    print(f"  ! {msg}")


def pass_(msg: str) -> None:
    print(f"  v {msg}")


def walk(suffixes: tuple[str, ...]) -> list[Path]:
    out = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in suffixes:
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        out.append(p)
    return out


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def split_front_matter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            meta = {}
            for ln in lines[1:i]:
                if ":" in ln:
                    k, v = ln.split(":", 1)
                    meta[k.strip()] = v.strip()
            return meta, "\n".join(lines[i + 1:])
    return None, text


def estimate_tokens(text: str) -> int:
    cjk = len(CJK_RE.findall(text))
    words = len(WORD_RE.findall(text))
    return int(cjk * 0.7 + words * 1.3)


def check_front_matter() -> None:
    global checks
    print("\n[1/5] Front matter（identity/ 下必填）")
    targets = [p for p in walk((".md",)) if p.parent.name == "identity"]
    if not targets:
        err("没有找到 identity/*.md")
        return
    for p in targets:
        checks += 1
        meta, _ = split_front_matter(p.read_text(encoding="utf-8"))
        if meta is None:
            err(f"{rel(p)} 缺少 front matter")
            continue
        missing = [k for k in REQUIRED_FM if not meta.get(k)]
        if missing:
            err(f"{rel(p)} front matter 缺少字段：{', '.join(missing)}")
        if meta.get("visibility") and meta["visibility"] not in VISIBILITY:
            err(f"{rel(p)} visibility 非法：{meta['visibility']}")
        if meta.get("confidence") and meta["confidence"] not in CONFIDENCE:
            err(f"{rel(p)} confidence 非法：{meta['confidence']}")
        raw = meta.get("as_of", "")
        try:
            d = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            err(f"{rel(p)} as_of 格式应为 YYYY-MM-DD，当前：{raw!r}")
            continue
        age = (TODAY - d).days
        if age > STALE_DAYS:
            warn(f"{rel(p)} 已 {age} 天未更新（{raw}），建议复核")
        if age < 0:
            err(f"{rel(p)} as_of 在未来：{raw}")
    if checks and not errors:
        pass_(f"{checks} 个文件的 front matter 均合法")


def check_json() -> None:
    global checks
    print("\n[2/5] JSON 结构")
    for name, keys in JSON_REQUIRED.items():
        p = ROOT / name
        checks += 1
        if not p.exists():
            err(f"缺少 {name}")
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"{name} 不是合法 JSON：{e}")
            continue
        missing = [k for k in keys if k not in data]
        if missing:
            err(f"{name} 缺少顶层字段：{', '.join(missing)}")
        else:
            pass_(f"{name} 合法，字段齐全")


def check_links() -> None:
    global checks
    print("\n[3/5] 内部链接")
    targets = walk((".md", ".txt"))
    broken = 0
    total = 0
    for p in targets:
        in_fence = False
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in LINK_RE.findall(line):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                total += 1
                clean = target.split("#", 1)[0]
                if not clean:
                    continue
                resolved = (p.parent / clean).resolve()
                if not resolved.exists():
                    err(f"{rel(p)} 死链 -> {target}")
                    broken += 1
    checks += total
    if total and not broken:
        pass_(f"{total} 个内部链接全部可达")
    elif not total:
        warn("未发现内部链接")


def check_sensitive() -> None:
    global checks
    print("\n[4/5] 敏感信息扫描")
    hits = 0
    for p in walk((".md", ".txt", ".json", ".yml", ".yaml")):
        text = p.read_text(encoding="utf-8")
        for label, pattern in SENSITIVE:
            for m in pattern.finditer(text):
                snippet = m.group(0)
                if label == "手机号" and snippet.startswith("2026"):
                    continue
                line_no = text[: m.start()].count("\n") + 1
                err(f"{rel(p)}:{line_no} 疑似{label}：{snippet[:6]}…")
                hits += 1
    checks += 1
    if not hits:
        pass_("未发现手机号 / 身份证 / 密钥 / 私钥模式")


def check_budget() -> None:
    global checks
    print("\n[5/5] 上下文预算")
    llms = ROOT / "llms.txt"
    checks += 1
    if not llms.exists():
        err("缺少 llms.txt")
        return
    text = llms.read_text(encoding="utf-8")
    tokens = estimate_tokens(text)
    if tokens > LLMS_BUDGET:
        warn(f"llms.txt 约 {tokens} tokens，超过 {LLMS_BUDGET} 预算，建议精简")
    else:
        pass_(f"llms.txt 约 {tokens} tokens（预算 {LLMS_BUDGET}）")
    for p in walk((".md",)):
        size = len(p.read_text(encoding="utf-8"))
        if size > 20000:
            warn(f"{rel(p)} 超过 2 万字符，考虑拆分")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"档案校验 · {TODAY} · root={ROOT}")
    check_front_matter()
    check_json()
    check_links()
    check_sensitive()
    check_budget()
    print("\n" + "=" * 46)
    print(f"检查 {checks} 项 | 错误 {len(errors)} | 警告 {len(warnings)}")
    if errors:
        print("结果：FAIL")
        return 1
    print("结果：PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
