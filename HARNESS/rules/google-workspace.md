# Google Workspace

檢查項目：skill 視服務而定（如 `gws-gmail`）；CLI `gws`。

## 用途
- Gmail / Drive / Calendar / Slides / Sheets / Docs 操作時使用 `gws`。

## 安裝前判斷
- 先套用 `rules/tools-install-check.md` 的通用慣例：skill 與 CLI 分開查、分開提示。
- skill name：`gws-gmail` / `gws-slides` / `gws-sheets` / `gws-docs`
- CLI name：`gws`

## 安裝與使用
- 常用四個 skill：`gws-gmail`、`gws-slides`、`gws-sheets`、`gws-docs`。
- 其他服務先用 `gws --list` 查可用服務／skill，不要只寫裸的 `--list`，也不要憑記憶猜 skill 名稱。
- 來源：Google Workspace CLI 官方 repo／首頁 `https://github.com/googleworkspace/cli`。
- CLI 安裝：`npm install -g @googleworkspace/cli`
- skill 安裝來源：`https://github.com/googleworkspace/cli`（repo 有 AI agent skills；但目前這份檔案仍缺對應 `-s` 具體名稱）。
- skill 安裝：若需要先安裝，先依對應 skill repo / skills manifest 補齊，不要自行猜指令。

## 退出條件
- 未裝時先提示對應安裝指令；若使用者拒絕安裝，fallback 為 Gmail / Drive / Calendar 的 MCP 工具。
