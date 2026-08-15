# CodeGraph

repo 根目錄有 `.codegraph/` 索引時，理解/定位程式碼優先用 CodeGraph，取代 grep/find 或逐檔 Read：

- **MCP tool**（有裝時優先）：`codegraph_explore` 一次回傳相關符號的完整原始碼（含行號）與彼此的呼叫路徑，
  含 grep 抓不到的 dynamic-dispatch 呼叫鏈。查詢字串可直接帶檔名或符號名，取得該符號目前的行號原始碼。
  若工具列在 deferred 清單但還沒載入，先用 tool search 依名稱載入。
- **Shell**（一定可用）：`codegraph explore "<符號名或問題描述>"`，輸出跟 MCP tool 相同。

沒有 `.codegraph/` 目錄就整段跳過——要不要對某個 repo 建索引是使用者的決定，不要自作主張跑 `codegraph init`。

以上內容原文照抄自 `codegraph install` 官方寫入 agent instructions 檔（CLAUDE.md / AGENTS.md / GEMINI.md）的
`<!-- CODEGRAPH_START -->…<!-- CODEGRAPH_END -->` 區塊（來源：`@colbymchenry/codegraph` 套件
`dist/installer/instructions-template.js`）。官方刻意把這段寫進 instructions 檔本體、且刻意保持簡短，
是因為 Task-tool 派生的 subagent 只會拿到 project instructions 檔內容，拿不到 MCP 的 `initialize`
instructions——官方實測這段區塊存在與否，subagent 主動用 codegraph 的比例是 9/9 vs 1/9。
改動這段文字前請留意這個限制。

## 已知風險：`codegraph install` / `codegraph upgrade --refresh` 會弄斷入口 symlink
這兩個指令會直接改寫 agent 的全域 CLAUDE.md（例如 `~/.claude/CLAUDE.md`），寫入方式不是透過 symlink 寫入，
而是整份檔案重建，因此會把 harness 的入口 symlink 換成一般檔案，導致路由表的 `HARNESS_DIR` 動態解析失效。

發現症狀（`~/.claude/CLAUDE.md` 不再是 symlink，或內容比 `HARNESS/CLAUDE.md` 舊）時：
1. 執行 `python3 HARNESS/check_harness.py` 確認診斷。
2. 用以下指令重建 symlink（會先備份現有內容到 `HARNESS/backup/`，不會丟資料）：
   ```bash
   DATE=$(date +%Y-%m-%d)
   cp ~/.claude/CLAUDE.md HARNESS/backup/CLAUDE.md.replaced.$DATE.md
   cp ~/.gemini/GEMINI.md HARNESS/backup/GEMINI.md.replaced.$DATE.md
   ln -sf "$(pwd)/HARNESS/CLAUDE.md" ~/.claude/CLAUDE.md
   ln -sf "$(pwd)/HARNESS/CLAUDE.md" ~/.gemini/GEMINI.md
   ```
3. 比對備份內容，若有新的、有價值的說明區塊（例如工具自己塞進去的使用說明），
   評估後搬進對應的 `rules/*.md`，不要留在 `~/.claude/CLAUDE.md` 裡等下次又被覆寫掉。
