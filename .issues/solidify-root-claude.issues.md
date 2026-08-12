## 2026-07-09 根目錄 CLAUDE.md 用 symlink 在 Windows 環境不相容

- 情境：專案根目錄的 `CLAUDE.md` 原本是指向 `HARNESS/CLAUDE.md` 的軟連結（symlink）。
- 失敗的方法：維持根目錄 `CLAUDE.md` 為 symlink，讓 AI 工具（含跨平台使用者）直接讀取。
- 原因：Windows 對 symlink 的建立與讀取相容性不佳（需權限/開發者模式，或工具鏈不follow symlink），
  導致跨平台（尤其 Windows）使用時可能讀不到內容。
- 改用：`.archive/solidify-root-claude.plan.md`（commit `bb7fdea`）把根目錄 `CLAUDE.md`
  由 symlink 改為實體檔案，內容直接同步自 `HARNESS/CLAUDE.md`，並更新 `@tree.md` 標記其為實體檔案。
