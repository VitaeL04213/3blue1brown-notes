# 3Blue1Brown 中文课程笔记 · LaTeX + Lean 4

[![Notes and Lean](https://github.com/VitaeL04213/3blue1brown-notes/actions/workflows/ci.yml/badge.svg)](https://github.com/VitaeL04213/3blue1brown-notes/actions/workflows/ci.yml)

按 2026-10-24 的[官方目录](https://www.3blue1brown.com/)编写的独立中文伴读笔记：**6 组课程、66 节独立课、72 页 PDF、67 个 Lean 定理**。每节含概念、数学表述、算例、易错点、自测答案与形式化边界。

**[阅读 PDF](dist/3blue1brown-notes-zh.pdf)** · [逐课目录与原课链接](COURSES.md) · [形式化覆盖](FORMALIZATION.md) · [验证记录](VALIDATION.md)

## 覆盖范围

| 官方课程目录 / 系列 | 目录位置 | 正文 |
|---|---:|---|
| Linear Algebra | 16 | [线性代数](notes/chapters/linear-algebra.tex) |
| Calculus | 17 | [微积分及补充课](notes/chapters/calculus.tex) |
| Neural Networks | 11 | [神经网络、Transformer、扩散模型](notes/chapters/neural-networks.tex) |
| Differential Equations | 10 | [微分方程、傅里叶、拉普拉斯](notes/chapters/differential-equations.tex) |
| Lockdown Math | 11 | [基础代数、复数与对数，含公告](notes/chapters/lockdown-math.tex) |
| Compression & Intelligence | 2 | [熵与交叉熵](notes/chapters/compression.tex) |

67 个目录位置中，**交叉熵重复出现一次**，故为 66 节独立课。65 节数学课各有 Lean 对照；公告页不设数学定理。采用官网主题目录中的顺序并保留补充课；不同年份视频的章号与官网正文的章号可能不同。

“所有课程”在此指上述五个课程型目录，以及明确编号的“压缩与智能”系列。其他分类中的独立专题、演讲、外部频道视频、未来新课不在本次范围内。完整英文题名、发布日期、视频与页面链接保存在 [目录快照](sources/catalog.json)。

## 笔记与证明怎样配合

这是围绕课程主题独立组织的中文数学伴读，含原创例子与推导，**不是字幕全文翻译，也未声称逐帧观看全部视频**。官网有文字课的部分参照其概念组织；官网只有视频入口的部分，依据核实的题目、简介及标准数学独立重构。66 个官方页面的获取结果见 [来源记录](sources/retrieval.json)。

LaTeX 正文中的 `Lean 对照` 列出实际命题：有的是完整一般定理，有的是特例或局部恒等式。比如：

- 微积分基本定理保留区间可导性和导函数可积性假设。
- 克拉默法则保留非零行列式条件。
- 幂塔定理证明“**若收敛**，极限为不动点”，没有把收敛当作结论。
- KL 非负性证明针对严格正、归一化的有限分布。
- 傅里叶收敛、一般 PDE 解理论、网络泛化与生成质量等没有被局部代数例子冒充为完整形式化。

67 个定理均由 Lean 检查，不含 `sorry`、`admit`、自设 `axiom` 或 `native_decide`。它们依赖 Lean / mathlib 的常规逻辑基础，不能理解成“无任何基础公理”。详见 [逐课边界](FORMALIZATION.md)。

## 本地复现

### Lean

先按 [Lean 官方安装说明](https://lean-lang.org/install/)配置 Elan。项目固定 **Lean 4.19.0** 与 **mathlib v4.19.0**；锁文件还固定了传递依赖提交。

```sh
git clone https://github.com/VitaeL04213/3blue1brown-notes.git
cd 3blue1brown-notes
lake exe cache get
lake build
python scripts/audit.py
lake env lean scripts/AxiomAudit.lean
```

首次构建需要下载 Lean 与数学库缓存，可能占用数 GB 磁盘。后续构建复用 `.lake/`。`scripts/audit.py` 检查目录覆盖和命题链接，不能替代 `lake build`。

### PDF

使用 [Tectonic](https://tectonic-typesetting.github.io/) 0.17.0，或安装含 `ctex`、Fandol 中文字体、TikZ、AMS 与 hyperref 的 XeLaTeX：

```sh
python scripts/build_pdf.py
```

若 Tectonic 不在 PATH：

```sh
python scripts/build_pdf.py --tectonic /absolute/path/to/tectonic
```

输出为 `dist/3blue1brown-notes-zh.pdf`，构建日志在 `build/latex.log`。源码使用 Fandol 字体，不依赖某台机器的商业中文字体。首次运行 Tectonic 需要网络下载 TeX 包。

## 仓库结构

```text
notes/                    中文 LaTeX 主文件与六章正文
ThreeBlueOneBrown/         六个 Lean 模块
ThreeBlueOneBrown.lean     导入所有证明，lake build 的入口
sources/                  官方目录、获取记录、笔记/定理映射
scripts/                  PDF 构建、目录审计、来源刷新、依赖公理检查
dist/                     可直接阅读的 PDF
.github/workflows/ci.yml   Lean 和 PDF 持续构建
```

修改正文或命题后，运行 `python scripts/audit.py --write-index` 更新目录、覆盖表与公理审计入口。刷新官网清单是显式操作：`python scripts/catalog.py --refresh --snapshot-date YYYY-MM-DD`；网站结构改变时解析器会失败，需人工检查，不能自动把新增课程标成已完成。正文仍须逐节编写与审阅。

## 来源与许可

原课程归 Grant Sanderson / 3Blue1Brown 及署名合作者；扩散模型客座课署名 Stephen Welch / Welch Labs。本项目无官方隶属关系，不附原视频、原图、字幕全文或网页正文。

[MIT 许可](LICENSE)仅适用于本项目独立编写的笔记、证明、脚本和图示，不改变第三方作品或 mathlib 自身的许可。
