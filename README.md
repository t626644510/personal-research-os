# Personal Research OS v0.1

Personal Research OS 是一个以 Obsidian 为阅读界面、Git 为审计与版本层、Python 为确定性维护工具的个人科研知识库。v0.1 以稳定的 Concept Database 和 Hover Encyclopedia 数据为基础，并包含最小 Obsidian Foundation、RW-03 人工审阅草稿入口和 RW-04 冻结阅读笔记；不包含 RAG、向量数据库、AI 实时查询、自动爬虫或定时扫描。

## 快速开始

1. 在 Obsidian 中选择 `ResearchOS/` 作为 Vault。
2. 从 `ResearchOS/Home.md` 进入 Vault 导航。
3. 通过 `[[Concept name]]` 建立概念链接；Obsidian 原生悬浮预览可直接查看 Concept 笔记。
4. 新建概念时复制 `ResearchOS/99_Meta/templates/Concept.md`，按 Schema 填写后再放入 `ResearchOS/01_Concept/`。
5. 在仓库根目录运行校验和索引生成：

```powershell
python ResearchOS/99_Meta/tools/concept_tools.py validate
python ResearchOS/99_Meta/tools/concept_tools.py scan
python ResearchOS/99_Meta/tools/hover_resolver.py "HOM impedance and wake field"
```

工具只依赖 Python 3.9+ 标准库。`scan` 会先校验全部 Concept，并检查 ID、规范名称和别名冲突；只有全部通过时才会原子更新 `ResearchOS/99_Meta/concept_index.json`。若 Windows 已安装 Python Launcher 但 `python` 不在 `PATH`，把上述命令中的 `python` 换成 `py -3.9`（或已安装的对应版本）。

## 数据结构

```text
ResearchOS/
├── Home.md                  # Vault 导航入口
├── 00_Inbox/
│   ├── reading/<paper_id>/  # source record、RW-03 draft、RW-04 final note 与本地阅读 bundle
│   │   └── _local/          # ignored；论文、session、译文与展示产物不提交
│   ├── papers/              # 待处理论文
│   ├── html/                # 待处理网页快照
│   └── notes/               # 临时记录
├── 01_Concept/              # 稳定概念节点；Hover 数据的唯一来源
├── 02_Project/
│   └── 1500 MHz TM020 Harmonic Cavity.md  # 当前项目页
├── 03_Paper/                # 论文级笔记与阅读结论
├── 04_Experiment/           # 实验/仿真设置、运行和结果
├── 05_Tool/                 # 软件与可复用操作流程
└── 99_Meta/
    ├── Concept_Schema_v0.1.md
    ├── concept_index.json
    ├── templates/
    │   ├── Concept.md
    │   ├── Project.md
    │   ├── Paper.md
    │   └── Reading_Note.md
    └── tools/
        ├── concept_tools.py
        ├── hover_resolver.py
        ├── hover_ui.py
        ├── reading_ui.py
        ├── reading_ui.js
        └── reading_ui.css
```

## Obsidian Foundation / RW-03 / RW-04

`ResearchOS/Home.md` 是当前 Vault 导航入口。当前 Project 是
`ResearchOS/02_Project/1500 MHz TM020 Harmonic Cavity.md`，当前主阅读笔记是
`ResearchOS/00_Inbox/reading/ipac2019-weprb066/reading_note.md`；RW-03 草稿仍作为历史记录保留在
`ResearchOS/00_Inbox/reading/ipac2019-weprb066/reading_note.draft.md`。

