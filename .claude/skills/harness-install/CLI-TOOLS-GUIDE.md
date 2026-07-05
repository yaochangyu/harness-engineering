# harness-install 改進：CLI/IDE 工具選擇器

## 新增功能

升級後的 `/harness-install` skill 現在支持用戶在安裝時**選擇要 symlink 的 CLI/IDE 工具**，並顯示每個工具的實際路徑。

## 完整流程

### 步驟 1：互動式工具選擇

當你執行 `/harness-install` 時，系統會自動掃描你的環境，發現已安裝的 CLI 工具，並以互動式菜單讓你選擇：

```
════════════════════════════════════════════
可用的 CLI / IDE 工具
════════════════════════════════════════════

✓ 已安裝：
  1. copilot
     → /home/yao/.nvm/versions/node/v22.20.0/bin/copilot
  2. opencode
     → /home/yao/.nvm/versions/node/v22.20.0/bin/opencode

✗ 未安裝（可自行安裝後重跑安裝程序）：
  - codex
  - antigravity

選擇要 symlink 的工具：
  a = 全部已安裝
  1,2,3,... = 選擇特定工具編號
  (直接按 Enter 略過此步驟)

請輸入選擇: 
```

**選擇方式**：
- `a` → symlink 所有已安裝的工具
- `1,2` → 只 symlink 編號 1、2 的工具
- 按 Enter → 跳過此步驟（只做核心安裝，不 symlink CLI）

### 步驟 2：自動建立 symlink

根據你的選擇，系統會在 `~/.claude/cli/` 目錄建立 symlink：

```bash
[OK] 已建立：~/.claude/cli/copilot → /home/yao/.nvm/versions/node/v22.20.0/bin/copilot
[OK] 已建立：~/.claude/cli/opencode → /home/yao/.nvm/versions/node/v22.20.0/bin/opencode
```

之後可以直接用：
```bash
~/.claude/cli/copilot --help
~/.claude/cli/opencode --help
```

### 步驟 3：其他安裝步驟

後續步驟維持不變：
- 填寫個人環境配置 (`~/.claude/env.md`)
- 跑健康檢查 (`bash claude/check-harness.sh`)

## 工具掃描邏輯

系統自動在以下位置尋找工具：

1. **PATH 環境變數** - 系統 PATH 裡的可執行檔
2. **npm global** - `npm list -g` 安裝的全域套件
   - `@github/copilot` → `copilot`
   - `opencode-ai` 或 `opencode` → `opencode`
   - `codex-cli` 或 `codex` → `codex`
   - `antigravity-cli` 或 `antigravity` → `antigravity`

## 常見使用情境

### 情境 1：只想 symlink copilot
```
請輸入選擇: 1
→ 只會建立 ~/.claude/cli/copilot
```

### 情境 2：想全部安裝
```
請輸入選擇: a
→ 會建立 ~/.claude/cli/copilot, ~/.claude/cli/opencode
```

### 情境 3：想先跳過，以後再加
```
請輸入選擇: (按 Enter)
→ 跳過 CLI symlink，只做核心安裝
之後手動執行：bash ~/projects/harness-engineering/claude/select-cli-tools.sh
```

### 情境 4：安裝了新工具後重跑
```bash
# 安裝新工具後
npm install -g codex-cli
# 重新執行安裝精靈
/harness-install
# 會再次顯示選擇菜單，這次會看到 codex
```

## 技術細節

### 選擇器腳本
- 位置：`claude/select-cli-tools.sh`
- 輸出格式：`tool1=/path/to/tool1,tool2=/path/to/tool2`
- 可獨立執行測試：`bash select-cli-tools.sh`

### 安裝腳本改進
- 支持 `--cli-tools=tool1=/path1,tool2=/path2` 參數
- 冪等（重跑安全）
- 自動驗證路徑存在且可執行

## 回滾

若要移除某個工具的 symlink：
```bash
rm ~/.claude/cli/copilot
# 或整個目錄
rm -rf ~/.claude/cli/
```

若要重新配置：
```bash
bash ~/projects/harness-engineering/claude/install.sh --cli-tools="copilot=/path/to/copilot"
```
