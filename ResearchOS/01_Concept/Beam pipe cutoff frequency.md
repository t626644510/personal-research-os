---
id: beam_pipe_cutoff_frequency
aliases:
  - beam-pipe cutoff
  - waveguide cutoff frequency
  - 束管截止频率
category:
  - RF engineering
  - waveguide theory
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

# Beam pipe cutoff frequency

## Hover Summary

Beam pipe cutoff frequency 是给定波导 mode 从倏逝变为可传播的最低频率；它决定 cavity HOM 能否沿束管逃逸到外部 absorber 或被局域困住。

## Definition

束管可视为波导。对每个 TE 或 TM mode，横向边界条件给出 cutoff wavenumber；低于相应 cutoff 的场沿轴向指数衰减，高于 cutoff 才具有实数传播常数。

## My Understanding

截止频率不是束管唯一的一个数字，而是“某个截面、某个 mode”的阈值。一个 HOM 可能高于某 mode 的 cutoff，却因对称性而仍耦合很弱。

## Engineering View

评估传播时要使用真实截面、极化和边界，不应只套圆波导最低 mode。渐变、coupler 和周期结构会改变局部传播与反射，必要时用 S parameter 验证。

## Formula

半径为 $a$ 的理想圆波导中：

$$
f_{c,\mathrm{TE}_{mn}}=\frac{x'_{mn}c}{2\pi a},
\qquad
f_{c,\mathrm{TM}_{mn}}=\frac{x_{mn}c}{2\pi a},
$$

其中 $x'_{mn}$ 与 $x_{mn}$ 分别为 Bessel 导数和 Bessel 函数的零点。

## Application

用于选择 beam pipe 半径、判断 propagating 与 trapped HOM、布置 HOM absorber，并设置开放边界或 waveguide port 的 mode 数量。

## Related Concepts

- [[Higher-order mode]]
- [[HOM coupler]]
- [[Cavity mode]]
- [[S parameter]]

## Sources

- E. Jensen, [Cavity basics](https://cds.cern.ch/record/1416619), CERN Accelerator School, 2011.
- [CAS: RF for Accelerators](https://cds.cern.ch/record/1231364), CERN, 2011.

## Decision Log

- 2026-08-02 — cutoff 数据必须与截面和 mode 标签绑定，禁止在项目中只写无上下文的单一 cutoff 值。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
