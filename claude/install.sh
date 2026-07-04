#!/usr/bin/env bash
# 安裝 harness：把 ~/.claude/CLAUDE.md 指向本 repo 的 CLAUDE.md。
# 用法（clone 到任何位置皆可）：
#   bash install.sh
# 冪等：重跑安全。會動到的東西只有 ~/.claude/CLAUDE.md（覆蓋前自動備份）。

set -euo pipefail

HARNESS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HARNESS/CLAUDE.md"
ENTRY="$HOME/.claude/CLAUDE.md"

[ -f "$SRC" ] || { echo "錯誤：找不到 $SRC，請在 repo 目錄內執行"; exit 1; }
mkdir -p "$HOME/.claude"

# 1. 若 repo 位置與 CLAUDE.md 內寫的 HARNESS 路徑不同（clone 到新位置或改過名），
#    改寫所有制度檔內的舊路徑（backup/ 除外，備份保持原貌）
OLD_PATH=$(grep -oE '`/[^`]*`（下稱 HARNESS）' "$SRC" | sed 's/^`//; s/`（下稱 HARNESS）//; s:/$::')
if [ -n "$OLD_PATH" ] && [ "$OLD_PATH" != "$HARNESS" ]; then
  echo "[更新] repo 位置改變：$OLD_PATH → $HARNESS"
  cp "$SRC" "$HARNESS/backup/CLAUDE.md.before-install.$(date +%F).md"
  for f in "$HARNESS"/*.md "$HARNESS"/*.sh "$HARNESS"/rules/*.md; do
    [ -f "$f" ] || continue
    if grep -q "$OLD_PATH" "$f"; then
      sed -i "s:$OLD_PATH:$HARNESS:g" "$f"
      echo "       已改寫：$f"
    fi
  done
fi

# 2. 建立入口 symlink（既有檔案先備份，除非它已經是正確的 symlink）
if [ -L "$ENTRY" ] && [ "$(readlink -f "$ENTRY")" = "$(readlink -f "$SRC")" ]; then
  echo "[OK] 入口 symlink 已存在且正確，無需變更"
else
  if [ -e "$ENTRY" ] && [ ! -L "$ENTRY" ]; then
    BAK="$HARNESS/backup/CLAUDE.md.replaced.$(date +%F).md"
    cp "$ENTRY" "$BAK"
    echo "[備份] 原本的 ~/.claude/CLAUDE.md → $BAK"
  fi
  ln -sf "$SRC" "$ENTRY"
  echo "[OK] 已建立：~/.claude/CLAUDE.md → $SRC"
fi

# 3. 個人環境配置：~/.claude/env.md 不存在就從範本建立（內網/公司資訊只寫在那裡，不進版控）
ENV_FILE="$HOME/.claude/env.md"
if [ ! -f "$ENV_FILE" ] && [ -f "$HARNESS/env.example.md" ]; then
  cp "$HARNESS/env.example.md" "$ENV_FILE"
  echo "[建立] $ENV_FILE（從範本複製，請填入實際值）"
fi

# 4. 健康檢查收尾
echo ""
bash "$HARNESS/check-harness.sh"
