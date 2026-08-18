---
type: reading_note
schema_version: reading-note-v0.1
paper_id: ipac2019-weprb066
state: draft
title: "Utilizing the High Shunt Impedance TM020-Mode Cavity in the Double RF Systems for the Storage Ring of the Thailand New Light Source"
authors:
  - N. Juntong
  - T. Phimsen
  - N. Chulakham
  - S. Malichan
doi: 10.18429/JACoW-IPAC2019-WEPRB066
source_path: 00_Inbox/reading/ipac2019-weprb066/_local/source.reading.md
session_path: 00_Inbox/reading/ipac2019-weprb066/_local/reading_session.md
external_summary_path: 00_Inbox/reading/ipac2019-weprb066/_local/external_llm_conversation_summary.md
synthesis_method: manually_triggered_llm
created: 2026-08-11
updated: 2026-08-18
---

# 1. Draft Status and Provenance Legend

**Workflow status — 2026-08-18:** RW-03 synthesis content human accepted on 2026-08-18; selected-text presentation correction applied; RW-03 accepted and complete.

`reading_note.draft.md` remains `state: draft`. No artifact is assigned `human_reviewed`; RW-04 Human Review and Freeze has not started; final `reading_note.md` does not exist; Concept proposal and KA-01 remain unauthorized and unstarted.

[paper/paraphrase] 论文事实只来自英文阅读转写；每一处均给出论文 section、PDF page marker，以及适用时的 Table 或 Figure locator。`source.reading.md` 是本草稿唯一的论文文本权威。

[human/question] 两个人类问题逐字来自 `reading_session.md`；草稿保留 entry ID、原始 locator 和问题文本，不把外部回答写回 session。

[human/note] 三个人类笔记逐字来自 `reading_session.md`；“拓展阅读相关文献”和“概念解析”只转化为待办或分层说明，不被提升为论文结论。

[external-llm/unverified] 可选外部总结是本次由人明确选择的辅助输入，但仍属于 external LLM、unverified、session-external；它不是论文证据、human note、session `llm_answer` 或 human-reviewed 内容。

[synthesis-inference/unverified] 这一标签表示本轮为连接已分层材料而形成的解释或项目推断；它不是来源中的直接陈述。

[requires-verification] 这一标签表示证据不足、约定未固定，或需要原始参考文献、机器参数、仿真、计算或实验才能关闭的问题。

# 2. Why This Paper Matters

[paper/paraphrase] 论文针对一台 3 GeV、300 mA 的低发射度储存环，提出约 500 MHz 的常导主 RF 腔和三次谐波腔，用主系统提供总计 2.2 MV，并以三次谐波系统延长束团。（Abstract and Introduction，PDF page 1，printed page 2972）

[paper/paraphrase] 论文设计的主腔频率为 500.12 MHz，谐波腔频率为 1500.36 MHz；两种论文腔型都采用 TM020 工作模。（Main RF Cavity Design，PDF page 1；Harmonic Cavity Design，PDF pages 2–3，printed pages 2973–2974；Conclusion，PDF page 3）

[synthesis-inference/unverified] 对当前项目最有价值的不是直接复制该腔体，而是把它作为一个有明确数值的案例，用来分开研究工作模选择、`R/Q` 与 `Q` 的乘积、被动谐波运行、调频与调耦、寄生模阻尼，以及束团寿命声明所需的机器条件。

[requires-verification] 论文的 SPS-II 参数、端口、腔数和几何并不自动适用于当前约 1500 MHz 谐波腔项目；项目必须以自己的束流、空间、功率、热、机械、阻抗和运行条件重新验证。

# 3. Paper-Supported Findings

## 3.1 Double-RF context and frequencies

[paper/paraphrase] 论文背景是新的 3 GeV、300 mA 低发射度环。主 RF 采用 500 MHz 量级常导系统，四个主腔各提供 550 kV，总电压 2.2 MV；三次谐波腔用于束团延长。（Abstract and Introduction，PDF page 1，printed page 2972；Main RF Cavity Design，PDF page 1）

[paper/paraphrase] 具体设计频率为主腔 500.12 MHz、谐波腔 1500.36 MHz。（Main RF Cavity Design，PDF page 1；Table 1，PDF page 2；Harmonic Cavity Design，PDF page 2；Table 2，PDF page 3）

