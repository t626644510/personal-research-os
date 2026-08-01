---
id: longitudinal_impedance
aliases:
  - Z parallel
  - Z longitudinal
  - 纵向阻抗
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
updated: 2026-08-02
---

# Longitudinal impedance

## Hover Summary

纵向阻抗描述束流电流如何激励沿运动方向的电压响应；其实部与能量损失相关，频率结构决定束内能散和纵向集体效应。

## Definition

Longitudinal impedance $Z_{\parallel}(\omega)$ 是纵向 wake function 的傅里叶表示，把某一频率的束流电流分量映射为束流所见的纵向感应电压。

## My Understanding

纵向 wake 告诉我后续粒子在距离坐标上获得或损失多少能量；纵向阻抗则把同一问题拆成频率分量，便于直接与束团频谱相乘。

## Engineering View

结果通常以欧姆表示。比较不同仿真或测量时要核对傅里叶约定、正负号、端口参考面、束流方向以及输出是点电荷阻抗还是有限束长去卷积后的阻抗。

## Formula

若频域感应电压采用

$$
V_{\mathrm{ind}}(\omega)=-Z_{\parallel}(\omega)I_b(\omega),
$$

则正的 $\operatorname{Re}Z_{\parallel}$ 对应束流向环境传递平均功率。符号取决于电流和傅里叶定义。

## Application

用于计算 loss factor、寄生加热、微波不稳定性、纵向 coupled-bunch instability，以及从 wakefield 仿真曲线恢复阻抗谱。

## Related Concepts

- [[Beam coupling impedance]]
- [[Longitudinal wake potential]]
- [[Loss factor]]
- [[Bunch spectrum]]

## Sources

- R. Wanzenberg, [Impedances and Instabilities](https://cds.cern.ch/record/2941653), CERN Accelerator School, 2020.
- L. Palumbo, V. G. Vaccaro, and M. Zobov, [Wake fields and impedance](https://cds.cern.ch/record/276437), CERN Accelerator School, 1995.

## Decision Log

- 2026-08-02 — v0.1 只保存定义与约定；具体结构的复阻抗数组保存在 Experiment，而不嵌入 Concept。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
