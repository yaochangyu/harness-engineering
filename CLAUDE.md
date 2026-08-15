# 全域指令

你是資深 DevOps / DX 工程師的協作夥伴。制度檔案庫在 `HARNESS/`（下稱 HARNESS）。

## 路由指引
- 各情境的子制度檔案用途與讀取時機，請**直接參考並讀取** [HARNESS/README.md](HARNESS/README.md)。
- 遇到特定開發或工具情境時，必須先讀取對應的子制度檔再開始實作。

## 新增 skill / CLI
- 使用者要新增工具、skill 或 CLI 時，先讀取 [README.md「新增工具時怎麼說」](README.md#新增工具時怎麼說)，
  確認來源 repo/文件、skill 安裝、CLI 安裝、是否要問全域或專案、fallback 與目標檔案。
- 缺少欄位時先查官方來源，仍無法判斷才詢問使用者；不要假設每個工具同時具備 skill 與 CLI。
- 新增工具時，檔案描述格式必須固定為 `新增工具 / 來源 repo/文件 / skill 安裝 / CLI 安裝 / 是否要問範圍 / fallback / 要更新的檔案`，不得自行改寫成其他順序或欄位名。

## session 開始時
- 檢查當前目錄有無 `*.plan.md`；有未完成項目就詢問使用者是否繼續。
