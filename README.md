# harness-engineering

Claude Code 制度檔案庫（harness）。目的：把高階模型的判斷力外化成弱模型（Sonnet 等級）可執行的制度，讓每個 session 都因此變強。2026-07-03 由 Claude Fable 5 session 建立。

## 運作方式

- 制度檔全部放在 [`HARNESS/`](HARNESS/)，入口是 [`HARNESS/CLAUDE.md`](HARNESS/CLAUDE.md)（單一事實來源）。
- 指向此入口的各 AI Agent 提示詞檔案會被自動載入：
  - **Claude Code / OpenCode**：透過 `~/.claude/CLAUDE.md` 軟連結載入。
  - **Antigravity**：透過 `~/.gemini/GEMINI.md` 軟連結載入。
  - **Copilot CLI**：透過 `~/.github/copilot-instructions.md` 與 `~/.copilot/copilot-instructions.md` 軟連結載入。
- 入口採「精簡路由」設計：只保留永遠生效的核心規則與一張路由表，遇到特定情境（派工、git、.NET、多步驟實作……）才讀對應子檔，避免 context 肥大。

## 新增工具時怎麼說

你可以直接這樣說：

> 幫我把 XXX 工具補進 HARNESS，請更新對應章節，並標明 skill / CLI / 安裝指令 / 是否要先問全域或專案。

最理想格式：

```text
新增工具：XXX
來源 repo/文件：...
skill 安裝：...
CLI 安裝：...
是否要問範圍：要 / 不要
fallback：...
要更新的檔案：tools.md / web-automation.md / 其他
```

例如：

```text
新增工具：foo-cli
來源 repo：https://github.com/org/foo-cli
skill 安裝：npx skills add https://github.com/org/foo-cli -s foo-cli
CLI 安裝：npm install -g @org/foo-cli
是否要問範圍：要
fallback：沒有 skill 時改用 CLI
要更新的檔案：HARNESS/rules/tools.md
```

如果你只想我照規則自己判斷，也可以說：

> 幫我新增 XXX 工具，照現有 HARNESS 規則處理。

## 快速開始（新機器 / 重灌 / clone 之後）

最省事的方式：在 repo 目錄開 Claude Code，輸入 `/harness-install`。
安裝精靈（`skills/harness-install/`）會跑安裝腳本、訪談並填好個人環境配置
（`~/.claude/env.md`）、跑健康檢查、最後給你一分鐘導覽。

手動方式：

```bash
git clone <本 repo> fable-harness   # 位置隨意
cd fable-harness
uv run HARNESS/install.py
# 然後編輯 ~/.claude/env.md 填入實際值（範本會自動複製過去）
```

`install.py` 冪等、重跑安全（Python，跨平台），會自動：

1. 運行 AI CLI 工具選擇器，建立選擇之 CLI 工具（如 `opencode`、`antigravity` 等）的 symlink。
2. 將各 AI Agent 的系統提示詞關聯至 [HARNESS/CLAUDE.md](HARNESS/CLAUDE.md)：
   - **Claude Code / OpenCode**：建立 `~/.claude/CLAUDE.md` 軟連結。
   - **Antigravity**：建立 `~/.gemini/GEMINI.md` 軟連結。
   - **Copilot CLI**：建立 `~/.github/copilot-instructions.md` 與 `~/.copilot/copilot-instructions.md` 軟連結。
3. 備份既有的提示詞實體檔案（若存在）。
4. 偵測 repo 實際位置，位置變了就改寫制度檔內的 HARNESS 路徑。
5. 列出全域 skills 安裝清單（`HARNESS/skills-manifest.txt`），詢問是否安裝；同意才逐條安裝到全域。
6. 建立個人環境配置檔 `~/.claude/env.md`（若不存在時從 `env.example.md` 複製）。
7. 跑一次健康檢查。

## 個人配置與公開範圍

本 repo 是公開的，只放**通用制度**。個人與內網資訊分層如下：

| 層 | 位置 | 版控 |
|---|---|---|
| 制度層（派工、判準、模板、流程） | `HARNESS/` | ✅ 公開，內文用 `<GITLAB_HOST>` 等佔位符 |
| 個人環境層（內網位址、公司專案、工具路徑） | `~/.claude/env.md` | ❌ 不進版控 |
| 範本 | `HARNESS/env.example.md` | ✅ 公開 |

紅線：內網位址、公司名稱、憑證相關資訊不可寫進 repo 內任何檔案。

安裝任何 Claude 相關工具或升級 Claude Code 後，跑一次健康檢查確認 harness 仍生效：

```bash
uv run HARNESS/check_harness.py
```

## 目錄結構

