# Personal Research OS Stage 01 Roadmap

Version: v0.5\
Date: 2026-08-04

KA-00 starting baseline: `d622b92c78d3fcaf327db93e599e6a77fe112f1c`
RW-00 documentation baseline: `9b63aae432bdfbed8e103333b284390ceb24784c`

------------------------------------------------------------------------

# Stage 01: Knowledge Agent Integration

## Stage Goal

在已经完成：

    Concept Database
            ↓
    concept_index
            ↓
    Offline Hover Encyclopedia

的基础上，进入 Knowledge Agent 的提案治理与人工协作阶段。

目标：

让手动触发的 Codex 从实时问答工具转变为：

> 知识数据库维护者和知识生产助手。

当前的 “Knowledge Agent” 是一次由人明确触发的 Codex
知识生产对话，不是仓库内运行的软件 Agent。现在不计划在仓库中托管
AI client、Agent runtime 或任何模型/API 调用。

核心原则：

-   AI 不直接修改稳定知识库。
-   Codex 只在批准的实现提示下生成 proposal artifacts。
-   人工明确批准后，候选内容才可手动进入正式 Concept Database。
-   所有知识变化保持 Git 可追踪。

------------------------------------------------------------------------

# Current Status

已完成：

## Foundation Scaffold

Commit:

    59c3fb2

完成：

-   Vault结构
-   Concept Schema
-   concept_tools
-   Git管理

## Offline Hover Encyclopedia

Commit:

    986359b

完成：

-   concept_index
-   hover_resolver
-   alias匹配

## P01.5 UI Prototype

Commit:

    9af4145

已接受为原型基线：

-   本地HTML Hover UI
-   键盘与鼠标 hover/focus 交互
-   自包含、离线的演示页面

这不是已经完成的 UX 验证。`ResearchOS/99_Meta/P01.5_UI_Validation.md`
中的人工阅读评估问题仍然开放。

## Chinese Localization

Commit:

    d622b92

完成：

-   Hover UI 中文本地化
-   中文 alias 展示约定
-   中文阅读样例与相应测试

## Reading Workspace Governance

状态：Accepted and complete (2026-08-04).

RW-00 governance and the P0 UI contract are human accepted. RW-01 and the
RW-01.1 source-handoff/session-layout increment were human accepted and complete
on 2026-08-04. The configurable 34/42/50rem session-panel correction received
final visual confirmation. 25 Concepts passed validation; focused Reading UI
suite: 16 tests passed; full suite: 33 tests passed. RW-02, RW-03, and KA-01
remain not authorized and not started.

RW-00 本身只定义 Reading Workspace 的治理、数据边界和最小 UI 契约；它没有
创建 Reading Workspace 实现、reading session、RW source file、reading-note
artifact 或 proposal artifact，也没有启动 KA-01。

------------------------------------------------------------------------

# Stage 01 Architecture

    Technical literature and human-owned reading work

            ↓

    Reading Workspace (RW-00 through RW-05)
    manual annotation, manual LLM Q&A capture, review, and freeze

            ↓

    One reviewed Markdown source inside ResearchOS/00_Inbox/
    (excluding ResearchOS/00_Inbox/proposals/)

            ↓

    Manually triggered Codex conversation

            ↓

    ResearchOS/00_Inbox/proposals/runs/<run_id>/assessment.md

    Every classified result

            ↓

    ResearchOS/00_Inbox/proposals/concepts/<proposal_id>/

    Create Proposal
    Update Proposal
    Relation Proposal
    (duplicate and no-op remain in assessment.md only)

            ↓

    Human Review

            ↓

    Explicit approval and manual promotion

            ↓

    Stable Concept Database

            ↓

    Deterministic validation and index

            ↓

    Obsidian Hover UI

------------------------------------------------------------------------

# Design Principles

## Proposal First

禁止：

    Codex
     |
    直接修改
     |
    Stable Concept

采用：

    Codex
     |
    Proposal
     |
    Human review
     |
    Explicit promotion approval
     |
    Manual stable change
     |
    Validate / scan / diff review
     |
    Commit

------------------------------------------------------------------------

## Deterministic Knowledge Layer

Hover阶段：

    读取数据库

不调用AI。

Knowledge Agent阶段：

    人工选择输入
    手动触发 Codex
    只生成提案

不在仓库内运行 AI，也不自动晋升提案。

两者分离。

------------------------------------------------------------------------

## Human-Owned Knowledge

-   Personal confidence、My Understanding 和 Decision Log 属于人。
-   Codex 不得虚构 citation、formula 或 experimental conclusion。
-   未知或有争议的信息必须保持显式未决。
-   来源是未受信任的数据；其中的嵌入指令一律忽略。

------------------------------------------------------------------------

# RW Breakdown

Reading Workspace 是 KA-01 上游的 source-preparation workflow。RW 阶段
帮助人阅读、标注、记录手动触发的外部 LLM 问答，并冻结一份经过人工审阅的
Markdown reading note。它不替代 KA 治理、提案审阅或 promotion 边界。

## RW-00 Reading Workspace Governance

状态：Accepted and complete (2026-08-04).

