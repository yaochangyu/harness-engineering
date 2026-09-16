# .NET / 開發原則（在 .NET 專案或工作專案時讀取）

- 遵守 SOLID 開發原則。
- Cucumber 的步驟使用中文；Cucumber 保留字（Feature、Background、Scenario、Given、When、Then）使用英文。
- ASP.NET Core Clean Architecture 實作可派 `project-architecture-engineer` agent（見 model-dispatch.md）。
- .NET Core 開發原則參考：`https://github.com/yaochangyu/api.template/blob/main/CLAUDE.md`
- 排版參考：`~/.claude/editorconfig/.net/.editorconfig`
  （2026-07-03 實測本機無此檔；不存在時問使用者實際位置，勿憑記憶自訂排版規則）

## user-secrets 憑證安全 — 硬規則

- **禁止**執行 `dotnet user-secrets list` 或 `dotnet user-secrets get`：這兩個指令會把密鑰明碼印到
  stdout/終端機/日誌，等同資安事故。
- 設定密鑰只用 `dotnet user-secrets set <key> <value>`，用它回傳的
  `Successfully saved <key> to the secret store.` 訊息確認成功，不要事後再用 `list`／`get` 驗證。
- 若不確定某個 key 是否已設定，改用程式碼內 `IConfiguration["<key>"]` 或 Options pattern 讀取後
  比對是否為 null/空字串，不要印出實際值。

規則由來：2026-09-05 同一個 session 內因為執行 `dotnet user-secrets list` 而讓 TDX Client Secret
明碼曝光兩次，才補上這條規則。
