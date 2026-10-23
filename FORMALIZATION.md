# 形式化覆盖

所有名称均在 `ThreeBlueOneBrown` 命名空间内。这里列出实际被 Lean 检查的命题边界；一般定理、特例和局部恒等式不能互相替代。

通过 `lake build` 才算证明编译通过；本表由源码生成，单凭此表不是通过凭证。

| 课 | 定理 / 代码 | 校验边界 |
|---|---|---|
| 向量究竟是什么 | [`LinearAlgebra.vectors_distribute`](ThreeBlueOneBrown/LinearAlgebra.lean#L7) | 在实数对上完整验证数乘分配律；没有把几何直觉替代成浮点数计算。 |
| 线性组合、张成与基 | [`LinearAlgebra.coordinates_span`](ThreeBlueOneBrown/LinearAlgebra.lean#L10) | 验证标准基的张成等式。一般基的线性无关性与坐标唯一性在本节纸笔解释中给出，未在此命题中形式化。 |
| 线性变换与矩阵 | [`LinearAlgebra.linear_combination`](ThreeBlueOneBrown/LinearAlgebra.lean#L14) | 对任意实向量空间间的线性映射验证线性组合保持律，形式化范围比二维例子更广。 |
| 矩阵乘法就是复合 | [`LinearAlgebra.matrix_composition`](ThreeBlueOneBrown/LinearAlgebra.lean#L18) | 复用 mathlib 的矩阵作用复合定理，在任意实 $2\times2$ 矩阵和向量上验证等式。 |
| 三维线性变换 | [`LinearAlgebra.rotation_preserves_square_norm`](ThreeBlueOneBrown/LinearAlgebra.lean#L22) | 验证该 $90^\circ$ 旋转保持平方长度。未宣称已经证明一般三维旋转的分类。 |
| 行列式：有向体积倍率 | [`LinearAlgebra.determinant_product`](ThreeBlueOneBrown/LinearAlgebra.lean#L25) | 通过坐标展开严格证明两个一般实 $2\times2$ 矩阵的行列式乘法公式。 |
| 逆矩阵、列空间与零空间 | [`LinearAlgebra.kernel_translation`](ThreeBlueOneBrown/LinearAlgebra.lean#L29) | 证明给任意输入加上核中的向量不会改变输出；形式化的是解集结构的核心方向。 |
| 非方阵与维度变化 | [`LinearAlgebra.projection_surjective`](ThreeBlueOneBrown/LinearAlgebra.lean#L32) | 完整证明这一坐标投影满射，构造每个输出 $(x,y)$ 的原像 $(x,y,0)$。 |
| 点积与对偶 | [`LinearAlgebra.dot_linear`](ThreeBlueOneBrown/LinearAlgebra.lean#L37) | 验证二维点积对第二个输入可加，即固定向量所定义测量的线性结构之一。 |
| 叉积与有向面积 | [`LinearAlgebra.cross_orthogonal`](ThreeBlueOneBrown/LinearAlgebra.lean#L40) | 完整验证一般三维实坐标下，叉积与第一个输入正交。 |
| 从线性测量重新认识叉积 | [`LinearAlgebra.scalar_triple_product`](ThreeBlueOneBrown/LinearAlgebra.lean#L43) | 展开并验证一般实坐标下的标量三重积等式；唯一表示的抽象论证未包含在该命题中。 |
| 克拉默法则 | [`LinearAlgebra.cramers_rule`](ThreeBlueOneBrown/LinearAlgebra.lean#L47) | 给定两条线性方程和非零行列式，完整推导这两个商公式。 |
| 换基：改变坐标语言 | [`LinearAlgebra.change_of_basis`](ThreeBlueOneBrown/LinearAlgebra.lean#L58) | 用可逆线性等价验证“换回旧坐标后得到原动作”的恒等式，明确要求坐标变换可逆。 |
| 特征向量与特征值 | [`LinearAlgebra.eigenvector_scaling`](ThreeBlueOneBrown/LinearAlgebra.lean#L62) | 证明特征方程在向量缩放后仍成立。若要称缩放结果为特征向量，还须另加原向量及缩放系数非零的条件。 |
| 快速求二维特征值 | [`LinearAlgebra.characteristic_centering`](ThreeBlueOneBrown/LinearAlgebra.lean#L67) | 验证配方后的特征多项式恒等式。平方根的取值与实根存在性在正文中单独讨论。 |
| 抽象向量空间 | [`LinearAlgebra.function_space_distribute`](ThreeBlueOneBrown/LinearAlgebra.lean#L70) | 验证整个实函数空间的数乘分配律。这里只形式化向量空间操作，未把任意函数都错误地视为可微。 |
| 从面积发现微积分 | [`Calculus.area_derivative`](ThreeBlueOneBrown/Calculus.lean#L7) | 完整验证简化面积函数 $x^2/2$ 的导数为 $x$；圆环几何分割未形式化。 |
| 导数的“零除以零”悖论 | [`Calculus.square_secant`](ThreeBlueOneBrown/Calculus.lean#L12) | 验证非零步长下的差商恒等式，分母条件显式写为 $h\ne0$。导数极限由下一节的形式化幂法则保证。 |
| 幂法则的几何来源 | [`Calculus.power_rule`](ThreeBlueOneBrown/Calculus.lean#L15) | 完整调用并验证自然数幂的一般导数定理；Lean 中自然数的 $n-1$ 是截断减法，$n=0$ 由前面的零系数正确处理。 |
| 三角函数的导数 | [`Calculus.sine_derivative`](ThreeBlueOneBrown/Calculus.lean#L18) | 完整验证实正弦在任意实点的导数；采用 mathlib 的弧度三角函数。 |
| 乘积法则与链式法则 | [`Calculus.chain_rule`](ThreeBlueOneBrown/Calculus.lean#L25) | `chain_rule` 与同文件的 `product_rule` 完整保留两函数在相应点可导的假设。 |
| 为什么自然常数 e 特别 | [`Calculus.exponential_derivative`](ThreeBlueOneBrown/Calculus.lean#L29) | 完整验证实指数在每个实点的导数；增长模型只作为数学例子。 |
| 隐函数求导 | [`Calculus.circle_tangent`](ThreeBlueOneBrown/Calculus.lean#L32) | 从微分约束 $2x\,dx+2y\,dy=0$ 和 $y\ne0$ 推导 $dy=-x\,dx/y$；隐函数存在性定理未形式化。 |
| 极限与导数的定义 | [`Calculus.square_limit`](ThreeBlueOneBrown/Calculus.lean#L37) | 完整验证平方函数的双侧极限；使用邻域过滤器表达“趋近”。 |
| 把任意精度写清楚 | [`Calculus.epsilon_delta_linear`](ThreeBlueOneBrown/Calculus.lean#L41) | 显式构造并验证斜率 $3$ 的函数的 $\varepsilon$--$\delta$ 证明；该结论允许 $x=a$，比去心版本更强。 |
| 洛必达法则：比较消失速度 | [`Calculus.removable_limit`](ThreeBlueOneBrown/Calculus.lean#L50) | 完整验证上述有理函数的去心极限，方法是局部化简与连续性；没有把它标成一般洛必达法则的形式化证明。 |
| 积分与微积分基本定理 | [`Calculus.fundamental_theorem`](ThreeBlueOneBrown/Calculus.lean#L64) | 调用完整的基本定理第二部分，保留区间上处处可导及导函数区间可积的精确假设。 |
| 面积为什么与斜率相连 | [`Calculus.triangle_area`](ThreeBlueOneBrown/Calculus.lean#L70) | 完整验证 $\int_0^a x\dd x=a^2/2$，也涵盖有向积分 $a<0$ 的情况。 |
| 高阶导数 | [`Calculus.second_derivative_cubic`](ThreeBlueOneBrown/Calculus.lean#L73) | 完整计算三次函数的二阶导数为 $6x$，同时核实中间的一阶导函数。 |
| 泰勒多项式与余项 | [`Calculus.cubic_taylor_exact`](ThreeBlueOneBrown/Calculus.lean#L82) | 验证三次多项式的精确泰勒恒等式；一般泰勒定理、级数收敛和余项界未纳入这一形式命题。 |
| 泰勒展开的面积解释 | [`Calculus.quadratic_error`](ThreeBlueOneBrown/Calculus.lean#L85) | 精确验证平方函数减去一次近似后等于 $h^2$；这给出二阶修正的可核查例子。 |
| 导数作为局部变换 | [`Calculus.derivative_composition_scale`](ThreeBlueOneBrown/Calculus.lean#L87) | 完整验证两个线性缩放复合后的导数为 $ab$。一般非线性链式法则另见本章对应定理。 |
| 散度与旋度 | [`Calculus.planar_divergence`](ThreeBlueOneBrown/Calculus.lean#L91) | 计算对角线性向量场的两个偏方向导数之和；未形式化散度定理或斯托克斯定理。 |
| 神经网络的基本单元 | [`NeuralNetworks.affine_composition`](ThreeBlueOneBrown/NeuralNetworks.lean#L5) | 精确验证两个标量仿射层的复合公式，说明非线性激活为何重要。 |
| 梯度下降如何学习 | [`NeuralNetworks.quadratic_gradient_step`](ThreeBlueOneBrown/NeuralNetworks.lean#L8) | 完整证明上述一维二次损失在闭区间步长条件下不增加；没有推广为所有网络的收敛保证。 |
| 检查网络究竟学到了什么 | [`NeuralNetworks.affine_input_sensitivity`](ThreeBlueOneBrown/NeuralNetworks.lean#L14) | 精确验证单输入仿射模型的扰动等式；范数界、校准与泛化的经验主张未形式化。 |
| 反向传播的直觉 | [`NeuralNetworks.gradient_accumulation`](ThreeBlueOneBrown/NeuralNetworks.lean#L17) | 完整证明两条可导损失分支相加时导数相加，作为共享梯度累积的标量核心。 |
| 反向传播的微积分 | [`NeuralNetworks.squared_loss_weight_gradient`](ThreeBlueOneBrown/NeuralNetworks.lean#L21) | 完整证明线性输出的平方损失对权重的导数。非线性层及矩阵反传公式在正文推导，未由此单命题覆盖。 |
| 语言模型的简明图景 | [`NeuralNetworks.conditional_product_bounds`](ThreeBlueOneBrown/NeuralNetworks.lean#L27) | 验证两个合法概率的乘积仍在 $[0,1]$；完整条件概率的测度论链式法则未形式化。 |
| Transformer 的整体结构 | [`NeuralNetworks.softmax_shift`](ThreeBlueOneBrown/NeuralNetworks.lean#L34) | 完整证明双分类 Softmax 的平移不变性。定理使用精确实指数；浮点稳定性仍属于数值实现问题。 |
| 注意力：按上下文加权信息 | [`NeuralNetworks.attention_convex`](ThreeBlueOneBrown/NeuralNetworks.lean#L44) | 完整证明两标量值的凸组合处在二者之间，保留权重 $0\le w\le1$ 的条件。 |
| 前馈层如何表达特征与关联 | [`NeuralNetworks.mlp_rank_one`](ThreeBlueOneBrown/NeuralNetworks.lean#L50) | 验证二维检测后写回等于相应外积矩阵作用的坐标公式；不是对模型知识存储机制的经验证明。 |
| 交叉熵：错误概率模型的编码代价 | [`Information.cross_entropy_decomposition`](ThreeBlueOneBrown/Information.lean#L19) | 完整验证严格正有限向量的熵、交叉熵与 KL 代数分解；此分解本身不要求归一化。同文件的 `kl_nonnegative` 进一步在两分布归一化时证明 KL 非负；零概率与无穷代价情形不在这两个定理的覆盖范围内。 |
| 扩散模型：从噪声中逐步恢复 | [`NeuralNetworks.denoising_reconstruction`](ThreeBlueOneBrown/NeuralNetworks.lean#L56) | 完整验证非零信号系数下的代数恢复式；未形式化随机扩散过程、训练有效性或生成质量。客座原课署名 Stephen Welch。 |
| 微分方程与向量场 | [`DifferentialEquations.exponential_solution`](ThreeBlueOneBrown/DifferentialEquations.lean#L5) | 完整验证 $\e^{kt}$ 的导数等于 $k\e^{kt}$；不是对所有微分方程的存在唯一性证明。 |
| 偏微分方程与热扩散 | [`DifferentialEquations.heat_stencil`](ThreeBlueOneBrown/DifferentialEquations.lean#L10) | 验证三点二阶差分算子对相加的线性性；连续 PDE 的分析及离散极限未由此命题覆盖。 |
| 用基本模式求解热方程 | [`DifferentialEquations.heat_mode_decay`](ThreeBlueOneBrown/DifferentialEquations.lean#L13) | 完整验证模式振幅的时间导数。空间正弦导数可由微积分模块组合；无限级数解与边界条件未形式化。 |
| 傅里叶级数：旋转与叠加 | [`DifferentialEquations.fourier_superposition`](ThreeBlueOneBrown/DifferentialEquations.lean#L17) | 验证单频复指数模式的线性叠加恒等式；不将它冒充傅里叶完备性或收敛定理。 |
| 复指数与旋转的物理图像 | [`DifferentialEquations.rotating_exponential_norm`](ThreeBlueOneBrown/DifferentialEquations.lean#L21) | 完整验证任意实角度的纯旋转复指数模长为一。 |
| 拉普拉斯变换：带衰减的频率探测 | [`DifferentialEquations.laplace_kernel`](ThreeBlueOneBrown/DifferentialEquations.lean#L24) | 验证实指数与拉普拉斯核相乘后合并为 $\e^{-(s-a)t}$ 的恒等式；不声称该恒等式本身证明了反演定理。 |
| 把微分方程变成代数方程 | [`DifferentialEquations.transformed_oscillator`](ThreeBlueOneBrown/DifferentialEquations.lean#L30) | 从已得到的变换域等式及非零分母推导商公式。积分分部、拉普拉斯存在性和反演不在该形式命题中。 |
| 动态理解欧拉恒等式 | [`DifferentialEquations.euler_identity`](ThreeBlueOneBrown/DifferentialEquations.lean#L36) | 完整验证复指数的欧拉恒等式，复用 mathlib 已证明的结论。 |
| 矩阵指数与线性动力系统 | [`DifferentialEquations.nilpotent_exponential_add`](ThreeBlueOneBrown/DifferentialEquations.lean#L39) | 完整证明平方零矩阵的上述半群恒等式；矩阵指数级数的收敛与求导由正文解释，未包含于此定理。 |
| 指数增长与饱和 | [`DifferentialEquations.logistic_threshold`](ThreeBlueOneBrown/DifferentialEquations.lean#L45) | 验证正增长率、正容量且状态处于 $(0,K)$ 时导数严格为正；未形式化流行病预测或参数估计。 |
| 课程公告与学习路线 | 不适用（公告） | 不适用：这是公告和学习方法页，没有需要机器证明的课程命题。仓库的覆盖统计对此显式豁免。 |
| 更简洁的二次公式 | [`Lockdown.quadratic_centering`](ThreeBlueOneBrown/Lockdown.lean#L5) | 完整验证配方恒等式；从平方等式分类实根或复根需另行处理。 |
| 三角函数从单位圆出发 | [`Lockdown.unit_circle`](ThreeBlueOneBrown/Lockdown.lean#L8) | 完整验证实数任意角度的单位圆恒等式。 |
| 复数：缩放与旋转 | [`Lockdown.complex_square_i`](ThreeBlueOneBrown/Lockdown.lean#L11) | 验证复数单位的核心关系 $\ii^2=-1$；其余运算公式可通过复数域的代数规则推出。 |
| 欧拉公式在说什么 | [`Lockdown.exponential_add`](ThreeBlueOneBrown/Lockdown.lean#L13) | 完整验证复指数的加法到乘法规则。欧拉特值另由微分方程模块中的 `euler_identity` 验证。 |
| 虚数利率与连续旋转 | [`Lockdown.imaginary_step_norm`](ThreeBlueOneBrown/Lockdown.lean#L16) | 验证单步复数的模长平方公式。复利序列收敛到复指数的极限定理未在此命题中形式化。 |
| 对数的基础结构 | [`Lockdown.logarithm_product`](ThreeBlueOneBrown/Lockdown.lean#L20) | 完整验证正实数乘积的自然对数公式，并显式要求两个真数为正。 |
| 自然对数为何自然 | [`Lockdown.natural_log_derivative`](ThreeBlueOneBrown/Lockdown.lean#L23) | 完整验证正实数处的自然对数导数，写明 $x>0$ 避免除零和实定义域误解。 |
| 幂塔与不动点 | [`Lockdown.tower_limit_fixed_point`](ThreeBlueOneBrown/Lockdown.lean#L28) | 完整证明一般连续迭代在已知收敛时，其极限为不动点；收敛是假设，绝不隐含在代数方程里。 |
| 为什么 i 的 i 次方可以是实数 | [`Lockdown.i_log_branch_exponent`](ThreeBlueOneBrown/Lockdown.lean#L41) | 验证任意实角度的关键指数恒等式 $\ii(\theta\ii)=-\theta$；并未将多值复幂误写成全局单值定理。 |
| 解题：找表示、找不变量、查边界 | [`Lockdown.symmetric_problem_reduction`](ThreeBlueOneBrown/Lockdown.lean#L47) | 完整验证对称二次式的代数变换。一般解题策略不是数学全称定理，不声称已被形式化证明。 |
| 熵：平均要问多少个二选一问题 | [`Information.entropy_term_nonnegative`](ThreeBlueOneBrown/Information.lean#L8) | 验证正概率 $p\le1$ 的单项 $-p\ln p$ 非负。代码还定义了有限分布的熵；编码下界、可达性和熵率并未形式化。 |

补充命题：

- [`Calculus.product_rule`](ThreeBlueOneBrown/Calculus.lean#L21)
- [`Information.kl_nonnegative`](ThreeBlueOneBrown/Information.lean#L29)
