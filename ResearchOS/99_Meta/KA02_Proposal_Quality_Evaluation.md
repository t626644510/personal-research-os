# KA-02 Proposal Quality Evaluation

- Status: Completed; human review completed and audit interpretation accepted on 2026-08-18
- Preparation date: 2026-08-18
- Run ID: `ka01-20260818t065446z-67f9fb66`
- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Source SHA-256: `67f9fb66faa227d27947e75fb5bd7c4ecfedd222bd09ad4ae2648673c2629627`
- KA-01 publication commit: `5418b92f2b6d007ad94150755a6fd30599e9ecaf`
- Proposal states: all `proposed`
- KA-03: not started
- Promotion: not authorized

本 worksheet 记录已完成的 KA-02 人工质量评估，不代替 repository owner 的科学
接受、proposal lifecycle state transition 或 promotion。KA-02 已完成，但这不表示
五个 proposal 全部 accepted。评估汇总为 2 revision、1 merge/supersede plan 和
2 defer plans。唯一 source 是
[reading_note.md](../00_Inbox/reading/ipac2019-weprb066/reading_note.md)；
assessment 是
[KA-01 assessment.md](../00_Inbox/proposals/runs/ka01-20260818t065446z-67f9fb66/assessment.md)。

## KA-02 Closeout Decision Summary

以下是 repository owner 已完成人工评估并接受审计解释后的 worksheet-level
evaluation outcomes。它们不是 Knowledge Proposal Protocol 的 lifecycle states；
五份 proposal 当前仍全部为 `proposed`。

| Proposal | Normalized evaluation disposition | Closeout interpretation |
| --- | --- | --- |
| P01 `Harmonic cavity` | `retain_for_revision` | 保留 `create` 方向，作为未来主体 proposal；P02 的被动运行方式在后续修订中作为 P01 内部运行方式/小节吸收。 |
| P02 `Passive harmonic cavity` | `merge_into_p01` | 计划并入 P01；未来如获 KA-03 授权可考虑 supersede，但本轮不改变 `State: proposed`，也不删除历史 artifact。 |
| P03 `Frequency tuner` | `revise_identity_and_aliases` | 后续改用 `Tuner` / `调谐器` 作为候选名称，保留 `Frequency tuner` 作为兼容 alias；本轮不修改 candidate。 |
| P04 `Coupling tuner` | `defer_for_reference_11` | 等待论文 reference `[11]` 后再判断是否建立独立 Concept；本轮不获取来源、不修改 candidate、不执行 deferred 状态转换。 |
| P05 `Bunch lengthening` | `defer_for_later_beam_physics_study` | 束团物理内容暂缓，等待后续系统学习；这不是 reject，也不执行 deferred 状态转换。 |

P01 的 `retain_for_revision` 是综合审计解释后的 normalized disposition：依据是
P01 已勾选的 create 决定、P02 的明确合并决定，以及 repository owner 对该审计
解释的接受。该记录不宣称 repository owner 已逐项接受未勾选的 evidence、
provenance、granularity 或 Related Concepts 检查。

本次 closeout 没有修改任何 `proposal.md` 或 `candidate.md`。KA-03、proposal
state transition 和 promotion 仍未启动、未获授权。

## Global KA-02 Checks

