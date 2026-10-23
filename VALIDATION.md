# 验证记录

验证日期：2026-10-24（Asia/Shanghai）。以下为本次交付的本地检查；后续提交的云端状态以 [GitHub Actions](https://github.com/VitaeL04213/3blue1brown-notes/actions) 为准。

| 检查 | 结果 |
|---|---|
| 官方课目录 | 6 组，67 个位置，66 节独立课 |
| 官方页面读取 | 66 / 66 成功；记录不等同于观看视频 |
| LaTeX 正文章节 | 66 / 66 有概念、公式、例题、易错点、自测答案与 Lean 边界 |
| 数学课程对应 | 65 / 65 有形式命题，另 1 页公告明确豁免 |
| Lean 构建 | `lake build` 成功，67 个命名定理；最终构建无警告 |
| 未完成证明构造 | `sorry` / `admit` / 自设 `axiom` / `native_decide` 均未使用 |
| 依赖公理审计 | 67 个定理已检查，仅出现 `propext`、`Classical.choice`、`Quot.sound` |
| PDF | Tectonic 0.17.0 编译成功，72 页 A4 |
| PDF 文本检查 | 无空白页，无替代字符，无 `??` 引用，146 个链接注释 |
| PDF 视觉检查 | 已浏览 72 页缩略图，并放大检查公式密集页与最终修改页；未发现溢出、重叠或缺字 |

固定依赖：

- Lean：`leanprover/lean4:v4.19.0`
- mathlib：`v4.19.0`，提交 `c44e0c8ee63ca166450922a373c7409c5d26b00b`
- 传递依赖：[lake-manifest.json](lake-manifest.json)

可核查证据：

- [最终 Lean 构建输出](validation/lean-build.txt)
- [逐定理公理依赖](validation/axioms.txt)
- [逐课来源读取记录](sources/retrieval.json)
- [逐课笔记与形式命题映射](sources/coverage.json)

PDF SHA-256：

```text
79fd5747bf86b942b1dc6122c4d73ca6ab655be6009520feac6d3d7ca0d888d0
```

这些检查验证交付物的构建、覆盖一致性和列明的形式命题；并未将整套课程的全部叙述、经验事实与未形式化定理称为机器证明。未形式化部分的边界逐课列在 [FORMALIZATION.md](FORMALIZATION.md)。
