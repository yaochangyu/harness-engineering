# HackMD 詳細使用指南

## 用途
- HackMD（hackmd.io / HackMD EE）的命令行工具，管理筆記、資料夾、team 等。
- 只支援 hackmd.io 官方或 HackMD EE ≥ 1.38.1，不支援 CodiMD。

## 安裝

### 方式選擇
- **優先裝 skill**（觸發層）：告訴 agent 何時該用、怎麼下指令。
- **再裝 CLI**（執行層）：底層實際執行的二進位檔。

### 安裝步驟

1. 檢查是否已安裝：
   ```bash
   test -d ~/.claude/skills/hackmd-cli && echo "skill installed" || echo "skill not installed"
   command -v hackmd-cli >/dev/null 2>&1 && echo "CLI installed" || echo "CLI not installed"
   ```

2. 若未裝 CLI，先安裝：
   ```bash
   npm install -g @hackmd/hackmd-cli
   ```

3. 安裝 skill（**先詢問使用者要全域還是專案**，依回答決定帶不帶 `-g`）：
   ```bash
   npx skills add https://github.com/hackmdio/hackmd-cli -s hackmd-cli [-g] -y -a '*'
   ```

## 認證

### 登入流程
```bash
hackmd-cli login
```
系統會引導開啟瀏覽器授權。

### Token 管理
- **取得方式**：hackmd.io → Setting → API → 建立 Access Token。
- **存放位置**：`~/.claude/creds/.creds`（與其他憑證一致）。
- **使用方式**：指令中用環境變數 `$HMD_API_ACCESS_TOKEN` 帶入。
- **注意**：**不要**寫進 repo 或用 `echo` 印出。

### 自訂 Endpoint（HackMD EE）
- 若使用 HackMD EE（非官方 hackmd.io），API endpoint 存在 `~/.claude/env.md`。
- 環境變數名稱：`$HMD_API_ENDPOINT_URL`。

## 使用 hackmd-cli

具體指令用 `hackmd-cli --help` 或 `hackmd-cli <command> --help` 查詢；支援筆記、資料夾、team、匯出等操作。

## 優先順序

1. **一般操作**：優先用 `hackmd-cli`（已包好認證）。
2. **進階需求**：CLI 涵蓋不到的需求（更細的查詢、程式化整合）才直接呼叫 HackMD 官方 REST API。

## REST API

- **預設 endpoint**：`https://api.hackmd.io/v1`
- **認證**：token-based（同一組 access token）
- **文件**：https://hackmd.io/@hackmd-api/developer-portal（Swagger、Postman collection、社群 SDK）

