# 工具細則（需要用到該工具時才讀）

## RTK
- skill name：無
- CLI name：`rtk`
- Bash 指令已由 `rtk hook claude` 自動處理；平常不用手動背規則。
- 需要省 token 時才加 `rtk`，要看完整輸出時改用原始指令。
- 串接指令每段各自加前綴：`rtk git add . && rtk git commit -m "msg"`。
- 安裝方式：優先 `brew install rtk`；Linux/macOS 也可用 `curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh`。
- 其他方式：`cargo install --git https://github.com/rtk-ai/rtk`；或從 GitHub releases 下載預編譯 binary。

## ctx7 / context7（查函式庫文件）
檢查項目：skill `find-docs`；CLI `ctx7`。
- skill name：`find-docs`
- CLI name：`ctx7`
- 這是觸發層＋執行層同一套工具；優先照 `find-docs` skill 走。
- 未安裝時才手動用 `ctx7`，不要默默改用 web search。
- 安裝與判斷規則見 `tools-install-check.md`；fallback 為 web search。

## ticket 工具
- skill name：無
- CLI name：`<TICKET_CLI>`
- 所有 ticket 操作用 `<TICKET_CLI>`；實際工具名與用法見 `~/.claude/env.md`。

## Google Workspace
- 檢查項目：skill 視服務而定（如 `gws-gmail`）；CLI `gws`。
- skill name：`gws-gmail` / `gws-slides` / `gws-sheets` / `gws-docs`
- CLI name：`gws`
- 安裝前先套用 `rules/tools-install-check.md`；細節見 `rules/google-workspace.md`。
- fallback：Gmail / Drive / Calendar 的 MCP 工具。

## 程式碼分析／搜尋工具（graphify / codegraph）
已搬到 `rules/code-search.md`；這裡只保留入口，不放細節。

## playwright-cli
- skill name：`playwright-cli`
- CLI name：`playwright-cli`
- 需要錄製 Playwright 程式碼、檢查 selector、截圖時才用。
- 安裝前先問全域或專案；skill 目錄 `playwright-cli`。
- 安裝與使用細節見該 skill；fallback 為 `rules/web-automation.md`。

## LLM Wiki
- skill name：無
- CLI name：無
- 知識庫路徑見 `~/.claude/env.md`；操作規則見 `<WIKI_ROOT>/CLAUDE.md`。
- 程式碼直接從原始路徑 ingest，不複製到 `sources/`。
- 外部資料才放 `sources/`，歸檔資料先進 `wiki/raw/` 再問要不要 ingest。

## HackMD（hackmd-cli）
檢查項目：skill `hackmd-cli`；CLI `hackmd-cli`。
- skill name：`hackmd-cli`
- CLI name：`hackmd-cli`
- 筆記與資料夾管理；細節見 `rules/hackmd.md`。
- 安裝前先問全域或專案；skill 目錄 `hackmd-cli`。
- 未裝時提示安裝指令；fallback 為官方 REST API。

## Gemini Notebook / NotebookLM
- 檢查項目：skill `notebooklm`（teng-lin）／`nlm-skill`（jacob-bd）；CLI `notebooklm` ／ `nlm`。
- skill name：`notebooklm` / `nlm-skill`
- CLI name：`notebooklm` / `nlm`
- 安裝前先套用 `rules/tools-install-check.md`；細節見 `rules/notebooklm.md`。
- fallback：NotebookLM 官方 web UI。

## CodeGraph
檢查項目：CLI `codegraph`；MCP `codegraph_explore`。
- skill name：無
- CLI name：`codegraph`
- 這裡只保留入口；細節見 `rules/code-search.md`。
- 未裝 CLI 時再提示 `npm install -g @colbymchenry/codegraph`。
- fallback 為系統內建 `codegraph_explore` MCP。

## OneDrive
檢查項目：skill `onedrive`；CLI 無。
- skill name：`onedrive`
- CLI name：無
- skill 安裝：`npx skills add https://github.com/membranedev/application-skills -s onedrive [-g] -y -a '*'`。
- 先問全域或專案；如果 skill 沒有安裝，先安裝再用。
- 需要真正連線時才改用 Membrane CLI。
- fallback 為 Microsoft Graph API 或請使用者提供 connection。

## 中文寫作 skills
- skill name：`stop-slop-zh-tw` / `write-yaochangyu-style`
- CLI name：無
檢查項目：skill `stop-slop-zh-tw`；CLI 無。
- 長文時再考慮 `stop-slop-zh-tw` 與 `write-yaochangyu-style`。
- `stop-slop-zh-tw` 有公開 repo；`write-yaochangyu-style` 只檢查本機是否存在。
- fallback 為略過去 AI 腔處理。

## pass（password-store）
- skill name：無
- CLI name：`pass`
檢查項目：CLI `pass`。
- 標準密碼管理器使用 `pass`。
- `gpg-agent` 快取與權限細節維持既有設定；需要時再看原檔。
- fallback 為手動提供密碼或憑證。
