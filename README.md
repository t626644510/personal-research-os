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
        └── hover_resolver.py
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

## Offline Hover Encyclopedia prototype

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
