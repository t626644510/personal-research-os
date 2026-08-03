---
id: s_parameter
aliases:
  - S-parameter
  - scattering parameter
  - 散射参数
category:
  - microwave engineering
  - network analysis
level: working
confidence:
  textbook: high
  personal: high
origin:
  - textbook
  - measurement
created: 2026-08-01
updated: 2026-08-03
---

# S parameter

## Hover Summary

散射参数（S 参数）用复数矩阵描述多端口网络中入射波到出射波的线性映射；它同时包含幅度与相位，并依赖端口参考阻抗和参考面。

## Definition

对线性 $N$ 端口网络，散射矩阵把各端口的归一化入射波幅 $a_j$ 映射为出射波幅 $b_i$。测量单个 $S_{ij}$ 时，其余端口按定义接匹配负载。

## My Understanding

S 参数是高频系统的“黑箱接口”：不必在端口建立难以实现的开路或短路，就能用反射与传输波说明器件如何分配输入能量。

## Engineering View

任何 S 参数结果都应连同频率范围、参考阻抗、参考面、端口模态、校准或去嵌方式保存。常见两端口量包括输入反射 $S_{11}$、正向传输 $S_{21}$、反向传输 $S_{12}$ 和输出反射 $S_{22}$。

## Formula

$$
\mathbf{b}=\mathbf{S}\mathbf{a},
\qquad
S_{ij}=\left.\frac{b_i}{a_j}\right|_{a_k=0,\,k\ne j}.
$$

以功率波归一化且参考阻抗为实数时，$|S_{ij}|^2$ 可对应从端口 $j$ 到端口 $i$ 的功率比例；其他归一化或复参考阻抗下需要重新检查解释。

## Application

用于验证 RF 腔、耦合器、滤波器、波导和馈电网络的匹配与传输，并可从共振附近的复数响应拟合频率、耦合和 Q factor。

## Related Concepts

- [[Q factor]]
- [[HOM impedance]]

## Sources

- D. F. Williams, [NIST Technical Note 2076](https://doi.org/10.6028/NIST.TN.2076), chapter 3 on VNA scattering-parameter definitions.
- NIST, [Microwave S-Parameter Measurement Service](https://shop.nist.gov/ccrz__ProductDetails?cclcl=en_US&sku=61290S).

## Decision Log

- 2026-08-01 — v0.1 将参考阻抗与参考面视为解释 S 参数的必要上下文；具体 Touchstone 数据保存在 Experiment 或 Project，而不嵌入 Concept。

## History

- 2026-08-01 — 按 Concept Schema v0.1 创建验证样例。
- 2026-08-03 — 将 Hover Summary 调整为中文主语言；稳定 ID、canonical name 和 aliases 不变。
