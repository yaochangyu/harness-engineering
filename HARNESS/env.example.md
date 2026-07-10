# 個人環境配置（範本）

> 複製本檔到 `~/.claude/env.md` 並填入實際值。
> `~/.claude/env.md` **不納入版控**——所有內網位址、公司專案、個人路徑只能寫在那裡，
> 不可寫回制度檔（repo 內的檔案一律用 `<佔位符>`）。
> `install.py` 會在 `~/.claude/env.md` 不存在時自動從本範本複製一份。

## 內網服務
- 自架 GitLab：`<GITLAB_HOST>`（例：`gitlab.example.com` 或內網 IP）
- 基礎建設服務位置清單：`~/.claude/infra.md`

## 工作專案
- ticket 工具：`<TICKET_CLI>`（使用說明位置：`<TICKET_CLI_DOC_URL>`）
- 工作專案對應表：`<PROJECT_MAPPING_CSV_PATH>`

## 知識庫
- LLM Wiki 路徑：`<WIKI_ROOT>`（操作規則見該目錄的 CLAUDE.md）

## 本機注意事項
- （範例）`~/.claude/` 下的某些檔案是舊工具遺留檔，勿當作現行規則引用
