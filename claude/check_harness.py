#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def main():
    harness = Path(__file__).parent.resolve()
    entry = Path.home() / ".claude" / "CLAUDE.md"
    src = harness / "CLAUDE.md"
    problems = 0

    print("=== harness 健康檢查 ===")

    if entry.is_symlink() and Path(entry.resolve()) == Path(src.resolve()):
        print(f"[OK] 入口 symlink 正常：~/.claude/CLAUDE.md → {src}")
    else:
        problems = 1
        print("[問題] ~/.claude/CLAUDE.md 不再指向制度庫（可能被安裝器覆蓋成普通檔案）")
        if entry.exists() and not entry.is_symlink():
            print("  ├─ 以下是安裝器寫入的內容與制度庫版本的差異（> 開頭為安裝器新增）：")
            os.system(f"diff {src} {entry} 2>/dev/null | head -40 | sed 's/^/  │ /' || true")
            print("  ├─ 修復步驟：")
            print(f"  │  1. 有價值的新增內容 → 搬到 {harness}/rules/ 新子檔，並在 {src} 路由表加一行")
            print(f"  │  2. 先備份安裝器版本：cp {entry} {harness}/backup/CLAUDE.md.installer.$(date +%F).md")
            print(f"  └─ 3. 還原入口：ln -sf {src} {entry}")
        else:
            print(f"  └─ 修復：ln -sf {src} {entry}")

    lines = sum(1 for _ in open(src)) if src.exists() else 0
    if lines <= 60:
        print(f"[OK] 制度庫 CLAUDE.md 為 {lines} 行（門檻 60）")
    else:
        problems = 1
        print(f"[問題] 制度庫 CLAUDE.md 已達 {lines} 行（>60），可能被安裝器 append 汙染或制度退化")
        print(f"  └─ 比對備份找出多出來的內容：diff {harness}/backup/CLAUDE.md.original.2026-07-03.md {src}")
        print(f"     （若有 git 歷史，改用 git -C {harness} diff CLAUDE.md）")

    known_rules = {"context7.md"}
    rules_dir = Path.home() / ".claude" / "rules"
    if rules_dir.exists():
        for f in rules_dir.glob("*.md"):
            base = f.name
            if base not in known_rules:
                problems = 1
                print(f"[注意] ~/.claude/rules/{base} 是新出現的自動載入檔（每個 session 都會吃 token）")
                print(f"  └─ 檢視內容後決定：留著（真的每次都需要）或搬到 {harness}/rules/ 改為按需讀取")

    required_files = [
        "CLAUDE.md", "README.md", "model-dispatch.md", "judgment-rubrics.md",
        "delegation-templates.md", "maintenance-protocol.md", "letter-to-future-sessions.md",
        "diagnosis.md", "rules/git.md", "rules/workflow.md", "rules/dotnet.md", "rules/tools.md"
    ]
    missing = []
    for f in required_files:
        if not (harness / f).exists():
            problems = 1
            missing.append(f)
            print(f"[問題] 缺檔：{harness}/{f}（從 backup/ 或 git 歷史還原）")

    if not missing:
        print(f"[OK] 制度庫 {len(required_files)} 個關鍵檔齊全")

    print("========================")
    if problems == 0:
        print("結果：全部通過，機制生效中。")
    else:
        print("結果：發現問題，請依上方指示修復（修完再跑一次本腳本確認）。")
    sys.exit(problems)

if __name__ == "__main__":
    main()