`Project.md` 用于项目目标、边界、决策与行动；`Paper.md` 用于后续论文级记录；
`Reading_Note.md` 用于 mandatory source/session 加 optional external summary 的阅读
综合草稿。当前没有 `ResearchOS/03_Paper/IPAC2019-WEPRB066.md` 或共享 `.obsidian/` 配置。
最终 `reading_note.md` 已由 RW-04 从明确接受的 RW-03 内容冻结，状态为
`human_reviewed`。RW-03 synthesis content human accepted on 2026-08-18;
selected-text presentation correction applied; RW-03 accepted and complete and
published at commit `7c5dc4f`。RW-04 accepted and complete and published at
commit `fb0538c`。`reading_note.draft.md` 仍为 `state: draft` 的 RW-03 历史记录；
最终笔记已作为唯一来源选择用于已接受的 KA-01 run
`ka01-20260818t065446z-67f9fb66`，使用 prompt `v0.1`，分类为 5 create / 16
duplicate / 7 no-op。RW-05 accepted and complete；KA-01 accepted and complete
as a one-source manual proposal trial。KA-02 已完成人工评估和审计收口；KA-03
Stage 2 已在 owner-01 的明确人工门后完成：P01/P03 accepted and promoted，
P02 superseded by P01，P04/P05 deferred。KA-04 remains unstarted and
unauthorized。

每个 Concept 的稳定身份由 YAML `id` 提供，文件名和 H1 是规范显示名称，`aliases` 保存缩写、译名和历史名称。正文遵循固定的十个 H2 区块；详细约束见 [Concept Schema v0.1](ResearchOS/99_Meta/Concept_Schema_v0.1.md)。

生成的索引格式为：

```json
{
  "Concept name": {
    "path": "01_Concept/Concept name.md",
    "aliases": ["alternate name"],
    "hover_summary": "A short, stable summary.",
    "id": "concept_id",
    "category": ["research domain"],
    "related_concepts": ["Related concept"]
  }
}
```

`concept_index.json` 是派生数据，不手工编辑。P01 保留了原有的 `path`、`aliases` 和 `hover_summary`，因此旧消费者仍可工作；新增字段提供稳定 ID、分类和规范化关系。路径统一使用 Vault 相对的 `/` 分隔形式，因此索引可在 Windows、macOS 和 Linux 间复用。

## 离线悬浮概念百科原型

`hover_resolver.py` 只读取本地 JSON，不进行 AI 或网络调用。它在输入 Markdown 中匹配规范名称与 aliases，大小写不敏感，并在同一位置优先选择最长词组。例如 `HOM impedance` 会优先于别名 `HOM`。输出按文本位置排序，每个非重叠命中包含位置、规范名称、匹配词、摘要和索引元数据。

直接解析一段 Markdown：

```powershell
py -3.9 ResearchOS/99_Meta/tools/hover_resolver.py "HOM impedance overlaps the bunch spectrum."
```

解析 UTF-8 Markdown 文件：

```powershell
py -3.9 ResearchOS/99_Meta/tools/hover_resolver.py --file ResearchOS/00_Inbox/notes/example.md
```

Python API：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path("ResearchOS/99_Meta/tools").resolve()))
from hover_resolver import load_concept_index, resolve_mentions