| Check                              | Agent assessment                                                                                                       | Evidence                                                                  | Human decision |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------------- |
| create/duplicate/no-op 分类          | assessment 的 28 个结果记录为 5 create / 16 duplicate / 7 no-op；P01–P05 对应五个 create。                                          | `assessment.md` 的 Classification Results、Classification totals            |                |
| update/relation 限制                 | 本 run 没有执行 update 或 relation；worksheet 不会把未执行变成通过。                                                                     | `assessment.md` 的 Run Exercise Summary                                    |                |
| quote/paraphrase/inference 可追溯     | 五个 proposal 的 evidence id、Vault-relative source path 和 locator 均可回到唯一 `reading_note.md`；inference 明确标记。                | P01 E01–E06；P02 E01–E04；P03 E01–E03；P04 E01–E03；P05 E01–E05               |                |
| 来源洗白                               | proposal 与 candidate 保留 paper、external-llm、synthesis-inference 和 requires-verification 的边界；没有把外部材料伪装成 paper fact。      | `reading_note.md` 的 provenance legend；各 proposal 的 Unresolved or Disputed |                |
| external-llm / synthesis inference | 候选只把直接 paper-supported 内容作为事实；外部总结和综合推断没有被升级为来源事实。                                                                     | `assessment.md` 的 Execution boundary；各 proposal evidence uncertainty      |                |
| human-owned 字段                     | `level`、`confidence`、`My Understanding`、`Decision Log` 和未支持公式仍为 `TODO(HUMAN)` 或 `UNRESOLVED`。                          | 五份 candidate 的 YAML 和正文；五份 proposal 的 Proposed Changes                    |                |
| candidate Schema                   | 五份 candidate 都有正确 YAML 顺序、H1 和十个有序 H2；proposal metadata 没有泄漏进 candidate YAML。                                          | `Concept_Schema_v0.1.md`；五份 candidate                                     |                |
| proposal metadata                  | Run ID、source、SHA、prompt、version、baseline、Prepared by/at 与 assessment 一致。                                              | assessment metadata 与五份 proposal metadata                                 |                |
| Related Concepts                   | 现有链接只作为 provisional mapping；P04 保持 `UNRESOLVED`，没有把导航推断写成 stable relation。                                             | 五份 candidate 的 Related Concepts；各 proposal 的 inference evidence           |                |
| stable Concept/index 隔离            | 本轮只读稳定 Concepts 用于 canonical name、alias、duplicate 和粒度对照；不修改 `01_Concept/` 或 `concept_index.json`。                      | `KA01_Trial_Validation.md` 的 Governance Boundary；Git baseline             |                |
| Concept 粒度                         | P01 是 generic hardware/function 候选；P02 是 operating configuration；P03/P04 是不同工程调节功能；P05 是设计目标。P02 与 P01 的边界需要人工决定。      | 五份 proposal Summary、candidate Definition 和 focused questions              |                |
| 中文正文与 aliases                      | 五份 proposal 都明确保留 Chinese-first body localization and Chinese aliases 为 `TODO(HUMAN)`；本 worksheet 只提出建议，不写回 candidate。 | 五份 proposal 的 Unresolved or Disputed                                      |                |

## P01 — Harmonic cavity

### Identity

- Proposal ID: `ka01-20260818t065446z-67f9fb66-p01-create`
- Candidate id: `harmonic_cavity`
- Current state: `proposed`
- Proposal: [P01 proposal.md](../00_Inbox/proposals/concepts/ka01-20260818t065446z-67f9fb66-p01-create/proposal.md)
- Candidate: [P01 candidate.md](../00_Inbox/proposals/concepts/ka01-20260818t065446z-67f9fb66-p01-create/candidate.md)

### Classification Review

- `create` 分类有来源支持：论文给出第三谐波 RF / harmonic-cavity 的独立设计
  context；assessment 记录没有 canonical、alias 或 semantic duplicate。
- 与 `Cavity mode`、`Shunt impedance`、`R over Q`、`Q factor` 的关系是
  provisional Related Concepts mapping，不等于 duplicate、subtype 或 alias。
- 这个候选更接近 generic hardware/function Concept；但当前文本仍主要是单篇
  论文案例，是否足以成为长期可复用 Concept 需人决定。
- Agent recommendation: `pass_with_revision`。这是辅助意见，不是 proposal
  lifecycle state。

### Evidence and Provenance

- E01–E04 是来自 `reading_note.md` 的 paper paraphrase，分别覆盖 Double-RF
  context、harmonic-cavity parameters、tuner/coupler 区分和六腔/lifetime
  paper claim。
