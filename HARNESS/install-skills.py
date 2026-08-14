#!/usr/bin/env python3
"""
全域 skills 安裝器（install.py 於安裝流程中呼叫）。
讀取 skills-manifest.txt (通用工具) 與 skills-manifest-workflow.txt (工作流)，列出分類清單讓使用者選擇安裝。
"""

import subprocess
import sys
from pathlib import Path

HARNESS = Path(__file__).parent.resolve()
MANIFEST_GENERAL = HARNESS / "skills-manifest.txt"
MANIFEST_WORKFLOW = HARNESS / "skills-manifest-workflow.txt"


def load_manifest(filepath):
    entries = []
    if not filepath.exists():
        return entries
    for line in filepath.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "," not in line:
            continue
        repo, skill = line.split(",", 1)
        entries.append((repo.strip(), skill.strip()))
    return entries


def install_entries(category_name, entries):
    if not entries:
        print(f"[跳過] {category_name} 清單為空")
        return

    print("\n" + "═" * 44)
    print(f"{category_name} 安裝清單（共 {len(entries)} 條）")
    print("═" * 44 + "\n")

    skills_dir = Path.home() / ".claude" / "skills"
    already_installed = []
    to_install = []

    for i, (repo, skill) in enumerate(entries, 1):
        skill_path = skills_dir / skill
        if skill_path.exists() and skill_path.is_dir():
            already_installed.append((i, skill, repo))
        else:
            to_install.append((i, skill, repo))

    # 列出清單（已安裝和待安裝）
    for i, skill, repo in already_installed:
        print(f"  {i:2}. {skill:32} ← {repo} [已安裝]")
    for i, skill, repo in to_install:
        print(f"  {i:2}. {skill:32} ← {repo}")

    if not to_install:
        print(f"\n[OK] {category_name} 全部已安裝")
        return

    print(f"\n待安裝：{len(to_install)} 條，已安裝：{len(already_installed)} 條")

    try:
        choice = input(f"\n是否安裝【{category_name}】中待安裝的項目？(y/N): ").strip().lower()
    except EOFError:
        print(f"[跳過] {category_name} 無互動輸入")
        return
    if choice not in ("y", "yes"):
        print(f"[跳過] 未安裝 {category_name}")
        return

    ok, failed = [], []
    for i, skill, repo in to_install:
        print(f"\n--- 安裝 {skill}（{repo}）---")
        try:
            result = subprocess.run(
                ["npx", "skills", "add", repo, "-s", skill, "-g", "-y", "-a", "*"],
                timeout=180,
            )
            if result.returncode == 0:
                ok.append(skill)
            else:
                failed.append(skill)
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"[錯誤] {skill} 安裝失敗：{e}")
            failed.append(skill)

    print("\n" + "═" * 44)
    print(f"[{category_name} 完成] 新安裝 {len(ok)} 條，失敗 {len(failed)} 條，已有 {len(already_installed)} 條")
    if failed:
        print("失敗清單：" + ", ".join(failed))
    print("═" * 44)


def main():
    general_entries = load_manifest(MANIFEST_GENERAL)
    workflow_entries = load_manifest(MANIFEST_WORKFLOW)

    if not general_entries and not workflow_entries:
        print("[跳過] 找不到 skills-manifest 檔案或清單皆為空")
        return

    install_entries("通用工具類 Skills", general_entries)
    install_entries("開發工作流程類 Skills", workflow_entries)


if __name__ == "__main__":
    main()
