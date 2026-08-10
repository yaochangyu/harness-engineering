# 網頁探索工具選擇（Web Automation Tools）

需要自動化探索網頁時，按優先順序選擇：
1. **agent-browser** — 適合複雜的多步驟網頁互動、表單填寫、深入探索
2. **webwright** — 微軟出品，LLM-powered 瀏覽器 agent 框架，適合高階網頁任務自動化
3. **playwright** — 通用自動化工具，跨平臺，適合快速測試

`playwright-cli` skill（錄製產生程式碼、檢查 selector）另見 `rules/tools.md`。

## 使用前判斷是否已安裝（三工具共用 `tools-install-check.md` 通用慣例）
- agent-browser：`command -v agent-browser`（或 `npx agent-browser --version`）
- webwright：`python3 -c "import webwright"`（或檢查對應虛擬環境是否已裝）
- playwright：`command -v playwright`（或 `npx playwright --version`）
fallback：拒絕安裝目前優先序的工具時，才能改選下一順位的替代工具。

## 安裝方式（按工具區分，因為涉及不同生態）

### agent-browser（NPM）
檢查項目：skill `agent-browser`；CLI `agent-browser`。
官方 repo：https://github.com/vercel-labs/agent-browser
```bash
npm install -g agent-browser
agent-browser install    # 首次使用才需要：下載 Chrome for Testing
# 或用 npx 直接執行（無需全域安裝）
npx agent-browser --help
```
skill 安裝：`npx skills add https://github.com/vercel-labs/agent-browser -s agent-browser [-g] -y -a '*'`
（**安裝前先問使用者裝全域還是專案**，依回答決定帶不帶 `-g`，不要自行預設；
已查證 repo 有 `skills/agent-browser/SKILL.md`）。
**特點**: CLI 工具，Vercel 出品；無需編寫程式碼，直接執行命令進行瀏覽器操作（open, click, type, screenshot, eval 等）。
**適用**: 自動化簡單至中等複雜度的網頁任務、互動測試。

### webwright（Python）
檢查項目：skill `webwright`；CLI 無（只走 Python 套件 / skill）。
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

### playwright（NPM / Python）
檢查項目：skill `playwright-cli`；CLI `playwright-cli`。
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

## 實踐驗證（2026-07-16）
三個工具並行探索 https://www.104.com.tw/ 實驗結果：

### agent-browser（NPM CLI）
- ✅ 執行成功（2 分鐘完成）
- 方式：Bash 腳本呼叫 CLI 命令（open, screenshot, snapshot, eval）
- 優點：無需編寫程式碼，直接命令操作；支援豐富的互動（drag, upload, keyboard 等）
- 輸出：JavaScript 評估結果、DOM snapshot、截圖

### webwright（Python 框架）
- ✅ 執行成功（9 分鐘完成，含安裝時間）
- 方式：Python 非同步代碼 + Playwright 後端
- 安裝注意：系統 Python 限制（PEP 668），需 `--break-system-packages`；推薦用虛擬環境隔離
- 官方版本：v0.0.7（GitHub: microsoft/Webwright）
- 優點：LLM-driven，適合複雜多步驟自動化；支援長地平線任務程式碼化

### playwright（Node.js / Python）
- ✅ 執行成功（9 分鐘完成）
- 方式：Node.js 非同步 API，支援 Chromium / Firefox / WebKit
- 優點：功能完整（效能指標、無障礙樹、多瀏覽器）；文檔和社區最完善
- 輸出：詳細的結構化資訊（meta、主要元素、互動元素、效能計時）

### 共同發現
- 三個工具都遇到 Cloudflare 驗證頁面（104.com.tw 的反爬蟲機制）
- 並行執行無衝突，各工具結果已分別存放驗證
- 建議：若要突破 Cloudflare，需實現 JavaScript challenge 或使用 API 密鑰

## 變更紀錄
- 2026-08-10：各工具章節補上「檢查項目」標頭，明確標示 skill / CLI 是否存在；
  目的是讓 `tools-install-check.md` 先看章節宣告再決定查哪一項（使用者已確認此修改）。
- 2026-08-10：自 `rules/tools.md` 整章搬出（原檔 249/250 行、逼近精簡門檻，且本主題與
  「工具設定」性質不同，獨立成檔後兩邊都有擴充空間），同步在 `CLAUDE.md` 路由表加一行
  （使用者已確認此搬檔方案）。搬移時未改動原文，僅標題層級上提一級。
- 2026-08-10：agent-browser 補官方 repo 連結、`agent-browser install`（首次下載 Chrome for
  Testing，查證自官方 README）與 skill 安裝指令；`-g` 標為可選並要求安裝前先問使用者範圍
  （使用者提供指令與要求）。