- E05 是 provisional Related Concepts 的 inference；E06 是 category
  `accelerator physics` / `RF engineering` 的 inference，来自 accelerator RF
  cavity 与 double-RF/harmonic-cavity context，不是论文原句。
- `unloaded Q, Q0 = 36,000`、paper-reported `R/Q = 68 ohm`、2.45 Mohm、
  90 mm 和六腔 14.7 Mohm 都保持为 paper-specific；R/Q convention 不能无条件
  泛化，lifetime factor 4 也没有被写成当前机器结论。
- locator 可回到唯一 source；没有看到无来源扩写，uncertainty 保持在 evidence
  和 proposal unresolved text 中。

### Candidate Structure

- YAML 顺序符合 Schema；H1 为 `Harmonic cavity`；十个 H2 section 顺序完整。
- `Hover Summary`、`Sources`、provisional Related Concepts 和历史记录存在。
- `level`、confidence、`My Understanding`、`Formula`、`Decision Log` 的
  placeholder 没有被伪造；candidate YAML 没有 proposal metadata。

### Granularity and Reuse

- 作为 generic hardware/function 名称，它可能适合长期复用和 Hover Encyclopedia；
  但 Definition、Formula、当前机器适用性和 operating boundary 仍不足以支持 promotion。
- P02 是被动 operating configuration，不能仅因属于 harmonic-cavity 运行方式就
  自动判为 alias 或独立 Concept；需要与 P02 一起人工决定保留、section 化或合并。
- promotion 前需要更通用的 RF cavity 来源、人类填写字段、明确 convention 和
  中文 localization。

### Chinese Localization and Aliases

- 建议中文显示术语：`谐波腔`；可能 alias：`三次谐波腔`，仅供人确认。
- `腔`、`三次` 等过短词容易误匹配，不应自动加入 aliases。
- 中文正文和任何 alias 都必须由人确认；本 worksheet 不声称已接受这些建议。

### Human Review Form

- [x] 我同意 create 分类
- [ ] 我同意证据与 provenance
- [ ] 我同意 Concept 粒度
- [ ] 我同意 provisional Related Concepts
- [ ] 需要中文化与 aliases 修订
- [ ] 需要补充来源
- [ ] 需要修改 candidate
- [ ] 建议进入后续 KA-03
- [ ] 建议 defer
- [ ] 建议 merge/supersede
- [ ] 建议 reject

Human decision:

Human rationale:

Required revisions:

Required additional sources:

## P02 — Passive harmonic cavity

### Identity

- Proposal ID: `ka01-20260818t065446z-67f9fb66-p02-create`
- Candidate id: `passive_harmonic_cavity`
- Current state: `proposed`
- Proposal: [P02 proposal.md](../00_Inbox/proposals/concepts/ka01-20260818t065446z-67f9fb66-p02-create/proposal.md)
- Candidate: [P02 candidate.md](../00_Inbox/proposals/concepts/ka01-20260818t065446z-67f9fb66-p02-create/candidate.md)

### Classification Review

- `create` 分类有来源支持：论文明确描述 harmonic cavity 的 passive operation；
  assessment 没有找到同名或 semantic duplicate。
- P02 可能是 P01 的 operating configuration 或 section，而不一定是独立
  hardware Concept。subtype 不自动等于 alias，也不自动要求独立 Concept。
- `Cavity mode`、`Q factor`、`Shunt impedance` 仅是 provisional mapping，不是
  passive operation 的 canonical identity。
- Agent recommendation: `defer_for_more_sources`，重点是先解决 P01/P02 的粒度
  与可复用边界；这不是 lifecycle state。

### Evidence and Provenance

- E01 paraphrase 区分正常运行时没有 RF power supply 主动给腔体供能，以及 possible
  active-operation case using a rotatable coaxial loop coupler；没有把 coaxial loop
  写成 cavity mode。
- E02 paraphrase 保留 passive operation、coupler、port 和 active mode 的开放问题。
- E03 是 Related Concepts inference；E04 是从 accelerator RF cavity、double-RF/
  harmonic-cavity 和 passive-operation context 得出的 category inference，需人审。
