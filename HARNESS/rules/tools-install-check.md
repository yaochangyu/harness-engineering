# 工具安裝前判斷通用慣例（`rules/tools.md` 各工具章節共用）

適用情境：`rules/tools.md` 內任何要求先裝 skill 或 CLI 才能用的工具。
使用前一律套用下列 4 步驟；**各工具章節都要明確列出 skill name 與 CLI name**，沒有就寫 `無`。
再分別寫出對應的 skill 目錄名稱、CLI 指令、專屬安裝指令與 fallback 方式，不用整段複製這 4 步驟。

1. 先看工具章節有沒有宣告 skill：有才查 `ls ~/.claude/skills/<skill 名稱>`；目錄不存在 → 視為 skill 未裝。
2. 再看工具章節有沒有宣告 CLI：有才查 `command -v <CLI 指令>`；沒有輸出 → 視為 CLI 未裝。
3. skill 與 CLI 分開判斷、分開提示：
   - skill 未裝 → 告知使用者「<工具> skill 尚未安裝」，並列出該工具章節記載的 skill 安裝指令。
   - CLI 未裝 → 告知使用者「<工具> CLI 尚未安裝」，並列出該工具章節記載的 CLI 安裝指令。
   - 若該工具同時有 CLI 與 skill，像 Google Workspace 的 `gws`、HackMD 的 `hackmd-cli`，
      則先提醒使用者補裝 CLI（`gws`：`npm install -g @googleworkspace/cli`；
      `hackmd-cli`：`npm install -g @hackmd/hackmd-cli`），再繼續詢問是否安裝對應 skills。
   - 若安裝方式支援全域 vs 專案（`npx skills add` 的 `-g/--global`），**要先問使用者要裝哪一種範圍**，
     依回答決定指令帶不帶 `-g`，不要自行預設。取得使用者同意才真的執行安裝指令。
   - **註記慣例**：`rules/tools.md`、`rules/web-automation.md` 內的 `npx skills add` 指令一律把 `-g`
     寫成 `[-g]`，代表「這裡要先問使用者、依回答決定帶不帶」，不是可以直接複製執行的預設值
     （不加 `-g` 時預設裝到目前專案）。例外：`install-skills.py` 讀 `skills-manifest*.txt` 做的批次
     安裝本來就是全域路徑，使用者選擇跑它即視為已同意全域，不用再逐條問。
4. 使用者明確拒絕安裝、或要求先用其他方式時，才能改用該工具章節記載的 fallback 方式；
   且必須在回覆中註明「<工具> 未安裝，已改用替代方式」，不可默默切換，也不可默默跳過整個需求。
