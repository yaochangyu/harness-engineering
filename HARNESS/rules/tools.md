# 工具細則（需要用到該工具時才讀）

## RTK（Rust Token Killer）
- Bash 指令已由 `rtk hook claude` 自動處理；平常不用手動背規則。
- 需要省 token 時才加 `rtk`，要看完整輸出時改用原始指令。
- 串接指令每段各自加前綴：`rtk git add . && rtk git commit -m "msg"`。

## ctx7 / context7（查函式庫文件）
檢查項目：skill `find-docs`；CLI `ctx7`。
- 這是觸發層＋執行層同一套工具；優先照 `find-docs` skill 走。
- 未安裝時才手動用 `ctx7`，不要默默改用 web search。
- 安裝與判斷規則見 `tools-install-check.md`；fallback 為 web search。

## ticket 工具
- 所有 ticket 操作用 `<TICKET_CLI>`；實際工具名與用法見 `~/.claude/env.md`。

## Google Workspace
詳見 `rules/google-workspace.md`。

## 程式碼分析／搜尋工具（graphify / codegraph）
已搬到 `rules/code-search.md`；這裡只保留入口，不放細節。

## playwright-cli
- 需要錄製 Playwright 程式碼、檢查 selector、截圖時才用。
- 安裝前先問全域或專案；skill 目錄 `playwright-cli`。
- 安裝與使用細節見該 skill；fallback 為 `rules/web-automation.md`。

## LLM Wiki
- 知識庫路徑見 `~/.claude/env.md`；操作規則見 `<WIKI_ROOT>/CLAUDE.md`。
- 程式碼直接從原始路徑 ingest，不複製到 `sources/`。
- 外部資料才放 `sources/`，歸檔資料先進 `wiki/raw/` 再問要不要 ingest。

## HackMD（hackmd-cli）
檢查項目：skill `hackmd-cli`；CLI `hackmd-cli`。
- 筆記與資料夾管理；細節見 `rules/hackmd.md`。
- 安裝前先問全域或專案；skill 目錄 `hackmd-cli`。
- 未裝時提示安裝指令；fallback 為官方 REST API。

## Gemini Notebook / NotebookLM
詳見 `rules/notebooklm.md`。

## CodeGraph
檢查項目：skill（在 `.claude/skills/` 底下）；CLI `codegraph`。
- 這裡只保留入口；細節見 `rules/code-search.md`。
- 未裝 CLI 時再提示 `npm install -g @colbymchenry/codegraph`。
- fallback 為系統內建 `codegraph_explore` MCP。

## OneDrive
檢查項目：skill `onedrive`；CLI 無。
- 只裝 skill，不另外寫 CLI skill。
- 先問全域或專案；需要真正連線時才改用 Membrane CLI。
- fallback 為 Microsoft Graph API 或請使用者提供 connection。

## 中文寫作 skills
檢查項目：skill `stop-slop-zh-tw`；CLI 無。
- 長文時再考慮 `stop-slop-zh-tw` 與 `write-yaochangyu-style`。
- `stop-slop-zh-tw` 有公開 repo；`write-yaochangyu-style` 只檢查本機是否存在。
- fallback 為略過去 AI 腔處理。

## pass（password-store）
檢查項目：CLI `pass`。
- 標準密碼管理器使用 `pass`。
- `gpg-agent` 快取與權限細節維持既有設定；需要時再看原檔。
- fallback 為手動提供密碼或憑證。

## 變更紀錄
- 2026-08-15：本檔改成索引頁，重點是延遲載入；細節盡量移到子檔或工具本身。
- 2026-08-15：graphify / codegraph 已改走 `rules/code-search.md`。
- 2026-08-15：HackMD 已縮到核心版；其餘舊細節見 git history。
