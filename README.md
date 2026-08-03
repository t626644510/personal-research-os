# Personal Research OS v0.1

Personal Research OS 是一个以 Obsidian 为阅读界面、Git 为审计与版本层、Python 为确定性维护工具的个人科研知识库。v0.1 只建立稳定的 Concept Database 和 Hover Encyclopedia 数据基础，不包含 RAG、向量数据库、AI 实时查询、自动爬虫或定时扫描。

## 快速开始

1. 在 Obsidian 中选择 `ResearchOS/` 作为 Vault。
2. 通过 `[[Concept name]]` 建立概念链接；Obsidian 原生悬浮预览可直接查看 Concept 笔记。
3. 新建概念时复制 `ResearchOS/99_Meta/templates/Concept.md`，按 Schema 填写后再放入 `ResearchOS/01_Concept/`。
4. 在仓库根目录运行校验和索引生成：

```powershell
python ResearchOS/99_Meta/tools/concept_tools.py validate
python ResearchOS/99_Meta/tools/concept_tools.py scan
python ResearchOS/99_Meta/tools/hover_resolver.py "HOM impedance and wake field"
```

工具只依赖 Python 3.9+ 标准库。`scan` 会先校验全部 Concept，并检查 ID、规范名称和别名冲突；只有全部通过时才会原子更新 `ResearchOS/99_Meta/concept_index.json`。若 Windows 已安装 Python Launcher 但 `python` 不在 `PATH`，把上述命令中的 `python` 换成 `py -3.9`（或已安装的对应版本）。

## 数据结构

```text
ResearchOS/
├── 00_Inbox/
│   ├── papers/              # 待处理论文
│   ├── html/                # 待处理网页快照
│   └── notes/               # 临时记录
├── 01_Concept/              # 稳定概念节点；Hover 数据的唯一来源
├── 02_Project/              # 项目目标、状态、决策和概念入口
├── 03_Paper/                # 论文级笔记与阅读结论
├── 04_Experiment/           # 实验/仿真设置、运行和结果
├── 05_Tool/                 # 软件与可复用操作流程
└── 99_Meta/
    ├── Concept_Schema_v0.1.md
    ├── concept_index.json
    ├── templates/Concept.md
    └── tools/
        ├── concept_tools.py
        ├── hover_resolver.py
        └── hover_ui.py
```

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
