---
id: external_q
aliases:
  - external quality factor
  - Qext
  - 外部Q值
category:
  - RF engineering
  - resonator physics
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

# External Q

## Hover Summary

External Q 衡量 cavity mode 通过某个外部端口或 coupler 泄出能量的速度；数值越低表示耦合越强、外部阻尼越快。

## Definition

$Q_{\mathrm{ext}}$ 由模式储能与指定外部通道带走的功率定义，不包含 cavity 壁面和介质的内部耗散。每个独立 coupler 或传播端口可有自己的 external Q。

## My Understanding

它把 coupler 对某个 mode 的“抽能能力”变成无量纲数字。对危险 HOM，希望 $Q_{\mathrm{ext}}$ 足够低；对工作模则按 RF 功率和带宽需求选择耦合。

## Engineering View

端口位置、极化、参考面和边界条件都会改变求得的 $Q_{\mathrm{ext}}$。比较方案时应逐模记录，并检查 coupler 是否意外加载 accelerating mode。

## Formula

对角频率 $\omega_0$ 的 mode：

$$
Q_{\mathrm{ext}}=\frac{\omega_0 U}{P_{\mathrm{ext}}},
$$

其中 $P_{\mathrm{ext}}$ 是经指定外部通道流出的平均功率。

## Application

用于 power coupler 匹配、HOM coupler 阻尼规格、loaded Q 计算，以及评估 mode 能否通过 beam pipe 传播到外部 absorber。

## Related Concepts

- [[Loaded Q]]
- [[Q factor]]
- [[HOM coupler]]
- [[Beam pipe cutoff frequency]]

## Sources

- E. Jensen, [Cavity basics](https://cds.cern.ch/record/1416619), CERN Accelerator School, 2011.
- V. Veshcherevich et al., [Input Coupler for ERL Injector Cavities](https://cds.cern.ch/record/677988), PAC 2003.

## Decision Log

- 2026-08-02 — external Q 按 mode 和外部通道建模，不把多个 coupler 的效果提前压成一个无法追溯的数值。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