index = load_concept_index()
matches = resolve_mentions("Wake field and HOM impedance", index)
```

P01 有意扫描原始 Markdown 字符串，不解析 Markdown AST；因此 fenced code、inline code、frontmatter 和 link target 中出现的词也可能命中。后续若真实使用场景证明需要，再增加确定性的 Markdown 区域屏蔽，不在本阶段引入解析依赖。

运行测试：

```powershell
py -3.9 -m unittest discover -s tests -v
```

## 悬浮概念百科 UI 验证

P01.5 在现有解析器之后增加一个最小展示层，用于评估概念高亮密度、摘要长度和阅读干扰。它不改变 Concept Schema、索引格式或匹配规则，也不是 Obsidian 插件。`hover_ui.py` 将一篇 UTF-8 Markdown 笔记和本地 `concept_index.json` 合成为单个自包含中文 HTML 文件；样式全部内联，不启动服务器，不加载网络资源，也不调用 AI。

先校验 Concept 并重新生成本地索引：

```powershell
python ResearchOS/99_Meta/tools/concept_tools.py validate
python ResearchOS/99_Meta/tools/concept_tools.py scan
```

生成并打开示例笔记的演示页：

```powershell
python ResearchOS/99_Meta/tools/hover_ui.py "ResearchOS/00_Inbox/notes/HOM impedance reading note.md" --open
```

默认输出到操作系统临时目录中的 `personal-research-os-hover-demo.html`，命令会打印绝对路径。若浏览器无法自动打开，可手工打开该文件；也可通过 `--output <path>` 指定位置。把鼠标停在绿色高亮词上，或使用 Tab 键聚焦，即可看到概念名称、悬浮摘要、分类和相关概念。卡片不会展示完整 Concept、公式、来源或决策记录。

### 中文与 aliases 约定

- `id`、英文 canonical name、Concept 文件名和索引键保持稳定。
- `Hover Summary` 等 Schema 标题继续使用英文，作为校验器依赖的稳定结构；标题下的知识内容以中文为主。
- 中文术语、英文缩写和历史名称通过 `aliases` 多对一映射到 canonical name；扫描器继续禁止不同 Concept 共用同一 alias。
- 中文笔记既可写 canonical name，也可直接写中文 alias。卡片优先显示“中文 alias（英文 canonical name）”；没有中文 alias 时回退到 canonical name。
- `category` 在索引中继续使用稳定英文值，HTML 只在展示层转换为中文标签，不回写 Concept 数据。
- 避免使用“场”“模”等过短中文 alias，以减少无词边界文本中的子串误命中。
- 页面声明为 `zh-CN`，使用中文系统字体，并从笔记首个 H1 提取中文页面标题。

可用于人工比较的真实阅读样例位于 `ResearchOS/00_Inbox/notes/`：

- `HOM impedance reading note.md`（高次模阻抗阅读笔记）
- `CST wakefield solver note.md`（CST 尾场求解器设置笔记）
- `Q0 measurement note.md`（Q0 测量笔记）
- `PSO impedance fitting note.md`（PSO 阻抗拟合笔记）

逐个替换上述命令中的输入文件即可检查不同概念密度和 alias 命中。自动验证运行：

```powershell
python -m unittest discover -s tests -v
```

演示页有意保留经过 HTML 转义的 Markdown 源文本及其换行，而不实现完整 Markdown 渲染；P01.5 只验证 Hover 交互是否帮助阅读。修改 Concept 或索引后应重新执行 `scan` 并再次生成页面，因为 HTML 是当时本地索引的静态快照。人工评估问题与已知限制记录在 [P01.5 UI Validation](ResearchOS/99_Meta/P01.5_UI_Validation.md)。

## Reading Workspace UI Prototype

RW-01 与 RW-01.1 session-layout 增量已在 commit 8afa9aa 由人工接受并完成（2026-08-04）。
可配置的 34/42/50rem session-panel 修正已获得最终视觉确认；25 Concepts 通过验证，
Focused Reading UI suite 通过 16 项测试，Full suite 通过 33 项测试。

RW-02.1 是一次窄范围的 presentation correction，不是架构重设计：英文
`source.reading.md` 仍是唯一权威阅读源，PDF 仍是图形视觉权威；Figure 1–7 使用
本地 PNG 裁剪并以内联 data URI 显示。可选的 `source.zh-CN.reading.md` 是机器/LLM
辅助、未验证的派生参考译文，不重复图形、不进入 `rw-session-v0.1`。RW-02.1 当时
只有英文面板的选择可以创建 session entry；中英面板不做同步选区或 overlay；远程
图片资源始终禁止。这些是历史事实，RW-02.2 只修正后续真实阅读发现的可用性边界。

2026-08-11 的真实人工阅读发现五项问题：中英文需要按小节横向对应，中文参考译文
需要支持个人笔记和问题，已批注正文块需要明显标记，图和表需要独立成栏并独立滚动，
以及 4K 屏幕需要可拖动栏宽。RW-02.2 status: **Human UI accepted on
2026-08-11**。当前实现按 18 个同序 H1/H2/H3 边界形成小节行；中文参考选区只允许
`human_note` 和 `human_question`，禁止 `source_excerpt`；正文标记由 canonical
entries 派生；Figure 1–7 与 Table 1–2 只从英文权威来源提取到独立图表栏；桌面布局
提供三个可访问 resizer。`_local/reading_session.md` 是五条旧英文条目的原样本地
副本；`_local/external_llm_conversation_summary.md` 仍是 unverified、
session-external 的外部 LLM 辅助材料，没有进入 session。

RW-02.2 当前自动验证：25 个 Concepts 通过校验，Reading UI 聚焦套件 32 项、完整
套件 49 项均通过；离线 HTML 为 974,523 bytes，含 18 组双语小节、7 张图、2 张
渲染表、3 个可访问 resizer 和 131 个唯一可标注源块。这些工程验证指标独立于人工
验收记录，不得用 RW-02.1 的历史指标替代。Repository owner 于 2026-08-11 给出的
总体人工 UI 结论为“通过，未报告其他问题”。RW-02 已接受并完成，HTML 原型已冻结；
commit `792c802` 是已发布的 RW-02 baseline。RW-03 已于 2026-08-11 另行授权；
RW-03 synthesis content human accepted on 2026-08-18; selected-text
presentation correction applied; RW-03 accepted and complete and published at
commit `7c5dc4f`。最终 `reading_note.md` 已冻结为 `state: human_reviewed`；
`reading_note.draft.md` 仍作为 RW-03 历史记录保留。RW-04 accepted and complete
and published at commit `fb0538c`。RW-05 accepted and complete；KA-01 accepted
and complete as a one-source manual proposal trial in run
`ka01-20260818t065446z-67f9fb66`，使用 prompt `v0.1`，分类为 5 create / 16
duplicate / 7 no-op；At the KA-01 publication boundary, all five proposals
were proposed and KA-02/KA-03 had not started. KA-02 completed; KA-03 Stage 2
completed under reviewer `owner-01`; P01/P03 were accepted and manually
promoted; P02 was superseded by P01; and P04/P05 were deferred. KA-04 remains
unstarted and unauthorized.
这个原型是 `concept_index.json` 的第二个本地确定性消费者，
不替换 P01/P01.5：
`reading_ui.py` 读取一篇 UTF-8 Markdown 技术资料，复用
`hover_resolver.resolve_mentions()`，再把维护用的 `reading_ui.css` 与
`reading_ui.js` 内联为一个自包含 HTML 阅读工作区。页面不需要服务器、Node/npm、
网络资源、模型 API 或新增 Python 依赖。

在仓库根目录生成并打开工作区：

```powershell
py -3.9 ResearchOS/99_Meta/tools/reading_ui.py `
  "ResearchOS/00_Inbox/notes/HOM impedance reading note.md" --open
```

