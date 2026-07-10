# AI 代理指令檔完整位置對應表

基於實際檢查結果和 PowerShell 腳本配置。

## 已確認的文件位置

### 源檔位置（Repo 層）

| AI 代理 | 源檔位置 | 大小 | 描述 |
|--------|--------|------|------|
| **Copilot** | `/mnt/d/lab/github-copilot/.github/copilot-instructions.md` | 10.1K | GitHub Copilot 主要指令檔 |
| **Copilot (舊版)** | `/mnt/d/lab/github-copilot/.github/copilot-instructions-old.md` | 5.6K | 備份/舊版本 |
| **通用準則** | `/mnt/d/lab/github-copilot/.github/通用準則.md` | 1.0K | 共用指導原則 |
| **Claude** | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` | 主入口 | harness 制度檔 |

### Windows 用戶家目錄映射（由 link-ai-instructions.ps1 建立）

| AI 代理 | 位置 | 指向 | 類型 |
|--------|------|------|------|
| **Copilot** | `%USERPROFILE%\.github\copilot-instructions.md` | `/mnt/d/lab/github-copilot/.github/copilot-instructions.md` | Hard Link / SymLink |
| **Copilot** | `%USERPROFILE%\.copilot\copilot-instructions.md` | `/mnt/d/lab/github-copilot/.github/copilot-instructions.md` | Hard Link / SymLink |
| **Claude** | `%USERPROFILE%\.claude\CLAUDE.md` | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` | SymLink (WSL path) |
| **Gemini / Antigravity** | `%USERPROFILE%\.gemini\GEMINI.md` | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` (WSL) | SymLink |

### WSL/Linux 用戶家目錄映射（由 install.py 建立）

| AI 代理 | 位置 | 指向 | 類型 | 狀態 |
|--------|------|------|------|------|
| **Copilot** | `~/.github/copilot-instructions.md` | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` | SymLink | ✅ 已建立 |
| **Copilot** | `~/.copilot/copilot-instructions.md` | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` | SymLink | ✅ 已建立 |
| **Claude** | `~/.claude/CLAUDE.md` | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` | SymLink | ✅ 已建立 |
| **Gemini / Antigravity** | `~/.gemini/GEMINI.md` | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` | SymLink | ✅ 已建立 |
| **Hermes** | `~/.hermes/SOUL.md` | ⚠️ 源檔未找到 | SymLink | ❌ 待建立 |

## harness-engineering 完整結構

```
/home/yao/projects/harness-engineering/
├── claude/
│   ├── CLAUDE.md                          # ← Claude 主指令檔（symlink 目標）
│   ├── diagnosis.md                       # 問題診斷
│   ├── model-dispatch.md                  # 派工紀律
│   ├── judgment-rubrics.md                # 判準表
│   ├── delegation-templates.md            # 派工範本
│   ├── maintenance-protocol.md            # 維護協議
│   ├── letter-to-future-sessions.md       # 未來 session 說明
│   ├── env.example.md                     # 環境配置範本
│   ├── install.py                        # 安裝腳本
│   ├── check_harness.py                  # 健康檢查
│   ├── uninstall.py                      # 解除安裝
│   ├── select-cli-tools.py                # CLI 工具選擇器
│   ├── backup/                            # 備份目錄
│   └── rules/
│       ├── git.md                         # Git 操作規則
│       ├── workflow.md                    # 工作流程
│       ├── dotnet.md                      # .NET 開發
│       ├── tools.md                       # 工具使用
│       └── context7.md                    # Context7 配置
├── .claude/
│   └── skills/
│       └── harness-install/
│           ├── SKILL.md                   # Skill 定義
│           └── CLI-TOOLS-GUIDE.md         # 使用指南
└── README.md                              # 專案說明

↓ Symlink 到

