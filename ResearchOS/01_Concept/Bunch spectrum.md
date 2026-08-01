---
id: bunch_spectrum
aliases:
  - beam current spectrum
  - bunch frequency spectrum
  - 束团频谱
category:
  - accelerator physics
  - signal analysis
level: working
confidence:
  textbook: high
  personal: medium
origin:
  - textbook
  - measurement
created: 2026-08-02
updated: 2026-08-02
---

# Bunch spectrum

## Hover Summary

Bunch spectrum 是束流纵向电荷或电流分布的频域表示；单束团 envelope 与重复束团形成的离散谱线共同决定哪些结构阻抗会被有效激励。

## Definition

对归一化纵向线密度 $\lambda(t)$，其 Fourier transform $\Lambda(\omega)$ 给出单束团 spectral envelope。周期性 bunch train 进一步在 revolution 或 RF harmonics 上形成离散梳状谱线。

## My Understanding

阻抗峰存在不等于它一定危险；只有束流在相同频率上有足够谱功率时才会强烈激励。束长越短，单束团频谱通常越宽。

## Engineering View

频谱必须与真实 fill pattern、bunch spacing、charge variation 和 measurement window 一起计算。只用连续 envelope 会遗漏窄带 HOM 与离散谱线的共振风险。

## Formula

归一化 Gaussian bunch 的频谱幅度为：

$$
\Lambda(\omega)=\exp\left[-\frac{1}{2}(\omega\sigma_t)^2\right],
$$

其功率权重为 $|\Lambda(\omega)|^2$。

## Application

用于计算 loss factor、beam-induced heating 和 coupled-bunch drive，选择 wakefield 仿真的 bunch length，并解释频谱分析仪上的 beam lines。

## Related Concepts

- [[Gaussian bunch]]
- [[Loss factor]]
- [[Beam coupling impedance]]
- [[Coupled-bunch instability]]

## Sources

- R. Wanzenberg, [Impedances and Instabilities](https://cds.cern.ch/record/2941653), CERN Accelerator School, 2020.
- L. Palumbo, [Diffraction by an Iris and its Effect on the Longitudinal Bunch Distribution](https://cds.cern.ch/record/1108078), Particle Accelerators 25, 1990.

## Decision Log

- 2026-08-02 — P01 将 bunch spectrum 保持为确定性解析概念；真实 fill pattern 的谱线计算以后放入 Experiment 工具。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