- port、loading、pickup、HOM/test/parking 端口和 steady-state 条件没有被补造；
  source-specific boundary 保持清楚。

### Candidate Structure

- YAML 顺序、H1、十个 H2、Hover Summary、Sources 和 provisional Related Concepts
  均存在；proposal metadata 未进入 candidate YAML。
- `TODO(HUMAN)` / `UNRESOLVED` 保留了 general scope、ports、loading 和 passive/active
  boundary；candidate 不是 promotion-ready 的假装完成版本。

### Granularity and Reuse

- 作为运行配置，它可能长期复用；但当前唯一 source 只给出一篇论文中的 operation
  description，尚不足以决定独立 Concept、P01 的 section，或 alias。
- 人需要比较 generic hardware/function Concept 与 passive operating configuration，
  并决定是否保留两个 Concept；若合并，也需明确未来哪个 proposal supersede 哪个。
- promotion 前需要更多 passive-cavity、port/loading 和 operating-boundary 来源，
  以及人类字段和中文内容。

### Chinese Localization and Aliases

- 建议中文显示术语：`被动谐波腔`；可能 alias：`无源谐波腔`，仅供人确认。
- `被动腔` 过短且可能覆盖其他 cavity，`无源` 也需确认是否符合项目术语。
- 不自动添加 aliases，不把候选术语写成已接受命名。

### Human Review Form

- [ ] 我同意 create 分类
- [ ] 我同意证据与 provenance
- [ ] 我同意 Concept 粒度
- [ ] 我同意 provisional Related Concepts
- [ ] 需要中文化与 aliases 修订
- [ ] 需要补充来源
- [ ] 需要修改 candidate
- [ ] 建议进入后续 KA-03
- [ ] 建议 defer
- [x] 建议 merge/supersede
- [ ] 建议 reject

Human decision:
并入谐波腔即可，然后在谐波腔栏目内提到被动谐波腔
Human rationale:

Required revisions:

Required additional sources:

## P03 — Frequency tuner

### Identity

- Proposal ID: `ka01-20260818t065446z-67f9fb66-p03-create`
- Candidate id: `frequency_tuner`
- Current state: `proposed`
- Proposal: [P03 proposal.md](../00_Inbox/proposals/concepts/ka01-20260818t065446z-67f9fb66-p03-create/proposal.md)
- Candidate: [P03 candidate.md](../00_Inbox/proposals/concepts/ka01-20260818t065446z-67f9fb66-p03-create/candidate.md)

### Classification Review

- `create` 分类有来源支持：P03 描述 resonance-frequency adjustment 的 copper rods
  与 plungers，assessment 未找到 canonical、alias 或 semantic duplicate。
- `Frequency tuner` 与 P04 `Coupling tuner` 的工程功能不同；P03 的 provisional
  `Cavity mode` link 不是 duplicate 或 subtype 结论。
- 是否适合独立 Concept 仍需人判断；不能仅把它当作某个 cavity 的正文 section。
- Agent recommendation: `pass_with_revision`，不是 proposal state。

### Evidence and Provenance

- E01 是唯一 paper paraphrase：two copper rods, each 95 mm in diameter, each moves
  ±50 mm, about ±0.5 MHz；two plungers, each 30 mm in diameter, each moves ±25 mm,
  about ±0.5 MHz。
- E02 是 `Cavity mode` provisional mapping inference；E03 是从 accelerator RF cavity
  与 tuner context 得出的 `RF engineering` category inference，明确需 human review。
- 两组尺寸和范围仍是论文设计值；没有增加来源没有提供的机理解释、公式或当前机器结论。

### Candidate Structure

- YAML 顺序、H1、十个 H2、Hover Summary、Sources 和 provisional Related Concepts
  均符合审阅准备要求；proposal metadata 未泄漏到 candidate YAML。
- `Formula`、level、confidence、`My Understanding`、`Decision Log` 保持 placeholder。

### Granularity and Reuse

