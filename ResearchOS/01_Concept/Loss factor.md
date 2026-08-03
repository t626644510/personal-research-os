---
id: loss_factor
aliases:
  - wake loss factor
  - k loss
  - 损耗因子
category:
  - accelerator physics
  - RF engineering
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

# Loss factor

## Hover Summary

损耗因子把给定束团形状经过结构时的纵向能量损失归一化到束团电荷平方；它同时依赖结构阻抗和束团频谱，不是只由结构决定的常数。

## Definition

纵向 loss factor $k_{\mathrm{loss}}$ 定义单个束团因 wakefield 留在结构中的能量 $U_{\mathrm{loss}}$ 与束团电荷 $q$ 的关系，常写成 $U_{\mathrm{loss}}=k_{\mathrm{loss}}q^2$。

## My Understanding

同一结构对短束团和长束团可给出不同 loss factor，因为短束团含有更多高频成分，能够激励更多高频模态。

## Engineering View

记录 loss factor 时必须同时保存束团分布、rms 长度、归一化、积分频带和单位。不同软件可能输出 V/C、V/pC 或能量形式，比较前要换算。

## Formula

对归一化线密度频谱 $\Lambda(\omega)$，一种约定为：

$$
k_{\mathrm{loss}}=\frac{1}{2\pi}\int_{-\infty}^{\infty}
\operatorname{Re}Z_{\parallel}(\omega)|\Lambda(\omega)|^2\,d\omega.
$$

## Application

用于估算真空部件和 RF 结构的单束团寄生能量损失、平均发热功率，并比较几何优化前后的 broadband wake 性能。

## Related Concepts

- [[Longitudinal wake potential]]
- [[Longitudinal impedance]]
- [[Gaussian bunch]]
- [[Bunch spectrum]]

## Sources

- L. Palumbo, V. G. Vaccaro, and M. Zobov, [Wake fields and impedance](https://cds.cern.ch/record/276437), CERN Accelerator School, 1995.
- M. Migliorati, [Introduction to Accelerator Physics exercises](https://cds.cern.ch/record/2928175), CERN Yellow Reports: Monographs, 2024.

## Decision Log

- 2026-08-02 — 将束团长度视为解释 loss factor 的必需上下文；不接受只有单一数值而无分布信息的记录。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
- 2026-08-03 — 将 Hover Summary 调整为中文主语言；稳定 ID、canonical name 和 aliases 不变。
