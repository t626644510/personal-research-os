---
id: harmonic_cavity
aliases:
  - 谐波腔
category:
  - accelerator physics
  - RF engineering
level: working
confidence:
  textbook: medium
  personal: low
origin:
  - paper
  - manual
created: 2026-08-18
updated: 2026-08-18
---
# Harmonic cavity

## Hover Summary

谐波腔是工作在主 RF 系统整数谐波频率、用于塑造纵向 RF 势阱的 RF 腔；选定论文案例为约 500.12 MHz 主频的 1500.36 MHz 三次谐波腔。

## Definition

谐波腔是工作在主 RF 系统整数谐波频率的 RF cavity，用附加的谐波电压塑造纵向 RF 势阱。若主频为 $f_0$，谐波频率可写为 $f_h=nf_0$，其中 $n$ 为正整数；这一定义与单篇论文案例区分开。选定论文的案例是 $n=3$、约 500.12 MHz 主 RF 与 1500.36 MHz 谐波腔，不构成当前项目的设计决定。

## My Understanding

我把 harmonic cavity 理解为用整数谐波 RF 电压改变纵向势阱形状的腔体，而不是某一个固定频率或固定几何。被动运行和主动运行是同一硬件 Concept 下的 operating mode；当前项目采用哪一种、需要哪些端口，仍须另行决定。

## Engineering View

论文案例报告 unloaded Q, Q0 = 36,000、paper-reported R/Q = 68 ohm、shunt impedance 2.45 Mohm、腔体直径 354.514 mm、Table 2 insertion length 300 mm、90 mm effective length 和 40 mm beam-port diameter；R/Q 的 convention 不能无条件泛化。这些数值以及六腔、总 shunt impedance 14.7 Mohm 的配置都只是论文特定设计。被动运行表示正常情况下没有 RF power supply 主动驱动；可选 active operation 可使用 rotatable coaxial loop coupler。P02 的被动运行方式作为本 Concept 内部小节，而不是自动 alias；当前项目的主动/被动模式、端口、腔数、几何和适用性仍未决定。

## Formula

$$
f_h=nf_0,\qquad \omega_h=n\omega_0,
$$

其中 $f_0$ 和 $\omega_0$ 是主 RF 频率和角频率，$f_h$ 和 $\omega_h$ 是谐波腔频率和角频率，$n\in\mathbb{Z}_{>0}$ 是谐波次数。该关系只定义频率关系，不定义谐波电压、相位、束团分布或完整的 bunch-lengthening model；选定论文的示例为 $n=3$。

该整数谐波关系以及被动/主动运行方式的解释，是基于选定论文案例和人类批准的 KA-02 范围决定的有界综合；它不是论文原句，也不是完整的 bunch-lengthening model。

## Application

选定论文将谐波腔作为三次谐波系统用于 bunch lengthening，并报告六腔的论文特定方案。当前项目可用它作为 benchmark/reference，仍需以本机 RF、束流、热、机械、真空、阻抗和集成输入重新验证；论文的 lifetime factor 4 不是通用规则或当前项目指标。

## Related Concepts

- [[Cavity mode]]
- [[Shunt impedance]]
- [[R over Q]]
- [[Q factor]]
- [[Tuner]]

These links resolve to existing stable Concepts; this promotion does not alter
those Concepts.

## Sources

- Origin handling: `paper` covers source-specific facts; `manual` covers the
  bounded synthesis accepted by human reviewer `owner-01` in KA-03 Stage 2.

- Selected source: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`; locators `3.1 Double-RF context and frequencies`, `3.3 Harmonic-cavity parameters`, `3.4 Frequency tuners and couplers are different functions`, and `3.5 Six harmonic cavities and the lifetime claim`.

## Decision Log

2026-08-18：依据 KA-02 `retain_for_revision` 方向，owner-01 接受将 P02 的 passive operation 吸收为 Harmonic cavity 的 operating-mode 小节；不把 `Passive harmonic cavity` 或 `被动谐波腔` 自动设为 alias，不冻结当前项目的运行模式或工程参数。

## History

- 2026-08-18 - Created as a proposed candidate by KA-01; pending human review.
- 2026-08-18 - Revised under the human-approved KA-02 direction; state remained proposed and human approval is pending.
- 2026-08-18 - owner-01 accepted the complete revised candidate and authorized manual promotion in KA-03 Stage 2; project-specific mode and engineering limitations remain open.
