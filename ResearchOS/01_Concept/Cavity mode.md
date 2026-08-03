---
id: cavity_mode
aliases:
  - resonant cavity mode
  - electromagnetic cavity mode
  - 腔模
category:
  - cavity physics
  - electromagnetics
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

# Cavity mode

## Hover Summary

腔模是满足结构边界条件的离散电磁本征场分布；每个模具有特定频率、极化、储能、Q 值和束流耦合强度。

## Definition

在给定材料与边界条件下，Maxwell 方程允许一组离散本征解。每个解的电场、磁场和本征频率共同定义一个 cavity mode，可按 TE、TM、multipole 或 passband 位置分类。

## My Understanding

几何决定 cavity 可以怎样“振铃”。Accelerating mode 是有意使用的一个解，其余能被束流激励的解可能成为 higher-order modes。

## Engineering View

识别 mode 不能只看频率，还要检查场分布、极化、phase advance、$R/Q$、Q 和端口耦合。几何对称性可能产生简并 mode，网格或 coupler 会打破简并。

## Formula

无源频域电场本征问题可写为：

$$
\nabla\times\mu^{-1}\nabla\times\mathbf E
=\omega^2\varepsilon\mathbf E,
$$

并满足导体、周期或开放边界条件。

## Application

用于设计 RF cavity、识别 accelerating 和 parasitic modes、计算 $R/Q$ 与 Q，并为 wakefield 频谱中的共振峰提供 mode 归属。

## Related Concepts

- [[Higher-order mode]]
- [[R over Q]]
- [[Q factor]]
- [[Eigenmode solver]]

## Sources

- E. Jensen, [Cavity basics](https://cds.cern.ch/record/1416619), CERN Accelerator School, 2011.
- [CAS: RF for Accelerators](https://cds.cern.ch/record/1231364), CERN, 2011.

## Decision Log

- 2026-08-02 — mode 身份由场分布和对称性共同确认；禁止仅按频率最近邻自动命名 mode。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
- 2026-08-03 — 将 Hover Summary 调整为中文主语言；稳定 ID、canonical name 和 aliases 不变。