## 3.2 Main-cavity parameters

[paper/paraphrase] Table 1 对一个 modified SPring-8 方案和 SPS-II new design 作了如下比较；表中 `R/Q` 的定义是 $V^2/(\omega U)$。（Main RF Cavity Design，Table 1，PDF page 2，printed page 2973）

| Table 1 parameter | Modified SPring-8 | SPS-II new design |
| --- | ---: | ---: |
| Frequency | 500.12 MHz | 500.12 MHz |
| $Q$ | 57,000 | 51,000 |
| $R/Q$ | 126 Ω | 163 Ω |
| Shunt impedance | 7.2 MΩ | 8.3 MΩ |
| Maximum voltage | 900 kV | 800 kV |
| Cavity diameter | 1040 mm | 960 mm |
| Insertion length | 500 mm | 500 mm |
| Beam-port diameter | 70 mm | 40 mm |

[paper/paraphrase] 正文把 SPS-II 新主腔的 51,000 称为 unloaded $Q$，并给出 $R/Q=163\ \Omega$ 和 shunt impedance 8.3 MΩ。（Main RF Cavity Design，PDF page 1，printed page 2972）

## 3.3 Harmonic-cavity parameters

[paper/paraphrase] 论文的 TM020 谐波腔参数包括 1500.36 MHz、$Q=36{,}000$、$R/Q=68\ \Omega$、单腔 shunt impedance 2.45 MΩ、腔体直径 354.514 mm、Table 2 中 insertion length 300 mm，以及 40 mm beam-port diameter；正文另给出 90 mm effective cavity length。（Harmonic Cavity Design，PDF page 3，printed page 2974；Table 2，PDF page 3；Figure 5）

[paper/paraphrase] 摘要明确把 36,000 表述为 unloaded $Q$。（Abstract，PDF page 1，printed page 2972）

[synthesis-inference/unverified] 因此不能把 36,000 直接当成包含所有实际端口、吸收体和外部负载后的 [[Loaded Q]]；dressed value 仍需单独核验。

## 3.4 Frequency tuners and couplers are different functions

[paper/paraphrase] 主腔频率调谐采用两根直径 95 mm 的铜杆，各移动 ±50 mm，对应约 ±0.5 MHz 的频率调节范围。（Main RF Cavity Design → Frequency Tuner Design，PDF page 1；Figure 2，PDF page 2）

[paper/paraphrase] 主腔的 WR-1500 waveguide input coupler 通过 coupling slot 送入 RF 功率；coupling-tuner post 用来改变 coupling factor $\beta$。论文以 slot 优化到 $\beta=1$ 为目标，并报告 40 mm post 对应 $\beta=2.4$。（Power Coupler Design，PDF page 2，printed page 2973；Figure 3）

[paper/paraphrase] 谐波腔拟以 passive mode 运行，正常运行时没有 RF power supply 主动给腔体供能。其频率调谐采用两个直径 30 mm 的 plunger，各移动 ±25 mm，对应约 ±0.5 MHz。（Harmonic Cavity Design → Frequency Tuner Design，PDF page 3，printed page 2974；Figure 6）

[paper/paraphrase] 论文另外为可能的 active-mode 情形讨论了可旋转的 coaxial loop coupler；旋转 loop 可调 coupling factor。（Harmonic Cavity Design → Frequency Tuner Design，PDF page 3，printed page 2974）

[synthesis-inference/unverified] 该结构属于可选主动运行情形，不能写成被动基线必需的功率输入 coupler。

## 3.5 Six harmonic cavities and the lifetime claim

[paper/paraphrase] 论文方案使用六个谐波腔；由单腔 2.45 MΩ 得到总 shunt impedance 14.7 MΩ，并针对论文的 3 GeV、300 mA 电子束案例给出 lifetime improvement factor 4。（Harmonic Cavity Design，PDF page 3，printed page 2974；Table 2）

[requires-verification] 论文这段文字没有在当前阅读转写中给出足以复算 factor 4 的完整光学、填充和寿命模型。该数字必须保留为论文特定工况下的声明，不能解释为束长四倍、阻抗四倍，或当前机器的设计指标。

## 3.6 Parasitic-mode damping

