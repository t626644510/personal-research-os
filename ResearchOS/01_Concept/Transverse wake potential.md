---
id: transverse_wake_potential
aliases:
  - transverse wake
  - transverse wake voltage
  - 横向尾势
category:
  - accelerator physics
  - electromagnetics
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

# Transverse wake potential

## Hover Summary

Transverse wake potential 是有限束团激励后对测试粒子产生的横向积分力响应，通常按源束团偏移归一化，并分为水平、垂直及交叉平面分量。

## Definition

Transverse wake potential 由 transverse point wake 与 drive bunch 分布卷积得到。偶极项与源偏移一阶相关，并给出后续粒子的横向动量变化或等效 transverse voltage。

## My Understanding

它描述“偏轴束团走过以后，后面的粒子在每个 longitudinal separation 上会被踢多少”。正负号同时依赖源偏移方向和坐标定义。

## Engineering View

应分别保存 drive offset、test offset、观测平面、单位和 normalization。偏移过大可能混入高阶 multipole，偏移过小则可能被数值噪声淹没。

## Formula

对线密度 $\lambda(s)$，可写成：

$$
\mathbf V_{\perp}(s)=q\int_{-\infty}^{\infty}
\mathbf W_{\perp}(s-s')\lambda(s')\,ds'.
$$

具体实现常再除以源横向偏移，以得到偶极归一化量。

## Application

用于计算 kick factor、beam break-up、transverse impedance 和多束团累积踢力，并评估非对称结构的 cross-plane coupling。

## Related Concepts

- [[Wakefield]]
- [[Transverse impedance]]
- [[Kick factor]]
- [[Panofsky-Wenzel theorem]]

## Sources

- K. Bane and M. Sands, [Wakefields of Very Short Bunches in an Accelerating Cavity](https://www.slac.stanford.edu/pubs/slacpubs/4000/slac-pub-4169.pdf), SLAC-PUB-4169, 1986.
- M. Ferrario, M. Migliorati, and L. Palumbo, [Wake fields and instabilities in linear accelerators](https://cds.cern.ch/record/941328), CERN Accelerator School, 2006.

## Decision Log

- 2026-08-02 — transverse 数据必须带 drive offset 和平面标签；P01 索引只暴露概念摘要，不承载数值曲线。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