~/.claude/
├── CLAUDE.md → /home/yao/projects/harness-engineering/claude/CLAUDE.md
├── cli/
│   ├── claude → /home/yao/.local/bin/claude
│   ├── codex → /home/yao/.nvm/versions/.../bin/codex
│   ├── copilot → /home/yao/.nvm/versions/.../bin/copilot
│   ├── gemini → /home/yao/.nvm/versions/.../bin/gemini
│   ├── hermes → /home/yao/.local/bin/hermes
│   └── opencode → /home/yao/.nvm/versions/.../bin/opencode
└── ...（其他目錄）
```

## GitHub Copilot 完整結構

```
/mnt/d/lab/github-copilot/.github/
├── copilot-instructions.md                # ← 主指令檔（10.1K）
├── copilot-instructions-old.md            # 舊版備份
├── 通用準則.md                             # 共用指導原則
├── link-ai-instructions.ps1               # ← Windows/WSL 指令檔 symlink 建立腳本
├── link-ai-agents.ps1                     # agents 同步腳本
├── unlink-ai-agents.ps1                   # 移除 agents
├── sync-ai-agents.ps1                     # 同步 agents
├── sync-editorconfig.ps1                  # 同步 editorconfig
├── README.md                              # PowerShell 腳本說明
├── mcp-config.json                        # MCP 配置
├── .editorconfig                          # 編輯器配置
├── agents/                                # Agent 定義檔
├── prompts/                               # 提示詞範本
└── skills/                                # Skill 定義檔
```

## 快速查詢表

### 查詢場景 1：「我要編輯 Copilot 的指令」

| 平台 | 編輯位置 | 實際指向 |
|-----|--------|--------|
| Windows | `%USERPROFILE%\.copilot\copilot-instructions.md` | `/mnt/d/lab/github-copilot/.github/copilot-instructions.md` |
| WSL/Linux | `~/.copilot/copilot-instructions.md` | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` |
| 源檔位置 | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` | ← 直接編輯這個（Windows 下為 `/mnt/d/...`） |

### 查詢場景 2：「我要編輯 Claude 的制度檔」

| 平台 | 編輯位置 | 實際指向 |
|-----|--------|--------|
| Windows | `%USERPROFILE%\.claude\CLAUDE.md` | → WSL path |
| WSL/Linux | `~/.claude/CLAUDE.md` | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` |
| 源檔位置 | `/home/yao/projects/harness-engineering/claude/CLAUDE.md` | ← 直接編輯這個 |

### 查詢場景 3：「我要用某個 AI CLI 工具」

| 工具 | 位置 |
|-----|-----|
| Copilot CLI | `~/.claude/cli/copilot` |
| OpenCode CLI | `~/.claude/cli/opencode` |
| Codex CLI | `~/.claude/cli/codex` |
| Gemini CLI | `~/.claude/cli/gemini` |
| Hermes CLI | `~/.claude/cli/hermes` |
| Claude CLI | `~/.claude/cli/claude` |

## 待建立/確認的項目 ⚠️

### 1. Gemini 指令檔

**現狀**：
- Windows 期望位置：`%USERPROFILE%\.gemini\GEMINI.md`
- WSL 期望位置：`~/.gemini/GEMINI.md`
- 源檔位置：已連結至此 repo 的 `claude/CLAUDE.md`

**需要**：
- [x] 找到或建立 Gemini 指令檔源 (已完成，與 Claude Code 共用 `CLAUDE.md`)
- [ ] 重新執行 link-ai-instructions.ps1 建立 Windows 端的 symlink

### 2. Hermes 指令檔

**現狀**：
- WSL 期望位置：`~/.hermes/SOUL.md`
- 源檔位置：**未找到**

**需要**：
- [ ] 找到或建立 Hermes 指令檔源
- [ ] 確認應放在哪個 repo
- [ ] 重新執行 link-ai-instructions.ps1 建立 symlink

### 3. 其他 AI 代理指令檔

目前環境中還有：
- Codex CLI ✅ （已在 `~/.claude/cli/`）
- Antigravity CLI ✅ （已與 Gemini 共用 `~/.gemini/GEMINI.md` 連結至 `CLAUDE.md`）
