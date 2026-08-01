---
id: shunt_impedance
aliases:
  - shunt resistance
  - cavity shunt impedance
  - 分路阻抗
category:
  - RF engineering
  - accelerator physics
level: working
confidence:
  textbook: high
  personal: medium
origin:
  - textbook
  - measurement
created: 2026-08-02
updated: 2026-08-02
---

# Shunt impedance

## Hover Summary

Shunt impedance 衡量 RF cavity 用给定耗散功率建立加速电压的效率；它同时包含几何耦合能力 R/Q 与损耗水平 Q，比较时必须注明定义约定。

## Definition

分路阻抗 $R$ 把 cavity mode 的有效加速电压与功率损耗联系起来。CERN 常见的 circuit-ohm 约定为 $R=|V_{\mathrm{acc}}|^2/(2P)$，linac 文献中也常省略因子 2。

## My Understanding

$R/Q$ 说明几何能否把储能变成有效电压，Q 说明能量漏得多快；shunt impedance 是两者结合后的实际 RF 效率指标。

## Engineering View

报告时要注明 circuit-ohm 或 linac-ohm、使用 unloaded 还是 loaded Q、积分路径、transit-time factor 和 mode 类型。不同约定下的数值不能直接排名。

## Formula

在 circuit-ohm 约定中：

$$
R=\frac{|V_{\mathrm{acc}}|^2}{2P}
=\left(\frac{R}{Q}\right)Q.
$$

## Application

用于优化 accelerating cavity 的功率效率，建立 HOM resonator 模型，并把 eigenmode 求得的 $R/Q$ 与材料损耗或外部阻尼结合起来。

## Related Concepts

- [[R over Q]]
- [[Q factor]]
- [[Loaded Q]]
- [[HOM impedance]]

## Sources

- E. Jensen, [Cavity basics](https://cds.cern.ch/record/1416619), CERN Accelerator School, 2011.
- [CAS: RF for Accelerators](https://cds.cern.ch/record/1231364), CERN, 2011.

## Decision Log

- 2026-08-02 — 默认正文采用 circuit-ohm 约定，并要求任何项目数据显式记录是否含因子 2。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