默认输出是系统临时目录中的
`personal-research-os-reading-workspace.html`。可用 `--index` 指定只读本地索引，
用 `--output` 指定另一个仓库外 HTML 路径。生成页只保存文件名或 Vault 相对来源标签，
不会把绝对工作站路径写入会话导出。

使用流程：

1. 在正确渲染的标题、段落、列表、链接与代码中阅读资料；概念卡片支持鼠标悬浮和
   键盘聚焦。
2. 使用工具栏切换全部出现、每段首次或每节首次高亮，也可关闭高亮、静音某个
   canonical Concept 或仅静音当前匹配词，并随时恢复。
3. 选择英文正文或图表文本，可创建来源摘录、个人笔记或人类问题；选择中文参考译文
   只能创建个人笔记或人类问题，不能保存来源摘录。新条目以可选的
   `selected_text_origin` 区分 `authoritative_source` 与
   `reference_translation`，并可记录 `selected_block_id`；旧条目缺少这两个字段时
   保持原样。`author_type` 仍由 `entry_type` 决定并只读。
4. 对人类问题打开“问题包”，由人复制到外部 LLM；再把回答手动粘贴回来，选择对应
   问题并可填写模型标签。页面不会发送问题、调用模型或自动获取回答。
5. 每次会话变更都会尝试写入该来源专属的浏览器本地恢复数据，并显示已保存、未保存、
   可恢复或保存失败状态。重新加载或重新打开同一生成页时会显式提供恢复选择；清除
   恢复数据必须由人确认。