- `Frequency tuner` 的功能名称可能适合 Hover Encyclopedia；P03 与 P04 的调整目标
  不同，初步不应因同属 tuner 就合并。
- 现有证据仍只有单篇论文的 geometry/range；promotion 前需要更通用的 tuner
  来源、灵敏度/边界定义、人类字段和中文命名。

### Chinese Localization and Aliases

- 建议中文显示术语：`频率调谐器`；可能 alias：`调频器`，仅供人确认。
- `调谐器` 过于宽泛，`调频器` 可能与通信/电子语境混淆；任何 alias 需人确认。
- 本 worksheet 不修改 candidate，也不声称建议已被接受。

### Human Review Form

- [ ] 我同意 create 分类
- [ ] 我同意证据与 provenance
- [ ] 我同意 Concept 粒度
- [ ] 我同意 provisional Related Concepts
- [x] 需要中文化与 aliases 修订
- [ ] 需要补充来源
- [ ] 需要修改 candidate
- [ ] 建议进入后续 KA-03
- [ ] 建议 defer
- [ ] 建议 merge/supersede
- [ ] 建议 reject

Human decision:
直接用“Tuner”和“调谐器”即可，不用刻意强调Frequency，虽然可能过于宽泛，但是在加速器领域基本就特指这个东西
Human rationale:

Required revisions:

Required additional sources:

## P04 — Coupling tuner

### Identity

- Proposal ID: `ka01-20260818t065446z-67f9fb66-p04-create`
- Candidate id: `coupling_tuner`
- Current state: `proposed`
- Proposal: [P04 proposal.md](../00_Inbox/proposals/concepts/ka01-20260818t065446z-67f9fb66-p04-create/proposal.md)
- Candidate: [P04 candidate.md](../00_Inbox/proposals/concepts/ka01-20260818t065446z-67f9fb66-p04-create/candidate.md)

### Classification Review

- `create` 分类有来源支持：P04 描述 coupling-tuner post 改变 coupling factor
  `beta`，assessment 未找到 canonical、alias 或 semantic duplicate。
- P04 与 P03 的工程含义不同：一个调 coupling factor，另一个调 resonance frequency。
  但论文中的结构是单一来源实例，不能自动推广为通用 Concept。
- Candidate 的 Related Concepts 保持 `UNRESOLVED` 是谨慎边界；不应为了完整性
  强行链接 `External Q` 或 `Loaded Q`。
- Agent recommendation: `defer_for_more_sources`，尤其等待论文 reference `[11]`；
  这不是 proposal lifecycle state。

### Evidence and Provenance

- E01 paraphrase 区分 WR-1500 input coupler 与 coupling-tuner post，并记录 beta 1
  target、40 mm post 对应 beta 2.4；这些是 paper-specific values。
- E02 paraphrase 保留 passive-cavity coupler、ports 和 active operation 的开放问题。
- E03 是从 accelerator RF cavity 与 RF coupling-tuner context 得出的 category inference，
  不是论文原句，需人审。
- source 没有完整给出 coupling convention、所有端口行为或参考文献 `[11]` 的内容；
  candidate 没有补造公式或通用结构。

### Candidate Structure

- YAML 顺序、H1、十个 H2、Hover Summary、Sources 和 `UNRESOLVED` Related Concepts
  均存在；proposal metadata 没有进入 candidate YAML。
- beta 数值、结构、范围、passive applicability 和 human-owned fields 都保留不确定性。

### Granularity and Reuse

- coupling tuner 与 frequency tuner 的目标变量不同，可能值得独立 Concept；但当前
  source 只支持一个 main-cavity structure，且 reference `[11]` 尚未读取。
- 人需判断它是否是通用工程 Concept，还是应 defer，或与另一 proposal merge/supersede。
- promotion 前至少需要 reference `[11]` 或其他专门 coupling-tuner 来源、convention、
  port boundary、人类字段和中文 localization。

### Chinese Localization and Aliases

