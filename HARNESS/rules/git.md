# Git 規則（commit / MR / 憑證）

## 憑證安全（HTTPS 認證）— 硬規則，違反等於資安事故

適用所有 git HTTPS 主機（GitLab、GitHub 等），不限特定 host。

### 禁止事項
- **禁止**將 token 內嵌在 remote URL（如 `https://oauth2:<token>@host/...`）：
  clone 時用的 URL 會原封不動寫入 `.git/config`，導致 token 明文落地。
- 不要把 `~/.claude/creds/.creds` 複製到 repo、log、聊天紀錄，或用來做其他可分享備份。

### 正確做法
- 一律使用 git credential helper 取得憑證，remote URL 保持乾淨（`https://host/group/repo.git`）。
- credential helper 對應：GitLab 用 `glab auth git-credential`、GitHub 用 `gh auth git-credential`
  （或系統的 credential manager）。
- `~/.claude/creds/` 只放憑證，不放一般筆記或暫存資料；目錄建議權限 `700`，`.creds` 檔案建議權限 `600`。
- helper 回傳的 username 可能為空；若 HTTP Basic 被拒，username 用 `oauth2`，
  token 仍走 helper（勿寫進 URL）。
- 若不得已曾用內嵌 URL，事後立即 `git remote set-url origin <乾淨URL>`，並評估是否輪替該 token。

GitLab 範例（`<GITLAB_HOST>` 填實際位址，見 `~/.claude/env.md`）：
```
git -c "credential.https://<GITLAB_HOST>.helper=!f() { GITLAB_HOST=<GITLAB_HOST> glab auth git-credential \"$@\"; }; f" clone <url> <dir>
```

## gh / glab CLI（GitHub / GitLab 官方指令列工具）

檢查項目：CLI 而已（`gh`、`glab`），無對應 skill；安裝判斷套用 `tools-install-check.md` 的通用流程
（`command -v gh`／`command -v glab` 判斷是否已裝）。

- 用途：開/查 PR・MR、查 issue，以及上方憑證安全段落用到的
  `gh auth git-credential`／`glab auth git-credential` credential helper。
- 認證：`gh auth login`／`glab auth login`（互動式設定），設定完成後才能用上方 credential helper 指令。
- fallback：未安裝時改用 git 原生指令操作，credential helper 段落須改手動設定（不強制要求安裝 gh/glab）。

### 安裝

**GitHub CLI（`gh`）**，官方 apt repo（Debian/Ubuntu）：
```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
  && sudo mkdir -p -m 755 /etc/apt/keyrings \
  && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
  && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && sudo apt update && sudo apt install gh -y
```
macOS：`brew install gh`。

**GitLab CLI（`glab`）**，官方不提供 apt repo；優先用 Homebrew（macOS/Linux 皆可）：
```bash
brew install glab
```
Debian/Ubuntu 無 Homebrew 時，改用社群維護的 WakeMeOps apt repo：
```bash
curl -sSL "https://raw.githubusercontent.com/upciti/wakemeops/main/assets/install_repository" | sudo bash
sudo apt install glab
```

## 發 MR/PR 前：變更影響報告（code-review-graph）

發 MR／PR 前，先用 **code-review-graph** 針對本次變更（相對上次建圖的 diff）產出變更影響（Blast Radius）
報告，確認波及範圍後再送出 MR／PR。

檢查項目：CLI `code-review-graph`（含常駐服務 `crg-daemon`）；MCP server（是否可用視該 session 有沒有列出
`mcp__code-review-graph__*` 系列工具，未列出就改用 CLI）；skill（7 個：`build-graph`／`review-pr`／
`review-changes`／`review-delta`／`debug-issue`／`explore-codebase`／`refactor-safely`，本機有裝時才會列出）。

- 官方 repo／文件：https://github.com/tirth8205/code-review-graph （首頁 https://code-review-graph.com）
- 核心用法：
  - `code-review-graph build`：首次對目標 repo 全量建圖（大型 repo 可能要數分鐘）。
  - `code-review-graph update`：只重新解析上次建圖後變更過的檔案，例行維護用。
  - `code-review-graph detect-changes`：唯讀分析目前變更的影響範圍，不重新解析——這是「發 MR/PR 前」
    這個場景的核心指令，直接對應要產出的變更影響報告。
  - `code-review-graph visualize --serve`：啟動本機 Web Server（預設 `http://localhost:8765`）看互動式
    衝擊半徑拓撲圖；大型專案（5,900+ 節點）會自動切換成社群聚合視圖。
  - `crg-daemon start`：多 repo 常駐監看，背景自動增量更新索引，不用手動重跑 `build`。
- 安裝：
```bash
uv tool install code-review-graph   # 或 pip install code-review-graph
code-review-graph install --platform claude-code   # 產出 Claude Code 用的 7 個 skill
```
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例；CLI 用 `command -v code-review-graph`；
  skill 看 `~/.claude/skills/` 底下是否有上列 7 個之一；MCP 工具看該 session 有沒有列出對應工具。
  fallback：未安裝或該 repo 未建圖時，改用 `git diff`／`gh pr diff`／`glab mr diff` 手動看變更範圍，
  並在回覆中註明「code-review-graph 未安裝，已改用 git diff 手動分析」。

## commit message 格式

1. 若沒有 ticket id，詢問使用者是否需要加上 ticket id。
   - 若有 ticket id，最後一行加上 `Bundle: (ticket id)`。
2. 從 `git diff --staged` 產生精簡訊息，格式：
   `[EMOJI] [TYPE](file/topic)(ticket id): [繁中描述]`
   使用 GitMoji（如 ✨ → feat）、現在式、主動語態、每行最多 120 字元、不含 code block。
3. body 使用 markdown 格式。
4. **不可包含 Co-authored-by**。
5. 安裝後由 `commit-msg` hook 再次檢查，不通過就拒絕提交。

## MR description（markdown 格式）

必含：變更的背景與目的、主要的變更內容、相關 ticket id（如果有的話）。

## git worktree 衝突解決

1. 開啟 `git rerere`。
2. 在其中一個 worktree 執行 `git rebase develop` 並手動解衝突。
3. 在其他 worktree 執行 `git rebase develop`，git 會自動套用剛才的解法。
