# Gemini Notebook / NotebookLM

檢查項目：skill `notebooklm`（teng-lin）／`nlm-skill`（jacob-bd）；CLI `notebooklm` ／ `nlm`。

## 選用原則
- 兩套 client 可並存；優先 `nlm`，只有做不到時才換 `notebooklm`。
- 若要深入安裝／認證／換手條件，再看對應 repo 與 skill。

## 安裝前判斷
- 先套用 `rules/tools-install-check.md` 的通用慣例：skill 與 CLI 分開查、分開提示。
- skill name：`notebooklm` / `nlm-skill`
- CLI name：`notebooklm` / `nlm`

## 安裝與使用
- 兩套 client 可並存；優先 `nlm`，只有做不到時才換 `notebooklm`。
- CLI 安裝來源：
  - `https://github.com/jacob-bd/notebooklm-mcp-cli`
  - `https://github.com/teng-lin/notebooklm-py`
- skill 安裝來源：
  - `teng-lin/notebooklm-py@notebooklm` → `https://skills.sh/teng-lin/notebooklm-py/notebooklm`
  - `pleaseprompto/notebooklm-skill@notebooklm` → `https://skills.sh/pleaseprompto/notebooklm-skill/notebooklm`
- 正式安裝命令與對應 CLI 名稱：待確認；若要執行，先查對應 repo / skill，再決定是否要全域或專案安裝。
- 若要深入安裝／認證／換手條件，再看對應 repo 與 skill。

## 退出條件
- 使用前先判斷是否已安裝；fallback 為 NotebookLM 官方 web UI。
