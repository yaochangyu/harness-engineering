# 程式碼分析／搜尋工具（避免直接用 grep）

分析、搜尋既有程式碼時，按此順序判斷：
1. **codegraph** — 純結構化程式碼查詢（找 symbol、呼叫關係、影響範圍、避免 grep+Read 迴圈）優先用。
2. **graphify** — 需要跨程式碼＋文件/論文/圖片的知識圖譜、跨 session 持久記憶、Q&A 累積時用。
3. grep／Read 只在上述兩者都不可用（未安裝、該路徑沒有索引、要找非程式碼文字）時才當 fallback。

## codegraph
檢查項目：CLI `codegraph`；MCP server（單一工具 `codegraph_explore`，此環境已啟用）；無 skill（沒有 npx skills 套件，靠 CLI + MCP）。
- 官方 repo／文件：https://github.com/colbymchenry/codegraph （https://colbymchenry.github.io/codegraph/）
- 核心用法：`codegraph_explore`（MCP）一次回傳相關 symbol 的完整原始碼（含行號）＋呼叫路徑＋影響範圍摘要，
  取代「grep 找 symbol → Read 逐一開檔」的迴圈；可傳 `projectPath` 查詢當前 session root 以外、
  但有自己 `.codegraph/` 索引的專案（例如 monorepo 內的子服務、第二個 repo）。
- CLI 對應：`codegraph query <search>` / `explore <query...>` / `node <name>` / `callers <symbol>` /
  `callees <symbol>` / `impact <symbol>` / `affected [files...]` / `status` / `files`。
  MCP 預設只列 `codegraph_explore`；其餘工具（`codegraph_node/search/callers/callees/impact/files/status`）
  仍可用但預設不列出，需要時改用對應 CLI 指令，或設 `CODEGRAPH_MCP_TOOLS` 環境變數重新啟用。
- 安裝（不需要 Node.js）：
```bash
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh   # macOS/Linux
# 已有 Node 也可以：npm i -g @colbymchenry/codegraph
codegraph install   # 把 MCP server 接到 Claude Code / Cursor / Codex 等 agent；裝 CLI 不會自動做這步
```
- 索引：`codegraph init` 會在專案根目錄建立 `.codegraph/` 並建完整圖，之後預設自動 sync
  （檔案變動即時更新，不需手動重跑）。**要不要在某個專案跑 `codegraph init` 是使用者決定，不要自行執行**；
  沒有索引的專案，MCP 會回傳清楚的提示改用內建工具，不會噴錯。
- 升級／移除：`codegraph upgrade`；`codegraph uninstall`（移除 agent 設定＋CLI 本身，`--keep-cli` 只移除
  agent 設定，保留 CLI）；單一專案移除索引用 `codegraph uninit`（不動 CLI／agent 設定）。
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例，但只檢查 CLI（無 skill 可查）；
  `command -v codegraph` 判斷 CLI 是否存在；MCP 工具是否可用，看該 session 有沒有列出
  `mcp__codegraph__codegraph_explore`。
  fallback：CLI／MCP 都不可用，或該路徑沒有 `.codegraph/` 索引時，才退回 grep／Read。
- 官方 instructions 短區塊、以及 `codegraph install/upgrade` 弄斷入口 symlink 的已知風險與修復步驟，
  見 `rules/codegraph.md`。

## graphify
檢查項目：skill `graphify`；CLI `graphify`。
- 使用者輸入 `/graphify` 時，先呼叫 Skill tool（`skill: "graphify"`）再做其他事。
- Skill 位置：`~/.claude/skills/graphify/SKILL.md`。
- 官方 repo：https://github.com/Graphify-Labs/graphify
  **注意套件名稱**：PyPI 上是 `graphifyy`（雙 y），不是 `graphify`；其他 `graphify*` 套件非官方。
  安裝完後終端機指令仍是 `graphify`。
- 安裝（新環境沒有這個 skill 時）：
```bash
  uv tool install graphifyy      # 推薦；替代方案 pipx install graphifyy
  graphify install               # 註冊為全域 skill（僅當前 repo 用 --project）
```
- Mac/Windows 避免直接 `pip install graphifyy`：安裝路徑常跟 skill 執行時解析的 Python 環境不一致，
  會導致 `ModuleNotFoundError`。
- 免安裝直接跑：`uvx --from graphifyy graphify install`
  （不可直接 `uvx graphify ...`——`uv tool run` 會把第一個字當套件名找，套件實際叫 `graphifyy`）。
- 額外功能（PDF / MCP server / Neo4j 等）：`uv tool install "graphifyy[pdf]"` / `"[mcp]"` / `"[all]"`。
- **使用前判斷是否已安裝**：套用 `tools-install-check.md` 通用慣例；skill 目錄／CLI 皆是 `graphify`；
  fallback 為停用 graphify 相關操作。
