---
id: wakefield
aliases:
  - wake field
  - 尾场
  - 尾流场
category:
  - accelerator physics
  - electromagnetics
level: working
confidence:
  textbook: high
  personal: medium
origin:
  - textbook
  - simulation
created: 2026-08-01
updated: 2026-08-01
---

# Wakefield

## Hover Summary

尾场是带电粒子束经过结构后留下的电磁响应；它对后续粒子产生纵向能量变化或横向偏转，是阻抗、束流损失和集体不稳定分析的时域基础。

## Definition

当源电荷穿过真空结构时，其场与几何或材料不连续性相互作用并在源电荷之后留下电磁场。以单位源电荷和单位测试电荷归一化后，测试粒子所受的纵向电压或横向冲量随两粒子间距的函数称为 wake function。

## My Understanding

前面的粒子不仅“看到”结构，也会改变结构中的场；后面的粒子随后穿过这段场并受到影响。Wakefield 是这段因果记忆在纵向距离上的表示，而 impedance 是同一响应的频域表示。

## Engineering View

数值结果对束团长度、wake length、网格、边界条件、端口和材料模型敏感。必须区分纵向与横向 wake，保存归一化和符号约定，并通过网格或计算域收敛检查确认窄带尾振荡没有被过早截断。

## Formula

一种常见约定把纵向阻抗写成纵向 wake function 的傅里叶变换：

$$
Z_{\parallel}(\omega)=\frac{1}{c}\int_{-\infty}^{\infty}
W_{\parallel}(s)e^{i\omega s/c}\,ds.
$$

其中 $s$ 是测试粒子相对源粒子的纵向间距，$c$ 是光速。积分范围、指数符号和负号会随领域约定变化，使用数据前必须记录具体定义。

## Application

用于评估加速腔、准直器、波纹管和束流位置监测器等结构的 loss factor、kick factor、阻抗谱以及单束团或多束团效应。

## Related Concepts

- [[HOM impedance]]
- [[Q factor]]
- [[CST wakefield solver]]

## Sources

- R. Wanzenberg, [Impedances and Instabilities](https://cds.cern.ch/record/2941653), CERN Accelerator School lecture notes, 2020.
- E. Métral, [Wake field, impedance and collective instability](https://arxiv.org/abs/2108.11655), 2021.

## Decision Log

- 2026-08-01 — v0.1 只记录概念、约定和来源；具体仿真曲线与参数分别进入 Experiment 笔记，避免 Concept 文件演化成运行日志。

## History

- 2026-08-01 — 按 Concept Schema v0.1 创建验证样例。
