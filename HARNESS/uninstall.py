#!/usr/bin/env python3
import sys
from pathlib import Path
from datetime import datetime
import os

def main():
    harness = Path(__file__).parent.resolve()
    entry = Path.home() / ".claude" / "CLAUDE.md"
    gemini_entry = Path.home() / ".gemini" / "GEMINI.md"
    copilot_entry1 = Path.home() / ".github" / "copilot-instructions.md"
    copilot_entry2 = Path.home() / ".copilot" / "copilot-instructions.md"
    src = harness / "CLAUDE.md"

    # 處理 ~/.claude/CLAUDE.md
    if entry.is_symlink():
        if Path(entry.resolve()) == Path(src.resolve()):
            entry.unlink()
            print(f"[OK] 已移除 symlink：~/.claude/CLAUDE.md")
        else:
            print(f"[跳過] ~/.claude/CLAUDE.md 是 symlink，但指向別處（{entry.readlink()}），不動它")
    elif entry.exists():
        print("[跳過] ~/.claude/CLAUDE.md 是一般檔案，不是本 harness 安裝的 symlink，不動它")
    else:
        print("[OK] ~/.claude/CLAUDE.md 不存在，無需移除")

    # 處理 ~/.gemini/GEMINI.md
    if gemini_entry.is_symlink():
        if Path(gemini_entry.resolve()) == Path(src.resolve()):
            gemini_entry.unlink()
            print(f"[OK] 已移除 symlink：~/.gemini/GEMINI.md")
        else:
            print(f"[跳過] ~/.gemini/GEMINI.md 是 symlink，但指向別處（{gemini_entry.readlink()}），不動它")
    elif gemini_entry.exists():
        print("[跳過] ~/.gemini/GEMINI.md 是一般檔案，不是本 harness 安裝的 symlink，不動它")
    else:
        print("[OK] ~/.gemini/GEMINI.md 不存在，無需移除")

    # 處理 Copilot 提示詞檔案
    for copilot_entry in [copilot_entry1, copilot_entry2]:
        if copilot_entry.is_symlink():
            if Path(copilot_entry.resolve()) == Path(src.resolve()):
                copilot_entry.unlink()
                print(f"[OK] 已移除 symlink：{copilot_entry}")
            else:
                print(f"[跳過] {copilot_entry} 是 symlink，但指向別處（{copilot_entry.readlink()}），不動它")
        elif copilot_entry.exists():
            print(f"[跳過] {copilot_entry} 是一般檔案，不是本 harness 安裝的 symlink，不動它")
        else:
            print(f"[OK] {copilot_entry} 不存在，無需移除")

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

    gemini_restore = None
    gemini_replaced_files = sorted(backup_dir.glob("GEMINI.md.replaced.*.md"), reverse=True) if backup_dir.exists() else []
    if gemini_replaced_files:
        gemini_restore = gemini_replaced_files[0]

    if gemini_restore and not gemini_entry.exists():
        gemini_entry.write_text(gemini_restore.read_text())
        print(f"[還原] {gemini_restore} → ~/.gemini/GEMINI.md")
    elif not gemini_restore:
        print("[提示] backup/ 沒有可還原的備份，~/.gemini/GEMINI.md 維持不存在")

    copilot_restore = None
    copilot_replaced_files = sorted(backup_dir.glob("copilot-instructions.md.replaced.*.md"), reverse=True) if backup_dir.exists() else []
    if copilot_replaced_files:
        copilot_restore = copilot_replaced_files[0]

    for copilot_entry in [copilot_entry1, copilot_entry2]:
        if copilot_restore and not copilot_entry.exists():
            copilot_entry.parent.mkdir(parents=True, exist_ok=True)
            copilot_entry.write_text(copilot_restore.read_text())
            print(f"[還原] {copilot_restore} → {copilot_entry}")
        elif not copilot_restore:
            print(f"[提示] backup/ 沒有可還原的備份，{copilot_entry} 維持不存在")

    print("")
    print(f"解除安裝完成。repo 與 backup/ 皆未刪除，重新安裝請執行：python3 {harness}/install.py")

if __name__ == "__main__":
    main()