- 建议中文显示术语：`耦合调谐器`；可能 alias：`耦合调节器`，仅供人确认。
- `耦合器` 会与一般 coupler 混淆，`调耦器` 过短且不稳定；别名必须由人确认。
- P04 当前没有 Related Concepts alias/link 决定，本 worksheet 不替它决定。

### Human Review Form

- [ ] 我同意 create 分类
- [ ] 我同意证据与 provenance
- [ ] 我同意 Concept 粒度
- [ ] 我同意 provisional Related Concepts
- [ ] 需要中文化与 aliases 修订
- [ ] 需要补充来源
- [ ] 需要修改 candidate
- [ ] 建议进入后续 KA-03
- [x] 建议 defer
- [ ] 建议 merge/supersede
- [ ] 建议 reject

Human decision:
reference11阅读完之后再考虑独立建concept
Human rationale:

Required revisions:

Required additional sources:

## P05 — Bunch lengthening

### Identity

- Proposal ID: `ka01-20260818t065446z-67f9fb66-p05-create`
- Candidate id: `bunch_lengthening`
- Current state: `proposed`
- Proposal: [P05 proposal.md](../00_Inbox/proposals/concepts/ka01-20260818t065446z-67f9fb66-p05-create/proposal.md)
- Candidate: [P05 candidate.md](../00_Inbox/proposals/concepts/ka01-20260818t065446z-67f9fb66-p05-create/candidate.md)

### Classification Review

- `create` 分类有来源支持：论文把 bunch lengthening 作为第三谐波 RF 设计目标，
  assessment 未找到 canonical、alias 或 semantic duplicate。
- P05 是设计目标/现象名称，不是现有 `Shunt impedance` 的 alias；provisional link
  只表示导航对照。
- 当前 source 没有给出完整 longitudinal-dynamics model；是否值得作为长期可复用
  Concept 需要人和专门来源共同判断。
- Agent recommendation: `defer_for_more_sources`，不是 proposal state。

### Evidence and Provenance

- E01–E03 是 paper paraphrase，分别支持 third-harmonic design context、six-cavity
  application/lifetime claim 和 bounded efficiency proportionality statement。
- E04 是 `Shunt impedance` provisional mapping inference；E05 是从 accelerator RF
  cavity、double-RF 和 bunch-lengthening context 得出的 category inference，非论文原句。
- shunt-impedance proportionality 继续保持 bounded / `UNRESOLVED`；没有写成公式、
  general efficiency law 或当前机器结论。
- detuning、fill pattern、beam distribution、lifetime interpretation 和模型条件仍
  处于 source-specific 或 requires-verification 边界。

### Candidate Structure

- YAML 顺序、H1、十个 H2、Hover Summary、Sources 和 provisional Related Concepts
  均存在；proposal metadata 未进入 candidate YAML。
- `Formula`、效率定义、model、level、confidence 和当前机器适用性保持 placeholder。

### Granularity and Reuse

- `Bunch lengthening` 可能是通用 accelerator-physics 目标，但本 source 目前只支持
  design objective 和 bounded claim，不足以完成 promotion-ready 的物理定义。
- 需要专门 longitudinal dynamics 来源解释效率、束团分布、失谐、填充图样与假设；
  stable `Shunt impedance` 不应吸收这一概念。
- 当前 evidence 可以支持 proposed review material，但不能支持科学接受或 promotion。

### Chinese Localization and Aliases

- 建议中文显示术语：`束团长度延长`；可能 alias：`束团拉长`，仅供人确认。
- `束团拉长` 可能偏口语，`展宽` 可能与横向/能量分布混淆；需要人确认领域用语。
- 本 worksheet 不修改 candidate 或 aliases。

### Human Review Form

- [ ] 我同意 create 分类
- [ ] 我同意证据与 provenance
- [ ] 我同意 Concept 粒度
- [ ] 我同意 provisional Related Concepts
- [ ] 需要中文化与 aliases 修订
- [ ] 需要补充来源
- [ ] 需要修改 candidate
- [ ] 建议进入后续 KA-03
- [x] 建议 defer
- [ ] 建议 merge/supersede
- [ ] 建议 reject

