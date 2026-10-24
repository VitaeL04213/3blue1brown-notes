# 教学媒体

本项目原创 9 组 Manim 动画与 9 个浏览器参数实验，围绕教材数学例子编写，完整源码随仓库公开。

| 主题 | Manim 场景 | 交互实验 |
|---|---|---|
| 矩阵、基与行列式 | LinearMap | 调整两列、变换进度与面积 |
| 导数 | Derivative | 调整固定点、正负步长，显式处理零步长 |
| 积分 | Integral | 调整矩形个数，对比真实积分 |
| 梯度下降 | GradientDescent | 调整学习率与迭代次数，观察振荡和发散 |
| 注意力 | Attention | 调整分数差与温度，观察权重和输出 |
| 热方程与傅里叶 | FourierHeat | 调整高频、振幅与时间 |
| 复指数 | ComplexRotation | 调整弧度与半径，观察投影及切向方向 |
| 熵与交叉熵 | Entropy | 改变真实与模型概率，比较熵与 KL |
| 泰勒近似 | Taylor | 调整阶数与观察点，显示误差 |

动画输出为 720p、30 fps MP4，并提供 600 像素宽的 GIF。均有中文画面说明、无音频。视频播放器可暂停、拖动和下载；正文提供等价文字解释。Manim 生成预渲染动画，实时参数实验由 Canvas 与独立数学模型实现。

## 重新生成

需要 Python 3.12、Manim Community 0.19.0、FFmpeg 与 FFprobe：

    python -m pip install -r media/requirements.txt
    python scripts/render_media.py

文字使用 Pango，不要求额外安装 LaTeX。Windows 默认使用 Microsoft YaHei；其他平台先安装中文字体，把环境变量 TEXTBOOK_FONT 设为该字体，例如 Noto Sans CJK SC。字体与渲染库差异可能改变像素输出。

输出在 docs/media/，PDF 关键帧在 notes/figures/，临时渲染在忽略的 build/manim/。manifest.json 记录场景、校验值、画幅、帧率、时长和关键帧时刻。

## 原课引用

官方目录提供 61 个条目的独立视频 ID；对应页面按需加载 YouTube 播放器。另外 5 个条目直接链接官方图文页和原图示，不推测视频配对或未核实的时间点。逐课观察提示在 teaching.json。

原视频需要网络访问，由外部播放器提供；不复制到仓库。原创动画、关键帧与代码采用本项目 MIT 许可，第三方课程的权利仍归原作者。

开发参考：[Manim 文档](https://docs.manim.community/en/stable/) · [YouTube 播放器文档](https://developers.google.com/youtube/player_parameters)。
