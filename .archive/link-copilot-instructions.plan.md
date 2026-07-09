# 讓 Copilot CLI 指向 CLAUDE.md 實作計畫

此計畫旨在修改 `claude/install.py`、`claude/uninstall.py` 與 `claude/check_harness.py`，使 Copilot CLI (使用 `~/.github/copilot-instructions.md` 與 `~/.copilot/copilot-instructions.md`) 的提示詞檔案同樣軟連結指向此專案的 `claude/CLAUDE.md`，實現多 AI 代理規則一體化。

## 實作步驟

- [x] **步驟 1**：修改 `claude/install.py`
  - *說明*：加入對 `~/.github/copilot-instructions.md` 與 `~/.copilot/copilot-instructions.md` 的 symlink 建立與備份邏輯。
- [x] **步驟 2**：修改 `claude/uninstall.py`
  - *說明*：加入對上述兩個 Copilot 提示詞 symlink 的移除與備份還原邏輯。
- [x] **步驟 3**：修改 `claude/check_harness.py`
  - *說明*：加入對這兩個 Copilot 提示詞連結狀態的健康度檢查。
- [x] **步驟 4**：執行安裝與健康檢查驗證
  - *說明*：實際運行 `python3 claude/install.py`，驗證 symlink 是否成功建立且健康檢查通過。
- [x] **步驟 5**：歸檔計畫檔案
  - *說明*：將本計畫檔案移至 `.archive/` 並更新 `@tree.md`。
