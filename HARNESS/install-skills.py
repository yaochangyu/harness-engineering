#!/usr/bin/env python3
"""
全域 skills 安裝器（install.py 於安裝流程中呼叫）。
讀取 skills-manifest.txt，列出清單讓使用者確認後才逐條執行 `npx skills add`。
"""

import subprocess
import sys
from pathlib import Path

HARNESS = Path(__file__).parent.resolve()
MANIFEST = HARNESS / "skills-manifest.txt"


def load_manifest():
    entries = []
    if not MANIFEST.exists():
        return entries
    for line in MANIFEST.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "," not in line:
            continue
        repo, skill = line.split(",", 1)
        entries.append((repo.strip(), skill.strip()))
    return entries


def main():
    entries = load_manifest()
    if not entries:
        print("[跳過] 找不到 skills-manifest.txt 或清單為空")
        return

    print("\n════════════════════════════════════════════")
    print(f"全域 skills 安裝清單（共 {len(entries)} 條，來源：skills-manifest.txt）")
    print("════════════════════════════════════════════\n")
    for i, (repo, skill) in enumerate(entries, 1):
        print(f"  {i:2}. {skill:32} ← {repo}")

    choice = input("\n是否安裝以上 skills 到全域（所有 agent）？(y/N): ").strip().lower()
    if choice not in ("y", "yes"):
        print("[跳過] 未安裝全域 skills")
        return

    ok, failed = [], []
    for repo, skill in entries:
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

    print("\n════════════════════════════════════════════")
    print(f"[完成] 成功 {len(ok)} 條，失敗 {len(failed)} 條")
    if failed:
        print("失敗清單：" + ", ".join(failed))
    print("════════════════════════════════════════════")


if __name__ == "__main__":
    main()
