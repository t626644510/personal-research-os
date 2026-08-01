---
id: hom_impedance
aliases:
  - HOM
  - Higher-order-mode impedance
  - 高次模阻抗
category:
  - accelerator physics
  - RF engineering
level: working
confidence:
  textbook: high
  personal: medium
origin:
  - paper
  - simulation
created: 2026-08-01
updated: 2026-08-01
---

# HOM impedance

## Hover Summary

高次模阻抗描述束流与加速结构中非基模共振的频域耦合强度；峰值频率、分路阻抗和 Q 值共同决定能量损失、发热及束流不稳定风险。

## Definition

HOM（higher-order mode）是加速结构中除目标工作模之外可被束流激励的本征模。HOM impedance 是这些模对束流呈现的纵向或横向耦合阻抗，用频域方式表征束流激励结构、结构再反作用于束流的关系。

## My Understanding

可以把每个明显的 HOM 看成束流能够“敲响”的窄带谐振器。阻抗谱告诉我它在哪个频率最容易被激励，以及激励后对后续粒子施加多强的纵向电压或横向踢力。

## Engineering View

工程判断不能只看最高阻抗峰，还要同时检查束流谱线、模频率、`R/Q`、加载 Q 值、重复频率和制造偏差。HOM coupler 或吸收材料的目标通常是降低危险模的加载 Q 和有效分路阻抗，同时尽量不扰动工作模。

## Formula

单个纵向谐振模常用并联谐振器近似：

$$
Z_{\parallel}(\omega)=\frac{R_s}{1+iQ_L\left(\frac{\omega}{\omega_r}-\frac{\omega_r}{\omega}\right)},
\qquad R_s=\left(\frac{R}{Q}\right)Q_L.
$$

其中 $\omega_r$ 是模的角频率，$Q_L$ 是加载品质因数，$R_s$ 是分路阻抗。傅里叶变换的符号和归一化在不同资料中可能不同，比较结果时必须先确认约定。

## Application

用于从尾场仿真得到的阻抗谱中识别危险 HOM，建立模态表，并为腔体、波导或 HOM coupler 的几何优化设置峰值阻抗和阻尼目标。

## Related Concepts

- [[Wakefield]]
- [[Q factor]]
- [[CST wakefield solver]]

## Sources

- R. Wanzenberg, [Impedances and Instabilities](https://cds.cern.ch/record/2941653), CERN Accelerator School lecture notes, 2020.
- H. Damerau et al., [CERN-ACC-NOTE-2016-0051](https://cds.cern.ch/record/2199926), sections on the SPS higher-order-mode impedance model.

## Decision Log

- 2026-08-01 — 在 v0.1 中把 HOM impedance 作为频域概念节点；具体 CST 后处理设置留在 Tool 或 Experiment 笔记，避免概念定义与软件步骤耦合。

## History

- 2026-08-01 — 按 Concept Schema v0.1 创建验证样例。
