# orca-cli 派工非原生 CLI worker（copilot / antigravity）

適用情境：用 orca-cli 的 orchestration 指令，把 copilot、antigravity（`agy`）這類
Orca 沒有完整原生支援的 agent CLI 掛進派工流程時的實測限制與繞過方法。
啟動指令需帶 `--yolo`（copilot）或 `--dangerously-skip-permissions`（antigravity）
啟用完整權限，避免自動化執行時卡在互動確認提示。

## 已知限制總覽（實測，非官方文件）
- `worker-start --model` 官方只支援 Claude／Codex／Cursor 的 opaque model id：
  - 對 copilot 帶 `--model`：不報錯，但**默默沒生效**。
  - 對 antigravity 帶 `--model`：直接回錯
    `Agent antigravity does not support launch-time model selection`（比 copilot 好抓，至少會報錯）。
- `worker-start --agent <id>`：`copilot`、`antigravity` 都能被接受並啟動 terminal，
  但 antigravity 常常在 `agent_readiness` 階段逾時失敗（見下方登入問題）。
- `dispatch --inject`（把任務直接注入某個已在跑的 terminal）：
  - `copilot`：可以被偵測到，inject 正常運作。
  - `antigravity`（`agy`）：**偵測不到**，即使已完全登入、輸入框已就緒，
    仍回 `no_agent_detected`（`agy` 雖然列在 Orca 錯誤訊息的支援清單名稱裡，
    這個版本〔Orca CLI 1.4.205〕實測就是偵測不到；之後版本更新後可再重測）。

## copilot 派工流程
1. `terminal create --command "copilot --yolo"`
2. `terminal wait --terminal <handle> --for tui-idle`
3. 切換模型：**必須用方向鍵導航，不能靠打字篩選**——在 `/model` 選單裡打字
   只會在畫面下方多出一個獨立的「Search models…」輸入框，不會移動選取游標；
   打完字直接按 Enter，選到的還是原本游標所在的項目（實測踩過這個雷，
   誤選到清單第一項而非搜尋到的項目）。
   - `terminal send --terminal <handle> --text "/model" --enter`
   - 用 `terminal send --terminal <handle> --text $'\x1b[B'`（方向鍵 Down）
     一步步移動，每按一次就用 `terminal read` 確認畫面上 `❯` 游標位置，
     直到停在目標模型上
   - 確認游標對了之後，`terminal send --terminal <handle> --text "" --enter` 送出選取
4. `orchestration dispatch --task <task_id> --to <handle> --run <run_id> --inject --json`
   掛進 orchestration Run。

## antigravity（agy）派工流程
1. 確認本機有 `agy`（`~/.local/bin/agy`，來自 `~/.gemini/antigravity-cli/`）。
2. 用 `agy models` 查詢目前實際可選的 model id（名稱會隨版本變動，
   不要憑印象猜；例如某次查到 `gemini-3.8-flash-medium`）。
3. 啟動：優先 `terminal create --command "agy --model <id> --dangerously-skip-permissions"`
   （手動帶 `--model` 有效，跟 `worker-start` 不支援 antigravity 的 `--model` 不同）。
4. **每個新啟動的 agy process 都可能要求重新互動登入**：畫面顯示
   「Welcome to the Antigravity CLI. You are currently not signed in.」＋轉圈圖示，
   即使 `~/.gemini/antigravity-cli/antigravity-oauth-token` 已存在也不會自動套用。
   這一步無法用指令自動化（沒有 `agy login` 子指令），需請使用者到 Orca App
   裡對那個 terminal 分頁手動完成登入；登入完成後畫面會出現正常帳號資訊
   （email、方案）＋模型名稱＋`>` 輸入框。
5. `dispatch --inject` 目前**必定失敗**（`no_agent_detected`，見上方總覽），
   改走通用 fallback（見下一節）：`dispatch --return-preamble`（不加 `--inject`）
   + 手動 `terminal send`。
6. **超長或多行文字貼不進去**：agy 的輸入框對含真正換行字元（`\n`）的長文字
   只會顯示成多行預覽掛在那裡，之後不管再按幾次 Enter 都只是換行，不會送出。
   對策：
   - 短訊息（單行、不含 `\n`）可以直接送，Enter 正常送出、agent 立刻開始處理。
   - 需要送完整 preamble（含派工指令說明）時，先把裡面所有換行/多餘空白
     攤平成單一空格（例如 `re.sub(r'\s+', ' ', text)`），變成一個長單行字串再送出；
     字串太長（實測約 5000 字元）可能會在輸入框卡住數秒到十幾秒不會自動送出，
     這時送一次 `terminal send --terminal <handle> --interrupt` 通常能觸發它
     把已貼入的內容當成一次輸入處理掉（實測有效，底層機制不確定，
     可能是強制 flush 或取消卡住的 render）。
   - 送出後務必用 `terminal read` 實際看畫面確認有沒有被處理——
     這個 provider 的 `prompt.observation` 固定回 `unsupported`，
     不能只看 `terminal send` 的回傳值判斷有沒有送達。
7. 收到 `worker_done` 後跟其他 worker 一樣 `worker-retain` 保留待命；
   因為是走 `dispatch`（非 `worker-start` 建立的 supervised worker），
   `resource.state` 永遠是 `absent`（`reason: unsupervised`），
   `worker-retain` 對它只是記錄用（`processAction: none`），terminal 本身
   要自己顧著別關掉——關掉分頁（`terminal close`）不代表底層 process 被殺
   （`ptyKilled: false`），已經貼進去但還沒送出的內容之後可能自己被處理掉，
   事後才收到遲到的 `worker_done`，要留意這個時序陷阱。

## 通用 fallback：任何被 Orca 判定 `no_agent_detected` 的 agent
1. `orchestration task-create --run <run_id> --spec "..." --task-title "..."` 建立任務。
2. `orchestration dispatch --task <task_id> --to <handle> --run <run_id> --return-preamble --json`
   （不加 `--inject`）：取得 `preamble` 文字，同時建立 dispatch 記錄。
3. 把回傳的 `preamble` 文字用 `terminal send` 貼給該 terminal
   （注意上面「超長或多行文字貼不進去」那條）。
4. `orchestration check --wait --types "worker_done,escalation,question" ...` 照常等待。
5. 收到 `worker_done` 後 `worker-retain` / `worker-release` 照常做，
   但預期 `resource.state: absent`、`reason: unsupervised`。
