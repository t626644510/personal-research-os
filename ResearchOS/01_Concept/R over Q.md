---
id: r_over_q
aliases:
  - R/Q
  - shunt impedance over Q
  - R比Q
category:
  - RF engineering
  - cavity physics
level: working
confidence:
  textbook: high
  personal: medium
origin:
  - textbook
  - simulation
created: 2026-08-02
updated: 2026-08-02
---

# R over Q

## Hover Summary

R over Q 是仅由 cavity mode 场分布和几何决定的耦合指标，衡量单位储能能产生多少有效加速电压；它不依赖壁面电导率造成的 Q 损耗。

## Definition

$R/Q$ 将某个本征模沿参考轨道的有效电压与该模储能归一化。对于给定 mode 和电压定义，它是几何量，不随壁面损耗模型改变。

## My Understanding

如果两个 cavity 有相同储能，$R/Q$ 较高者能在束流轨道上提供更高的有效电压；但实际所需 RF 功率还要乘入 Q 所反映的损耗。

## Engineering View

应保存 mode、积分路径、粒子速度、transit-time factor 和 circuit/linac 约定。纵向、横向及不同 multipole 的 $R/Q$ 具有不同单位和偏移归一化。

## Formula

在 circuit-ohm 约定中：

$$
\frac{R}{Q}=\frac{|V_{\mathrm{acc}}|^2}{2\omega_0 U},
$$

其中 $U$ 为总储能，$\omega_0$ 为本征角频率；linac-ohm 约定通常不含分母中的 2。

## Application

用于比较 cavity geometry、筛选危险 HOM、构造 resonator impedance，并将 eigenmode solver 输出与 Q factor 组合成 shunt impedance。

## Related Concepts

- [[Shunt impedance]]
- [[Cavity mode]]
- [[Q factor]]
- [[Eigenmode solver]]

## Sources

- E. Jensen, [Cavity basics](https://cds.cern.ch/record/1416619), CERN Accelerator School, 2011.
- N. Baboi, [HOM Mitigation](https://indico.cern.ch/event/1212689/contributions/5377906/), CERN Accelerator School, 2023.

## Decision Log

- 2026-08-02 — 不使用“geometry factor”作为别名，因为 SRF 中 geometry factor $G=Q_0R_s$ 是不同物理量。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
