# 工具細則（需要用到該工具時才讀）

## RTK（Rust Token Killer）
- `settings.json` 已設 PreToolUse hook `rtk hook claude`，Bash 指令會被自動處理；
  平常**不需要**手動背指令對照表。
- 原則：shell 指令加 `rtk` 前綴可省 60–90% token，無對應 filter 時原樣通過，永遠安全。
- 指令串接時每段都加前綴：`rtk git add . && rtk git commit -m "msg"`。
- 除錯時（需要看完整輸出）用原始指令，不加 rtk。
- `rtk proxy <cmd>`：不過濾但記錄用量。

## ctx7 / context7（查函式庫文件）
檢查項目：skill `find-docs`；CLI `ctx7`。
- 官方文件／repo：https://github.com/upstash/context7（`ctx7` 是其官方 CLI，兩個名字指同一個工具）。
- 安裝方式：裝成 skill `find-docs`，指令
  `npx skills add https://github.com/upstash/context7 -s find-docs [-g] -y -a '*'`。
  此條目已列在 `$HARNESS_DIR/skills-manifest.txt`（`$HARNESS_DIR` 解析規則見 `CLAUDE.md` 路由表），
  跑 `install-skills.py` 會自動安裝，不需另外手動裝。
- skill 與 CLI 不是二選一：`find-docs` 是觸發層（告訴 agent 何時該查、怎麼下 query），
  底層執行仍是 `npx ctx7@latest library` / `npx ctx7@latest docs` 兩段式查詢。
  所以裝了 skill 之後照 skill 指示走即可，不必再自己組指令；
  skill 不存在時才手動呼叫 `npx ctx7@latest ...`（有全域 `ctx7` 就直接用，省 npx 開銷）。
- 詳細查詢步驟、錯誤處理等規則以 `find-docs` skill 內容為準，不要在別處重複維護。
- 不可因為沒裝就默默跳過 Context7 或改用 web search。
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例；skill 目錄 `find-docs`
  （或有裝 OMC plugin 時可用 `list_omc_skills` 代替），全域 CLI `ctx7`；
  安裝指令二選一：`uv run $HARNESS_DIR/install-skills.py`（裝 manifest 全部工具）或上方 `npx skills add`；
  安裝完依 `maintenance-protocol.md` 第 5 節跑一次 `check_harness.py`；fallback 為 web search。

## ticket 工具
- 所有 ticket 操作用 `<TICKET_CLI>`（實際工具名與使用說明位置見 `~/.claude/env.md`）。

## Google Workspace
檢查項目：skill 視服務而定（如 `gws-gmail`）；CLI `gws`。
- 需要 Gmail / Drive / Calendar / Slides / Sheets / Docs 等操作時，優先用 googleworkspace cli
  （指令名稱 `gws`）：https://github.com/googleworkspace/cli。
- CLI 安裝：`npm install -g @googleworkspace/cli`（或抓 GitHub Releases 的預編譯二進位檔）。
- **常用快速路徑**（Gmail/Slides/Sheets/Docs，已查證這四個 skill 存在，不用現查）：
  `npx skills add https://github.com/googleworkspace/cli -s gws-gmail gws-slides gws-sheets gws-docs [-g] -y -a '*'`。
- **其他服務走動態查詢，不要憑記憶猜 skill 名稱**：該 repo 有 90+ 個 skill（Drive/Calendar/Chat/Forms/
  Admin…），本檔不逐一列舉（會過期）。命名慣例固定是 `gws-<服務>`；不確定時先跑
  `npx skills add https://github.com/googleworkspace/cli --list`（非互動，印出目前完整清單＋一行說明），
  依使用者需求關鍵字比對找出候選 skill，列給使用者確認要裝哪個，取得同意才裝。
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例；skill 目錄視所需服務而定
  （如 Gmail 查 `~/.claude/skills/gws-gmail`），全域 CLI `gws`；未裝時提示上方對應安裝指令
  （常用四個直接裝，其他先 `--list` 查再裝）；fallback 為 Gmail/Drive/Calendar 的 MCP 工具。

