---
id: longitudinal_wake_potential
aliases:
  - longitudinal wake
  - longitudinal wake voltage
  - 纵向尾势
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

# Longitudinal wake potential

## Hover Summary

Longitudinal wake potential 是点电荷纵向 wake 与有限束团电荷分布的卷积，给出束团内部或后续测试粒子沿束流方向所见的感应电压。

## Definition

给定 longitudinal wake function $W_{\parallel}(s)$ 和线密度 $\lambda(s)$，longitudinal wake potential 是对所有源切片贡献的因果叠加；它依赖结构，也依赖所选束团形状。

## My Understanding

Wake function 类似结构的 Green function，wake potential 则是把真实束团作为输入后得到的可直接观察响应。因此改变 bunch length 会改变 potential，即使几何不变。

## Engineering View

导出结果时应保存 drive bunch charge、归一化线密度、rms 长度、wake length、零点位置和符号。有限束长数据去卷积成阻抗时要避免在频谱尾部放大噪声。

## Formula

一种因果卷积约定为：

$$
V_{\parallel}(s)=-q\int_{-\infty}^{\infty}
W_{\parallel}(s-s')\lambda(s')\,ds'.
$$

负号是否显式出现取决于 wake 与感应电压的定义。

## Application

用于计算束内 energy variation、loss factor、后续束团能量偏移，并通过 Fourier transform 获得 longitudinal impedance。

## Related Concepts

- [[Wakefield]]
- [[Longitudinal impedance]]
- [[Loss factor]]
- [[Panofsky-Wenzel theorem]]

## Sources

- L. Palumbo, V. G. Vaccaro, and M. Zobov, [Wake fields and impedance](https://cds.cern.ch/record/276437), CERN Accelerator School, 1995.
- M. Ferrario, M. Migliorati, and L. Palumbo, [Wake fields and instabilities in linear accelerators](https://cds.cern.ch/record/941328), CERN Accelerator School, 2006.

## Decision Log

- 2026-08-02 — 将有限束团输出命名为 wake potential，与点电荷 wake function 严格区分。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