[paper/paraphrase] 主腔设计比较了 slot-type 与 rod-type damping mechanism，并认为 slot 方案更有效；ferrite slot damping 对 Figure 4 中所选的束流相关寄生模给出约 10–1000 的 loaded $Q$。（Parasitic Modes Damping Design，PDF page 2，printed page 2973；Figure 4）

[paper/paraphrase] 谐波腔也通过优化 slot width、slot length 和 ferrite dimensions 阻尼寄生模；Figure 7 中所示模式的 loaded $Q$ 约为 10–1000。（Harmonic Cavity Design → Parasitic Modes Damping Design，PDF page 3，printed page 2974；Figure 7）

[requires-verification] “10–1000”只由论文图示或所选模式支持，不能扩大为所有可能的 [[Higher-order mode|higher-order modes]]，也不能替代当前 dressed cavity 的纵横向阻抗、热负荷和工作模加载评估。

## 3.7 TM020 scope boundary

[paper/paraphrase] 论文明确为其 500.12 MHz 主腔和 1500.36 MHz 谐波腔都采用 TM020 resonant mode。（Abstract，PDF page 1；Figure 1 and Table 1，PDF pages 1–2；Figure 5 and Table 2，PDF page 3；Conclusion，PDF page 3）

[synthesis-inference/unverified] 当前项目只把 TM020 作为约 1500 MHz 谐波腔候选工作模；已知的约 500 MHz 常导主腔没有在本阶段冻结 TM020 模式。论文的双 TM020 选择不是用户的双腔设计决定。

# 4. Human Questions

## 4.1 rw-entry-0001 — TM020 shunt impedance and a low-emittance ring

- entry_id: `rw-entry-0001`
- source_locator: `Abstract`

**框选原文（session 原样）**

[paper/quote]

> The TM020-mode cavity has larger transverse dimension compared to the traditional TM010-mode cavity, but with its higher shunt impedance
>  it can be designed to fit in the new low emittance storage ring regardless.

[human/question] 原始问题：

> 我印象中TM020的分路阻抗并没有更高，虽然其Q0较高，但是R/Q相比传统的TM010腔是更低的，进一步导致其分路阻抗不高。除此之外，low emittance storage ring的要求是什么？为什么higher shunt impedance对其是有益的？把物理过程和其中的概念给我讲讲

### 论文能直接支持的回答

[paper/paraphrase] 论文的 Introduction 将 TM020 描述为具有较高 unloaded $Q$、较低 $R/Q$，并称二者的乘积仍得到较高 shunt impedance。（Introduction，PDF page 1，printed page 2972）

[paper/paraphrase] 论文没有提供同约束下 TM010 与 TM020 的成对比较；它给出的可核对数值是自身设计：500.12 MHz 新主腔 $Q_0=51{,}000$、$R/Q=163\ \Omega$、shunt impedance 8.3 MΩ，以及 1500.36 MHz 谐波腔 $Q_0=36{,}000$、$R/Q=68\ \Omega$、shunt impedance 2.45 MΩ。（Main RF Cavity Design，PDF page 1；Table 1，PDF page 2；Abstract and Table 2，PDF pages 1 and 3）

[requires-verification] 摘要中的 “higher shunt impedance” 没有给出足以确定其比较对象的完整基准，因此论文不能直接证明“所有 TM020 都比 TM010 的 shunt impedance 高”。

### External LLM 辅助解释

[external-llm/unverified] 在外部总结采用的论文约定下，$R_{\mathrm{sh}}=(R/Q)_aQ_0=V_{\mathrm{pk}}^2/P_{\mathrm{wall}}$。所以较低的 $R/Q$ 并不逻辑上强制较低的 shunt impedance；结果取决于 $Q_0$ 的增益是否足以补偿 $R/Q$ 的下降。

[external-llm/unverified] 外部总结认为，给定腔压下更高 shunt impedance 的直接收益是较低铜耗与冷却负担，或在系统层面减少腔数、纵向占地和辅助设备；它不会直接缩小 TM020 的横向半径。

[external-llm/unverified] 外部总结把低发射度环的相关系统约束列为直线节空间、束管孔径、阻抗与 HOM、真空、冷却、维护和可靠性；Touschek 收益还依赖垂直发射度与耦合、纵向分布、单束团电荷、IBS、RF acceptance 和动力学动量接受度。这些是一般工程解释，不是该论文逐项给出的低发射度设计要求。