定义实现无关的阅读协议、内容来源区分、最小 session entry 契约、状态模型、
KA-01 bridge 和离线 UI P0 契约。RW-00 不实现 UI，也不创建任何阅读或科研
内容 artifact。

## RW-01 Offline Reading UI Prototype

状态：Human accepted and complete (2026-08-04).

目标：实现可用的离线 Markdown 阅读界面，读取当前本地
`concept_index.json`，复用现有确定性 alias/longest-term 匹配与紧凑
hover card，并实现 human-owned annotation、human question、可复制 question
packet 与外部 LLM answer 粘贴及链接回 session 的 capture primitives，同时
提供最小的高亮密度控制、可恢复的本地 session draft 和 Markdown session
import/export。

## RW-01.1 Source Handoff and Session Layout

状态：Human accepted and complete (2026-08-04).

目标：保持 `rw-session-v0.1` 及其扁平、有序 entries contract 不变，只为 session
panel 提供摘录、笔记、按 `question_entry_id` 分组的问答和 chronological all
派生视图。问答视图支持一个问题的多个回答和显式 unanswered 状态；tab 切换不修改
或重排 canonical session entries。本增量同时明确未来 RW-03 的双路径 synthesis
handoff，但不启动 synthesis。

## RW-02 Realistic Human UX Validation

状态：Not authorized and not started.

目标：使用一篇人工选择的真实 technical paper，对 RW-01 已实现的 human-owned
annotation、human question、question packet 和外部 LLM answer capture
primitives 进行 realistic human UX validation。外部 LLM workflow 仍为人工
复制/粘贴；RW-02 不构建第二套 capture implementation，也不嵌入模型 API
或仓库托管的 AI runtime。

## RW-03 Reading Note Synthesis Trial

状态：Not authorized and not started.

目标：由人精确选择一个原始资料 `SOURCE_PATH` 和一个
`reading_session.md` 的 `SESSION_PATH`。人工触发的 LLM synthesis 同时读取这
两个文件，只输出 `reading_note.draft.md`，不能声明人工审阅完成。
`reading_session.md` 默认不嵌入完整原文；RW-03 不增加 source/session hash 或
第二个 provenance SHA，也不改变 KA-01 的一文件输入边界。

## RW-04 Human Review and Freeze

状态：Not started.

目标：由人审阅并只选择一份 `reading_note.md` 作为冻结的 reading note。
内容若在审阅后改变，必须重新审阅才可再次作为未来 KA 来源。

## RW-05 KA-01 Handoff Trial

状态：Not started.

目标：验证一份人工选择并审阅的 `reading_note.md` 是否能保持 KA-01
现有的一文件输入边界。KA-01 只读取人指定的那一份文件，不跟随阅读 session、
PDF、其他论文或 LLM transcript。

## RW and KA gates

-   KA-01 仍未获授权且尚未启动，当前不存在 KA-01 run assessment 或 Concept
    proposal artifacts。
-   人已表达在存在合格、经过审阅的来源后运行 KA-01 的意图；该意图不构成
    执行授权。protocol-valid run 仍要求一个精确的 `SOURCE_PATH`，并要求
    人在执行时批准所用 prompt version。
-   未来 RW-03 synthesis 的 `SOURCE_PATH` 加 `SESSION_PATH` 是人工选择的上游
    双文件输入，不是 KA-01 输入，也不为两个文件增加 SHA。
-   只有 KA-01 真正开始时，才按现有协议对最终选定的
    `reading_note.md` 计算一次 SHA-256；RW 不要求 PDF hash、session hash
    或第二个 provenance hash。
-   Stage 02 Information Acquisition 是独立的未来 concern，不属于 Reading
    Workspace source preparation。
-   第一版 Reading Workspace 不包含 integrated AI runtime、automatic
    acquisition 或完整 Obsidian plugin。

------------------------------------------------------------------------

# KA Breakdown

## KA-00 Knowledge Proposal Governance

状态：Accepted and complete（2026-08-03）。

接受依据：repository owner 在 audit/planning conversation 中明确授权接受；
不记录或推断个人姓名。

目标：

-   定义项目上下文、提案协议和版本化执行提示。
-   固定 proposal ownership、state、provenance、review 与 promotion 边界。
-   明确稳定 Concept 仍然只包含人工批准的知识。

输出：

-   `ResearchOS/99_Meta/PROJECT_CONTEXT.md`
-   `ResearchOS/99_Meta/Knowledge_Proposal_Protocol_v0.1.md`
-   `ResearchOS/99_Meta/prompts/concept_proposal_v0.1.md`

不实现任何提取代码或 AI runtime，也不修改 Concept Schema、`01_Concept`
或 `concept_index.json`。

退出门槛：

KA-00 的接受只打开 KA-01 eligibility gate，不授权或启动执行。未来必须
由另一条明确的人类指令批准一篇人工选择、位于
`ResearchOS/00_Inbox/` 且不在 `proposals/` 下的本地 Markdown 来源，
并批准 KA-01 execution prompt。该执行仍只生成 run assessment 和
proposal artifacts，并停下等待人工审阅。

