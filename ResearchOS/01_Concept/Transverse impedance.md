---
id: transverse_impedance
aliases:
  - Z transverse
  - transverse coupling impedance
  - 横向阻抗
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

# Transverse impedance

## Hover Summary

横向阻抗描述偏轴束流激励的电磁场如何对后续粒子施加横向踢力，常以 Ω/m 表示，是横向相干频移、发射度增长和不稳定性分析的核心量。

## Definition

Transverse impedance $Z_{\perp}(\omega)$ 是横向 wake 的频域表示。在偶极近似下，它把源束团的横向偏移和电流谱映射为测试粒子所受的横向感应电压或动量踢力。

## My Understanding

源束团若完全居中，理想对称结构中的偶极横向响应很小；一旦偏轴，它会留下带方向的 wake，后续束团因此被继续推离或拉回参考轨道。

## Engineering View

必须注明驱动平面、观测平面、源偏移归一化和单位。非对称结构可能需要完整的横向阻抗矩阵，而不能只保存一个标量峰值。

## Formula

一种常见约定为：

$$
Z_{\perp}(\omega)=-\frac{i}{c}\int_{-\infty}^{\infty}
W_{\perp}(s)e^{i\omega s/c}\,ds.
$$

$W_{\perp}$ 的源偏移归一化及整体符号必须与使用的束流动力学代码一致。

## Application

用于评估 transverse coupled-bunch instability、beam break-up、横向 mode coupling，以及 kicker、collimator、RF cavity 和 vacuum component 的偶极响应。

## Related Concepts

- [[Beam coupling impedance]]
- [[Transverse wake potential]]
- [[Kick factor]]
- [[Panofsky-Wenzel theorem]]

## Sources

- R. Wanzenberg, [Impedances and Instabilities](https://cds.cern.ch/record/2941653), CERN Accelerator School, 2020.
- K. Bane and M. Sands, [Wakefields of Very Short Bunches in an Accelerating Cavity](https://www.slac.stanford.edu/pubs/slacpubs/4000/slac-pub-4169.pdf), SLAC-PUB-4169, 1986.

## Decision Log

- 2026-08-02 — 将 transverse impedance 与 transverse wake potential 分开建模，以显式保留频域和时域的单位差异。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
- 2026-08-03 — 将 Hover Summary 调整为中文主语言；稳定 ID、canonical name 和 aliases 不变。
