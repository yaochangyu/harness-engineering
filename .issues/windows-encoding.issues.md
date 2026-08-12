## 2026-08-06 Windows 原生環境讀寫 UTF-8 檔案未指定編碼

- 情境：`install.py`／`check_harness.py`／`uninstall.py` 需要讀寫 CLAUDE.md 等含中文內容的檔案。
- 失敗的方法：呼叫 `read_text()` / `write_text()` / `open()` 時未指定 `encoding` 參數。
  在 Windows 原生環境（非 WSL）下，Python 預設使用地區編碼（如 cp950）讀取 UTF-8 中文檔案
  會拋出 `UnicodeDecodeError`，導致三支腳本在 Windows 原生環境直接執行失敗。
- 原因：開發環境（WSL/Linux）預設編碼即為 UTF-8，掩蓋了未顯式指定 encoding 的問題；
  只有在 Windows 原生環境才會暴露。
- 改用：commit `52dae84` 統一在 `check_harness.py`、`install.py`、`uninstall.py`
  的所有讀寫檔案呼叫補上 `encoding="utf-8"`。
