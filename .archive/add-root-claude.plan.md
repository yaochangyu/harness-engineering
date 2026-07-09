# 建立根目錄 CLAUDE.md 軟連結計畫

此計畫旨在專案根目錄建立 `CLAUDE.md` 指向 `claude/CLAUDE.md` 的軟連結，使 AI Agent（例如 opencode）在專案目錄下啟動時能自動載入制度檔，並更新專案目錄結構檔 `@tree.md`。

## 實作步驟

- [x] **步驟 1**：在專案根目錄建立軟連結 `CLAUDE.md` 指向 `claude/CLAUDE.md`
  - *說明*：讓 AI Agent 在專案根目錄啟動時，能自動偵測並讀取此專案的制度檔。
- [x] **步驟 2**：更新或初始化專案目錄結構檔案 `@tree.md`
  - *說明*：遵守專案規則，在新增檔案後更新 `@tree.md`，將新的 `CLAUDE.md` 納入結構紀錄中。
