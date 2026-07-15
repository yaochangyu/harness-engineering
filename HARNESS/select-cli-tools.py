#!/usr/bin/env python3
"""
Interactive CLI tool selector for harness-install.
Discovers installed AI tools and lets users choose which to symlink.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# Tool packages mapping (from PowerShell script equivalents)
TOOL_PACKAGES = {
    "claude": ["claude"],
    "copilot": ["copilot", "@github/copilot"],
    "codex": ["codex", "codex-cli"],
    "opencode": ["opencode", "oh-my-claudecode"],
    "gemini": ["gemini", "google-gemini-cli"],
    "hermes": ["hermes"],
    "antigravity": ["antigravity", "codex-antigravity", "agy"],
}


def discover_tool_in_path() -> Dict[str, str]:
    """Scan PATH for installed tools."""
    tools = {}
    for tool_name, pkgs in TOOL_PACKAGES.items():
        for cmd in [tool_name] + pkgs:
            try:
                result = subprocess.run(
                    ["which", cmd],
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
                if result.returncode == 0:
                    path = result.stdout.strip()
                    if os.path.isfile(path) and os.access(path, os.X_OK):
                        tools[tool_name] = path
                        break
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
    return tools


def discover_tool_in_npm_global() -> Dict[str, str]:
    """Scan npm global packages for installed tools."""
    tools = {}
    try:
        result = subprocess.run(
            ["npm", "list", "-g", "--json"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            import json

            data = json.loads(result.stdout)
            dependencies = data.get("dependencies", {})

            for tool_name, packages in TOOL_PACKAGES.items():
                for pkg in packages:
                    if pkg in dependencies:
                        # Try to find the binary
                        npm_prefix = subprocess.run(
                            ["npm", "config", "get", "prefix"],
                            capture_output=True,
                            text=True,
                        ).stdout.strip()
                        bin_path = os.path.join(npm_prefix, "bin", tool_name)
                        if os.path.isfile(bin_path) and os.access(bin_path, os.X_OK):
                            tools[tool_name] = bin_path
                            break
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    return tools


def discover_tools() -> Dict[str, str]:
    """Discover all installed tools."""
    tools = {}
    tools.update(discover_tool_in_path())
    tools.update(discover_tool_in_npm_global())
    return tools


def interactive_selection(tools: Dict[str, str]) -> List[Tuple[str, str]]:
    """Interactive tool selection UI."""
    if not tools:
        print("❌ 沒有找到任何 AI CLI 工具")
        return []

    print("\n🔍 找到的 AI 工具：\n")
    sorted_tools = sorted(tools.items())
    for i, (name, path) in enumerate(sorted_tools, 1):
        print(f"  {i}. {name:12} → {path}")

    print("\n選擇方式：")
    print("  a  - 全選")
    print("  1,2,3 - 指定編號（用逗號分隔）")
    print("  skip - 跳過")

    while True:
        choice = input("\n請選擇 (a/編號/skip): ").strip().lower()

        if choice == "skip":
            return []

        if choice == "a":
            return sorted_tools

        try:
            indices = [int(x.strip()) - 1 for x in choice.split(",")]
            selected = [sorted_tools[i] for i in indices if 0 <= i < len(sorted_tools)]
            if selected:
                return selected
        except (ValueError, IndexError):
            pass

        print("❌ 輸入無效，請重試")


def format_output(selected: List[Tuple[str, str]]) -> str:
    """Format selected tools as tool=/path output."""
    return ",".join(f"{name}={path}" for name, path in selected)


def main():
    tools = discover_tools()

    if not tools:
        print("❌ 沒有找到任何 AI CLI 工具")
        print("\n需要安裝：")
        for tool_name in TOOL_PACKAGES.keys():
            print(f"  - {tool_name}")
        sys.exit(1)

    selected = interactive_selection(tools)

    if not selected:
        print("⏭️  跳過 CLI 工具 symlink")
        sys.exit(0)

    output = format_output(selected)
    print(f"\n✅ 已選擇：{output}")
    print(output)


if __name__ == "__main__":
    main()
