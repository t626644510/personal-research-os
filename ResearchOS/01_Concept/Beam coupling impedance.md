---
id: beam_coupling_impedance
aliases:
  - coupling impedance
  - beam impedance
  - 束流耦合阻抗
category:
  - accelerator physics
  - collective effects
level: working
confidence:
  textbook: high
  personal: medium
origin:
  - textbook
  - paper
created: 2026-08-02
updated: 2026-08-02
---

# Beam coupling impedance

## Hover Summary

束流耦合阻抗是加速器环境对束流电流扰动的频域响应，连接结构产生的 wake 与束流能量变化、横向踢力、发热和集体不稳定性。

## Definition

Beam coupling impedance 描述运动电荷激励真空室、RF 结构和材料后，这些电磁场如何反作用于束流。它是 wake function 的频域表示，通常分为 longitudinal 和 transverse 两类。

## My Understanding

它相当于束流“看到”的机器传递函数：束流频谱是输入，阻抗是环境响应，两者在频率上的重叠决定哪些场会真正影响束流。

## Engineering View

机器阻抗模型应注明结构、材料、归一化、参考轨道和频率范围。窄带共振需与离散束流谱线比较，宽带阻抗则常与单束团频谱和束长一起评估。

## Formula

一种纵向约定为：

$$
Z_{\parallel}(\omega)=\frac{1}{c}\int_{-\infty}^{\infty}
W_{\parallel}(s)e^{i\omega s/c}\,ds.
$$

不同资料对指数符号、负号和横向归一化的约定可能不同，合并数据前必须统一定义。

## Application

用于建立整机 impedance budget，预测寄生功率损耗、束团长度变化、相干频移和不稳定性阈值，并确定需要优化或阻尼的部件。

## Related Concepts

- [[Longitudinal impedance]]
- [[Transverse impedance]]
- [[Wakefield]]
- [[Bunch spectrum]]

## Sources

- R. Wanzenberg, [Impedances and Instabilities](https://cds.cern.ch/record/2941653), CERN Accelerator School, 2020.
- L. Palumbo, V. G. Vaccaro, and M. Zobov, [Wake fields and impedance](https://cds.cern.ch/record/276437), CERN Accelerator School, 1995.

## Decision Log

- 2026-08-02 — 将 beam coupling impedance 作为纵向和横向阻抗的上位概念，避免把不同单位与归一化混入一个数值字段。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
