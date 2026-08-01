---
id: q_factor
aliases:
  - quality factor
  - Q值
  - 品质因数
category:
  - resonator physics
  - RF engineering
level: working
confidence:
  textbook: high
  personal: high
origin:
  - textbook
  - measurement
created: 2026-08-01
updated: 2026-08-01
---

# Q factor

## Hover Summary

Q factor 是谐振器储能相对损耗的无量纲指标；Q 越高，衰减越慢、共振越窄。工程上必须明确讨论的是 unloaded、external 还是 loaded Q。

## Definition

品质因数衡量谐振系统在每个周期中保存能量相对于耗散能量的能力。对孤立且近似洛伦兹线型的共振，也可用共振频率与半功率带宽之比表示。

## My Understanding

Q 把“存得住多少能量”和“每秒漏掉多少能量”压缩成一个尺度。高 Q 模会振铃更久，因此即使频带很窄，只要与束流谱线重合也可能积累出显著响应。

## Engineering View

本征模求解常给出由壁损耗等决定的 unloaded Q；端口或 HOM coupler 引入 external Q；实际系统响应由 loaded Q 决定。比较仿真与测量时，若 Q 的类型、带宽定义或耦合状态不同，数值不能直接对照。

## Formula

在角频率 $\omega_0$ 处：

$$
Q=\frac{\omega_0 U}{P_{\mathrm{loss}}}
=2\pi\frac{\text{stored energy}}{\text{energy lost per cycle}},
\qquad Q\approx\frac{f_0}{\Delta f_{3\,\mathrm{dB}}}.
$$

内部与外部损耗独立时：

$$
\frac{1}{Q_L}=\frac{1}{Q_0}+\frac{1}{Q_{\mathrm{ext}}}.
$$

## Application

用于评估加速腔工作模效率、HOM 阻尼效果、阻抗峰宽度和尾场衰减时间，并连接本征模分析、S 参数测量与束流耦合模型。

## Related Concepts

- [[HOM impedance]]
- [[S parameter]]
- [[Wakefield]]

## Sources

- NIST, [Time and Frequency from A to Z: Quality Factor](https://www.nist.gov/pml/time-and-frequency-division/popular-links/time-frequency-z/time-and-frequency-z-q-ra).
- Z. Chen et al., [Materials loss measurements using superconducting microwave resonators](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=930293), NIST, 2020.

## Decision Log

- 2026-08-01 — Schema 示例明确区分 $Q_0$、$Q_{\mathrm{ext}}$ 和 $Q_L$；后续任何实验记录必须在字段或正文中标注 Q 的类型。

## History

- 2026-08-01 — 按 Concept Schema v0.1 创建验证样例。
