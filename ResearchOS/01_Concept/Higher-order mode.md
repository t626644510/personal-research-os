---
id: higher_order_mode
aliases:
  - higher order mode
  - parasitic cavity mode
  - 高次模
category:
  - cavity physics
  - accelerator physics
level: working
confidence:
  textbook: high
  personal: medium
origin:
  - textbook
  - simulation
created: 2026-08-02
updated: 2026-08-03
---

# Higher-order mode

## Hover Summary

高次模是加速结构中除目标工作模之外的本征电磁模；束流可激励这些模，导致附加能量损失、发热、发射度增长或多束团不稳定性。

## Definition

在 RF accelerating structure 中，设计用于主要加速或操纵束流的 mode 之外，其余 cavity eigenmodes 统称 higher-order modes。它们可能是 monopole、dipole 或更高 multipole。

## My Understanding

HOM 不是天然“坏模”；危险性取决于其频率、$R/Q$、loaded Q、束流谱线和极化。低耦合或快速衰减的 mode 通常影响有限。

## Engineering View

需要联合 eigenmode 和 wakefield 结果建立 mode table，并检查 trapped mode、制造误差、极化分裂和 coupler 加载。只按频率阈值区分 HOM 不够可靠。

## Formula

单个 HOM 的纵向阻抗常近似为 resonator：

$$
Z_{\parallel}(\omega)=\frac{R_s}
{1+iQ_L(\omega/\omega_r-\omega_r/\omega)}.
$$

## Application

用于制定 HOM damping 指标、选择 coupler 和 absorber、预测 beam-induced heating，并识别 wake impedance spectrum 中的窄带峰。

## Related Concepts

- [[Cavity mode]]
- [[HOM impedance]]
- [[HOM coupler]]
- [[Beam pipe cutoff frequency]]

## Sources

- N. Baboi, [HOM Mitigation](https://indico.cern.ch/event/1212689/contributions/5377906/), CERN Accelerator School, 2023.
- R. Wanzenberg, [Impedances and Instabilities](https://cds.cern.ch/record/2941653), CERN Accelerator School, 2020.

## Decision Log

- 2026-08-02 — 保留 HOM 缩写对既有 `HOM impedance` 的向后兼容映射；本概念使用完整名称和“高次模”作为查询词。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
- 2026-08-03 — 将 Hover Summary 调整为中文主语言；稳定 ID、canonical name 和 aliases 不变。
