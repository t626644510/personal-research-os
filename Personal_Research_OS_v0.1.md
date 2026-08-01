# Personal Research OS v0.1

## 基于 Obsidian + Codex 的个人科研知识数据库系统

Version: v0.1\
Date: 2026-08-01

------------------------------------------------------------------------

# 1. 项目目标

建立一个个人科研知识操作系统，将：

-   论文
-   HTML资料
-   实验记录
-   仿真记录
-   学习笔记
-   项目经验

转化为结构化知识数据库。

核心目标：

实现类似 Civilization / Victoria 风格的知识百科体验：

-   阅读过程中识别已有概念
-   鼠标悬浮快速显示概念摘要
-   随知识库增长自动扩展

------------------------------------------------------------------------

# 2. 核心设计理念

## AI不是实时查询引擎

禁止：

    Hover关键词
        ↓
    调用AI
        ↓
    生成解释

原因：

-   延迟高
-   成本高
-   输出不稳定

正确架构：

    资料输入

    ↓

    Knowledge Agent (Codex)

    ↓

    Concept Database

    ↓

    Obsidian Hover Preview

AI负责：

-   创建知识
-   更新知识
-   建立关系

数据库负责：

-   快速查询
-   稳定展示

------------------------------------------------------------------------

# 3. 总体架构

    External Source

    Paper
    HTML
    Experiment
    Simulation

            ↓

    Inbox Layer

            ↓

    Knowledge Processing Agent
    (Codex)

            ↓

    Concept Database
    Project Database
    Research Log

            ↓

    Obsidian

            ↓

    Hover Encyclopedia UI

------------------------------------------------------------------------

# 4. Vault目录结构

    ResearchOS/

    ├── 00_Inbox
    │   ├── papers
    │   ├── html
    │   └── notes
    │
    ├── 01_Concept
    │
    ├── 02_Project
    │
    ├── 03_Paper
    │
    ├── 04_Experiment
    │
    ├── 05_Tool
    │
    └── 99_Meta

------------------------------------------------------------------------

# 5. Concept设计

Concept是知识数据库核心节点。

示例：

`Concept/HOM impedance.md`

## YAML Metadata

``` yaml
type: concept

id:
hom_impedance

aliases:
  - HOM
  - Higher order mode impedance

category:
  - accelerator
  - RF

level:
  - familiar

confidence:
  textbook: high
  personal: medium

origin:
  - paper
  - simulation

created:
2026-08-01

updated:
2026-08-01
```

------------------------------------------------------------------------

# 6. Concept正文结构

``` markdown
# Concept Name

## Hover Summary

用于悬浮百科显示的简短介绍。


## Definition

教材或文献中的正式定义。


## My Understanding

个人理解。


## Engineering View

工程应用。


## Formula

关键公式。


## Application

当前项目中的应用。


## Related Concepts

相关知识。


## Sources

来源。


## Decision Log

重要科研判断记录。


## History

修改历史。
```

------------------------------------------------------------------------

# 7. Hover Encyclopedia设计

Hover只读取：

-   Hover Summary
-   Metadata
-   Related Concepts

不读取全文。

目标：

-   显示速度 \<100 ms
-   类似游戏百科tooltip体验

示例：

    HOM impedance

    高次模阻抗。

    描述RF腔中高次模
    与束流相互作用的频域特性。

    Category:
    Accelerator RF

    Related:
    Wakefield
    Q factor

    Updated:
    2026-08-01

------------------------------------------------------------------------

# 8. Knowledge Agent职责

## Concept生成

输入：

-   PDF
-   HTML
-   Markdown

输出：

-   Concept draft

## Concept更新

根据新资料：

-   更新已有概念
-   提出修改建议
-   建立关系

## 关系维护

自动发现：

Concept A

↓

Related

↓

Concept B

------------------------------------------------------------------------

# 9. 工作流

    User

    ↓

    Inbox

    ↓

    Manual trigger

    ↓

    Codex Knowledge Agent

    ↓

    Generate proposal

    ↓

    Human review

    ↓

    Git commit

    ↓

    Obsidian refresh

------------------------------------------------------------------------

# 10. 触发机制

第一阶段：

采用：

## 手动触发

例如：

    process paper xxx.pdf

第二阶段：

加入：

## Git Commit Hook

    git commit

    ↓

    knowledge check

    ↓

    update index

不采用：

## 定时扫描

原因：

科研资料需要人工判断价值。

------------------------------------------------------------------------

# 11. 后续扩展

## Phase 2

Arxiv Daily Agent

流程：

    arxiv API

    ↓

    paper metadata

    ↓

    summary

    ↓

    Inbox

------------------------------------------------------------------------

## Phase 3

HTML Collector

    saved html

    ↓

    classification

    ↓

    Concept update

------------------------------------------------------------------------

## Phase 4

Obsidian Plugin

功能：

-   Hover Encyclopedia
-   Concept lookup
-   AI assisted update

------------------------------------------------------------------------

# 12. 设计原则总结

1.  Concept Database 是唯一知识源。
2.  Hover 是离线快速读取，不调用AI。
3.  AI负责知识生产与维护。
4.  人负责最终确认。
5.  Git负责版本管理。
6.  保留Decision Log，记录科研判断过程。