Human decision:
束团物理方面的内容可以都暂时delay，等后面系统学习
Human rationale:

Required revisions:

Required additional sources:

## Mandatory Focused Questions

### Harmonic cavity vs Passive harmonic cavity

- `Harmonic cavity` 是 generic hardware/function 候选，P01 直接描述第三谐波 RF
  cavity；`Passive harmonic cavity` 是 operation configuration，P02 直接描述无 RF
  power supply 主动驱动的 passive baseline。
- P02 不应仅因是 P01 的运行方式就自动成为 alias，也不应仅因名称不同就自动成为
  独立 Concept。需比较长期可复用性、Hover Encyclopedia 价值和是否只是 P01 的
  section。
- 保留两个 Concept 的理由必须分别是 hardware/function 与 operating-configuration
  的稳定复用价值；合并时需要人明确哪个 proposal 在未来 supersede 哪一个，不能由本
  worksheet 代填。
- Subtype 不自动等于 alias，也不自动要求独立 Concept；Human decision 留空。

### Frequency tuner vs Coupling tuner

- P03 的 frequency tuner 调整 resonance frequency；P04 的 coupling tuner 调整
  coupling factor `beta`。这两个目标变量和工程问题不同，初步不视为同一 Concept。
- P03 有两类具体 tuner geometry 与范围；P04 只有单一论文结构和 beta 例子，不能
  无条件泛化。
- P04 是否都值得独立 Concept，以及是否应等待论文 reference `[11]`，留给人决定；
  本 worksheet 对 P04 给出 `defer_for_more_sources` 辅助推荐。

### Bunch lengthening

- 当前 source 支持它是第三谐波 cavity design objective，但没有完整的通用物理模型。
- shunt-impedance proportionality 继续保持 bounded / `UNRESOLVED`，不能转成公式或
  当前机器的 design rule。
- promotion 前需要专门的 longitudinal dynamics 来源，明确 efficiency 定义、运行
  模式、失谐、束流分布、fill pattern 和自洽条件。

### TM020 mode

- 本 run 对 TM020 正确保持 `no-op`；后续不重新生成 TM020 proposal。
- generic `Cavity mode` 不是 TM020 的 semantic duplicate；TM020 是具体模态类型，
  当前唯一 source 没有足够的可复用 modal definition。
- 后续若重新提案，需要专门解释 TM010/TM020 mode indices、field pattern、R/Q、
  geometry factor 和工程比较的来源；本轮不读取第二来源。

## Agent Recommendations for Human Review

以下是基于当前本地 assessment、唯一 `reading_note.md`、五份 proposal/candidate
和相关稳定 Concepts 的非权威辅助意见：

- P01 `Harmonic cavity` — `pass_with_revision`：证据与 Schema 准备较完整，但通用
  Definition、human-owned fields、convention、中文内容及与 P02 的粒度仍需修订。
- P02 `Passive harmonic cavity` — `defer_for_more_sources`：当前 source 支持一种
  operating description，但不足以决定它是独立 Concept、P01 section 还是 alias。
- P03 `Frequency tuner` — `pass_with_revision`：功能边界和尺寸/范围 locator 清楚，
  但仍需人确认独立粒度、通用性、中文术语和 provisional relation。
- P04 `Coupling tuner` — `defer_for_more_sources`：beta 与 frequency tuning 的功能
  区分清楚，但 reference `[11]`、coupling convention 和可复用边界尚未补足。
- P05 `Bunch lengthening` — `defer_for_more_sources`：设计目标和 bounded claim 可追溯，
  但缺少专门 longitudinal dynamics 来源，不能把 proportionality 当成完整模型。

这些 recommendation 不是 proposal state，也不是 repository owner 的决定。只有
repository owner 的后续明确指令才能启动 KA-03；本文件不能把任何 proposal 改成
`accepted`、`rejected`、`deferred` 或 `superseded`。