## graphify
檢查項目：skill `graphify`；CLI `graphify`。
- 使用者輸入 `/graphify` 時，先呼叫 Skill tool（`skill: "graphify"`）再做其他事。
- Skill 位置：`~/.claude/skills/graphify/SKILL.md`。
- 官方 repo：https://github.com/Graphify-Labs/graphify
  **注意套件名稱**：PyPI 上是 `graphifyy`（雙 y），不是 `graphify`；其他 `graphify*` 套件非官方。
  安裝完後終端機指令仍是 `graphify`。
- 安裝（新環境沒有這個 skill 時）：
  ```bash
  uv tool install graphifyy      # 推薦；替代方案 pipx install graphifyy
  graphify install               # 註冊為全域 skill（僅當前 repo 用 --project）
  ```
  - Mac/Windows 避免直接 `pip install graphifyy`：安裝路徑常跟 skill 執行時解析的 Python 環境不一致，
    會導致 `ModuleNotFoundError`。
  - 免安裝直接跑：`uvx --from graphifyy graphify install`
    （不可直接 `uvx graphify ...`——`uv tool run` 會把第一個字當套件名找，套件實際叫 `graphifyy`）。
  - 額外功能（PDF / MCP server / Neo4j 等）：`uv tool install "graphifyy[pdf]"` / `"[mcp]"` / `"[all]"`。
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例；skill 目錄／CLI 皆是 `graphify`；
  fallback 為停用 graphify 相關操作。

## playwright-cli
- 官方文件：https://github.com/microsoft/playwright-cli
  （錄製並產生 Playwright 程式碼、檢查 selector、截圖）。
- 安裝：`npx skills add https://github.com/microsoft/playwright-cli -s playwright-cli [-g] -y -a '*'`
  （**安裝前先問使用者裝全域還是專案**，依回答決定帶不帶 `-g`，不要自行預設；已查證 repo 有 `skills/playwright-cli/SKILL.md`）。
- 安裝後依該 skill 的說明使用，不要自行猜測子指令。
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例（含「先問全域還是專案」步驟）；
  skill 目錄 `playwright-cli`；fallback 為 `web-automation.md` 的其他網頁自動化工具。

## LLM Wiki
- 知識庫路徑 `<WIKI_ROOT>` 見 `~/.claude/env.md`；操作規則見 `<WIKI_ROOT>/CLAUDE.md`。
- Ingest 程式碼時直接從原始路徑讀取，不複製到 `sources/`；
  `sources/` 只放外部資料（文章、論文、技術文件等沒有 repo 的資料）。
- wiki 頁面 frontmatter 的 `sources` 欄位，程式碼引用用絕對路徑
  （如 `/path/to/project/src/...`）。
- 使用者要求歸檔到 wiki：資料放 `<WIKI_ROOT>/wiki/raw/{歸檔}.md`，
  然後詢問是否需要 ingest 到 wiki。

## HackMD（hackmd-cli）
檢查項目：skill `hackmd-cli`；CLI `hackmd-cli`。
- 官方文件：https://github.com/hackmdio/hackmd-cli（只支援 hackmd.io 官方或 HackMD EE ≥ 1.38.1，不支援 CodiMD）。
- 安裝方式：優先裝成 skill（觸發層，告訴 agent 何時該用、怎麼下指令），指令
  `npx skills add https://github.com/hackmdio/hackmd-cli -s hackmd-cli [-g] -y -a '*'`
  （已查證該 repo 目前只有一個 skill，名稱就是 `hackmd-cli`，`-l/--list` 可自行複查）。
  底層執行仍需要 `hackmd-cli` 這支二進位檔：`npm install -g @hackmd/hackmd-cli`（查證自官方 README）。
  只有在偵測不到 `hackmd-cli` 時，才先提醒使用者補裝 CLI，再繼續詢問是否要安裝對應 skill。
- skill 安裝指令也可直接寫成使用者指定的基底：`npx skills add https://github.com/hackmdio/hackmd-cli -s hackmd-cli`
  （是否加 `-g` 依使用者回答決定）。
