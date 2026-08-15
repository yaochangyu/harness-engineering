# Git 規則（commit / MR / 憑證）

## 憑證安全（HTTPS 認證）— 硬規則，違反等於資安事故
- 適用所有 git HTTPS 主機（GitLab、GitHub 等），不限特定 host。
- **禁止**將 token 內嵌在 remote URL（如 `https://oauth2:<token>@host/...`）：
  clone 時用的 URL 會原封不動寫入 `.git/config`，導致 token 明文落地。
- 一律使用 git credential helper 取得憑證，remote URL 保持乾淨（`https://host/group/repo.git`）。
- credential helper 對應：GitLab 用 `glab auth git-credential`、GitHub 用 `gh auth git-credential`
  （或系統的 credential manager）。
- `~/.claude/creds/` 只放憑證，不放一般筆記或暫存資料；目錄建議權限 `700`，`.creds` 檔案建議權限 `600`。
- 不要把 `~/.claude/creds/.creds` 複製到 repo、log、聊天紀錄，或用來做其他可分享備份。
- GitLab 範例（`<GITLAB_HOST>` 填實際位址，見 `~/.claude/env.md`）：
  ```
  git -c "credential.https://<GITLAB_HOST>.helper=!f() { GITLAB_HOST=<GITLAB_HOST> glab auth git-credential \"$@\"; }; f" clone <url> <dir>
  ```
- helper 回傳的 username 可能為空；若 HTTP Basic 被拒，username 用 `oauth2`，
  token 仍走 helper（勿寫進 URL）。
- 若不得已曾用內嵌 URL，事後立即 `git remote set-url origin <乾淨URL>`，並評估是否輪替該 token。

## gh / glab CLI（GitHub / GitLab 官方指令列工具）
檢查項目：CLI 而已（`gh`、`glab`），無對應 skill；安裝判斷套用 `tools-install-check.md` 的通用流程
（`command -v gh`／`command -v glab` 判斷是否已裝）。
- 用途：開/查 PR・MR、查 issue，以及上方憑證安全段落用到的
  `gh auth git-credential`／`glab auth git-credential` credential helper。
- 安裝：
  - **GitHub CLI（`gh`）**，官方 apt repo（Debian/Ubuntu）：
    ```bash
    (type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
      && sudo mkdir -p -m 755 /etc/apt/keyrings \
      && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
      && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
      && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
      && sudo apt update && sudo apt install gh -y
    ```
    macOS：`brew install gh`。
  - **GitLab CLI（`glab`）**，官方不提供 apt repo；優先用 Homebrew（macOS/Linux 皆可）：
    ```bash
    brew install glab
    ```
    Debian/Ubuntu 無 Homebrew 時，改用社群維護的 WakeMeOps apt repo：
    ```bash
    curl -sSL "https://raw.githubusercontent.com/upciti/wakemeops/main/assets/install_repository" | sudo bash
    sudo apt install glab
    ```
- 認證：`gh auth login`／`glab auth login`（互動式設定），設定完成後才能用上方 credential helper 指令。
- fallback：未安裝時改用 git 原生指令操作，credential helper 段落須改手動設定（不強制要求安裝 gh/glab）。

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

## 變更紀錄
- 2026-07-04：GitLab 範例的內網位址改為 `<GITLAB_HOST>` 佔位符（公開 repo 去識別化）。
- 2026-08-15：新增「gh / glab CLI」章節，補齊安裝指令（gh 官方 apt repo；glab 用 Homebrew 或社群
  WakeMeOps apt repo，官方無自有 apt repo）與 `auth login` 認證步驟，安裝指令已逐一驗證來源。
