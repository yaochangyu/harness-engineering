#!/usr/bin/env python3
import sys
from pathlib import Path
from datetime import datetime
import os

def main():
    harness = Path(__file__).parent.resolve()
    entry = Path.home() / ".claude" / "CLAUDE.md"
    src = harness / "CLAUDE.md"

    if entry.is_symlink():
        if Path(entry.resolve()) == Path(src.resolve()):
            entry.unlink()
            print(f"[OK] 已移除 symlink：~/.claude/CLAUDE.md")
        else:
            print(f"[跳過] ~/.claude/CLAUDE.md 是 symlink，但指向別處（{entry.readlink()}），不動它")
            sys.exit(0)
    elif entry.exists():
        print("[跳過] ~/.claude/CLAUDE.md 是一般檔案，不是本 harness 安裝的 symlink，不動它")
        sys.exit(0)
    else:
        print("[OK] ~/.claude/CLAUDE.md 不存在，無需移除")

    backup_dir = harness / "backup"
    restore = None

    replaced_files = sorted(backup_dir.glob("CLAUDE.md.replaced.*.md"), reverse=True) if backup_dir.exists() else []
    if replaced_files:
        restore = replaced_files[0]
    else:
        original_files = sorted(backup_dir.glob("CLAUDE.md.original.*.md"), reverse=True) if backup_dir.exists() else []
        if original_files:
            restore = original_files[0]

    if restore and not entry.exists():
        entry.write_text(restore.read_text())
        print(f"[還原] {restore} → ~/.claude/CLAUDE.md")
    elif not restore:
        print("[提示] backup/ 沒有可還原的備份，~/.claude/CLAUDE.md 維持不存在")

    print("")
    print(f"解除安裝完成。repo 與 backup/ 皆未刪除，重新安裝請執行：python3 {harness}/install.py")

if __name__ == "__main__":
    main()