### Synthesis inference

[synthesis-inference/unverified] 用户对“TM020 往往有较低 $R/Q$”的质疑与论文自身表述并不冲突。应把问题拆成三层：模态几何是否适合可用空间；具体 dressed geometry 的 $R/Q$、$Q_0$ 与 shunt impedance；更低功耗或更少腔体是否改善整机集成。

[synthesis-inference/unverified] “更高 shunt impedance 使腔体 fit”最安全的理解是间接系统收益，而不是 shunt impedance 改变模态尺寸。只有在相同频率、材料、有效长度、孔径、端口和 HOM 约束下比较，才能判断 TM010 与 TM020 的净优势。

### 尚未解决的问题

- [requires-verification] 核对论文 “higher” 的准确比较对象和引用依据。
- [requires-verification] 在同一工程约束下比较 TM010/TM020 的 $R/Q$、geometry factor、$Q_0$、shunt impedance、峰值表面场与空间包络。
- [requires-verification] 取得当前机器的可用空间、目标电压、功率与冷却预算、腔数和阻抗预算。
- [requires-verification] 取得束流与光学参数，进行自洽束团分布、IBS、Touschek 和接受度计算。

## 4.2 rw-entry-0002 — Coupling tuner and passive-cavity couplers

- entry_id: `rw-entry-0002`
- source_locator: `Power Coupler Design`

**框选原文（session 原样）**

[paper/quote]

>  The waveguide input coupler with a coupling tuner concept [11] was applied for the SPS-II cavity.

[human/question] 原始问题：

> coupling tuner是什么概念，如何工作的？被动式的谐波腔需要coupler吗?

### 论文能直接支持的回答

[paper/paraphrase] 被选中的 coupling-tuner 句子属于 500.12 MHz 主腔：WR-1500 waveguide input coupler 通过 coupling slot 输入功率，post 长度用来改变 coupling factor $\beta$。（Power Coupler Design，PDF page 2，printed page 2973；Figure 3）

[paper/paraphrase] 1500.36 MHz 谐波腔的论文基线是 passive mode，没有 RF power supply 主动供能；论文只为可能的 active mode 讨论可旋转 coaxial loop coupler。（Harmonic Cavity Design → Frequency Tuner Design，PDF page 3，printed page 2974）

[requires-verification] 论文这些段落能区分主腔功率耦合和谐波腔被动运行，但没有完整回答实际被动腔是否需要 pickup、测试端口、HOM load 或 parking/de-Q 端口。

### External LLM 辅助解释

[external-llm/unverified] 外部总结把 coupling tuner 的主要作用解释为改变耦合孔附近局部场或等效电纳，从而改变 [[External Q]]、$\beta$ 和 [[Loaded Q]]；frequency tuner 的主要作用是改变共振频率。两者可能交叉扰动，但不是同一调节量。

[external-llm/unverified] 被动谐波腔不需要 generator-side high-power input coupler 来建立工作电压，但工程上仍可能需要弱耦合 pickup、[[HOM coupler|HOM damping coupler]]、VNA/老炼用临时接口或其他诊断端口。外部总结明确把 pickup 视为一般工程建议，而不是论文事实。

### Synthesis inference

[synthesis-inference/unverified] 回答“需不需要 coupler”之前必须先按功能分类：power input、pickup、HOM damping、temporary test。纯被动运行可以取消永久高功率输入 coupler，却不等于完全没有任何 RF 耦合或测试接口。

[synthesis-inference/unverified] 当前 1500 MHz 项目尚未决定主动或被动运行，因此不能照搬论文的主腔 coupling tuner，也不能提前删除或冻结任一类端口。

### 尚未解决的问题

- [requires-verification] 获取并阅读论文参考文献 `[11]`，核对 coupling-tuner 结构、调节范围和适用边界。
- [requires-verification] 为所有候选端口计算工作模 [[External Q]]、总 [[Loaded Q]] 与附加频移。
- [requires-verification] 定义 pickup 动态范围、信噪比、标定方法和允许抽取功率。
- [requires-verification] 明确无永久高功率输入端口时的 VNA 冷测、高场老炼、multipacting 与热试验方案。

