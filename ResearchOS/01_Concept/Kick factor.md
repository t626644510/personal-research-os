---
id: kick_factor
aliases:
  - transverse kick factor
  - k kick
  - 踢因子
category:
  - accelerator physics
  - collective effects
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

# Kick factor

## Hover Summary

踢因子把有限长度束团激励的横向尾场归一化为单位电荷、单位源偏移下的横向踢力强度，用于快速比较结构的束流崩溃（BBU）风险。

## Definition

横向 kick factor 是 transverse wake potential 对给定束团分布的有效加权结果。在偶极近似中，它关联源束团偏移、源与测试电荷以及测试粒子的横向动量变化。

## My Understanding

它是横向版本的 loss factor，但衡量的不是耗散能量，而是偏轴源束团给后续粒子留下多强的方向性踢力。

## Engineering View

必须注明平面、源偏移归一化、束团长度、测试粒子位置和单位。对非对称结构，应分别报告 direct 与 cross-plane 项，而不是混成一个数值。

## Formula

一种偶极归一化写法为：

$$
\Delta p_{\perp}c=q_s q_t x_s k_{\perp},
$$

其中 $q_s$、$q_t$ 是源和测试电荷，$x_s$ 是源偏移；整体符号由坐标与 wake 定义决定。

## Application

用于比较 cavity、collimator、beam position monitor 和 taper 的横向 wake，设置偏轴 wakefield 仿真的验收指标，并估算多束团累积踢力。

## Related Concepts

- [[Transverse wake potential]]
- [[Transverse impedance]]
- [[Gaussian bunch]]
- [[Panofsky-Wenzel theorem]]

## Sources

- K. Bane and M. Sands, [Wakefields of Very Short Bunches in an Accelerating Cavity](https://www.slac.stanford.edu/pubs/slacpubs/4000/slac-pub-4169.pdf), SLAC-PUB-4169, 1986.
- M. Ferrario, M. Migliorati, and L. Palumbo, [Wake fields and instabilities in linear accelerators](https://cds.cern.ch/record/941328), CERN Accelerator School, 2006.

## Decision Log

- 2026-08-02 — 在 Concept 中保留物理归一化；软件特定的 kick factor 单位换算交给 Experiment 记录。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
- 2026-08-03 — 将 Hover Summary 调整为中文主语言；稳定 ID、canonical name 和 aliases 不变。
