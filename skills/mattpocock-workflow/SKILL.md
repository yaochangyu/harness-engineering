---
name: mattpocock-workflow
description: 端到端軟體工程工作流。結合 /grill-with-docs 磨礪、/to-spec、/to-tickets、plan.md 步驟追蹤、/tdd 紅綠切片與 /code-review 雙軸審查。
---

# Matt Pocock Skills × Harness 本地規範 端到端工作流

當使用者下達 `/mattpocock-workflow` 指令，或要求進行高階軟體工程重構與多步驟開發時，載入本技能。

> [!IMPORTANT]
> 完整 SOP（前置檢查、四階段細部規範、Mermaid 流程圖）的權威來源在
> `HARNESS/rules/mattpocock-workflow.md`。**本檔只做觸發入口與速查索引，不重複維護步驟細節**——
> 執行前務必先讀該檔，勿只憑下方摘要動作，避免兩處文件內容 drift。

## 何時用這套工作流，而非 `rules/workflow.md`

跨模組的複雜重構、或需要先盤問對齊設計邊界／TDD 紅綠切片／雙軸審查時，才升級到本工作流；
一般多檔案/多步驟的實作仍走 `rules/workflow.md`（單一 plan.md 追蹤即可，不需要磨礪與雙軸審查儀式）。

## 四階段速查

1. **對齊** — `/grill-with-docs` 盤問邊界 → 更新 `CONTEXT.md` / `docs/adr/`
2. **計畫** — `/to-spec` + `/to-tickets` 拆解 → 建立 Harness `plan.md`，取得使用者確認
3. **實作** — 逐步 `/tdd`（Seam → 紅 → 綠），每步完成停下請示確認
4. **審查封存** — `/code-review` 雙軸審查（Standards + Spec 平行子代理）→ commit（無 Co-authored-by）→ plan.md 移入 `.archive/`

詳細規則、前置技能安裝流程、Mermaid 時序圖，見 `HARNESS/rules/mattpocock-workflow.md`。
