#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

# ─── How to run ───
# 1. 直接在 repo 內跑：uv run HARNESS/install.py
# 2. 沒先 clone 也可以：uv run https://raw.githubusercontent.com/yaochangyu/harness-engineering/main/HARNESS/install.py
# 3. 要換來源或落點可加 --repo / --target
# ──────────────────

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime
import shutil
import stat
import tarfile
import tempfile
import urllib.error
import urllib.request
from typing import TypedDict

DEFAULT_REPO_URL = "https://github.com/yaochangyu/harness-engineering"
DEFAULT_BRANCH = "main"
DEFAULT_TARGET_NAME = "harness-engineering"
BOOTSTRAP_MARKER = ".harness-bootstrap-complete"
RTK_REPO_URL = "https://github.com/rtk-ai/rtk"
RTK_INSTALL_SCRIPT = "https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh"


class BootstrapArgs(TypedDict, total=False):
    repo: str
    branch: str
    tag: str | None
    target: str
    git_enabled: bool
    forwarded_args: list[str]


def parse_bootstrap_args(argv: list[str]) -> BootstrapArgs:
    args: BootstrapArgs = {
        "repo": DEFAULT_REPO_URL,
        "branch": DEFAULT_BRANCH,
        "tag": None,
        "target": str(Path.cwd() / DEFAULT_TARGET_NAME),
        "git_enabled": True,
        "forwarded_args": [],
    }
    for arg in argv:
        if arg.startswith("--repo-url=") or arg.startswith("--repo="):
            args["repo"] = arg.split("=", 1)[1]
        elif arg.startswith("--branch="):
            args["branch"] = arg.split("=", 1)[1]
        elif arg.startswith("--tag="):
            args["tag"] = arg.split("=", 1)[1]
        elif arg.startswith("--target-dir=") or arg.startswith("--target="):
            args["target"] = arg.split("=", 1)[1]
        elif arg == "--no-git":
            args["git_enabled"] = False
        else:
            args["forwarded_args"].append(arg)
    return args


def tarball_url(repo: str, branch: str | None = None, tag: str | None = None) -> str:
    if repo.startswith("file://") or repo.endswith(".tar.gz"):
        return repo
    base = repo[:-4] if repo.endswith(".git") else repo
    if tag and not branch:
        return f"{base}/archive/refs/tags/{tag}.tar.gz"
    return f"{base}/archive/refs/heads/{branch or DEFAULT_BRANCH}.tar.gz"


def acquire_repo(url: str, target: str, git_enabled: bool = True, branch: str = DEFAULT_BRANCH, tag: str | None = None) -> bool:
    target_dir = Path(target)
    harness_install = target_dir / "HARNESS" / "install.py"
    marker = target_dir / BOOTSTRAP_MARKER
    if harness_install.exists() or marker.exists():
        return True
    if target_dir.exists() and (not target_dir.is_dir() or any(target_dir.iterdir())):
        print(f"[錯誤] 目標位置已存在且不是 HARNESS repo：{target_dir}")
        return False

    try:
        target_dir.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"[錯誤] 無法建立目標位置：{error}")
        return False

    if git_enabled and shutil.which("git"):
        try:
            subprocess.run(["git", "clone", url, str(target_dir)], check=True)
            return True
        except (OSError, subprocess.CalledProcessError):
            print("[警告] git clone 失敗，改用 tarball 下載")

    try:
        archive_source = tarball_url(url, branch, tag)
        with urllib.request.urlopen(archive_source, timeout=60) as response:
            with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp_file:
                tmp_file.write(response.read())
                tmp_path = Path(tmp_file.name)
        with tempfile.TemporaryDirectory() as extract_root:
            with tarfile.open(tmp_path, "r:gz") as archive:
                archive.extractall(extract_root, filter="data")
            extracted_root = Path(extract_root)
            roots = [item for item in extracted_root.iterdir()]
            source_root = roots[0] if len(roots) == 1 and roots[0].is_dir() else extracted_root
            target_dir.mkdir(parents=True, exist_ok=True)
            for item in source_root.iterdir():
                shutil.move(str(item), target_dir / item.name)
        marker.write_text("ok", encoding="utf-8")
        tmp_path.unlink(missing_ok=True)
        return True
    except (OSError, tarfile.TarError, urllib.error.URLError, urllib.error.HTTPError) as error:
        print(f"[錯誤] 無法取得 HARNESS repo：{error}")
        return False


