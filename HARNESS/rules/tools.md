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