# 5. Human Notes and Follow-ups

## 5.1 rw-entry-0003 — Parasitic-mode damping references

- entry_id: `rw-entry-0003`
- source_locator: `Parasitic Modes Damping Design`

**框选原文（session 原样）**

[paper/quote]

> The slot-type damped mechanism [3] and the rod-type damped mechanism [8, 12] were investigated

[human/note] 原始笔记：`拓展阅读相关文献`

[paper/paraphrase] 笔记所对应的论文句子比较 slot-type damping `[3]` 与 rod-type damping `[8, 12]`。（Parasitic Modes Damping Design，PDF page 2，printed page 2973）

[requires-verification] Follow-up actions：

1. 从论文 bibliography 精确核验 `[3]`、`[8]`、`[12]` 的完整元数据；在取得原文前不补造题名、作者或 DOI。
2. 获取三篇原文，分别记录 slot-type 与 rod-type 的结构和适用模式。
3. 比较目标寄生模、阻尼几何、吸收材料、频率、纵横向 $R/Q$、阻尼前后 $Q_L$、工作模加载、热功率、真空兼容性和制造约束。
4. 单独核对 TM020 工作模泄漏，不能把工作模与 [[Higher-order mode|HOM/寄生模]] 混为一类。
5. 所有后续结论附具体原文页码、Table 或 Figure locator。

## 5.2 rw-entry-0004 — Bunch-lengthening references

- entry_id: `rw-entry-0004`
- source_locator: `Harmonic Cavity Design`

**框选原文（session 原样）**

[paper/quote]

> The efficiency of bunch lengthening is proportional to the shunt impedance
>  of the cavity [6, 7],

[human/note] 原始笔记：`拓展阅读相关文献`

[paper/paraphrase] 笔记所对应的论文句子声称 bunch-lengthening efficiency 与 cavity shunt impedance 成正比，并引用 `[6, 7]`。（Harmonic Cavity Design，PDF page 2，printed page 2973）

[requires-verification] Follow-up actions：

1. 从 bibliography 精确取得 `[6]`、`[7]`，并阅读原文；未取得前不补造引用信息。
2. 查清 “efficiency” 的定义：束长比、峰值密度下降、目标谐波电压、功耗效率，或其他指标。
3. 查清 shunt impedance 使用 $V^2/P$ 还是 $V^2/(2P)$，以及使用 $Q_0$ 还是实际 $Q_L$。
4. 核对该比例关系对主动/被动、束流电流、失谐、填充图样、线性化和自洽分布的假设。
5. 用真实电流、填充图样和自洽 [[Bunch spectrum]] 重新验证，分别记录论文命题、参考文献推导和本机结果。

## 5.3 rw-entry-0005 — Meaning of the lifetime factor

- entry_id: `rw-entry-0005`
- source_locator: `Source page marker: PDF page 3 (printed page 2974)`

**框选原文（session 原样）**

[paper/quote]

> the lifetime improvement factor of the 3 GeV 300 mA electron beam is 4.

[human/note] 原始笔记：`概念解析`

[paper/paraphrase] 论文声称，在其六个谐波腔、总 shunt impedance 14.7 MΩ 的 SPS-II 方案中，3 GeV、300 mA 电子束的 lifetime improvement factor 为 4。（Harmonic Cavity Design，PDF page 3，printed page 2974；Table 2）

[external-llm/unverified] 外部总结给出的一般物理解释是：三次谐波电压整形纵向势阱，可延长束团并降低峰值密度，从而可能改善 Touschek lifetime；实际收益仍依赖完整纵向分布、垂直发射度与耦合、单束团电荷和填充图样、IBS、RF acceptance 与局部动力学动量接受度。

[synthesis-inference/unverified] factor 4 应视为机器与模型特定的结果。它不等于束长变为四倍、shunt impedance 提高四倍，也不能在没有当前机器复算时迁移为项目指标。

[requires-verification] 关闭该笔记需要：确认论文所指寿命类型和基线；记录光学、$\varepsilon_x$、$\varepsilon_y$、耦合、能散、自然束长、逐 bucket 电荷、RF 参数、局部动量接受度和 IBS 模型；自洽求解基线与双 RF 分布；在相同粒子数、光学、接受度和散射模型下比较寿命及不确定性。