```
skills/
├── harness-install/             # Claude Code 專案層級 skill：安裝精靈
│   ├── SKILL.md
│   └── CLI-TOOLS-GUIDE.md
└── mattpocock-workflow/         # 端到端軟體工程工作流 custom skill
    └── SKILL.md

HARNESS/
├── AI-INSTRUCTIONS-MAPPING.md
├── CLAUDE.md                    # 入口：核心規則＋路由表（symlink 目標）
├── README.md
├── check_harness.py             # 健康檢查：symlink、汙染、缺檔（Python）
├── delegation-templates.md      # 五種任務的派工 prompt 模板
├── diagnosis.md                 # harness 三大問題診斷，所有制度檔的設計依據
├── env.example.md               # 個人環境配置範本（實際值填 ~/.claude/env.md，不進版控）
├── install.py                   # 安裝腳本（冪等，Python，跨平台）
├── install-skills.py            # 全域 skills 安裝腳本（讀 skills-manifest*.txt）
├── skills-manifest.txt          # 全域通用工具 skills 安裝清單
├── skills-manifest-workflow.txt # 全域工作流程 skills 安裝清單
├── judgment-rubrics.md          # 五套判準：升級/完成/該問/換路/品質底線
├── letter-to-future-sessions.md # 給未來 session：環境要事與制度退化預防
├── maintenance-protocol.md      # 制度檔修改權限分級、備份、精簡門檻
├── model-dispatch.md            # 派工紀律：指揮官不下場、回報合約、升降級
├── plan-template.md             # 實作計畫範本
├── uninstall.py                 # 解除安裝：移除 symlink、還原備份（Python）
├── select-cli-tools.py          # 互動式 AI CLI 工具選擇器（Python，跨平台）
├── rules/
│   ├── git.md                   # commit / MR / 憑證安全 / worktree
│   ├── workflow.md              # plan.md / .issues / tree.md 流程與觸發條件
│   ├── mattpocock-workflow.md   # 高階軟體工程實作工作流條文（Grilling/Spec/TDD/CodeReview）
│   ├── dotnet.md                # .NET / Cucumber 開發原則
│   ├── python.md                # Python 開發原則（uv）
│   ├── tools.md                 # rtk / ctx7 / ticket CLI / Workspace / 寫作 skills
│   └── omc.md                   # oh-my-claudecode (OMC) 多代理協作層
└── backup/                      # 舊版備份，僅存在本機（.gitignore 排除）
```

各檔案的詳細用途與讀取時機，見 [`HARNESS/README.md`](HARNESS/README.md)。

## 高階工程工作流程與技能安裝 (mattpocock-workflow)

本專案提供整合 **Matt Pocock 技能庫** 與 **Harness 本地規範** 的端到端進階工作流程（含需求磨礪、領域建模、規格拆解、TDD 紅綠切片與雙軸代碼審查）。

### 1. 觸發方式
* 在 AI 對話中下達 **`/mattpocock-workflow`**。
* 或對 AI 說明：「*請進行高階工作流/雙軸審查*」，AI 便會自動路由讀取 [`HARNESS/rules/mattpocock-workflow.md`](HARNESS/rules/mattpocock-workflow.md)。

### 2. 所需子技能之 `npx skills` 安裝方式
當執行高階工作流時，若環境缺乏子技能（`grill-with-docs`, `to-spec`, `to-tickets`, `tdd`, `code-review`, `domain-modeling`, `setup-matt-pocock-skills`），可以使用 `npx skills` 進行安裝：

* **全域安裝 (Global)**：將子技能安裝至全域 (`~/.agents/skills/`)，所有專案皆可調用：
  ```bash
  npx skills add https://github.com/mattpocock/skills -s setup-matt-pocock-skills -s grill-with-docs -s to-spec -s to-tickets -s tdd -s code-review -s domain-modeling -g -y -a '*'
  ```

* **專案本機安裝 (Project)**：僅安裝至當前專案的 `.agents/skills/` 目錄：
  ```bash
  npx skills add https://github.com/mattpocock/skills -s setup-matt-pocock-skills -s grill-with-docs -s to-spec -s to-tickets -s tdd -s code-review -s domain-modeling -y -a '*'
  ```

* **透過 Harness 制度庫自動安裝**：
  若執行 `uv run HARNESS/install-skills.py`，安裝器會自動讀取 [`HARNESS/skills-manifest-workflow.txt`](HARNESS/skills-manifest-workflow.txt) 並提示安裝。

### 3. 技能更新與刪除方式 (Update & Remove)

* **更新技能 (Update)**：更新已安裝之技能至遠端 Git 最新版本
  ```bash
  npx skills update
  ```

* **刪除/解除安裝技能 (Remove)**：
  * **刪除全域技能**：
    ```bash
    npx skills remove <skill_name> -g
    ```
  * **刪除專案本機技能**：
    ```bash
    npx skills remove <skill_name>
    ```

## 維護原則

- 要修改任何制度檔，先讀 `HARNESS/maintenance-protocol.md`。
- `CLAUDE.md` 超過 60 行即為警訊；新規則一律進 `rules/` 子檔並在路由表加一行。
- 搬移 repo 後重跑 `uv run HARNESS/install.py` 即可，路徑會自動改寫。
- 所有腳本均為 Python（`*.py`），支援 Windows/WSL/Linux，無外部依賴。

## 命令行工具

安裝後可直接使用：

```bash
harness-install    # 安裝並配置 harness
harness-check      # 執行健康檢查
harness-uninstall  # 解除安裝
```

## 變更紀錄

- 2026-08-10：新增「新增工具時怎麼說」段落，提供標準提問格式與範例，方便下次直接照格式描述工具補充需求。
