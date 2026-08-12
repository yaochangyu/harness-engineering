# harness-engineering：制度檔案庫

2026-07-03 由 Claude Fable 5 session 建立。目的：把高階模型的判斷力外化成
弱模型（Sonnet 等級）可執行的制度，讓之後每個 session 都因此變強。

入口：本目錄的 `CLAUDE.md`（單一事實來源）。`~/.claude/CLAUDE.md` 是指向它的 symlink，
Claude Code 每個 session 自動載入後，依情境路由到本目錄其他檔案。

## 快速開始（新機器 / 重灌 / clone 下來之後）
在 repo 根目錄開 Claude Code 輸入 `/harness-install`（安裝＋訪談填 env.md＋驗證），或手動：
```bash
git clone <本 repo> fable-harness   # 或直接複製資料夾，位置隨意
cd fable-harness
uv run HARNESS/install.py
```

還沒 clone 也可以直接跑，uv 會自己抓腳本：
```bash
uv run https://raw.githubusercontent.com/yaochangyu/harness-engineering/main/HARNESS/install.py
```
預設會把官方 repo（`yaochangyu/harness-engineering`）clone 到目前目錄下的 `harness-engineering`，
再對該份執行安裝；要換來源或落點就加 `--repo` / `--target`。已經有本機 repo 的人維持上面的做法即可。
`install.py` 會自動：運行 AI CLI 工具選擇器、偵測 repo 實際位置並改寫 CLAUDE.md 的 HARNESS 路徑（位置變了才改）、
備份既有的 `~/.claude/CLAUDE.md`（若有）、建立 symlink、
`~/.claude/env.md` 不存在時從 `env.example.md` 複製一份、跑一次健康檢查。冪等，重跑安全。

**公開 repo 紅線**：內網位址、公司專案、憑證相關資訊一律只寫 `~/.claude/env.md`（不進版控），
制度檔內用 `<GITLAB_HOST>`、`<TICKET_CLI>`、`<WIKI_ROOT>` 這類佔位符。

手動等效步驟（symlink 不可用的環境才需要）：
1. 改 `CLAUDE.md` 開頭那行 HARNESS 路徑定義為實際位置。
2. `ln -sf {實際位置}/CLAUDE.md ~/.claude/CLAUDE.md`（或退而求其次 cp，但要記住 repo 是正本）。
3. 驗證：`uv run HARNESS/check_harness.py` 全綠即完成。

| 檔案 | 內容 | 誰讀、何時讀 |
|---|---|---|
| CLAUDE.md | 入口：核心規則＋路由表（symlink 目標） | 每個 session 自動載入 |
| diagnosis.md | harness 三大問題診斷＋修法（含待使用者決定事項） | 使用者；未來 session 想懂「為什麼這樣設計」時 |
| model-dispatch.md | 派工紀律：指揮官不下場、三件套、回報合約、升降級、驗證不自驗 | 主模型，派 subagent 前 |
| judgment-rubrics.md | 五套判準（升級/完成/該問/換路/品質底線），各附正反例 | 主模型，拿不定主意時 |
| delegation-templates.md | 五種任務的派工 prompt 模板（搜尋/實作/重構/研究/審查） | 主模型，寫派工 prompt 時 |
| maintenance-protocol.md | 制度檔的修改權限分級、備份、教訓格式、精簡門檻 | 任何要改制度檔的 session |
| letter-to-future-sessions.md | 環境三要事、制度退化模式與預防、交接狀態 | 新 session 第一次接手時 |
| rules/git.md | commit/MR/憑證安全/worktree | 做 git 操作時 |
| rules/workflow.md | plan.md/.issues/tree.md 流程＋觸發條件 | 多步驟實作時 |
| rules/mattpocock-workflow.md | 高階軟體工程實作工作流（Grilling/Spec/TDD/CodeReview/plan.md） | 多模組重構或使用者要求進階工作流時 |
| rules/dotnet.md | .NET/Cucumber 開發原則 | .NET 專案 |
| rules/python.md | Python 開發原則（虛擬環境用 uv） | 使用 Python 開發 / 寫腳本 |
| rules/tools.md | rtk/ctx7/ticket CLI/Workspace/graphify/LLM wiki/寫作 skills | 用到對應工具時 |
| rules/web-automation.md | 網頁自動化探索三工具（agent-browser/webwright/playwright）選擇、安裝、實踐驗證 | 需要自動化探索或操作網頁時 |
| rules/tools-install-check.md | 工具安裝前判斷通用慣例（4 步驟：查 skill/查 CLI/引導安裝/fallback），供 rules/tools.md 各章節引用 | rules/tools.md 內任何工具的「使用前判斷是否已安裝」步驟 |
| rules/preprocess.md | 文件 / PDF / Office / 圖片分析前處理（markitdown） | 任何文件型輸入進 AI 分析前 |
| env.example.md | 個人環境配置範本（實際值填在 `~/.claude/env.md`，不進版控） | 新機器安裝後填一次 |
| select-cli-tools.py | 互動式 AI CLI 工具選擇器（Python，跨平台） | install.py 自動執行 |
| skills-manifest.txt | 全域通用工具類 skills 安裝清單（`repo,skill`，一行一條） | install-skills.py 讀取通用工具清單 |
| skills-manifest-workflow.txt | 全域開發工作流程類 skills 安裝清單（`repo,skill`，一行一條） | install-skills.py 讀取工作流清單 |
| install-skills.py | 讀取通用與工作流清單，供使用者選取後跑 `npx skills add ... -g -y -a '*'` 逐條安裝到全域 | install.py 自動執行 |
| install.py | 安裝：運行 Python 選擇器、偵測位置、改路由路徑、建立與關聯 AI Agent symlink (CLAUDE/GEMINI/COPILOT)、建 env.md、詢問並安裝全域 skills、跑檢查 | clone/搬移後跑一次 |
| check_harness.py | 健康檢查：symlink、汙染、新增自動載入檔、缺檔 | 安裝任何 Claude 相關工具後跑一次 |
| uninstall.py | 解除安裝：移除 symlink、還原備份 | 不需要 harness 時執行 |
| backup/ | 舊版 CLAUDE.md 等備份，**不可刪**；已從版控排除（.gitignore） | 需要還原時 |

搬移本目錄時：只需更新 `~/.claude/CLAUDE.md`、`~/.gemini/GEMINI.md` 或 `~/.copilot/copilot-instructions.md` 等開合的 HARNESS 路徑定義。
還原舊制度：`ln -sf /mnt/d/lab/github-copilot/.github/copilot-instructions.md ~/.claude/CLAUDE.md`，其餘 Agent 亦同理。

## 變更紀錄
- 2026-08-11：快速開始補上「免 clone」入口，改用 uv 直接跑 raw GitHub 上的 `install.py`，
  並說明預設 repo 與落點、`--repo` / `--target` 覆寫方式。
