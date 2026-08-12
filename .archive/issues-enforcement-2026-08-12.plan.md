---
計畫模板版本: 2026-07-12
用途: AI Agent 逐步實作任務，避免混亂
---

# .issues 補寫與強制檢查點

**建立日期**: 2026-08-12 GMT+8
**狀態**: [完成]

⚠️ **檔案命名**: `issues-enforcement-2026-08-12.plan.md`

## 概覽

- **目標**：
  1. 把 repo 歷史上 3 起未被記錄的失敗案例，依 `maintenance-protocol.md` 第 3 節格式補寫進 `.issues/`。
  2. 在 `rules/workflow.md` 新增強制檢查點：plan.md 步驟標為 ⚠️ 時，必須同步寫入/更新對應 `.issues` 檔，否則不算處理完畢。
- **關鍵決策**：
  - `.issues` 檔名對應「功能」而非單一 commit：`harness-install`、`windows-encoding`、`solidify-root-claude`（後者已有對應的 archived plan.md，沿用同名）。
  - 修改 `rules/workflow.md` 前依 `maintenance-protocol.md` 第 2 節先備份。
- **風險**：無（純新增規則與補寫歷史紀錄，不刪改既有判準本身）。
- **使用者已確認**：透過 AskUserQuestion 已確認「補寫歷史案例」與「加強制檢查點」兩項方向。

## 執行步驟

| # | 步驟 | 說明 | 狀態 |
|---|------|------|------|
| 1 | 備份 rules/workflow.md | 修改前依 maintenance-protocol.md 第 2 節備份到 HARNESS/backup/ | ✅ 完成 |
| 2 | 建立 .issues/ 並補寫 3 起歷史案例 | 依 maintenance-protocol.md 第 3 節格式，補寫 harness-install / windows-encoding / solidify-root-claude | ✅ 完成 |
| 3 | rules/workflow.md 新增強制檢查點規則 | .issues 段落加一條：⚠️ 狀態時必須同步寫 .issues，否則步驟不算完成 | ✅ 完成 |
| 4 | 更新 rules/workflow.md 變更紀錄 | 依 maintenance-protocol.md 第 2 節第 3 步 | ✅ 完成 |
| 5 | read-back 驗證 | 重新讀取修改後檔案，確認落地且未破壞其他段落 | ✅ 完成（68 行，未破 250 行門檻；3 個 .issues 檔皆存在） |
| 6 | 歸檔本計畫 | 移到 .archive/，此任務無 build/測試（純文件） | ✅ 完成 |

**狀態說明**：⬜ 待做／🟦 進行中／✅ 完成／⚠️ 阻塞（需要使用者決定）

## 遭遇的問題

（目前無）

## 完成檢查表

- [x] 所有步驟狀態都是 ✅ 完成
- [x] read-back 驗證通過
- [x] 計畫書已移到 `.archive/` 資料夾