6. “导出会话 Markdown”生成一个 UTF-8、可读且可 Git 审阅的
   `rw-session-v0.1` 文件，其中的 fenced JSON 是无损权威载荷。再次导入前会校验
   字段类型、枚举、唯一 ID、`author_type` 不变量和问题链接；无效导入不会替换当前
   会话，覆盖非空工作也必须确认。

RW-01.1 只改变 session panel 的派生视图：摘录、笔记、问答和全部。摘录与笔记按
类型过滤；问答按 `human_question.entry_id` 与每个 `llm_answer.question_entry_id`
配对，支持一个问题的多个回答并明确显示尚无回答的问题。桌面端问题与回答并排，窄屏
堆叠。标签切换不会改变或重排 canonical `state.entries`；`rw-session-v0.1` 仍导出
同一份扁平、有序 entries 列表，旧版 session Markdown 可继续导入。

RW-01.1 的历史修正保留紧凑（34rem）、平衡（42rem，默认）和宽屏（50rem）三种
会话栏预设。RW-02.2 移除桌面工作区的 `100rem` 最大宽度，并在双语桌面布局中提供
英文/中文、正文/图表、图表/会话三个 resizer；它们支持 Pointer Events、键盘方向键、
最小宽度 clamp 和双击重置。拖动会话栏后预设显示“自定义”，重置后恢复 Balanced。
布局只写入容错的 presentation localStorage；不进入 session preferences、canonical
recovery、`sessionPayload()`、session id、entries 或 Markdown export。窄屏隐藏
resizer 并恢复无页面级横向滚动的堆叠布局。

RW-03 必须由人精确选择一个原始资料 `SOURCE_PATH` 和一个
`reading_session.md` 的 `SESSION_PATH`，两者是强制输入。只有人对本次运行明确选择
`EXTERNAL_SUMMARY_PATH` 时，人工触发的 LLM synthesis 才能额外读取一份外部总结；
该总结始终是 unverified、session-external、非论文权威且不代表
`human_reviewed`。回答读取有两个独立 provenance channel：`SESSION_PATH` 内的
canonical `llm_answer`，以及 session 外的人选 optional external summary；本次 session
没有 `llm_answer`，只有 2 个 `human_question` 和 3 个 `human_note`。不得把外部总结
拆成 session entries、提升为 paper/source/human content，或用单一来源标签混合两个
channel。未来可合并重复措辞，但必须保留各自来源标签。RW-03 不为 source、session
或 external summary 新增 SHA 或其他 fingerprint。这个上游 synthesis 边界不改变
KA-01：KA-01 仍只读取人类选择并审阅的一份 `reading_note.md`，并只在 KA-01 真正
开始时计算现有的一次 Markdown SHA-256。

