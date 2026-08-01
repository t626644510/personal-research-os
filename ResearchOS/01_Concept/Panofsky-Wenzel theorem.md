---
id: panofsky_wenzel_theorem
aliases:
  - Panofsky Wenzel theorem
  - P-W theorem
  - 潘诺夫斯基-温泽尔定理
category:
  - accelerator physics
  - electromagnetics
level: working
confidence:
  textbook: high
  personal: medium
origin:
  - paper
  - textbook
created: 2026-08-02
updated: 2026-08-02
---

# Panofsky-Wenzel theorem

## Hover Summary

Panofsky-Wenzel theorem 用 Maxwell 方程把横向 wake 对纵向间距的变化与纵向 wake 的横向梯度联系起来，说明两类束流踢力不是独立响应。

## Definition

对满足适当边界和因果条件的超相对论性 wake，Panofsky-Wenzel relation 连接 integrated longitudinal force 与 transverse momentum kick 的空间导数。

## My Understanding

若纵向 wake 在横向位置上有梯度，就必然伴随随纵向间距变化的横向 wake。它是核对数值 wake 数据自洽性的物理约束。

## Engineering View

应用前必须统一 $s$ 的正方向、wake 的符号和 transverse normalization。有限积分范围、噪声与网格误差会让数值微分明显放大偏差。

## Formula

一种常见符号约定为：

$$
\frac{\partial\mathbf W_{\perp}}{\partial s}
=\nabla_{\perp}W_{\parallel}.
$$

若 $s$ 定义方向相反，等式会出现整体负号。

## Application

用于从纵向场梯度推导横向 wake、检查 wakefield solver 输出、理解 dipole mode 的 longitudinal 与 transverse coupling。

## Related Concepts

- [[Longitudinal wake potential]]
- [[Transverse wake potential]]
- [[Wakefield]]
- [[Kick factor]]

## Sources

- K. Bane and M. Sands, [Wakefields of Very Short Bunches in an Accelerating Cavity](https://www.slac.stanford.edu/pubs/slacpubs/4000/slac-pub-4169.pdf), SLAC-PUB-4169, 1986.
- S. Heifets and S. Kheifets, [Coupling Impedance in Modern Accelerators](https://www.slac.stanford.edu/pubs/slacpubs/5250/slac-pub-5297.pdf), SLAC-PUB-5297, 1991.

## Decision Log

- 2026-08-02 — 公式旁强制记录坐标约定，避免将不同文献中的正负号差异误判为物理冲突。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
