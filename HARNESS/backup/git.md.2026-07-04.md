# Git 規則（commit / MR / 憑證）

## 憑證安全（HTTPS 認證）— 硬規則，違反等於資安事故
- 適用所有 git HTTPS 主機（GitLab、GitHub 等），不限特定 host。
- **禁止**將 token 內嵌在 remote URL（如 `https://oauth2:<token>@host/...`）：
  clone 時用的 URL 會原封不動寫入 `.git/config`，導致 token 明文落地。
- 一律使用 git credential helper 取得憑證，remote URL 保持乾淨（`https://host/group/repo.git`）。
- credential helper 對應：GitLab 用 `glab auth git-credential`、GitHub 用 `gh auth git-credential`
  （或系統的 credential manager）。
- GitLab 範例（以 192.168.1.158 為例，其他 host 替換即可）：
  ```
  git -c "credential.https://192.168.1.158.helper=!f() { GITLAB_HOST=192.168.1.158 glab auth git-credential \"$@\"; }; f" clone <url> <dir>
  ```
- helper 回傳的 username 可能為空；若 HTTP Basic 被拒，username 用 `oauth2`，
  token 仍走 helper（勿寫進 URL）。
- 若不得已曾用內嵌 URL，事後立即 `git remote set-url origin <乾淨URL>`，並評估是否輪替該 token。

## commit message 格式
1. 若沒有 ticket id，詢問使用者是否需要加上 ticket id。
   - 若有 ticket id，最後一行加上 `Bundle: (ticket id)`。
2. 從 `git diff --staged` 產生精簡訊息，格式：
   `[EMOJI] [TYPE](file/topic)(ticket id): [繁中描述]`
   使用 GitMoji（如 ✨ → feat）、現在式、主動語態、每行最多 120 字元、不含 code block。
3. body 使用 markdown 格式。
4. **不可包含 Co-authored-by**。

## MR description（markdown 格式）
必含：變更的背景與目的、主要的變更內容、相關 ticket id（如果有的話）。

## git worktree 衝突解決
1. 開啟 `git rerere`。
2. 在其中一個 worktree 執行 `git rebase develop` 並手動解衝突。
3. 在其他 worktree 執行 `git rebase develop`，git 會自動套用剛才的解法。
