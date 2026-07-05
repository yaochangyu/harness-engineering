---
name: harness-install
description: 安裝並初始化本 repo 的 harness 制度庫（symlink、個人環境配置 env.md、健康檢查、導覽）。使用者 clone 本 repo 後說「安裝」「初始化」「setup」「裝起來」，或第一次在本 repo 目錄開 session 時使用。
---

# harness-install：安裝精靈

目標：讓 clone 本 repo 的人一次完成安裝＋個人配置＋驗證，並知道怎麼開始用。
全程使用台灣用語的繁體中文。

## 步驟 1：選擇要 symlink 的 CLI/IDE

自動掃描發現可用的 AI 代理 CLI 工具（copilot、opencode、codex、antigravity、gemini、hermes、claude 等），列出已安裝和未安裝的狀態：

```
════════════════════════════════════════════
可用的 CLI / IDE 工具
════════════════════════════════════════════

✓ 已安裝：
  1. claude          → /home/yao/.local/bin/claude
  2. codex           → /home/yao/.nvm/versions/node/v22.20.0/bin/codex
  3. copilot         → /home/yao/.nvm/versions/node/v22.20.0/bin/copilot
  4. gemini          → /home/yao/.nvm/versions/node/v22.20.0/bin/gemini
  5. hermes          → /home/yao/.local/bin/hermes
  6. opencode        → /home/yao/.nvm/versions/node/v22.20.0/bin/opencode

選擇要 symlink 的工具：
  a = 全部已安裝
  1,2,3,... = 選擇特定工具編號
  (直接按 Enter 略過此步驟)
```

規則：
- 自動掃描 PATH、npm global、常見 npm 套件位置
- 支持 6+ 個 AI 代理工具，並可擴展
- 已安裝的工具才能選，未安裝的工具不顯示
- 使用者可選「全部已安裝」(a) 或輸入編號組合 (1,2,3)
- 使用者略過本步驟 → 跳過 CLI symlink，只做核心安裝

## 步驟 2：跑安裝腳本

```bash
python3 claude/install.py
```

腳本是冪等的，會自動：
- 運行 AI CLI 工具選擇器（互動式選擇要 symlink 的工具）
- 改寫制度檔內的 HARNESS 路徑（repo 位置變了才改）
- 備份既有的 `~/.claude/CLAUDE.md`
- 建立入口 symlink
- 根據選擇在 `~/.claude/cli/` 建立 CLI 工具的 symlink
- `~/.claude/env.md` 不存在時從 `claude/env.example.md` 複製範本
- 跑健康檢查

若腳本失敗，把錯誤原文貼給使用者，不要腦補修法；
symlink 不可用的環境（少見）改走 `claude/README.md` 的手動步驟。

## 步驟 3：訪談並填寫個人環境配置

讀 `~/.claude/env.md`。若仍是範本佔位符（含 `<GITLAB_HOST>` 等字樣），逐項詢問使用者：

| 問題 | 對應欄位 | 可略過 |
|---|---|---|
| 有自架 GitLab 或其他內網 git 主機嗎？位址是？ | `<GITLAB_HOST>` | ✅ |
| 用什麼 CLI 操作 ticket？使用說明在哪？ | `<TICKET_CLI>`、`<TICKET_CLI_DOC_URL>` | ✅ |
| 有工作專案對應表（CSV 等）嗎？路徑是？ | `<PROJECT_MAPPING_CSV_PATH>` | ✅ |
| 有本機知識庫（LLM wiki）嗎？路徑是？ | `<WIKI_ROOT>` | ✅ |
| 本機有什麼要提醒未來 session 的注意事項？ | 本機注意事項 | ✅ |

規則：
- 一次問完（用一則訊息列出所有問題），不要一題一題往返。
- 使用者略過的項目：整行刪除或標「（無）」，**不要留佔位符**。
- 填完寫回 `~/.claude/env.md`。這個檔不在版控內，內網／公司資訊只能寫在這裡。
- 若 env.md 已有實際值（沒有佔位符），跳過本步驟，只回報「env.md 已配置」。

## 步驟 4：驗證

```bash
python3 claude/check_harness.py
```

- 全綠 → 繼續步驟 5。
- 有問題 → 照腳本印出的修復指令處理，修完重跑；連續兩輪修不好就停下來問使用者。
- 已知例外：若使用者自行安裝了會改 `~/.claude/CLAUDE.md` 的框架（如 OMC），
  行數警告可能持續存在，如實回報並讓使用者決定，不要自行刪除框架內容。

## 步驟 5：一分鐘導覽（安裝完成後回報）

用簡短篇幅告訴使用者：
1. 入口是 `~/.claude/CLAUDE.md`（symlink 到本 repo），每個 session 自動載入。
2. 核心機制是路由表：命中情境才讀對應子檔，不要一次全讀。
3. 紅線：內網位址、公司資訊、憑證只能寫 `~/.claude/env.md`，不可寫進 repo（公開的）。
4. 客製化入口：改制度檔前先讀 `claude/maintenance-protocol.md`。
5. 之後任何 Claude 相關工具安裝／升級後，重跑 `python3 claude/check-harness.py`。