# 6. Engineering Implications for the 1500 MHz TM020 Harmonic Cavity

[synthesis-inference/unverified] 当前已知输入只有：系统存在约 500 MHz 常导主腔；计划研究约 1500 MHz 谐波腔；TM020 是该谐波腔的候选工作模。500 MHz 主腔的工作模没有在 RW-03 中选择。

[paper/paraphrase] 论文方案包括：500.12 MHz 主腔、1500.36 MHz TM020 谐波腔、被动运行候选、plunger frequency tuner、可选 active coupler 和 ferrite slot damping。（Main RF Cavity Design，PDF page 1；Power Coupler Design，PDF page 2；Harmonic Cavity Design，PDF pages 2–3；Figures 3, 5, 6, and 7）

[synthesis-inference/unverified] 该架构只能产生候选问题，不能直接产生用户设计决定。主动或被动运行、目标谐波电压、腔数、最终几何、frequency tuner、power/pickup/test coupler 和 HOM damping 方案均保持未决。

[external-llm/unverified] 如果选择被动运行，外部总结建议从束流频谱与失谐共同求得稳态电压，并显式处理填充间隙和瞬态；如果选择主动运行，则还需定义 RF source、控制与高功率输入链路。这些是辅助设计提示，不是该论文完成的当前项目分析。

[synthesis-inference/unverified] 建议按以下关卡推进，而不是复制论文尺寸：

1. 固定机器与 RF convention，包括主频、谐波数、峰值/RMS、$R/Q$ 和 shunt impedance 定义。
2. 用 [[Eigenmode solver]] 比较 TM020 候选几何的频率、[[R over Q]]、[[Q factor|Q0]]、表面场和 geometry factor。
3. 在所有端口与吸收体存在时计算工作模 [[External Q]] 和 [[Loaded Q]]。
4. 结合 [[Bunch spectrum]] 与 [[Longitudinal impedance]] 求被动电压、失谐和 fill-gap transient。
5. 评估 [[Higher-order mode]]、[[HOM impedance]]、[[Beam coupling impedance]] 和 [[Coupled-bunch instability]] 风险。
6. 完成热、机械、真空、调谐、诊断、制造与冷测方案后再冻结腔数和几何。

# 7. Equations and Convention Risks

## 7.1 R/Q and shunt impedance

[paper/paraphrase] 论文 Table 1 使用 $(R/Q)_a=V^2/(\omega U)$ 的定义，并分别报告 $Q$、$R/Q$ 和 shunt impedance。（Table 1 note，PDF page 2，printed page 2973）

[external-llm/unverified] 外部总结按此 accelerator convention 写为

$$
R_{\mathrm{sh}}=(R/Q)_a Q_0=\frac{V_{\mathrm{pk}}^2}{P_{\mathrm{wall}}}.
$$

[external-llm/unverified] 若电路模型把峰值谐振电阻定义为 $R_c=V_{\mathrm{pk}}^2/(2P)$，则 $R_c=R_{\mathrm{sh}}/2$。必须同时记录 [[R over Q]] convention、peak/RMS voltage 和平均功率，避免因子 2 错误。

## 7.2 Loaded Q and multiple ports

[external-llm/unverified] 对多个外部负载，外部总结给出的记账关系是

$$
\frac{1}{Q_L}=\frac{1}{Q_0}+\sum_i\frac{1}{Q_{\mathrm{ext},i}}.
$$

[external-llm/unverified] 单端口的 $\beta=Q_0/Q_{\mathrm{ext}}$ 和 $Q_L=Q_0/(1+\beta)$ 不能不加说明地用于多端口系统。pickup、HOM load、真空接口与内部吸收体都可能改变 dressed [[Loaded Q]]。

## 7.3 Beam harmonic and passive voltage

[external-llm/unverified] 外部总结区分正频率复 Fourier coefficient $I_{3h}=I_0F_3$ 与真实余弦峰值相量 $\hat I_{3,\mathrm{pk}}=2I_0F_3$；当使用 accelerator shunt impedance 时，谐振等效阻抗中相应出现 $R_{a,L}/2$。两者必须成对使用，不能各取一半约定。

