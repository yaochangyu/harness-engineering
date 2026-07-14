# Python 開發原則（使用 Python 開發應用程式或寫腳本時讀取）

- 虛擬環境一律用 `uv`，不要用 `venv` / `virtualenv` / `conda`。
  - 建立環境＋安裝套件：`uv venv` 、 `uv pip install <pkg>`（或專案已用 `uv add`／`pyproject.toml` 就用 `uv sync`）。
  - 執行指令在該環境下跑：`uv run <script.py>` 或 `uv run <cmd>`，不要手動 `source .venv/bin/activate` 再下指令。
  - 若專案已存在別的虛擬環境機制（既有 `requirements.txt` + `venv/` 且非本次新建），先確認使用者是否要換成 uv，不要自行遷移。
