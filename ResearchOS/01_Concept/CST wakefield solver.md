---
id: cst_wakefield_solver
aliases:
  - CST Wakefield Solver
  - CST尾场求解器
  - CST wakefield analysis
category:
  - simulation tool
  - accelerator physics
level: familiar
confidence:
  textbook: high
  personal: medium
origin:
  - software documentation
  - simulation
created: 2026-08-01
updated: 2026-08-03
---

# CST wakefield solver

## Hover Summary

CST 尾场求解器用线电流表示粒子束，计算束流经过结构不连续处产生的尾场；结果可用于分析纵向或横向尾场、损耗因子及阻抗谱。

## Definition

CST Studio Suite 中面向加速器部件的专用电磁求解器。根据 Dassault Systèmes 的产品说明，它计算以线电流表示的粒子束周围电磁场，以及粒子束与周围结构不连续性相互作用所产生的 wakefield。

## My Understanding

它是把三维结构转换为“束团经过后留下什么场”的数值工具。软件给出的曲线不是独立事实；其可信度取决于几何、材料、边界、束团模型、网格和计算尾长是否与研究问题匹配。

## Engineering View

运行前应固定单位、束流方向、束团长度、横向偏置、边界与对称性；运行后应记录 CST 版本、网格统计、wake length、求解器警告和归一化。至少做一次网格或关键参数收敛比较，并避免把离散噪声或截断振铃误判为物理 HOM。

## Formula

求解器先得到时域 wake function，阻抗通常由其傅里叶变换得到：

$$
Z_{\parallel}(\omega)=\mathcal{F}\{W_{\parallel}(s)\}.
$$

实际比例因子、指数符号、纵向或横向归一化以当前 CST 版本的结果定义和项目设置为准，导出数据时必须一并保存这些约定。

## Application

用于加速腔、准直器和 beam position monitor 等结构的尾场分析；在本 Research OS 中，求解器概念只保存稳定知识，单次模型设置与结果进入 Experiment 笔记。

## Related Concepts

- [[Wakefield]]
- [[HOM impedance]]
- [[Q factor]]

## Sources

- Dassault Systèmes, [CST Studio Electromagnetic Solvers](https://www.3ds.com/products/simulia/cst-studio-suite/electromagnetic-simulation-solvers), section “Wakefield Solver”.
- R. Wanzenberg, [Impedances and Instabilities](https://cds.cern.ch/record/2941653), for the physical relation between wake fields and impedance.

## Decision Log

- 2026-08-01 — 将 CST Wakefield Solver 建模为 Tool 类 Concept，但保持统一 Concept Schema；版本相关操作步骤以后放入 `05_Tool`，仿真输入输出放入 `04_Experiment`。

## History

- 2026-08-01 — 按 Concept Schema v0.1 创建验证样例。
- 2026-08-03 — 将 Hover Summary 调整为中文主语言；稳定 ID、canonical name 和 aliases 不变。