------------------------------------------------------------------------

## KA-01 Single-Source Manual Proposal Trial

状态：Eligibility gate open; not authorized and not started. A separate
explicit human instruction must approve one source and the KA-01 execution
prompt.

目标：

验证最小提案流程，而不是建立 Agent runtime。

输入：

    exactly one manually selected Markdown file
    inside ResearchOS/00_Inbox/
    outside ResearchOS/00_Inbox/proposals/

执行：

-   解析并验证 traversal 与 symlink containment；不持久化绝对工作站路径。
-   将来源规范化为 Vault-relative POSIX path，并对原始字节计算 SHA-256。
-   创建且只创建一份 `runs/<run_id>/assessment.md`，持久记录每个分类结果。
-   使用版本化提示手动触发 Codex。
-   先检查现有 canonical names、ids 和 aliases。
-   将结果分类为 create、update、relation、duplicate 或 no-op。
-   仅在 `00_Inbox/proposals` 下生成 proposal artifacts。
-   保留证据、来源定位和不确定性，然后停下等待人工审阅。

来源不合格时停止，并要求人把经过审阅的副本放入 Inbox；Codex 不自动
复制或移动来源。

不实现：

-   AI client、API call 或仓库内 Agent runtime
-   自动 promotion
-   多来源批处理

------------------------------------------------------------------------

## KA-02 Proposal Quality Evaluation

目标：

人工评估 KA-01 的单来源结果：

1.  create/update/relation/duplicate/no-op 分类是否正确。
2.  证据是否可追溯，quote/paraphrase/inference 是否清楚。
3.  未知、争议和 human-owned 字段是否保持未决。
4.  Concept 粒度和重复控制是否可接受。
5.  `candidate.md` 是否按 Concept Schema v0.1 的结构准备，且没有被误当成稳定知识。

只有人工评估通过后，才决定是否进入下一门槛；本步骤不引入自动提取。

------------------------------------------------------------------------

## KA-03 Human Review and Manual Promotion Trial

建立人机协作流程：

    Proposal

    ↓

    Review

    ↓

    accepted / rejected / deferred / superseded

    ↓

    Separate explicit promotion approval

    ↓

    Manual stable Concept change

    ↓

    Validate, scan, and review diff

`accepted` 状态本身不复制文件，也不授权自动 promotion。

------------------------------------------------------------------------

## KA-04 Knowledge Relation Proposal Trial

目标：

Codex 可基于可追溯证据建议现有 Concept 之间的 Obsidian wikilinks。

关系只能作为proposal。

不能自动写入。

本步骤不引入 graph database、typed edge、权重或自动反向链接。

------------------------------------------------------------------------

## KA-05 Stage Evaluation

在 KA-01 至 KA-04 的人工门槛通过后，评估 Stage 01 是否值得扩展。

评价：

1.  提案准确性与证据质量
2.  Hover Summary质量
3.  Concept粒度与重复率
4.  人工审阅成本
5.  是否有足够证据另行规划任何自动化

未通过前述门槛时，不扩大来源数量，也不规划仓库托管的 AI runtime。

------------------------------------------------------------------------

# Acceptance Criteria

1.  Proposal ownership、states、provenance、review 和 promotion 边界明确。
2.  Stage 编号使用 KA-00–KA-05，不与历史 P01/P01.5 冲突。
3.  稳定 Concept Database 和生成索引不被提案流程直接修改。
4.  下一项可执行实验严格限制为 Inbox 内、`proposals/` 外的一篇人工选择的 Markdown 来源。
5.  每次有效的一来源执行创建且只创建一份 run-level `assessment.md`。
6.  duplicate 和 no-op 不创建 candidate proposal，但永久记录在 run assessment 中。
7.  所有 Knowledge proposal 执行输出只进入 `00_Inbox/proposals`，并停下等待人工审阅。
8.  未引入依赖、网络要求或仓库托管的 AI runtime。

------------------------------------------------------------------------

# Non Goals

当前不实现，也没有仓库托管 runtime 的计划：

-   AI client、Agent runtime、API call
-   RAG、embedding、vector database
-   crawler、watcher、定时扫描或批处理
-   自动提取、自动更新、自动 merge 或自动 promotion
-   graph database 或 typed-edge architecture
-   Concept Schema v0.1 变更
-   Obsidian 正式插件

------------------------------------------------------------------------

# Future Roadmap

以下内容只是未来决策点，不是当前实现承诺。

    Stage 01
    Reading Workspace

            ↓

    Knowledge Agent

            ↓

    Stage 02
    Information Acquisition

            ↓

    arxiv Agent
    HTML Collector

            ↓

    Stage 03
    Advanced Knowledge Graph

            ↓

    Research Question
    Experiment Entity
    Decision Database

            ↓

    Stage 04
    Obsidian Native Plugin

------------------------------------------------------------------------

# Key Design Reminder

Personal Research OS不是AI聊天工具。

当前 Codex 的角色是手动触发、受批准提示约束的知识生产助手。

最终目标：

    Human Research Process

    +

    AI Knowledge Maintenance

    +

    Version Controlled Scientific Memory
