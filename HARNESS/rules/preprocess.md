# 前處理標準化（markitdown）

## 來源
- markitdown 官方 repo：<https://github.com/microsoft/markitdown>

## 觸發條件
- 任何文件型輸入要進入 AI 分析前：PDF / Word / PowerPoint / Excel / 圖片 / HTML / 壓縮包等。

## 規則
- 先確認環境是否已安裝 markitdown；若缺少，執行 `pip install 'markitdown[all]'`（必要時先建立/啟用 Python virtual environment），安裝後沿用，不要每次重新分析或重抓安裝步驟。
- 任何文件型輸入進入 AI 分析前，都要先用 markitdown 轉成 Markdown。
- 轉換失敗時要中止流程並回報，不可直接把原始檔送進 AI。
- 轉出的 Markdown 視為標準輸入，原始檔與轉換結果都應保留，方便追查與重跑。

## 變更紀錄
- 2026-08-10：補上 markitdown 官方 repo 位置，並把前處理規則寫得更明確。
- 2026-08-09：從 workflow.md 抽出，作為文件分析的共用前處理規則（markitdown）。
