---
id: hom_coupler
aliases:
  - higher-order-mode coupler
  - HOM damper
  - 高次模耦合器
category:
  - RF engineering
  - accelerator hardware
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

# HOM coupler

## Hover Summary

高次模耦合器从加速腔中选择性抽取高次模功率并送往负载，从而降低危险模的外部 Q、阻抗峰值和束流诱导热负荷。

## Definition

Higher-order-mode coupler 是与 cavity 或 beam pipe 电磁耦合的阻尼器件，通常通过天线、环或波导结构把 HOM 能量导向外部匹配负载，同时抑制对工作模的耦合。

## My Understanding

它是给 HOM 增加一条受控的能量泄漏路径。设计关键不是“耦合越强越好”，而是对危险 HOM 强耦合、对 accelerating mode 足够隔离。

## Engineering View

需要逐模评估 $Q_{\mathrm{ext}}$、notch rejection、峰值场、热负荷、multipacting、真空与制造误差。单一端口可能因 mode 极化或场节点而漏掉某些 HOM。

## Formula

多个独立 coupler 加载同一 mode 时：

$$
\frac{1}{Q_L}=\frac{1}{Q_0}+\sum_k\frac{1}{Q_{\mathrm{ext},k}}.
$$

降低 $Q_L$ 通常同时降低 resonant shunt impedance。

## Application

用于 superconducting 和 normal-conducting cavity 的 HOM damping，降低 coupled-bunch growth rate、寄生功率沉积和 cryogenic heat load。

## Related Concepts

- [[Higher-order mode]]
- [[HOM impedance]]
- [[External Q]]
- [[Beam pipe cutoff frequency]]

## Sources

- N. Baboi, [HOM Mitigation](https://indico.cern.ch/event/1212689/contributions/5377906/), CERN Accelerator School, 2023.
- J. A. Mitchell, [HOM couplers for crab cavities and challenges](https://indico.cern.ch/event/817780/contributions/3715797/), CERN, 2020.

## Decision Log

- 2026-08-02 — HOM coupler 的性能以逐模 $Q_{\mathrm{ext}}$ 表保存；单一“damping factor”只作为摘要，不作为可追溯原始量。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
- 2026-08-03 — 将 Hover Summary 调整为中文主语言；稳定 ID、canonical name 和 aliases 不变。