- 安裝範圍（全域 vs 專案）：`npx skills add` 的 `-g/--global` 決定 skill 裝在使用者層級還是目前專案
  （不加 `-g` 預設裝專案層級）。
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例（含「先問全域還是專案」步驟）；
  skill 目錄 `hackmd-cli`，全域 CLI `hackmd-cli`；fallback 為官方 REST API 直接呼叫。
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

## Gemini Notebook / NotebookLM
檢查項目：skill `notebooklm`（teng-lin）／`nlm-skill`（jacob-bd）；CLI `notebooklm` ／ `nlm`。
- 同一個 Google 服務有**兩套獨立 client**，都是逆向私有 `batchexecute` API（Google 改端點就會壞）、
  皆 MIT。CLI 名（`notebooklm` vs `nlm`）與 skill 名（`notebooklm` vs `nlm-skill`）都不衝突，**可並存**。
- 兩者核心操作都走 HTTP，**平常不開瀏覽器**；瀏覽器只在取得／續期憑證時出現。
- **選哪個：一律優先 `nlm`（jacob-bd）**，只有 `nlm` 做不到時才換 `notebooklm`（teng-lin）。
  已查證的換手條件（成立才換）：
  - 要在 Python 程式裡直接呼叫：`nlm` 只有 CLI／MCP，`services/` 是內部實作無公開契約；
    `notebooklm` 有 async `NotebookLMClient`，且受公開 API 相容性閘門保護。
  - 要完全免瀏覽器的長期認證：`nlm` 的 cookie 約 2–4 週到期就得重跑需要 Chrome 的 `nlm login`；
    `notebooklm` 的 `[headless]` extra 可用 master token 免瀏覽器續期，適合 CI／無顯示主機／cron。
  - `nlm` 缺該功能、指令失敗、或端點壞掉時的臨時替代。
  換手前先講明是上列哪一項成立，不可默默改用另一個 client（同 `tools-install-check.md` 第 4 步）。
- **teng-lin/notebooklm-py**
  - repo：`https://github.com/teng-lin/notebooklm-py`
  - docs：`https://github.com/teng-lin/notebooklm-py/blob/main/docs/installation.md`
  - CLI：`uv tool install "notebooklm-py[browser]"`（或 `pipx install "notebooklm-py[browser]"`；PyPI 套件 `notebooklm-py`，指令 `notebooklm`）。
    `[browser]` 只供互動式 `notebooklm login` 用；`[cookies]`(rookiepy) 在 Python 3.13+ 裝不起來，跳過即可。
  - skill：`notebooklm skill install --scope user|project --target claude|agents|all`
    （**先問使用者 scope**）；或 `npx skills add teng-lin/notebooklm-py`。
  - 認證：`notebooklm login`，驗證要用 `notebooklm auth check --test --json`
    （少了 `--test` 只驗憑證檔能不能解析，過期 cookie 一樣回 ok，是誤判陷阱）。
    免瀏覽器路徑：`login --browser-cookies <browser>`／`NOTEBOOKLM_AUTH_JSON`／`[headless]` extra 的 master token。
- **jacob-bd/gemini-notebook-mcp-cli**
  - repo：`https://github.com/jacob-bd/gemini-notebook-mcp-cli`
  - CLI：`uv tool install notebooklm-mcp-cli`（**PyPI 套件名 ≠ repo 名**，指令 `nlm`）。
    裝之前先移除 legacy 套件：`uv tool uninstall notebooklm-cli` 與 `notebooklm-mcp-server`。
  - skill：`nlm skill install <tool> [--level user|project]`（**先問使用者 level**）；
    tool 可為 `claude-code`／`cursor`／`agents`／`opencode`／`antigravity`／`hermes`／`other`。
  - MCP 接線：`nlm setup add opencode`（另支援 claude-code／claude-desktop／gemini／cursor／
    github-copilot／windsurf／cline／codex／antigravity）。
  - 認證：`nlm login`（CDP 驅動系統既有 Chrome，不必另裝 chromium）；cookie 約 2–4 週過期需重登。
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例（含「先問全域還是專案」步驟——
  兩者的 `--scope`／`--level` 參數即對應）；fallback 為 NotebookLM 官方 web UI。

