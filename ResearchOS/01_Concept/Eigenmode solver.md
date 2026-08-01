---
id: eigenmode_solver
aliases:
  - eigenmode analysis
  - cavity eigenmode solver
  - 本征模求解器
category:
  - simulation tool
  - electromagnetics
level: familiar
confidence:
  textbook: high
  personal: medium
origin:
  - software documentation
  - simulation
created: 2026-08-02
updated: 2026-08-02
---

# Eigenmode solver

## Hover Summary

Eigenmode solver 在无外部驱动下求解结构允许的离散电磁本征频率与场分布，并可派生 Q、R/Q、储能和 mode classification。

## Definition

本征模求解器离散 Maxwell eigenvalue problem，在指定材料、对称性和边界条件下求得一组 eigenpairs $(\omega_n,\mathbf E_n,\mathbf H_n)$。

## My Understanding

它回答“这个 cavity 自己能以哪些方式振荡”，而 wakefield solver 回答“一个有限束团经过后实际激励出什么响应”。两者提供互补证据。

## Engineering View

应做网格和 mode 数量收敛，检查边界、对称面、频率搜索范围和简并模。跨几何参数跟踪 mode 时应比较场重叠，而不能只按频率排序。

## Formula

典型广义本征问题写为：

$$
\mathbf K\mathbf e_n=\omega_n^2\mathbf M\mathbf e_n,
$$

其中 $\mathbf K$ 与 $\mathbf M$ 来自 Maxwell 方程的空间离散。

## Application

用于寻找 accelerating mode 与 HOM、计算频率和 $R/Q$、生成 field monitor，并为 wakefield 谱峰匹配候选 mode。

## Related Concepts

- [[Cavity mode]]
- [[Higher-order mode]]
- [[R over Q]]
- [[CST wakefield solver]]

## Sources

- Dassault Systèmes, [CST Studio Electromagnetic Solvers](https://www.3ds.com/products/simulia/cst-studio-suite/electromagnetic-simulation-solvers), section “Eigenmode Solver”.
- E. Jensen, [Cavity basics](https://cds.cern.ch/record/1416619), CERN Accelerator School, 2011.

## Decision Log

- 2026-08-02 — mode tracking 的稳定身份以后应基于 field overlap；P01 不实现自动 mode tracking。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
