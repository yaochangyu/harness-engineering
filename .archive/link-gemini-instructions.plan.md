# 讓 Antigravity 與 OpenCode 共同指向 CLAUDE.md 實作計畫

此計畫旨在修改 `claude/install.py`、`claude/uninstall.py` 與 `claude/check_harness.py`，使 Antigravity (使用 `~/.gemini/GEMINI.md`) 與 OpenCode (使用 `~/.claude/CLAUDE.md`) 共同指向同一份實體制度檔 `claude/CLAUDE.md`，以落實「單一事實來源」原則。

## 實作步驟

- [x] **步驟 1**：修改 `claude/install.py`
  - *說明*：加入對 `~/.gemini/GEMINI.md` 的 symlink 建立邏輯。若原本有實體檔案則先備份至 `claude/backup/` 下，確保既有資料不遺失。
- [x] **步驟 2**：修改 `claude/uninstall.py`
  - *說明*：加入對 `~/.gemini/GEMINI.md` 的 symlink 移除與備份還原邏輯，確保能乾淨回復原狀。
- [x] **步驟 3**：修改 `claude/check_harness.py`
  - *說明*：加入對 `~/.gemini/GEMINI.md` 的 symlink 與健康度檢查，以確保環境安裝狀態正確。
- [x] **步驟 4**：執行測試與驗證
  - *說明*：實際運行 `python3 claude/install.py` 並執行 `python3 claude/check_harness.py`，確認 symlink 建立正確且健康檢查全數通過。
- [x] **步驟 5**：歸檔計畫檔案
  - *說明*：將本計畫檔案移動到 `.archive/` 資料夾下，並更新 `@tree.md`。
