#!/usr/bin/env bash
# 檢查 harness 機制是否仍生效。安裝任何 Claude 相關工具、或升級 Claude Code 後跑一次：
#   bash /mnt/d/lab/harness-engineering/claude/check-harness.sh
# 全部通過 → exit 0；有問題 → 印出修復指令、exit 1。

HARNESS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # 以腳本所在位置為準，repo 搬到哪都能用
ENTRY="$HOME/.claude/CLAUDE.md"
SRC="$HARNESS/CLAUDE.md"
PROBLEMS=0

echo "=== harness 健康檢查 ==="

# 1. 入口 symlink 是否還指向制度庫
if [ -L "$ENTRY" ] && [ "$(readlink -f "$ENTRY")" = "$(readlink -f "$SRC")" ]; then
  echo "[OK] 入口 symlink 正常：~/.claude/CLAUDE.md → $SRC"
else
  PROBLEMS=1
  echo "[問題] ~/.claude/CLAUDE.md 不再指向制度庫（可能被安裝器覆蓋成普通檔案）"
  if [ -f "$ENTRY" ] && [ ! -L "$ENTRY" ]; then
    echo "  ├─ 以下是安裝器寫入的內容與制度庫版本的差異（> 開頭為安裝器新增）："
    diff "$SRC" "$ENTRY" | head -40 | sed 's/^/  │ /'
    echo "  ├─ 修復步驟："
    echo "  │  1. 有價值的新增內容 → 搬到 $HARNESS/rules/ 新子檔，並在 $SRC 路由表加一行"
    echo "  │  2. 先備份安裝器版本：cp $ENTRY $HARNESS/backup/CLAUDE.md.installer.\$(date +%F).md"
    echo "  └─ 3. 還原入口：ln -sf $SRC $ENTRY"
  else
    echo "  └─ 修復：ln -sf $SRC $ENTRY"
  fi
fi

# 2. 事實來源是否被 append 汙染（安裝器透過 symlink 直寫）
LINES=$(wc -l < "$SRC" 2>/dev/null || echo 0)
if [ "$LINES" -le 60 ]; then
  echo "[OK] 制度庫 CLAUDE.md 為 $LINES 行（門檻 60）"
else
  PROBLEMS=1
  echo "[問題] 制度庫 CLAUDE.md 已達 $LINES 行（>60），可能被安裝器 append 汙染或制度退化"
  echo "  └─ 比對備份找出多出來的內容：diff $HARNESS/backup/CLAUDE.md.original.2026-07-03.md $SRC"
  echo "     （若有 git 歷史，改用 git -C $HARNESS diff CLAUDE.md）"
fi

# 3. ~/.claude/rules/ 有沒有冒出新的「全 session 自動載入」檔
KNOWN_RULES="context7.md"
for f in "$HOME"/.claude/rules/*.md; do
  [ -e "$f" ] || continue
  base=$(basename "$f")
  case " $KNOWN_RULES " in
    *" $base "*) echo "[OK] rules/$base（已知）" ;;
    *)
      PROBLEMS=1
      echo "[注意] ~/.claude/rules/$base 是新出現的自動載入檔（每個 session 都會吃 token）"
      echo "  └─ 檢視內容後決定：留著（真的每次都需要）或搬到 $HARNESS/rules/ 改為按需讀取"
      ;;
  esac
done

# 4. 制度庫關鍵檔完整性
for f in CLAUDE.md README.md model-dispatch.md judgment-rubrics.md delegation-templates.md \
         maintenance-protocol.md letter-to-future-sessions.md diagnosis.md \
         rules/git.md rules/workflow.md rules/dotnet.md rules/tools.md; do
  if [ ! -f "$HARNESS/$f" ]; then
    PROBLEMS=1
    echo "[問題] 缺檔：$HARNESS/$f（從 backup/ 或 git 歷史還原）"
  fi
done
[ "$PROBLEMS" -eq 0 ] && echo "[OK] 制度庫 12 個關鍵檔齊全"

echo "========================"
if [ "$PROBLEMS" -eq 0 ]; then
  echo "結果：全部通過，機制生效中。"
else
  echo "結果：發現問題，請依上方指示修復（修完再跑一次本腳本確認）。"
fi
exit "$PROBLEMS"
