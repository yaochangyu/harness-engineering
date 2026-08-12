## 2026-08-06 harness-install skill 安裝腳本路徑寫錯

- 情境：撰寫 `.claude/skills/harness-install/SKILL.md` 安裝步驟說明，指引使用者執行安裝／驗證腳本。
- 失敗的方法：SKILL.md 內把腳本路徑寫成 `python3 claude/install.py`、`python3 claude/check_harness.py`，
  以及 `claude/README.md`、`claude/maintenance-protocol.md`、`claude/env.example.md` 等共 6 處引用，
  但 repo 內實際目錄已是 `HARNESS/`，不是 `claude/`；照文件執行會找不到檔案。
- 原因：撰寫文件時沿用舊目錄命名（`claude/`），未同步 repo 實際已改名為 `HARNESS/` 的事實。
- 改用：commit `e9fb458` 把 SKILL.md 內全部 `claude/` 路徑改為 `HARNESS/`。
