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
- 安裝方式：裝成全域 skill `find-docs`，指令
  `npx skills add https://github.com/upstash/context7 -s find-docs -g -y -a '*'`。
  此條目已列在 `$HARNESS_DIR/skills-manifest.txt`（`$HARNESS_DIR` 解析規則見 `CLAUDE.md` 路由表），
  跑 `install-skills.py` 會自動安裝，不需另外手動裝。
- skill 與 CLI 不是二選一：`find-docs` 是觸發層（告訴 agent 何時該查、怎麼下 query），
  底層執行仍是 `npx ctx7@latest library` / `npx ctx7@latest docs` 兩段式查詢。
  所以裝了 skill 之後照 skill 指示走即可，不必再自己組指令；
  skill 不存在時才手動呼叫 `npx ctx7@latest ...`（有全域 `ctx7` 就直接用，省 npx 開銷）。
- 詳細查詢步驟、錯誤處理等規則以 `find-docs` skill 內容為準，不要在別處重複維護。
- 不可因為沒裝就默默跳過 Context7 或改用 web search。
- **使用前判斷是否已安裝**（避免假設一定裝好）：
  1. 先查 skill：`ls ~/.claude/skills/find-docs`（或有裝 OMC plugin 時用 `list_omc_skills`）；
     目錄不存在 → 視為未裝。
  2. 再查全域 CLI：`command -v ctx7`。兩者都查無 → 判定 context7 未安裝。
  3. 未安裝時，告知使用者「context7 尚未安裝」，並提供兩個安裝選項讓使用者選：
     - 跑 `uv run $HARNESS_DIR/install-skills.py`（安裝 manifest 內全部工具，含 find-docs）
     - 只裝這個：`npx skills add https://github.com/upstash/context7 -s find-docs -g -y -a '*'`
     等使用者同意才執行安裝指令；安裝完依 `maintenance-protocol.md` 第 5 節跑一次 `check_harness.py`。
  4. 使用者明確拒絕安裝、或要求先用其他方式時，才能 fallback（例如 web search），
     且必須在回覆中註明「context7 未安裝，已改用替代方式」，不可默默切換。

## ticket 工具
- 所有 ticket 操作用 `<TICKET_CLI>`（實際工具名與使用說明位置見 `~/.claude/env.md`）。

## Google Workspace
- 需要 Gmail / Drive / Calendar 操作時，優先用 googleworkspace cli：
  `https://github.com/googleworkspace/cli`。

## graphify
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

## playwright-cli
- 需要安裝 `playwright-cli` skill 時，使用：`npx skills add https://github.com/microsoft/playwright-cli --skill playwright-cli`
- 安裝後依該 skill 的說明使用，不要自行猜測子指令。

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

## 網頁探索工具選擇（Web Automation Tools）
需要自動化探索網頁時，按優先順序選擇：
1. **agent-browser** — 適合複雜的多步驟網頁互動、表單填寫、深入探索
2. **webwright** — 微軟出品，LLM-powered 瀏覽器 agent 框架，適合高階網頁任務自動化
3. **playwright** — 通用自動化工具，跨平臺，適合快速測試

### 安裝方式（按工具區分，因為涉及不同生態）

#### agent-browser（NPM）
```bash
npm install -g agent-browser
# 或用 npx 直接執行（無需全域安裝）
npx agent-browser --help
```
**特點**: CLI 工具，Vercel 出品；無需編寫程式碼，直接執行命令進行瀏覽器操作（open, click, type, screenshot, eval 等）。
**適用**: 自動化簡單至中等複雜度的網頁任務、互動測試。

#### webwright（Python）
```bash
# 用 uv（推薦，專案已配置）
uv pip install webwright playwright

# 或用系統 pip（需虛擬環境）
python3 -m venv .venv
source .venv/bin/activate
pip install webwright playwright
```
**特點**: Python 框架，微軟出品；LLM 驅動的瀏覽器 agent，以程式碼為中心；支援長地平線 web 任務。
**適用**: 複雜的多步驟 web 自動化、AI 代理開發、需要程式邏輯的網頁任務。
**官方資源**:
- GitHub: https://github.com/microsoft/Webwright
- 文件: https://microsoft.github.io/Webwright
- 部落格: https://www.microsoft.com/en-us/research/articles/webwright-a-terminal-is-all-you-need-for-web-agents/

#### playwright（NPM / Python）
```bash
# Node.js
npm install -D playwright
npx playwright install chromium

# Python（用 uv）
uv pip install playwright

# 或系統 pip
pip install playwright
```
**特點**: 跨平臺、多語言支援（Node.js / Python / .NET）；最廣泛使用的瀏覽器自動化工具。
**適用**: 通用網頁測試、快速原型開發、效能分析。

### 實踐驗證（2026-07-16）
三個工具並行探索 https://www.104.com.tw/ 實驗結果：

#### agent-browser（NPM CLI）
- ✅ 執行成功（2 分鐘完成）
- 方式：Bash 腳本呼叫 CLI 命令（open, screenshot, snapshot, eval）
- 優點：無需編寫程式碼，直接命令操作；支援豐富的互動（drag, upload, keyboard 等）
- 輸出：JavaScript 評估結果、DOM snapshot、截圖

#### webwright（Python 框架）
- ✅ 執行成功（9 分鐘完成，含安裝時間）
- 方式：Python 非同步代碼 + Playwright 後端
- 安裝注意：系統 Python 限制（PEP 668），需 `--break-system-packages`；推薦用虛擬環境隔離
- 官方版本：v0.0.7（GitHub: microsoft/Webwright）
- 優點：LLM-driven，適合複雜多步驟自動化；支援長地平線任務程式碼化

#### playwright（Node.js / Python）
- ✅ 執行成功（9 分鐘完成）
- 方式：Node.js 非同步 API，支援 Chromium / Firefox / WebKit
- 優點：功能完整（效能指標、無障礙樹、多瀏覽器）；文檔和社區最完善
- 輸出：詳細的結構化資訊（meta、主要元素、互動元素、效能計時）

#### 共同發現
- 三個工具都遇到 Cloudflare 驗證頁面（104.com.tw 的反爬蟲機制）
- 並行執行無衝突，各工具結果已分別存放驗證
- 建議：若要突破 Cloudflare，需實現 JavaScript challenge 或使用 API 密鑰

## 變更紀錄
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