## CodeGraph
檢查項目：skill（在 `.claude/skills/` 底下）；CLI `codegraph`。
- 官方文件：https://github.com/colbymchenry/codegraph
- 用途：為 Claude Code / Cursor / Gemini 等 AI 代碼編輯器建立預先索引的代碼知識圖（語義代碼智能），
  自動同步程式碼異動、100% 本地運行、無需外部 API。
- CLI 安裝方式：`npm install -g @colbymchenry/codegraph`。
- skill 安裝（如需要）：檢查 repo `.claude/skills/` 目錄中 SKILL.md；若有對應 Claude Code skill，
  依該檔指示安裝。查證自官方 repo 後補入具體 skill 安裝指令。
- 使用步驟（CLI）：
  1. 安裝 CLI 後運行 `codegraph install` 配置代理。
  2. 在專案目錄執行 `codegraph init` 建立索引。
  3. 按 CLI 提示完成設定。
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例；CLI `codegraph`；
  若無裝 CLI 則提示 `npm install -g @colbymchenry/codegraph`；若有 skill 則檢查 `~/.claude/skills/`
  對應目錄；fallback 為使用 `codegraph_explore` MCP 工具（已系統內建）。

## OneDrive
檢查項目：skill `onedrive`；CLI 無。
- repo：https://github.com/membranedev/application-skills
- docs：https://github.com/membranedev/application-skills/blob/main/skills/onedrive/SKILL.md
- skill：`npx skills add https://github.com/membranedev/application-skills -s onedrive [-g] -y -a '*'`
  （**先問使用者要裝全域還是專案**，依回答決定帶不帶 `-g`；OneDrive 這條只裝 skill，不另外寫 CLI skill）。
- 需要真正連 OneDrive 做操作時，改用 Membrane CLI（`npm install -g @membranehq/cli@latest`）做通用外部服務連線，
  但這不是 OneDrive skill 本身的專屬 CLI。
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例；skill 目錄 `onedrive`；
  fallback 為 Microsoft Graph API 或請使用者提供可用 connection。

## 中文寫作 skills
檢查項目：skill `stop-slop-zh-tw`；CLI 無。
- 寫中文長文（文件、部落格、報告）時考慮 `stop-slop-zh-tw`（去 AI 腔）
  與 `write-yaochangyu-style`（使用者文風）。
- `stop-slop-zh-tw`：來源 repo https://github.com/kevintsengtw/stop-slop-zh-tw，
  安裝 `npx skills add https://github.com/kevintsengtw/stop-slop-zh-tw -s stop-slop-zh-tw [-g] -y -a '*'`。
  **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例；skill 目錄 `stop-slop-zh-tw`；
  fallback 為略過去 AI 腔處理。
- `write-yaochangyu-style`：無公開 repo，本檔不記錄安裝方式；只能檢查
  `ls ~/.claude/skills/write-yaochangyu-style` 是否存在，找不到就告知使用者本檔沒有安裝資訊可引導。

## 變更紀錄
- 2026-08-14：新增 codegraph 條目（全域 CLI 安裝 `npm install -g @colbymchenry/codegraph`；
  建立預先索引代碼知識圖供 Claude Code / Cursor / Gemini 等 AI 編輯器使用；
  含使用步驟與 fallback 方案），對應用戶要求全域安裝需求。
- 2026-08-10：ctx7 / Google Workspace / graphify / HackMD / stop-slop-zh-tw 章節補上「檢查項目」標頭，
  明確標示 skill / CLI 是否存在；目的是讓 `tools-install-check.md` 先看章節宣告再決定查哪一項
  （使用者已確認此修改）。
