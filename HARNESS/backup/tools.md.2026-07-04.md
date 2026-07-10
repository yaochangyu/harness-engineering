# 工具細則（需要用到該工具時才讀）

## RTK（Rust Token Killer）
- `settings.json` 已設 PreToolUse hook `rtk hook claude`，Bash 指令會被自動處理；
  平常**不需要**手動背指令對照表。
- 原則：shell 指令加 `rtk` 前綴可省 60–90% token，無對應 filter 時原樣通過，永遠安全。
- 指令串接時每段都加前綴：`rtk git add . && rtk git commit -m "msg"`。
- 除錯時（需要看完整輸出）用原始指令，不加 rtk。
- `rtk proxy <cmd>`：不過濾但記錄用量。

## ctx7 / context7（查函式庫文件）
- 使用規則已在 `~/.claude/rules/context7.md` 自動載入，不要在別處重複維護。

## ua-cli（ticket 操作）
- 所有 ticket 操作用 `ua-cli`；使用步驟見 `https://192.168.1.158/JobBank1111/ua-cli`。

## Google Workspace
- 需要 Gmail / Drive / Calendar 操作時，優先用 googleworkspace cli：
  `https://github.com/googleworkspace/cli`。

## graphify
- 使用者輸入 `/graphify` 時，先呼叫 Skill tool（`skill: "graphify"`）再做其他事。
- Skill 位置：`~/.claude/skills/graphify/SKILL.md`。

## LLM Wiki
- 知識庫路徑：`/mnt/d/lab/llm-wiki/`；操作規則見 `/mnt/d/lab/llm-wiki/CLAUDE.md`。
- Ingest 程式碼時直接從原始路徑讀取，不複製到 `sources/`；
  `sources/` 只放外部資料（文章、論文、技術文件等沒有 repo 的資料）。
- wiki 頁面 frontmatter 的 `sources` 欄位，程式碼引用用絕對路徑
  （如 `/mnt/d/lab/gitlab-work/job/customer-api/src/...`）。
- 使用者要求歸檔到 wiki：資料放 `/mnt/d/lab/llm-wiki/wiki/raw/{歸檔}.md`，
  然後詢問是否需要 ingest 到 wiki。

## 中文寫作 skills
- 寫中文長文（文件、部落格、報告）時考慮 `stop-slop-zh-tw`（去 AI 腔）
  與 `write-yaochangyu-style`（使用者文風）。