[external-llm/unverified] $F_3$ 一般为复数。非对称束团、非高斯分布或 fill gap 存在时，不能只套用实数 Gaussian form factor；被动腔电压还依赖失谐、$Q_L$ 和自洽纵向分布。

## 7.4 Further convention traps

- [external-llm/unverified] Detuning 正负依赖 $e^{\pm i\omega t}$、电子电荷、相位坐标与正弦/余弦 convention。
- [external-llm/unverified] 场幅时间常数 $\tau_V=2Q_L/\omega$ 与储能时间常数 $\tau_U=Q_L/\omega$ 不可混用。
- [external-llm/unverified] 单模 [[Loss factor]] 公式也依赖所用的 $R/Q$ convention。
- [external-llm/unverified] $V_3/V_1\approx1/3$ 只对应特殊平势阱极限，不是所有被动谐波腔的通用目标。
- [requires-verification] “bunch-lengthening efficiency 与 shunt impedance 成正比”必须补齐 efficiency、运行模式、失谐、束流与自洽条件后再使用。

# 8. Conflicts, Uncertainties, and Required Verification

## 8.1 Evidence conflicts and scope limits

- [requires-verification] 论文 “higher shunt impedance” 的比较对象不清，不能建立普适 TM020 优势。
- [synthesis-inference/unverified] “high shunt impedance makes it fit” 更可能指功耗、冷却、腔数和整机集成收益，不是横向半径因果关系。
- [requires-verification] 主腔 coupling-tuner 结论不能直接迁移到 1500 MHz 被动谐波腔。
- [synthesis-inference/unverified] 论文为主腔和谐波腔都选 TM020；当前项目只把它作为约 1500 MHz 谐波腔候选。
- [requires-verification] 论文 $Q_0=36{,}000$ 不能当成带所有端口、吸收体和制造误差后的 $Q_L$。
- [external-llm/unverified] 外部总结没有当前设计的 EM、束流动力学、HOM、热机械或测试结果，其 Candidate Personal Notes 也没有完整原始对话可供独立核验。

## 8.2 Required machine and beam verification

- [requires-verification] 主 RF 电压与相位、目标谐波电压、总电流、逐 bucket 电荷、填充图样与 fill gap。
- [requires-verification] 动量压缩因子、同步相位、能散、自然束长、横纵向发射度、耦合、IBS、光学与局部动量接受度。
- [requires-verification] 以 Haïssinski/self-consistent longitudinal distribution 求基线和双 RF 束团分布，并检查 gap transient。
- [requires-verification] Touschek、IBS、RF acceptance、Robinson 与 coupled-bunch stability 的一致模型和不确定性。

## 8.3 Required cavity verification

- [requires-verification] Dressed eigenmode 频率、$R/Q$、$Q_0$、geometry factor、峰值表面电场/磁场和 multipacting。
- [requires-verification] 每个 port/load 的 $Q_{\mathrm{ext}}$、总 $Q_L$、工作模泄漏与可调范围。
- [requires-verification] 纵横向 HOM spectrum、阻抗、kick/loss factor、beam-pipe propagation 和 coupled-bunch thresholds。
- [requires-verification] tuner 灵敏度与交叉耦合、制造公差、热漂移、Lorentz/机械变形、冷却、真空和 ferrite 热负荷。
- [requires-verification] VNA 冷测、[[S parameter]]、pickup 标定、高场老炼、保护与运行恢复方案。

# 9. Existing Concepts

[synthesis-inference/unverified] 以下链接只指向当前数据库中已经存在的 canonical Concept；本阶段不修改 Concept 或 index。

- 工作模与 RF 参数：[[Cavity mode]]、[[R over Q]]、[[Q factor|Q0]]、[[Shunt impedance]]、[[Loaded Q]]、[[External Q]]。
- 束流与阻抗：[[Bunch spectrum]]、[[Beam coupling impedance]]、[[Longitudinal impedance]]、[[Loss factor]]、[[Coupled-bunch instability]]。
- 寄生模与端口：[[Higher-order mode]]、[[HOM impedance]]、[[HOM coupler]]。
- 数值与测量：[[Eigenmode solver]]、[[S parameter]]。

# 10. Concept Gaps