- 2026-07-04：內網位址、公司專案路徑抽到 `~/.claude/env.md`，本檔改用佔位符（公開 repo 去識別化）。
- 2026-07-14：ctx7/context7 條目加上關係說明與呼叫優先順序（優先用全域 `ctx7`，找不到才 fallback `npx`）。
- 2026-07-15：新增網頁探索工具選擇指南（agent-browser/webwright/playwright）。
- 2026-07-16：
  - 修正 webwright 安裝方式。Webwright 是 Python 框架（不是 npm 套件），應用 `pip install webwright`；agent-browser 是 npm 全域套件；三個工具分屬不同生態，詳細安裝指令已更新。
  - 新增實踐驗證章節：並行探索 104.com.tw，三個工具執行結果對比、安裝注意事項、各自優缺點文檔化。
- 2026-08-09：graphify 章節補上安裝腳本（官方 repo、PyPI 套件名為 `graphifyy` 非 `graphify`、
  `uv tool install` / `uvx` 用法、Mac/Windows 避免直接 `pip install` 的注意事項）。
- 2026-08-09：ctx7/context7 章節改以全域 skill `find-docs` 為主要安裝與使用方式
  （`npx skills add https://github.com/upstash/context7 -s find-docs -g -y -a '*'`，已列在 `skills-manifest.txt`）。
  原因：查證 `find-docs` SKILL.md 後確認它就是 Context7 官方 skill，底層仍呼叫 `ctx7` CLI，
  兩者是同一套機制的觸發層與執行層，不是兩個獨立工具；改寫後避免每次自行組指令、規則也不再兩處維護。
- 2026-08-10：`skills-manifest.txt` 引用改標註為 `$HARNESS_DIR/skills-manifest.txt`，
  對應 `CLAUDE.md` 路由表新增的 HARNESS_DIR 動態解析規則，避免跨工作目錄讀取失敗。
- 2026-08-10：ctx7/context7 章節新增「使用前判斷是否已安裝」步驟（查 skill 目錄／`command -v ctx7`），
  未裝時要引導使用者跑 `install-skills.py` 或單獨安裝指令，取得同意才裝，拒絕才能 fallback 且需註明。
  原因：使用者指出沒跑過 `install-skills.py` 時，這裡沒有具體判斷與引導流程（使用者已確認此修改）。
- 2026-08-10：同一套「使用前判斷是否已安裝」模式套用到 Google Workspace cli（補上指令名稱 `gws`
  與安裝指令，查證自官方 repo README）、graphify、playwright-cli、hackmd-cli（補安裝指令
  `npm install -g @hackmd/hackmd-cli`，查證自官方 repo README）、網頁探索工具三件套
  （agent-browser/webwright/playwright），以及中文寫作 skill `stop-slop-zh-tw`
  （補來源 repo 與安裝指令，使用者提供）。`write-yaochangyu-style` 因無公開 repo、
  ticket 工具因屬內網資訊（見 `~/.claude/env.md`），兩者維持不加安裝引導，避免腦補。
  原因：使用者要求其他工具比照 context7 的判斷+引導安裝流程辦理（使用者已確認此修改）。
- 2026-08-10：Google Workspace 章節補上 Gmail/Slides/Sheets/Docs 對應 skill
  （`gws-gmail`/`gws-slides`/`gws-sheets`/`gws-docs`）與安裝指令
  `npx skills add https://github.com/googleworkspace/cli -s gws-gmail gws-slides gws-sheets gws-docs`
  （使用者提供指令，並已對照官方 `docs/skills.md` 查證四個 skill 皆存在），
  使用前判斷步驟同步擴充為先查對應 skill 目錄、再查 `gws` CLI。
  原因：使用者需要操作 Gmail/Slides/Sheets/Docs，要求未安裝時引導安裝（使用者已確認此修改）。
- 2026-08-10：HackMD 章節安裝方式改以 `npx skills add ... -s hackmd-cli` 裝 skill 為主
  （底層仍需 `npm install -g @hackmd/hackmd-cli`），新增「先問使用者要裝全域還是專案」步驟，
  依回答決定指令帶不帶 `-g`。原因：使用者要求 hackmd-cli 改用 skill 安裝、且讓使用者選安裝範圍
  （使用者已確認此修改）。
