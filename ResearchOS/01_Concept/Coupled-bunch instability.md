---
id: coupled_bunch_instability
aliases:
  - multi-bunch instability
  - coupled bunch instability
  - 耦合束团不稳定性
category:
  - accelerator physics
  - collective effects
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

# Coupled-bunch instability

## Hover Summary

Coupled-bunch instability 是多个束团通过长程 wake 或窄带阻抗相互耦合后出现的相干振荡增长；RF cavity HOM 常是重要驱动源。

## Definition

当某结构的 wake 持续时间跨越一个或多个 bunch spacing 时，先前束团可影响后续束团。多个束团的相干本征模式若获得正增长率，就形成 longitudinal 或 transverse coupled-bunch instability。

## My Understanding

每个束团不再独立振荡，而是以固定束间相位关系组成 collective mode。窄带 HOM 若落在某条多束团谱线上，能连续向该 mode 输送能量。

## Engineering View

分析需同时保存 fill pattern、revolution frequency、synchrotron/betatron sideband、阻抗频率与 Q。缓解手段包括 HOM damping、频率 detuning、反馈和调整 bunch pattern。

## Formula

对 $M$ 个等间隔束团，coupled-bunch mode $\mu$ 的相邻束团相位差为：

$$
\Delta\phi_\mu=\frac{2\pi\mu}{M},
\qquad \mu=0,1,\ldots,M-1.
$$

对应谱线与机器谐波及 synchrotron 或 betatron sideband 相交。

## Application

用于解释高束流下的谱线增长、确定危险 HOM、设定 longitudinal/transverse feedback 带宽与功率，并评估不同 fill pattern 的稳定性。

## Related Concepts

- [[HOM impedance]]
- [[Bunch spectrum]]
- [[Longitudinal impedance]]
- [[Transverse impedance]]

## Sources

- A. Hofmann, [Impedance Measurements, Computations and their Interpretation](https://cds.cern.ch/record/309240), CERN-SL-96-055, 1996.
- R. Wanzenberg, [Impedances and Instabilities](https://cds.cern.ch/record/2941653), CERN Accelerator School, 2020.

## Decision Log

- 2026-08-02 — 将 coupled-bunch instability 与单束团效应分开记录；任何结论必须包含 fill pattern 和 mode index。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
