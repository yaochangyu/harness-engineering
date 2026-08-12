# Project Directory Tree

## Root
- [README.md](file:///home/yao/projects/harness-engineering/README.md) - 專案說明與快速開始指南
- [pyproject.toml](file:///home/yao/projects/harness-engineering/pyproject.toml) - 專案配置檔
- [CLAUDE.md](file:///home/yao/projects/harness-engineering/CLAUDE.md) - 實體檔案，內容同步自 `HARNESS/CLAUDE.md`
- [.archive/](file:///home/yao/projects/harness-engineering/.archive) - 已封存的實作計畫目錄
- [.issues/](file:///home/yao/projects/harness-engineering/.issues) - 問題/教訓紀錄目錄（harness-install、windows-encoding、solidify-root-claude）

## skills/ - Claude Code 專案層級 skills
### harness-install/
- [SKILL.md](file:///home/yao/projects/harness-engineering/skills/harness-install/SKILL.md) - 安裝精靈：symlink、env.md 訪談、健康檢查、導覽
- [CLI-TOOLS-GUIDE.md](file:///home/yao/projects/harness-engineering/skills/harness-install/CLI-TOOLS-GUIDE.md) - CLI 工具選擇使用指南

### mattpocock-workflow/
- [SKILL.md](file:///home/yao/projects/harness-engineering/skills/mattpocock-workflow/SKILL.md) - Matt Pocock 技能庫與 Harness 規範結合的端到端工作流技能

## HARNESS/ - 制度檔案目錄
- [CLAUDE.md](file:///home/yao/projects/harness-engineering/HARNESS/CLAUDE.md) - 入口：核心規則＋路由表
- [AI-INSTRUCTIONS-MAPPING.md](file:///home/yao/projects/harness-engineering/HARNESS/AI-INSTRUCTIONS-MAPPING.md) - AI 代理指令檔完整位置對應表
- [diagnosis.md](file:///home/yao/projects/harness-engineering/HARNESS/diagnosis.md) - harness 三大問題診斷
- [model-dispatch.md](file:///home/yao/projects/harness-engineering/HARNESS/model-dispatch.md) - 派工紀律
- [judgment-rubrics.md](file:///home/yao/projects/harness-engineering/HARNESS/judgment-rubrics.md) - 五套判準表
- [delegation-templates.md](file:///home/yao/projects/harness-engineering/HARNESS/delegation-templates.md) - 派工 prompt 模板
- [maintenance-protocol.md](file:///home/yao/projects/harness-engineering/HARNESS/maintenance-protocol.md) - 制度檔修改權限與維護協議
- [letter-to-future-sessions.md](file:///home/yao/projects/harness-engineering/HARNESS/letter-to-future-sessions.md) - 給未來 session 的環境說明
- [plan-template.md](file:///home/yao/projects/harness-engineering/HARNESS/plan-template.md) - 實作計畫範本
- [env.example.md](file:///home/yao/projects/harness-engineering/HARNESS/env.example.md) - 個人環境配置範本
- [README.md](file:///home/yao/projects/harness-engineering/HARNESS/README.md) - 制度檔細部用途說明
- [select-cli-tools.py](file:///home/yao/projects/harness-engineering/HARNESS/select-cli-tools.py) - 互動式 AI CLI 工具選擇器
- [install.py](file:///home/yao/projects/harness-engineering/HARNESS/install.py) - 安裝與連結腳本
- [install-skills.py](file:///home/yao/projects/harness-engineering/HARNESS/install-skills.py) - 全域 skills 安裝腳本
- [skills-manifest.txt](file:///home/yao/projects/harness-engineering/HARNESS/skills-manifest.txt) - 全域通用工具 skills 安裝清單
- [skills-manifest-workflow.txt](file:///home/yao/projects/harness-engineering/HARNESS/skills-manifest-workflow.txt) - 全域工作流程 skills 安裝清單
- [check_harness.py](file:///home/yao/projects/harness-engineering/HARNESS/check_harness.py) - 健康檢查腳本
- [uninstall.py](file:///home/yao/projects/harness-engineering/HARNESS/uninstall.py) - 卸載還原腳本

### rules/ - 子制度檔案目錄
- [tools.md](file:///home/yao/projects/harness-engineering/HARNESS/rules/tools.md) - 工具使用規範 (rtk, ctx7 等)
- [preprocess.md](file:///home/yao/projects/harness-engineering/HARNESS/rules/preprocess.md) - 文件 / PDF / Office / 圖片分析前處理規範
- [git.md](file:///home/yao/projects/harness-engineering/HARNESS/rules/git.md) - Git commit, MR 與憑證安全規範
- [workflow.md](file:///home/yao/projects/harness-engineering/HARNESS/rules/workflow.md) - plan.md, .issues, tree.md 工作流程
- [mattpocock-workflow.md](file:///home/yao/projects/harness-engineering/HARNESS/rules/mattpocock-workflow.md) - 高階軟體工程實作工作流條文
- [dotnet.md](file:///home/yao/projects/harness-engineering/HARNESS/rules/dotnet.md) - .NET 與 Cucumber 開發原則
- [python.md](file:///home/yao/projects/harness-engineering/HARNESS/rules/python.md) - Python 開發原則（uv）
- [omc.md](file:///home/yao/projects/harness-engineering/HARNESS/rules/omc.md) - oh-my-claudecode (OMC) 多代理協作層
