#!/usr/bin/env python3
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime
import shutil

def main():
    harness = Path(__file__).parent.resolve()
    src = harness / "CLAUDE.md"
    entry = Path.home() / ".claude" / "CLAUDE.md"
    gemini_entry = Path.home() / ".gemini" / "GEMINI.md"
    copilot_entry1 = Path.home() / ".github" / "copilot-instructions.md"
    copilot_entry2 = Path.home() / ".copilot" / "copilot-instructions.md"
    opencode_entry = Path.home() / ".config" / "opencode" / "AGENTS.md"
    cli_dir = Path.home() / ".claude" / "cli"
    
    if not src.exists():
        print(f"錯誤：找不到 {src}，請在 repo 目錄內執行")
        sys.exit(1)
    
    Path.home().joinpath(".claude").mkdir(parents=True, exist_ok=True)
    
    selected_tools = ""
    for arg in sys.argv[1:]:
        if arg.startswith("--cli-tools="):
            selected_tools = arg.split("=", 1)[1]
            break
    
    old_path = None
    if src.exists():
        for line in src.read_text().splitlines():
            if "（下稱 HARNESS）" in line:
                import re
                match = re.search(r"`([^`]+)`（下稱 HARNESS）", line)
                if match:
                    old_path = match.group(1).rstrip("/")
                    break
    
    if old_path and old_path != str(harness):
        print(f"[更新] repo 位置改變：{old_path} → {harness}")
        backup_dir = harness / "backup"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / f"CLAUDE.md.before-install.{datetime.now().strftime('%Y-%m-%d')}.md"
        shutil.copy(src, backup_file)
        
        for f in list(harness.glob("*.md")) + list(harness.glob("*.py")) + list(harness.glob("rules/*.md")):
            if not f.is_file():
                continue
            try:
                content = f.read_text()
                if old_path in content:
                    content = content.replace(old_path, str(harness))
                    f.write_text(content)
                    print(f"       已改寫：{f}")
            except Exception:
                pass
    
    if entry.is_symlink() and Path(entry.resolve()) == Path(src.resolve()):
        print(f"[OK] 入口 symlink 已存在且正確，無需變更")
    else:
        if entry.exists() and not entry.is_symlink():
            backup_dir = harness / "backup"
            backup_dir.mkdir(parents=True, exist_ok=True)
            bak = backup_dir / f"CLAUDE.md.replaced.{datetime.now().strftime('%Y-%m-%d')}.md"
            shutil.copy(entry, bak)
            print(f"[備份] 原本的 ~/.claude/CLAUDE.md → {bak}")
        try:
            entry.unlink(missing_ok=True)
            entry.symlink_to(src)
        except OSError:
            entry.unlink(missing_ok=True)
            shutil.copy(src, entry)
        print(f"[OK] 已建立：~/.claude/CLAUDE.md → {src}")
    
    # 建立 Gemini 入口軟連結
    Path.home().joinpath(".gemini").mkdir(parents=True, exist_ok=True)
    if gemini_entry.is_symlink() and Path(gemini_entry.resolve()) == Path(src.resolve()):
        print(f"[OK] Gemini 入口 symlink 已存在且正確，無需變更")
    else:
        if gemini_entry.exists() and not gemini_entry.is_symlink():
            backup_dir = harness / "backup"
            backup_dir.mkdir(parents=True, exist_ok=True)
            bak = backup_dir / f"GEMINI.md.replaced.{datetime.now().strftime('%Y-%m-%d')}.md"
            shutil.copy(gemini_entry, bak)
            print(f"[備份] 原本的 ~/.gemini/GEMINI.md → {bak}")
        try:
            gemini_entry.unlink(missing_ok=True)
            gemini_entry.symlink_to(src)
        except OSError:
            gemini_entry.unlink(missing_ok=True)
            shutil.copy(src, gemini_entry)
        print(f"[OK] 已建立：~/.gemini/GEMINI.md → {src}")
    
    # 建立 Copilot 入口軟連結
    for copilot_entry in [copilot_entry1, copilot_entry2]:
        copilot_entry.parent.mkdir(parents=True, exist_ok=True)
        if copilot_entry.is_symlink() and Path(copilot_entry.resolve()) == Path(src.resolve()):
            print(f"[OK] Copilot 入口 symlink ({copilot_entry.name}) 已存在且正確，無需變更")
        else:
            if copilot_entry.exists() and not copilot_entry.is_symlink():
                backup_dir = harness / "backup"
                backup_dir.mkdir(parents=True, exist_ok=True)
                bak = backup_dir / f"copilot-instructions.md.replaced.{datetime.now().strftime('%Y-%m-%d')}.md"
                shutil.copy(copilot_entry, bak)
                print(f"[備份] 原本的 {copilot_entry} → {bak}")
            try:
                copilot_entry.unlink(missing_ok=True)
                copilot_entry.symlink_to(src)
            except OSError:
                copilot_entry.unlink(missing_ok=True)
                shutil.copy(src, copilot_entry)
            print(f"[OK] 已建立：{copilot_entry} → {src}")
    
    # 建立 OpenCode 入口軟連結
    opencode_entry.parent.mkdir(parents=True, exist_ok=True)
    if opencode_entry.is_symlink() and Path(opencode_entry.resolve()) == Path(src.resolve()):
        print(f"[OK] OpenCode 入口 symlink ({opencode_entry.name}) 已存在且正確，無需變更")
    else:
        if opencode_entry.exists() and not opencode_entry.is_symlink():
            backup_dir = harness / "backup"
            backup_dir.mkdir(parents=True, exist_ok=True)
            bak = backup_dir / f"AGENTS.md.replaced.{datetime.now().strftime('%Y-%m-%d')}.md"
            shutil.copy(opencode_entry, bak)
            print(f"[備份] 原本的 {opencode_entry} → {bak}")
        try:
            opencode_entry.unlink(missing_ok=True)
            opencode_entry.symlink_to(src)
        except OSError:
            opencode_entry.unlink(missing_ok=True)
            shutil.copy(src, opencode_entry)
        print(f"[OK] 已建立：{opencode_entry} → {src}")
    
    if not selected_tools:
        print("")
        print("選擇 AI CLI 工具進行 symlink（可選）")
        try:
            result = subprocess.run([sys.executable, str(harness / "select-cli-tools.py")],
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                output = result.stdout.strip().split("\n")[-1] if result.stdout else ""
                if output and "跳過" not in output:
                    selected_tools = output
        except Exception:
            print("[警告] Python 工具選擇器失敗，跳過 CLI 工具選擇")
    
    if selected_tools:
        cli_dir.mkdir(parents=True, exist_ok=True)
        for item in selected_tools.split(","):
            item = item.strip()
            if "=" in item:
                tool, path = item.split("=", 1)
                path = Path(path.strip())
                if tool.strip() and path.exists() and os.access(path, os.X_OK):
                    link_path = cli_dir / tool.strip()
                    try:
                        link_path.unlink(missing_ok=True)
                        link_path.symlink_to(path)
                    except OSError:
                        link_path.unlink(missing_ok=True)
                        shutil.copy(path, link_path)
                    print(f"[OK] 已建立：~/.claude/cli/{tool.strip()} → {path}")
                else:
                    print(f"[警告] {item} 無效或路徑不存在/不可執行，跳過")
            else:
                tool = item.strip()
                try:
                    path = shutil.which(tool)
                    if path:
                        link_path = cli_dir / tool
                        try:
                            link_path.unlink(missing_ok=True)
                            link_path.symlink_to(path)
                        except OSError:
                            link_path.unlink(missing_ok=True)
                            shutil.copy(path, link_path)
                        print(f"[OK] 已建立：~/.claude/cli/{tool} → {path}")
                except Exception:
                    print(f"[警告] {tool} 未找到或未安裝，跳過")
    
    env_file = Path.home() / ".claude" / "env.md"
    if not env_file.exists():
        env_example = harness / "env.example.md"
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print(f"[建立] {env_file}（從範本複製，請填入實際值）")
    
    print("")
    subprocess.run([sys.executable, str(harness / "check_harness.py")])

if __name__ == "__main__":
    main()