RW-01 不生成 `reading_note.draft.md` 或最终 `reading_note.md`，不处理 PDF 文本层、
OCR 或坐标覆盖。内置 Markdown 渲染器支持标题、段落、扁平有序/无序列表、链接、
行内代码、围栏代码块、相对路径本地 PNG/JPEG/WebP 图片，以及项目所需的最小安全
GFM pipe table；表格单元格和原始 HTML 均先转义。Figure 1–7 和 Table 1–2 在图表栏
各出现一次，正文原位只保留跳转占位。远程、绝对路径、越界、符号链接逃逸、缺失和
不支持格式仍显示安全占位符。嵌套列表、强调、脚注、任务列表等完整 Markdown 语法
仍未实现。提供 `--reference-translation` 时才启用英文原文、中英并列、中文参考三种
presentation mode；中文参考仍是未验证、非权威派生显示。RW-02.2 human UI was
accepted on 2026-08-11; RW-02 is accepted and complete; the HTML prototype is
frozen; commit `792c802` is the published RW-02 baseline. RW-03 synthesis
content human accepted on 2026-08-18; selected-text presentation correction
applied; RW-03 accepted and complete and published at commit `7c5dc4f`. The
final `reading_note.md` is `state: human_reviewed`; `reading_note.draft.md`
remains available as RW-03 history. RW-04 is accepted and complete and published
at commit `fb0538c`. RW-05 is accepted and complete; KA-01 is accepted and
complete as a one-source manual proposal trial in run
`ka01-20260818t065446z-67f9fb66` using prompt `v0.1`, with 5 create / 16
duplicate / 7 no-op. At the KA-01 publication boundary, all five proposals
were proposed and KA-02/KA-03 had not started. KA-02 completed; KA-03 Stage 2
completed under reviewer `owner-01`; P01/P03 were accepted and manually
promoted; P02 was superseded by P01; and P04/P05 were deferred. KA-04 remains
unstarted and unauthorized. 实现与验收记录在
[RW-02 UI Validation](ResearchOS/99_Meta/RW02_UI_Validation.md)。

## 日常工作流

```text
资料进入 Inbox
    → 人工决定是否值得沉淀
    → 创建或更新 Concept 草稿
    → validate
    → scan 生成索引
    → 人工审阅 git diff
    → git commit
    → Obsidian 刷新
```

建议遵循以下边界：

- `01_Concept` 保存跨项目仍成立的定义、理解、公式、关系和决策依据。
- 单篇论文的摘录与评价进入 `03_Paper`。
- 单次 CST 模型、参数、日志和曲线进入 `04_Experiment`。
- 版本相关的软件步骤进入 `05_Tool`。
- 更新 `updated`，并在 `Decision Log` 或 `History` 中留下原因；不要把 Concept 当作无结构的运行日志。

## Python API

脚本也可作为模块加载：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path("ResearchOS/99_Meta/tools").resolve()))
from concept_tools import scan_concepts, validate_concept

errors = validate_concept(Path("ResearchOS/01_Concept/Wakefield.md"))
index = scan_concepts()
```

`validate_concept()` 返回错误字符串列表；空列表表示通过。`scan_concepts()` 成功时返回完整索引，失败时抛出 `ConceptFormatError` 且保留旧索引。

## 后续接入 Codex Agent

Codex 在后续阶段应作为“知识生产与维护者”，而不是 Hover 时的查询后端。推荐接入协议：

1. 人工把 PDF、HTML 或笔记放入 `00_Inbox`，然后明确触发处理。
2. Codex 读取来源、Schema 和已有相关 Concept，提出新增或更新草稿。
3. Codex 保留可追溯来源，建立 `[[wikilink]]`，更新 Decision Log 与 History。
4. Codex 运行 `validate` 和 `scan`，提交供人审阅的 Git diff。
5. 人工确认科学内容后再提交；Obsidian 和未来的 Hover 插件读取已确认的数据库与 JSON 索引。

未来插件可以把输入词先与规范名称和 `aliases` 做本地匹配，再用 `path` 打开笔记或直接显示 `hover_summary`。这一读取链路应保持离线、确定性且不调用 AI。

## v0.1 非目标

- 不构建 RAG 或 embedding 流程。
- 不引入向量数据库或全文检索服务。
- 不在 Hover 时调用 AI。
- 不自动抓取网页、论文或 arXiv。
- 不安装 Obsidian 插件或复杂后端。

系统设计与扩展边界见 [architecture.md](architecture.md)。