- 2026-08-10：精簡＋擴充：
  - 把 6 個工具章節重複的「使用前判斷是否已安裝」4 步驟抽到新檔 `rules/tools-install-check.md`
    （通用慣例），各章節改成一行引用＋列自己的 skill 目錄/CLI/fallback，省下約 14 行空間
    （逼近 250 行精簡門檻，使用者已確認此精簡方案）。
  - Google Workspace 章節新增「常用快速路徑（gws-gmail/slides/sheets/docs 直接裝）
    + 其他服務用 `npx skills add ... --list` 動態查清單再挑選」規則，避免把 90+ 個 skill 寫死在檔案裡
    （使用者已確認此設計）。
- 2026-08-10：playwright-cli 章節補官方 repo 連結與用途，安裝指令由 `--skill playwright-cli` 改為
  `-s playwright-cli [-g] -y -a '*'`（使用者提供）；`-g` 標為可選並要求安裝前先問使用者範圍，
  避免把全域寫死。已查證 repo 有 `skills/playwright-cli/SKILL.md`（使用者已確認此修改）。
- 2026-08-10：「網頁探索工具選擇」整章（agent-browser/webwright/playwright，含實踐驗證）搬到
  新檔 `rules/web-automation.md`，`CLAUDE.md` 路由表同步加一行；本檔 249 → 167 行。
  原因：本檔已達 250 行精簡門檻無法再擴充，且該主題與「工具設定」性質不同
  （使用者已確認此搬檔方案）。
- 2026-08-10：context7 / Google Workspace / HackMD / stop-slop-zh-tw 四條 `npx skills add` 指令的
  `-g` 一律改標 `[-g]`（context7 條目並拿掉「裝成**全域** skill」的預設措辭），語意定義寫在
  `tools-install-check.md` 的 `[-g]` 註記慣例。原因：指令把 `-g` 寫死時 agent 會直接複製執行、
  跳過該檔要求的「先問使用者裝全域還是專案」，規則與範例矛盾（使用者已確認此修改）。
- 2026-08-10：HackMD 章節補上使用者指定的 skill 安裝基底
  `npx skills add https://github.com/hackmdio/hackmd-cli -s hackmd-cli`，並保留 `[-g]`
  作為可選範圍；目的是讓使用者能看見原始安裝路徑，再依回答決定是否加 `-g`（使用者已確認此修改）。
- 2026-08-10：新增「Gemini Notebook / NotebookLM」章節，納入 teng-lin/notebooklm-py 與
  jacob-bd/gemini-notebook-mcp-cli 兩個 client。含選擇判準（MCP／opencode／batch 用 `nlm`，
  Python 嵌入／CI headless 長跑／多帳號用 `notebooklm`，可並存）、各自安裝與認證指令，
  以及三個陷阱：PyPI 套件名 ≠ repo 名、legacy 套件 `notebooklm-cli`/`notebooklm-mcp-server` 要先移除、
  `auth check` 少了 `--test` 會讓過期 cookie 誤判為 ok。所有指令與參數查證自兩 repo 原始碼
  （`cli/skill_cmd.py`、`cli/commands/skill.py`、`cli/commands/setup.py`、`pyproject.toml`），
  非憑記憶或文件片段（使用者要求納入這兩個工具）。
- 2026-08-10：「選哪個」由並列情境判準改為**優先序判準**：一律優先 `nlm`（jacob-bd），
  只有三項換手條件成立才用 `notebooklm`（teng-lin），且換手前要講明原因（使用者指定此優先順序）。
  同時移除原本「多帳號 profile → `notebooklm`」這條——查證後 `nlm` 也支援
  （`nlm login --profile work`，v0.9.8 release 主題即 profile isolation），該判準不成立。
- 2026-08-10：新增 OneDrive 章節，skill 採 `npx skills add ... -s onedrive [-g]` 讓使用者選全域/專案，
  CLI 記為 `@membranehq/cli`／`membrane`，並列出 login、connection ensure、action list 的基本路徑。
  依使用者要求把安裝範圍寫成可選項，讓每次都先問。
