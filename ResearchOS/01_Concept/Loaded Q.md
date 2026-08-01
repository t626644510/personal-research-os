---
id: loaded_q
aliases:
  - loaded quality factor
  - QL
  - 加载Q值
category:
  - RF engineering
  - resonator physics
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

# Loaded Q

## Hover Summary

Loaded Q 是谐振器同时计入内部损耗和所有外部耦合通道后的有效品质因数，决定实际共振带宽、场衰减时间和阻抗峰宽。

## Definition

$Q_L$ 用总储能除以所有损耗与外泄功率之和进行归一化。它包含导体、介质等内部损耗，也包含 power coupler、HOM coupler 和端口带走的功率。

## My Understanding

Unloaded Q 描述 cavity 自己能保存能量多久；接上外部端口后能量多了泄漏路径，实际看到的 loaded Q 因而更低。

## Engineering View

从 S parameter 带宽拟合得到的通常是 $Q_L$。把它与本征模求得的 $Q_0$ 比较前，应确认端口数量、耦合状态和所用 3 dB 或复数拟合方法。

## Formula

只有一个等效外部通道时：

$$
\frac{1}{Q_L}=\frac{1}{Q_0}+\frac{1}{Q_{\mathrm{ext}}}.
$$

多个独立外部通道时，各 $1/Q_{\mathrm{ext},k}$ 相加。

## Application

用于设定 cavity 带宽、填充时间、HOM 衰减和 resonator impedance 峰宽，并连接仿真本征值、端口耦合与网络分析测量。

## Related Concepts

- [[Q factor]]
- [[External Q]]
- [[Shunt impedance]]
- [[HOM coupler]]

## Sources

- E. Jensen, [Cavity basics](https://cds.cern.ch/record/1416619), CERN Accelerator School, 2011.
- NIST, [Materials loss measurements using superconducting microwave resonators](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=930293), 2020.

## Decision Log

- 2026-08-02 — 所有后续 Q 数据必须用下标或文字标明 $Q_0$、$Q_L$ 或 $Q_{\mathrm{ext}}$，不接受裸写 Q 的实验结果。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