def bootstrap(argv: list[str]) -> int:
    args = parse_bootstrap_args(argv)
    repo = args["repo"]
    target = args["target"]
    print(f"[bootstrap] repo={repo} target={target}")
    if not acquire_repo(repo, target, args["git_enabled"], args["branch"], args["tag"]):
        return 1
    child = Path(target) / "HARNESS" / "install.py"
    if not child.exists():
        print(f"[錯誤] 找不到後續安裝腳本：{child}")
        return 1
    result = subprocess.run([sys.executable, str(child), *args["forwarded_args"]])
    return result.returncode


def ensure_rtk_installed() -> bool:
    rtk_path = shutil.which("rtk")
    if rtk_path:
        print(f"[OK] RTK 已安裝：{rtk_path}")
        return True

    print("")
    print("═" * 44)
    print("RTK（Bash 輸出壓縮工具）")
    print("═" * 44)
    print("RTK 會搭配 Bash hook 壓縮命令輸出，減少 agent 讀取的 context。")
    print("")

    try:
        choice = input("是否安裝 RTK？(y/N): ").strip().lower()
    except EOFError:
        print("[略過] RTK 無互動輸入")
        return False

    if choice not in ("y", "yes"):
        print("[略過] RTK 未安裝")
        return False

    if sys.platform == "darwin" and shutil.which("brew"):
        command = ["brew", "install", "rtk"]
    elif shutil.which("cargo"):
        command = ["cargo", "install", "--git", RTK_REPO_URL]
    elif shutil.which("sh") and shutil.which("curl"):
        command = ["sh", "-lc", f"curl -fsSL {RTK_INSTALL_SCRIPT} | sh"]
    else:
        print("[錯誤] 找不到可用的安裝方式（brew/cargo/curl+sh）")
        return False

    print(f"[安裝] {' '.join(command)}")
    try:
        result = subprocess.run(command, timeout=600)
    except (subprocess.TimeoutExpired, FileNotFoundError) as error:
        print(f"[錯誤] RTK 安裝失敗：{error}")
        return False

    if result.returncode == 0:
        print("[成功] RTK 已安裝")
        return True

    print("[錯誤] RTK 安裝失敗")
    return False

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
        sys.exit(bootstrap(sys.argv[1:]))
    
    Path.home().joinpath(".claude").mkdir(parents=True, exist_ok=True)
    
    selected_tools = ""
    for arg in sys.argv[1:]:
        if arg.startswith("--cli-tools="):
            selected_tools = arg.split("=", 1)[1]
            break
    
    old_path = None
    if src.exists():
        for line in src.read_text(encoding="utf-8").splitlines():
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
                content = f.read_text(encoding="utf-8")
                if old_path in content:
                    content = content.replace(old_path, str(harness))
                    f.write_text(content, encoding="utf-8")
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

    print("")
    ensure_rtk_installed()

    print("")
    try:
        subprocess.run([sys.executable, str(harness / "install-skills.py")])
    except Exception:
        print("[警告] skills 安裝腳本執行失敗，跳過")

    # 檢查並引導安裝 CodeGraph CLI 工具
    print("")
    codegraph_path = shutil.which("codegraph")
    if not codegraph_path:
        print("═" * 44)
        print("CodeGraph（代碼索引化工具）")
        print("═" * 44)
        print("CodeGraph 為 Claude Code / Cursor 等 AI 編輯器")
        print("建立預先索引的代碼知識圖，自動同步程式碼異動。")
        print("")
        try:
            choice = input("是否安裝 CodeGraph？(y/N): ").strip().lower()
            if choice in ("y", "yes"):
                print("\n--- 安裝 CodeGraph ---")
                result = subprocess.run(
                    ["npm", "install", "-g", "@colbymchenry/codegraph"],
                    timeout=120,
                )
                if result.returncode == 0:
                    print("[成功] CodeGraph 已安裝")
                    print("後續可執行 codegraph install 配置 MCP 伺服器")
                else:
                    print("[錯誤] CodeGraph 安裝失敗，請檢查 npm 是否已安裝")
            else:
                print("[略過] CodeGraph 未安裝")
        except EOFError:
            print("[略過] CodeGraph 無互動輸入")
        except Exception as e:
            print(f"[警告] CodeGraph 安裝出錯：{e}")
    else:
        print(f"[OK] CodeGraph 已安裝：{codegraph_path}")
        print("後續如需配置 MCP 伺服器可執行 codegraph install")

    env_file = Path.home() / ".claude" / "env.md"
    if not env_file.exists():
        env_example = harness / "env.example.md"
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print(f"[建立] {env_file}（從範本複製，請填入實際值）")

    print("")
    subprocess.run([sys.executable, str(harness / "check_harness.py")])

    print("")
    print("[提示] 程式碼分析／搜尋工具（graphify／codegraph）為選用，未自動安裝；需要時見 HARNESS/rules/code-search.md。")

if __name__ == "__main__":
    main()
