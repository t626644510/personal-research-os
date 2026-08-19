---
id: tuner
aliases:
  - 调谐器
  - Frequency tuner
  - 频率调谐器
category:
  - RF engineering
level: working
confidence:
  textbook: medium
  personal: low
origin:
  - paper
  - manual
created: 2026-08-18
updated: 2026-08-18
---
# Tuner

## Hover Summary

调谐器是用于调整加速器 RF 腔体谐振频率的装置或机构；耦合因子调节属于 Coupling tuner，不在本 Concept 范围内。

## Definition

Tuner 是加速器 RF 腔体中用于调整谐振频率的装置或机构。它可以改变腔体的有效电磁边界或等效几何，但具体机制、方向和灵敏度依赖 cavity geometry。这里的 Tuner 不包含通过改变 coupling factor $\beta$ 进行耦合调节的 Coupling tuner。

## My Understanding

我把 tuner 理解为围绕 resonance frequency 的可控机械或电磁调节接口；Frequency tuner 是来源兼容 alias，Tuner / 调谐器是采用的通用名称。调谐范围、正负方向和灵敏度都必须绑定具体腔体与位置，不能从一个论文实例无条件泛化。

## Engineering View

论文实例包括两根直径各 95 mm 的铜杆，各移动 ±50 mm，约对应 ±0.5 MHz；还包括两个直径各 30 mm 的 plungers，各移动 ±25 mm，约对应 ±0.5 MHz。这些 geometry、travel、sign、sensitivity 和 range 都是论文特定设计值。Coupling factor $\beta$ 的调节属于 Coupling tuner，不能吸收到本 Concept。当前项目的 tuner 位置、范围、机械包络和交叉耦合仍未决定。

## Formula

对某一具体 geometry 的小位移，可用局部调谐灵敏度表示：

$$
\Delta f \approx \frac{df}{dx}\Delta x,
$$

其中 $x$ 是指定 tuner 的位移，$df/dx$ 是依赖腔体 geometry、位置和边界的局部灵敏度；其符号表示该位移使频率升高或降低。该近似不由选定论文给出通用数值，非线性范围必须由具体电磁扫描或测量确定。

该广义 tuner 定义和局部灵敏度关系，是基于选定论文案例和人类批准的 KA-02 范围决定的有界综合；它不是论文原句，论文也没有给出通用 tuning law。

## Application

选定论文用两类结构分别调节主腔和谐波腔的 resonance frequency；本候选只抽象频率调节功能，不把论文结构当作当前项目的固定机械方案。P04 `Coupling tuner` 仍是独立且 deferred 的 proposal。

## Related Concepts

- [[Cavity mode]]

This link resolves to an existing stable Concept; this promotion does not alter
that Concept.

## Sources

- Origin handling: `paper` covers source-specific facts; `manual` covers the
  bounded synthesis accepted by human reviewer `owner-01` in KA-03 Stage 2.

- Selected source: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`; locator `3.4 Frequency tuners and couplers are different functions`.

## Decision Log

2026-08-18：依据 KA-02 `revise_identity_and_aliases` 方向，owner-01 接受将候选 identity 改为 `Tuner` / `调谐器`，保留 `Frequency tuner` 和 `频率调谐器` 作为来源与检索兼容 aliases；不吸收 Coupling tuner 的耦合因子调节功能。

## History

- 2026-08-18 - Created as a proposed candidate by KA-01; pending human review.
- 2026-08-18 - Revised under the human-approved KA-02 direction; state remained proposed and human approval is pending.
- 2026-08-18 - owner-01 accepted the complete revised candidate and authorized manual promotion in KA-03 Stage 2; geometry-specific limitations remain open.
