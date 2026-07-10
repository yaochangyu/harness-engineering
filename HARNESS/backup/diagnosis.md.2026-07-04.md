# Harness 快速診斷（2026-07-03，由 Fable 5 session 產出）

> 本檔是後面所有制度檔的依據。每一條都有「證據」，不是印象分。
> 讀者注意：這裡描述的是 2026-07-03 的狀態，修法若已執行會標註〔已修〕。

## 第一名：全域規則儀式化＋重複載入（最漏 token）

**證據（已知事實）：**
- context7 使用說明全文同時存在於 `~/.claude/CLAUDE.md` 與 `~/.claude/rules/context7.md`，
  而 `~/.claude/rules/*.md` 會自動載入 → 每個 session 載入兩份一模一樣的內容（約 600 tokens/次）。
- CLAUDE.md 內有一大段 RTK 指令對照表，但 `settings.json` 已設 PreToolUse hook `rtk hook claude`，
  hook 層面已處理，說明文字純屬冗餘。
- plan.md 逐步確認流程、tree.md 維護、`.issues` 紀錄，這些是為多步驟 .NET 工作專案設計的儀式，
  卻寫成全域規則。弱模型在「回答一個小問題」時也會嘗試產生整套儀式 → 失焦＋浪費。

**修法：**
1. 〔已修〕CLAUDE.md 改為精簡路由，ctx7 段落刪除（`rules/context7.md` 已自動載入，留一份即可）。
2. 〔已修〕RTK 長說明移到 `rules/tools.md`，CLAUDE.md 只留一行。
3. 〔已修〕plan/tree/issues 流程移到 `rules/workflow.md`，並加上**觸發條件**：
   只有「使用者要求實作功能，且預計改 2 個以上檔案或多步驟」才啟用，回答問題、單檔小修不啟用。

## 第二名：設定層互相矛盾＋遺留堆積（最容易出錯）

**證據（已知事實）：**
- `~/.claude/CLAUDE.md` 是 **symlink** → `/mnt/d/lab/github-copilot/.github/copilot-instructions.md`，
  與 GitHub Copilot 共用。改其中一邊會默默影響另一邊，且兩個工具的最佳寫法不同。
- `~/.claude/settings.local.json` 的 `enabledMcpjsonServers` 與 `disabledMcpjsonServers`
  **同時**包含 `"memory"`，行為不可預期。
- `~/.claude/settings.local.json` 內含明文 Google API key，違反使用者自己的規則
  「憑證集中存放於 `~/.claude/creds/.creds`」。
- `~/.claude/` 有 superclaude 遺留檔（`RULES.md` 14K、`FLAGS.md`、`PRINCIPLES.md`、`RTK.md`），
  未被自動載入但容易被誤讀/誤引用。

**修法：**
1. 〔已修〕斷開 symlink：`~/.claude/CLAUDE.md` 改為 Claude 專屬實體檔；
   Copilot 的 `copilot-instructions.md` 原封不動。要還原：
   `ln -sf /mnt/d/lab/github-copilot/.github/copilot-instructions.md ~/.claude/CLAUDE.md`
2. 〔待使用者決定〕settings.local.json：把 API key 移到 `~/.claude/creds/.creds`
   （注意：2026-07-03 實測本機尚無 `~/.claude/creds/` 目錄，執行前先請使用者確認實際位置），
   並刪掉 memory 的矛盾設定其中一邊。**弱模型不可自行改 settings**（見 maintenance-protocol.md）。
3. 〔待使用者決定〕superclaude 遺留檔搬到 `~/.claude/backups/` 或刪除。

## 第三名：主對話下場做粗活＋完成無驗收（最容易失焦、宣稱完成但沒做好）

**證據（已知事實）：**
- 原規則對「怎麼派 subagent、什麼粗活不該在主對話做」零規範；
  主對話自己掃 repo、讀大檔、跑長輸出，context 很快被垃圾填滿，後半段品質崩。
- 常駐 MCP 眾多（github、gmail、calendar、drive、chrome-devtools、context7），
  每個 session 的 system prompt 都被撐大，即使該次任務用不到。
- 完成的判準只有一句「一定要 build」；沒有 read-back、沒有 fresh-context 驗收、
  沒有「測試輸出當證據」的要求。弱模型最常見的失效模式就是**宣稱完成但沒有證據**。

**修法：**
1. 〔已修〕`model-dispatch.md`：指揮官不下場、派工三件套、回報合約、升降級路徑、驗證不自驗。
2. 〔已修〕`judgment-rubrics.md`：完成判準、品質底線 checklist（附正反例）。
3. 〔待使用者決定〕不常用的 MCP 改為 per-project 啟用：用 `claude mcp list` 檢視，
   把 gmail/calendar/drive/chrome-devtools 這類從全域移除、只在需要的專案加回。

## 其他觀察（非前三，但值得知道）
- `stop-slop-zh-tw`、`write-yaochangyu-style` 等 skills 存在，弱模型應在寫中文長文時主動考慮使用。
- 專案記憶目錄（`~/.claude/projects/<路徑>/memory/`）是 per-project 的；
  跨專案要沿用的制度只能靠 CLAUDE.md 路由，不要指望記憶機制跨專案生效。
