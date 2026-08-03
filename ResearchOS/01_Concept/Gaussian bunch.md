---
id: gaussian_bunch
aliases:
  - Gaussian beam bunch
  - Gaussian longitudinal profile
  - 高斯束团
category:
  - accelerator physics
  - beam modeling
level: familiar
confidence:
  textbook: high
  personal: medium
origin:
  - textbook
  - simulation
created: 2026-08-02
updated: 2026-08-03
---

# Gaussian bunch

## Hover Summary

高斯束团用高斯函数近似纵向电荷分布；其均方根（rms）长度直接控制频谱宽度，因此是尾场仿真及损耗因子、踢因子比较的常用基准输入。

## Definition

归一化 Gaussian longitudinal profile 由均值位置和 rms 长度 $\sigma_z$ 决定。它具有解析 Fourier transform，便于连接时域 wake convolution 与频域 impedance weighting。

## My Understanding

短 Gaussian bunch 在时间上更尖，因此频谱更宽，能探测更高频的结构响应；长束团会自然过滤高频阻抗。

## Engineering View

记录时必须说明 $\sigma_z$ 或 $\sigma_t$ 是 rms 而非 full width，并确认软件输入使用长度还是时间单位。真实束团若非 Gaussian，不应只靠相同 rms 长度替代。

## Formula

归一化纵向线密度为：

$$
\lambda(z)=\frac{1}{\sqrt{2\pi}\sigma_z}
\exp\left(-\frac{z^2}{2\sigma_z^2}\right),
\qquad \sigma_t=\frac{\sigma_z}{c}.
$$

## Application

用于生成 wakefield solver 的 drive bunch，比较结构的 loss factor 与 kick factor，并作为 impedance 去卷积和收敛研究的标准测试分布。

## Related Concepts

- [[Bunch spectrum]]
- [[Loss factor]]
- [[Kick factor]]
- [[CST wakefield solver]]

## Sources

- R. Wanzenberg, [Impedances and Instabilities](https://cds.cern.ch/record/2941653), CERN Accelerator School, 2020.
- M. Migliorati, [Introduction to Accelerator Physics exercises](https://cds.cern.ch/record/2928175), CERN Yellow Reports: Monographs, 2024.

## Decision Log

- 2026-08-02 — 所有 Gaussian bunch 参数默认解释为 rms；任何 FWHM 输入必须在 Experiment 中显式换算。

## History

- 2026-08-02 — 按 Concept Schema v0.1 创建。
- 2026-08-03 — 将 Hover Summary 调整为中文主语言；稳定 ID、canonical name 和 aliases 不变。