[synthesis-inference/unverified] 下列名称仅是纯文本缺口，不是 Wikilink；本阶段不创建 Concept、不修改 index，也不生成 proposal。

- TM020 mode — 依据：论文两种腔型的候选工作模与 rw-entry-0001 的比较问题。
- Harmonic cavity — 依据：1500.36 MHz 三次谐波设计背景。
- Passive harmonic cavity — 依据：论文被动运行基线与 rw-entry-0002。
- Beam loading — 依据：被动腔由束流激励的物理过程尚未形成 canonical Concept。
- Frequency tuner — 依据：主腔铜杆和谐波腔 plunger 的频率调节。
- Coupling tuner — 依据：主腔 waveguide coupling-tuner post 与 rw-entry-0002。
- Detuning — 依据：被动电压、相位与 convention 风险。
- Bunch lengthening — 依据：rw-entry-0004 及谐波腔目标。
- Fill gap — 依据：非均匀填充下的瞬态和复数束流谱。
- Touschek lifetime — 依据：rw-entry-0005 的 factor 4 概念解析。
- Robinson instability — 依据：被动腔稳定性核验需求。
- Haïssinski equation — 依据：自洽纵向分布与寿命复算需求。

# 11. Session Coverage

[synthesis-inference/unverified] 覆盖以 `reading_session.md` 中的五个原始 entry 为准；外部总结没有被伪装或导入为 session entry。

| entry_id | entry_type | source_locator | draft section | disposition |
| --- | --- | --- | --- | --- |
| `rw-entry-0001` | `human_question` | `Abstract` | 4.1 | 保留 session 框选原文与原始问题；论文回答、外部解释、综合推断和未解决项分层 |
| `rw-entry-0002` | `human_question` | `Power Coupler Design` | 4.2 | 保留 session 框选原文与原始问题；区分主腔 coupling tuner、被动谐波腔与端口功能 |
| `rw-entry-0003` | `human_note` | `Parasitic Modes Damping Design` | 5.1 | 保留 session 框选原文与原始笔记；转为 `[3]`、`[8]`、`[12]` 的核验与比较行动，不虚构文献 |
| `rw-entry-0004` | `human_note` | `Harmonic Cavity Design` | 5.2 | 保留 session 框选原文与原始笔记；转为 `[6]`、`[7]` 和比例关系条件的核验行动，不虚构文献 |
| `rw-entry-0005` | `human_note` | `Source page marker: PDF page 3 (printed page 2974)` | 5.3 | 保留 session 框选原文与原始笔记；分开论文 factor 4、外部物理解释、本轮边界和机器复算 |

[synthesis-inference/unverified] Coverage result: **2 questions + 3 notes = 5/5 covered**.

# 12. Human Review Checklist

- [ ] 确认 YAML、`state: draft` 和三条输入路径正确；不要添加 `human_reviewed`。
- [ ] 核对所有 `[paper/*]` 陈述的 section、PDF page、Table/Figure locator 和数值。
- [x] 确认 rw-entry-0001 与 rw-entry-0002 的原始问题未被外部总结改写。
- [x] 确认 rw-entry-0003 与 rw-entry-0004 只产生文献 follow-up，没有虚构参考文献。
- [x] 确认 rw-entry-0005 的 factor 4 没有被误写为当前机器指标或通用规律。
- [ ] 决定 “higher shunt impedance” 的比较基准是否需要回查引用文献。
- [ ] 决定当前 1500 MHz 项目是否继续比较主动与被动方案，以及需要保留哪些 coupler/port 功能。
- [ ] 固定 $R/Q$、shunt impedance、peak/RMS/Fourier、detuning 与 $Q$ conventions。
- [ ] 核对所有正式 Wikilink 均指向现有 Concept，Concept Gaps 保持纯文本。
- [ ] 确认论文设计没有被写成用户 500 MHz 主腔的 TM020 决定。
- [ ] 记录审阅中接受、修改或删除的具体段落；只有后续人工冻结阶段才能生成最终 `reading_note.md`。
- [x] 记录 repository owner 于 2026-08-18 接受 RW-03 synthesis content；该决定不赋予 artifact `human_reviewed`。
- [ ] 除非另行授权，保持 RW-04、Concept proposal 和 KA-01 未启动。
