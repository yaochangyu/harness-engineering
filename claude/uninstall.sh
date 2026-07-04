#!/usr/bin/env bash
# 解除安裝 harness：移除 ~/.claude/CLAUDE.md 的 symlink，並還原安裝前的備份（若有）。
# 用法：
#   bash uninstall.sh
# 冪等：重跑安全。只動 ~/.claude/CLAUDE.md，不刪 repo 本身與 backup/。

set -euo pipefail

HARNESS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HARNESS/CLAUDE.md"
ENTRY="$HOME/.claude/CLAUDE.md"

# 1. 移除入口 symlink（只在它確實指向本 repo 時才動手）
if [ -L "$ENTRY" ]; then
  if [ "$(readlink -f "$ENTRY")" = "$(readlink -f "$SRC")" ]; then
    rm "$ENTRY"
    echo "[OK] 已移除 symlink：~/.claude/CLAUDE.md"
  else
    echo "[跳過] ~/.claude/CLAUDE.md 是 symlink，但指向別處（$(readlink "$ENTRY")），不動它"
    exit 0
  fi
elif [ -e "$ENTRY" ]; then
  echo "[跳過] ~/.claude/CLAUDE.md 是一般檔案，不是本 harness 安裝的 symlink，不動它"
  exit 0
else
  echo "[OK] ~/.claude/CLAUDE.md 不存在，無需移除"
fi

# 2. 還原安裝前的備份（優先 replaced，其次 original；取最新日期）
RESTORE=$(ls -1 "$HARNESS"/backup/CLAUDE.md.replaced.*.md 2>/dev/null | sort | tail -n 1 || true)
if [ -z "$RESTORE" ]; then
  RESTORE=$(ls -1 "$HARNESS"/backup/CLAUDE.md.original.*.md 2>/dev/null | sort | tail -n 1 || true)
fi

if [ -n "$RESTORE" ] && [ ! -e "$ENTRY" ]; then
  cp "$RESTORE" "$ENTRY"
  echo "[還原] $RESTORE → ~/.claude/CLAUDE.md"
elif [ -z "$RESTORE" ]; then
  echo "[提示] backup/ 沒有可還原的備份，~/.claude/CLAUDE.md 維持不存在"
fi

echo ""
echo "解除安裝完成。repo 與 backup/ 皆未刪除，重新安裝請執行：bash $HARNESS/install.sh"
