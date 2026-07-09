# 精簡 CLAUDE.md 實作計畫

此計畫旨在精簡 `claude/CLAUDE.md`，移除由 `opencode` 安裝器造成的行數汙染（超過 60 行警訊），並將詳細路由表改為直接參考 `claude/README.md`，以維持最核心規則。

## 實作步驟

- [x] **步驟 1**：備份目前的 `claude/CLAUDE.md`
  - *說明*：遵守 `maintenance-protocol.md` 規範，將檔案複製備份至 `claude/backup/CLAUDE.md.2026-07-09.md`。
- [x] **步驟 2**：重構並精簡 `claude/CLAUDE.md` 內容
  - *說明*：移除 OMC 安裝器注入的 1~70 行內容，並將第 87~97 行的路由表修改為直接參考 `claude/README.md`。
- [x] **步驟 3**：執行健康檢查驗證
  - *說明*：執行 `python3 claude/check_harness.py`，驗證行數是否低於 60 行限制且功能健全。
