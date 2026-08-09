---
name: mattpocock-workflow
description: 端到端軟體工程工作流。結合 /grill-with-docs 磨礪、/to-spec、/to-tickets、plan.md 步驟追蹤、/tdd 紅綠切片與 /code-review 雙軸審查。
---

# Matt Pocock Skills × Harness 本地規範 端到端工作流

當使用者下達 `/mattpocock-workflow` 指令，或要求進行高階軟體工程重構與多步驟開發時，載入本技能並按以下 SOP 執行：

## 0. 前置檢查與安裝 (Pre-flight Check)

1. **專案一次性設定檢查**：若本專案尚未建立 `docs/agents/` 設定檔（或 `docs/agents/issue-tracker.md` 不存在），應先引導執行一次 `/setup-matt-pocock-skills` 完成 Issue Tracker、Triage Labels 與 Domain Docs 配置。
2. **子技能檢查**：確認是否已具備所需子技能（`grill-with-docs`, `to-spec`, `to-tickets`, `tdd`, `code-review`, `domain-modeling`）。
   **若發現缺乏子技能，Agent 必須先打字向使用者確認安裝範圍 (Project 或 Global)**：
   - **Project (專案層級)**：僅安裝至當前專案
   - **Global (全域層級)**：安裝至全域環境

獲取選擇後，執行對應指令：
- **Project**: `npx skills add https://github.com/mattpocock/skills -s <missing_skills> -y -a '*'`
- **Global**: `npx skills add https://github.com/mattpocock/skills -s <missing_skills> -g -y -a '*'`

## 核心流程總覽

1. **階段一：對齊與領域設計 (Alignment)**
   - 執行 `/grill-with-docs` 技能，使用設計樹與輪次盤問（Rounds），向使用者確認決策邊界。
   - 確定新術語後，立刻修改/建立 `CONTEXT.md` 作為純 Glossary。
   - 若涉及難以逆轉的權衡，於 `docs/adr/` 中建立 ADR。

2. **階段二：制定計畫 (Planning)**
   - 使用 `/to-spec` 與 `/to-tickets` 將對話共識收斂為具體的實作步驟與相依性。
   - 複製 `HARNESS/plan-template.md`，於專案根目錄建立計畫檔：`{功能名稱(英文)}-{YYYY-MM-DD}.plan.md`。
   - 步驟表中使用 **狀態欄（⬜ 待做 / 🟦 進行中 / ✅ 完成 / ⚠️ 阻塞）** 追蹤進度。
   - 向使用者提交計畫書，**需獲得使用者明示確認 (Proceed) 後才開始實作**。

3. **階段三：實作與 TDD 循環 (Implementation Loop)**
   - 動手前檢查 `.issues/` 目錄，避免重複踩坑。
   - 步驟執行：每次只走一步，標記為 `🟦 進行中`。
   - 載入 `/tdd` 規約：**先打字確認 Seam (接縫) -> 寫紅燈測試 -> 寫綠燈最小實作**。
   - 異動檔案時同步更新專案的 `@tree.md`。
   - 完成步驟後標記 `✅ 完成`，提供 build 輸出證據，**停下來打字請示使用者確認**，才進行下一步。

4. **階段四：審查、提交與封存 (Review & Archive)**
   - 所有步驟完成後，自動啟動 `/code-review` 雙軸審查（Standards 軸 + Spec 軸平行子代理）。
   - 驗證 build 與測試通過後 commit，**commit message 嚴禁包含 "Co-authored-by"**。
   - 將計畫檔移入 `.archive/` 資料夾並 commit 封存。
