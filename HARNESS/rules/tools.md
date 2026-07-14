# 工具細則（需要用到該工具時才讀）

## RTK（Rust Token Killer）
- `settings.json` 已設 PreToolUse hook `rtk hook claude`，Bash 指令會被自動處理；
  平常**不需要**手動背指令對照表。
- 原則：shell 指令加 `rtk` 前綴可省 60–90% token，無對應 filter 時原樣通過，永遠安全。
- 指令串接時每段都加前綴：`rtk git add . && rtk git commit -m "msg"`。
- 除錯時（需要看完整輸出）用原始指令，不加 rtk。
- `rtk proxy <cmd>`：不過濾但記錄用量。

## ctx7 / context7（查函式庫文件）
- 官方文件／repo：https://github.com/upstash/context7（`ctx7` 是其官方 CLI，兩個名字指同一個工具）。
- 詳細使用規則（查詢步驟、fallback 條件等）已在 `~/.claude/rules/context7.md` 自動載入，不要在別處重複維護。
- 呼叫優先順序：先用 `command -v ctx7` 確認是否有全域安裝的 `ctx7` 指令；
  有就直接呼叫 `ctx7 ...`（比 `npx ctx7@latest` 快，不用每次重新解析/下載）；
  找不到才 fallback 用 `npx ctx7@latest ...`，並告知使用者可 `npm install -g ctx7` 全域安裝以省掉 npx 開銷。
  不可因為沒裝就默默跳過 Context7 或改用 web search。

## ticket 工具
- 所有 ticket 操作用 `<TICKET_CLI>`（實際工具名與使用說明位置見 `~/.claude/env.md`）。

## Google Workspace
- 需要 Gmail / Drive / Calendar 操作時，優先用 googleworkspace cli：
  `https://github.com/googleworkspace/cli`。

## graphify
- 使用者輸入 `/graphify` 時，先呼叫 Skill tool（`skill: "graphify"`）再做其他事。
- Skill 位置：`~/.claude/skills/graphify/SKILL.md`。

## LLM Wiki
- 知識庫路徑 `<WIKI_ROOT>` 見 `~/.claude/env.md`；操作規則見 `<WIKI_ROOT>/CLAUDE.md`。
- Ingest 程式碼時直接從原始路徑讀取，不複製到 `sources/`；
  `sources/` 只放外部資料（文章、論文、技術文件等沒有 repo 的資料）。
- wiki 頁面 frontmatter 的 `sources` 欄位，程式碼引用用絕對路徑
  （如 `/path/to/project/src/...`）。
- 使用者要求歸檔到 wiki：資料放 `<WIKI_ROOT>/wiki/raw/{歸檔}.md`，
  然後詢問是否需要 ingest 到 wiki。

## HackMD（hackmd-cli）
- 官方文件：https://github.com/hackmdio/hackmd-cli（只支援 hackmd.io 官方或 HackMD EE ≥ 1.38.1，不支援 CodiMD）。
- 指令用法如有不確定（子指令、flag 名稱），先跑 `hackmd-cli --help` 或 `hackmd-cli <command> --help` 確認，
  不要憑記憶或文件片段猜參數；CLI 版本可能與下方摘要不同。
- 登入：`hackmd-cli login`（access token 由 hackmd.io → Setting → API 建立）；
  token 存放與其他憑證一致，放 `~/.claude/creds/.creds`，**不要**寫進 repo 或用 echo 印出，
  指令中用 `$HMD_API_ACCESS_TOKEN` 環境變數帶入。
- 若用 HackMD EE（非官方 hackmd.io），API endpoint 存在 `~/.claude/env.md`（用 `$HMD_API_ENDPOINT_URL`）。
- 常用指令：
  - 筆記：`hackmd-cli notes` / `notes create --content=... --title=...` / `notes update --noteId=...` / `notes delete --noteId=...`
    （`create` 可用 pipe：`cat file.md | hackmd-cli notes create`）
  - 匯出：`hackmd-cli export --noteId=<id>`
  - 資料夾：`hackmd-cli folders` / `folders create` / `folders update` / `folders delete` / `folders order`
  - Team 版本：對應指令前綴改 `team-notes` / `team-folders`，需加 `--teamPath=<team>`
  - 其他：`hackmd-cli teams`（列出所屬 team）、`hackmd-cli whoami`、`hackmd-cli history`
- 輸出可加 `--output=json`（或 csv/yaml）方便程式化處理。
- 優先順序：一般操作優先用 `hackmd-cli`（已包好認證與常見指令）；
  CLI 涵蓋不到的需求（更細的查詢、程式化整合）才直接呼叫 HackMD 官方 REST API。
- 官方 REST API：預設 endpoint `https://api.hackmd.io/v1`，token-based 認證（同一組 access token）。
  Developer portal（Swagger 文件、Postman collection、社群 SDK）：
  https://hackmd.io/@hackmd-api/developer-portal

## 中文寫作 skills
- 寫中文長文（文件、部落格、報告）時考慮 `stop-slop-zh-tw`（去 AI 腔）
  與 `write-yaochangyu-style`（使用者文風）。

## 變更紀錄
- 2026-07-04：內網位址、公司專案路徑抽到 `~/.claude/env.md`，本檔改用佔位符（公開 repo 去識別化）。
- 2026-07-14：ctx7/context7 條目加上關係說明與呼叫優先順序（優先用全域 `ctx7`，找不到才 fallback `npx`）。
