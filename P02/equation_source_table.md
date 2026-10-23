# P02｜方程与单位来源表（第 1 步）

**状态：已完成方程框架、符号定义、单位规范及可追溯资料映射。**
**后续状态更新（2026-10-23）：**第一版教学参数已冻结为 `P02-EDU-V1`；最小解析模型、CSV/图表生成及自动检查已实现。冻结细节见 `model_parameters_v1.md`，运行结果见 `results_v1.md`。**
**核验日期：2026-10-21。**

## 1. 这一步在做什么

我们先把“准备计算什么、公式从哪里来、每个量用什么单位”写清楚，再动手编程。这样可以避免常见错误：把 cm⁻³ 和 m⁻³ 混用、把热电压和 MOSFET 阈值电压都叫 `V_T`、把课堂模型误说成产品模型，或把仿真结果误当成实测数据。

本项目的第一版范围是：

- 一个**硅（Si）PN 结二极管解析教学模型**；
- 一个**硅基 n 沟道、长沟道增强型 MOSFET（Metal–Oxide–Semiconductor Field-Effect Transistor，金属—氧化物—半导体场效应晶体管）解析教学模型**；
- 不是 SiC MOSFET 专用模型、不是 TCAD（Technology Computer-Aided Design，工艺/器件计算机辅助设计）模型、不是 COMSOL 半导体输运求解，也不是任何真实产品的拟合模型。

“长沟道”是说模型把沟道看成相对较长，足以先忽略短沟道效应；“增强型”表示栅压达到阈值后，才形成可导电的反型沟道。PN 结和 MOSFET 是两种不同器件；先学它们的基础方程，后续才更容易理解 SiC MOSFET。

## 2. 初学者先认识的词

| 术语/缩写 | 英文全称 | 中文释义 | 在本项目里的意思 |
|---|---|---|---|
| PN 结 / p–n junction | p-type–n-type junction | p 型半导体与 n 型半导体形成的结 | 一侧以空穴为多数载流子，另一侧以电子为多数载流子；交界附近形成耗尽区和内建电场。 |
| MOS | Metal–Oxide–Semiconductor | 金属—氧化物—半导体结构 | MOSFET 栅极控制沟道的基本叠层结构。 |
| MOSFET | Metal–Oxide–Semiconductor Field-Effect Transistor | 金属—氧化物—半导体场效应晶体管 | 用栅极电场控制源极和漏极之间电流的器件。 |
| I–V | Current–Voltage characteristic | 电流—电压特性 | 改变端口电压并观察模型电流如何变化的曲线。 |
| SI | International System of Units | 国际单位制 | 本项目代码统一采用米、秒、千克、安培、开尔文、库仑、伏特等 SI 单位。 |
| TE | Thermal Equilibrium | 热平衡 | 没有外部偏置导致的净载流子流动时的平衡状态。 |
| DA | Depletion Approximation | 耗尽近似 | 把 PN 结耗尽区内的自由电子/空穴近似为很少，只留下固定离化掺杂电荷。 |
| GCA | Gradual Channel Approximation | 渐变沟道近似 | 假设 MOSFET 沟道电势沿源—漏方向缓慢变化，用简化关系推导沟道电流。 |
| nMOS / NMOS | n-channel MOSFET | n 沟道 MOSFET | 本项目 MOSFET 模型的极性：沟道主要由电子导电。 |
| `N_A` | Acceptor concentration | 受主掺杂浓度 | p 型一侧的受主原子数密度。 |
| `N_D` | Donor concentration | 施主掺杂浓度 | n 型一侧的施主原子数密度。 |
| `n_i` | Intrinsic carrier concentration | 本征载流子浓度 | 无掺杂半导体在热平衡时的电子/空穴浓度基准。 |
| `V_bi` | Built-in potential | 内建电势 | p、n 两侧接触后形成的结区电势差。 |
| `V_th` | Threshold voltage | 阈值电压 | nMOS 开始形成强反型沟道所需的栅源电压近似值。 |
| `V_thermal` | Thermal voltage | 热电压 | `k_B T/q`，反映热能尺度折算成的电压；它不是 MOSFET 阈值电压。 |
| `C_ox` | Oxide capacitance per unit area | 单位面积栅氧电容 | 栅氧层把栅极电压耦合到沟道的能力。 |
| `V_OV` | Overdrive voltage | 过驱动电压 | `V_GS - V_th`，表示栅压超过阈值多少。 |
| `I_D` | Drain current | 漏极电流 | 从漏极流过 MOSFET 沟道的电流。 |
| `I_S` | Reverse saturation current | 反向饱和电流 | 理想二极管 I–V 方程里的尺度参数，不等同于实际器件所有反向漏电机制。 |
| 耗尽区 | Depletion region | 耗尽区 | PN 结附近可移动电子/空穴显著减少、主要由固定离化杂质电荷形成空间电荷的区域。 |
| 准中性区 | Quasi-neutral region | 准中性区 | 耗尽区外部的半导体区域；宏观正负电荷近似抵消。 |
| 低注入 | Low-level injection | 低水平注入 | 偏置产生的少数载流子增量远小于原有多数载流子浓度，便于使用线性扩散近似。 |
| 长基区 | Long-base diode | 长基区二极管条件 | 中性区长度远大于少数载流子扩散长度，载流子在抵达接触端前已显著复合。 |
| 强反型 | Strong inversion | 强反型 | MOS 电容表面已形成与衬底多数载流子极性相反、足以形成沟道的载流子层。 |
| 平带电压 `V_FB` | Flat-Band Voltage | 平带电压 | MOS 结构中半导体能带近似平直时对应的栅压，受栅材料功函数和界面电荷等影响。 |
| 夹断 | Pinch-off | 沟道夹断 | 长沟道 MOSFET 漏端附近反型沟道变薄至近零；进入理想模型的饱和区，不等于器件击穿。 |
| 沟道长度调制 | Channel-Length Modulation | 沟道长度调制 | 饱和区下漏压继续上升时，有效沟道变短、漏电流仍略增加的效应；第一版忽略。 |
| 声子散射 | Phonon Scattering | 声子散射 | 晶格热振动会散射载流子，是迁移率随温度变化的重要原因之一。 |
| `q` | Elementary charge | 元电荷量 | 单个基本电荷的大小，单位 C；符号取正的电荷量大小，电子电荷为 `-q`。 |
| `k_B` | Boltzmann constant | 玻尔兹曼常数 | 把温度换成热能尺度的物理常数，单位 J/K。 |
| `ε_0` | Vacuum electric permittivity | 真空介电率 | 真空的介电率，单位 F/m。 |
| `ε_r` | Relative permittivity | 相对介电常数 | 材料介电率相对真空介电率的比值，无量纲。 |
| `ε_s / ε_ox` | Semiconductor / oxide permittivity | 半导体/栅氧介电率 | `ε=ε_r ε_0`，单位 F/m。 |
| `E_g` | Bandgap energy | 带隙能量 | 价带与导带之间的能量间隔；若来源以 eV 表示，计算 SI 指数前须转 J。 |
| `eV` | Electronvolt | 电子伏特 | 能量单位；`1 eV=q J`。 |
| `N_C / N_V` | Effective density of states in the conduction / valence band | 导带/价带有效态密度 | 参与半导体载流子统计的有效状态数密度，单位 m⁻³。 |
| `D_n / D_p` | Electron / hole diffusion coefficient | 电子/空穴扩散系数 | 描述载流子因浓度梯度扩散的系数，单位 m²/s。 |
| `τ_n / τ_p` | Minority-carrier lifetime | 少数载流子寿命 | 少数载流子平均复合时间，单位 s。 |
| `L_n / L_p` | Electron / hole diffusion length | 电子/空穴扩散长度 | 少数载流子在复合前扩散的特征距离，单位 m。 |
| `V_GS` | Gate-to-Source Voltage | 栅—源电压 | 栅极相对源极的电压，单位 V。 |
| `V_DS` | Drain-to-Source Voltage | 漏—源电压 | 漏极相对源极的电压，单位 V。 |
| `V_SB` | Source-to-Body Voltage | 源—衬底电压 | 源极相对衬底/体区的电压；体偏置会改变阈值，本基础式先取 0。 |
| `W_ch / L_ch` | Channel width / channel length | 沟道宽度/长度 | MOSFET 沟道几何尺寸，单位 m；公式中以比值相除后无量纲。 |
| `n_d` | Diode ideality factor | 二极管理想因子 | 修正理想扩散方程指数斜率的无量纲参数；理想扩散基线设为 1。 |
| SPICE | Simulation Program with Integrated Circuit Emphasis | 集成电路仿真程序 | 电路仿真器常用格式/模型语境；这里只出现在相关研究背景，不是本项目运行工具。 |
| TCAD | Technology Computer-Aided Design | 工艺/器件计算机辅助设计 | 用数值方法模拟半导体工艺或器件；本 P02 解析教学模型不是 TCAD。 |
| 体效应 | Body effect | 基体效应 | 源—衬底偏压导致 MOSFET 阈值电压变化的现象；本第一版忽略。 |
| 亚阈值电流 | Subthreshold current | 亚阈值电流 | 栅压低于阈值时仍流过的电流；本第一版强反型模型不包含它。 |
| 短沟道效应 | Short-channel effects | 短沟道效应 | 沟道很短时电场、阈值和漏端控制偏离长沟道模型的现象；本第一版忽略。 |
| Si | Silicon | 硅 | 本项目 PN 结与基础 MOSFET 公式的教学材料；不代表 SiC。 |
| SiC | Silicon Carbide | 碳化硅 | 功率器件主线的材料背景；本 P02 基础方程并未建立 SiC 专用模型。 |
| MIT | Massachusetts Institute of Technology | 麻省理工学院 | 本方程表引用的大学课程资料来源。 |
| OCW | OpenCourseWare | 开放课程资源 | 大学公开课程讲义/教学资源。 |
| NIST | National Institute of Standards and Technology | 美国国家标准与技术研究院 | 本项目基础物理常数的来源机构。 |
| CODATA | Committee on Data of the International Science Council | 国际科学理事会数据委员会 | 国际科学理事会的科学数据委员会；此处指其推荐的基本物理常数值。 |
| ISC | International Science Council | 国际科学理事会 | CODATA 所属的国际科学组织。 |
| IEEE | Institute of Electrical and Electronics Engineers | 电气电子工程师学会 | Kubulus 等研究所发表的专业学会/出版机构名称。 |
| `I_diode` | Diode current | 二极管电流 | PN 结模型的端电流；避免与 MOSFET 漏极电流 `I_D` 混用。 |
| `V_diode` | Diode voltage | 二极管电压 | PN 结两端电压；避免与 MOSFET 漏极端电压混淆。 |

## 3. 方程来源与使用边界

### A. 公用热学与半导体平衡量

| 方程/关系 | 符号的含义 | 为什么要用 / 适用边界 | 主要来源 |
|---|---|---|---|
| `V_thermal = k_B T / q` | `k_B`：Boltzmann constant（玻尔兹曼常数）；`T`：绝对温度，K；`q`：元电荷量，C。结果单位为 V。 | 把热能 `k_B T`（J）除以电荷量（C），变成电压。300 K 时约 25.85 mV。二极管指数项和半导体载流子统计都会用到。 | NIST CODATA 常数；MIT 6.012 Lecture 1。 |
| `n_0 p_0 = n_i^2` | `n_0`、`p_0`：热平衡电子、空穴浓度；`n_i`：本征载流子浓度。三个浓度都用 m⁻³。 | 质量作用定律；用于检查平衡载流子数量级。适用于非简并、热平衡模型；重掺杂/非平衡时需更完整模型。 | MIT 6.012 Lecture 1（载流子浓度与热平衡）。 |
| `n_i(T) ≈ sqrt(N_C(T) N_V(T)) exp[-E_g(T)/(2 k_B T)]` | `N_C/N_V`：导带/价带有效态密度，m⁻³；`E_g`：带隙能量，J；指数无量纲。 | 说明本征浓度强烈依赖温度。要算温度扫描，不能把 300 K 的 `n_i` 原封不动用于所有温度；需同时指定材料的 `E_g(T)`、`N_C(T)`、`N_V(T)` 来源。本式是非简并统计近似，不单独提供这些材料参数。 | MIT 6.012 Lecture 1；材料参数需用可追溯的硅材料来源。 |

### B. PN 结解析模型

| 方程 | 符号说明 | 直观解释和有效条件 | 主要来源 |
|---|---|---|---|
| `V_bi = V_thermal ln(N_A N_D / n_i^2)` | `N_A`、`N_D`、`n_i` 均为 m⁻³；比例项无量纲；`ln` 是自然对数。 | 掺杂后 p、n 两侧载流子浓度不同，接触后扩散形成电场；电场建立到足以抵消继续扩散时，形成内建电势。采用热平衡、完全电离、非简并近似。 | MIT 6.012 Lecture 4《p-n Junctions: Electrostatics》。 |
| `W_dep = sqrt[(2 ε_s / q)(1/N_A + 1/N_D)(V_bi - V_a)]` | `W_dep`：总耗尽层宽度，m；`ε_s=ε_r,s ε_0`：半导体介电率，F/m；`V_a`：外加结电压，V，正值表示正向偏置。 | 外加正向偏压降低势垒、耗尽层变窄；反向偏压可用负的 `V_a` 表示，使耗尽层变宽。来自突变结与耗尽近似；仅用于根号内为非负、未进入强击穿/高注入等情形。 | MIT 6.012 Lecture 4；COMSOL 官方 PN 结案例用于对照基准设置，不是实测数据。 |
| `x_n = [N_A/(N_A+N_D)] W_dep`；`x_p = [N_D/(N_A+N_D)] W_dep` | `x_n`、`x_p`：耗尽区分别伸入 n、p 两侧的宽度，m。 | 由两侧固定电荷大小近似相等得出。较轻掺杂的一侧通常承担更大耗尽宽度。 | MIT 6.012 Lecture 4。 |
| `I_diode = I_S {exp[V_diode/(n_d V_thermal)] - 1}` | `I_diode`：二极管电流，A；`V_diode`：二极管端电压，V；`n_d`：理想因子，无量纲；第一版理想扩散模型取 `n_d=1`。 | 小正向电压时电流指数上升；零偏时电流为 0；反向电压下理想方程趋近 `-I_S`。真实器件会有串联电阻、复合、击穿等偏离，本项目不把这个公式用于产品预测。 | MIT 6.012 Lecture 5–6《Injection and Flow》《I-V Relationship》。 |
| `I_S = q A n_i² [D_n/(L_n N_A) + D_p/(L_p N_D)]`；`L_n=sqrt(D_n τ_n)`；`L_p=sqrt(D_p τ_p)` | `A`：结面积，m²；`D_n/D_p`：扩散系数，m²/s；`τ_n/τ_p`：少数载流子寿命，s；`L_n/L_p`：扩散长度，m。 | 这是长基区、低注入、理想扩散条件下，电子与空穴扩散电流合成的饱和电流表达式。若目前没有可靠的 `D` 和 `τ` 输入，代码中应把 `I_S` 作为注明“教学假设”的独立参数，而不是伪造测量值。 | MIT 6.012 Lecture 5–6。 |

### C. nMOS 长沟道教学模型

| 方程 | 符号说明 | 直观解释和有效条件 | 主要来源 |
|---|---|---|---|
| `C_ox = ε_ox / t_ox` | `ε_ox`：栅氧介电率，F/m；`t_ox`：氧化层厚度，m；`C_ox`：单位面积电容，F/m²。 | 氧化层越薄或介电率越高，单位面积电容通常越大，栅极对沟道的控制耦合更强。不要把 `C_ox`（每平方米）与总栅电容混为一谈。 | MIT 6.012 Lecture 9–10；COMSOL 材料文档提供 SI 单位口径。 |
| `φ_F = V_thermal ln(N_A/n_i)` | `φ_F`：p 型衬底的费米势大小，V。这里使用正值定义。 | 描述掺杂后费米能级相对本征能级的位置；这里面 `n_i` 随温度变，故 `φ_F` 也会变。 | MIT 6.012 Lecture 9–10。 |
| `V_th = V_FB + 2φ_F + sqrt(4 q ε_s N_A φ_F)/C_ox` | `V_FB`：Flat-Band Voltage（平带电压），V；本项目先将其作为输入参数；`N_A`：p 型衬底受主浓度；`V_th`：阈值电压。 | 作为 `V_SB=0`（源—衬底电压为 0）、nMOS、突变耗尽近似、强反型阈值定义的基础式；未包含复杂界面电荷、短沟道和器件工艺校准。 | MIT 6.012 Lecture 9–10 的 MOS 电容/阈值关系；符号转换采用本文件的正 `φ_F` 定义。 |
| `V_OV = V_GS - V_th` | `V_GS`：栅—源电压，V；`V_OV`：过驱动电压，V。 | 栅压高过阈值的余量。`V_OV≤0` 时第一版强反型模型置 `I_D=0`；这不代表现实 MOSFET 在阈值下完全无电流，因为亚阈值电流被省略。 | MIT 6.012 Lecture 10–11。 |
| `I_D=0`（截止）；`I_D=μ_n C_ox (W_ch/L_ch)[V_OV V_DS - V_DS²/2]`（线性/三极区）；`I_D=(1/2) μ_n C_ox (W_ch/L_ch) V_OV²`（饱和区） | `μ_n`：电子迁移率，m²/(V·s)；`W_ch/L_ch`：沟道宽度/长度，m；`V_DS`：漏—源电压，V；`I_D`：A。线性区条件 `0≤V_DS≤V_OV`；饱和区条件 `V_DS≥V_OV>0`。 | 小 `V_DS` 时，沟道像受栅压控制的电阻；`V_DS` 增大到约 `V_OV` 后，漏端沟道夹断，基础模型的电流进入饱和。两段在 `V_DS=V_OV` 处电流连续。 | MIT 6.012 Lecture 10–11 的 GCA/DA 长沟道模型。第一版忽略沟道长度调制、短沟道效应、自热、陷阱和高场迁移率退化。 |

### D. 温度扩展规则（供后续实现使用）

| 量 | 温度规则 | 本项目处理边界 |
|---|---|---|
| `V_thermal(T)` | `k_B T/q`，直接由 SI 常数计算。 | 可直接随 `T` 更新。 |
| `n_i(T)` | 用上表本征浓度关系，且需要硅的带隙/态密度随温度模型。 | 在这些输入有来源前，不允许只改热电压、却声称已完整刻画二极管温度效应。 |
| `μ_n(T)` | 可用简单幂律 `μ_n(T)=μ_n,0 (T/T_0)^(-α_n)` 做教学敏感性分析；COMSOL 的 Power Law Mobility Model（幂律迁移率模型）也将晶格/声子散射纳入简化表达。硅的参考参数示例为 `T_0=300 K`、`μ_n,0=1448 cm²/(V·s)=0.1448 m²/(V·s)`、`α_n=2.33`。 | 这是硅参数示例，不是 SiC 参数，也不等于完整迁移率模型；第一版须标为“硅教学参数/模型假设”。如要更真实地描述掺杂和高场依赖，需换更复杂的模型并追加验证。 |
| `V_th(T)` | 由 `V_thermal(T)`、`n_i(T)`、`φ_F(T)`、介电率、电容和 `V_FB` 等电学/材料参数影响。 | 迁移率会直接影响 `I_D(T)`，但不直接出现在本基础静电阈值公式中；阈值变化方向由参数模型共同决定，不能预先简单断言。 |

### E. 可追溯的硅参数候选（暂不等于已冻结输入）

COMSOL 6.3 Semiconductor Material Properties 表列出一组硅材料参考量：相对介电率 `ε_r,Si=11.7`、300 K 带隙 `E_g≈1.12 eV`、`N_C(300 K)=2.8×10^19 cm⁻³`、`N_V(300 K)=1.04×10^19 cm⁻³`。其幂律迁移率子模型给出电子迁移率参考 `μ_n,0=1448 cm²/(V·s)`、温度指数 `α_n=2.33`、参考温度 `T_0=300 K`。这些是软件文档所列的硅模型参数，不是本项目测量值；使用前需统一转成 SI 单位，并在输入表记录来源版本、模型名称和使用限制。数据手册器件参数不与上述通用硅教学参数混合。
## 4. 统一单位字典

| 变量/类别 | 代码内部单位 | 常见外部单位换算 | 备注 |
|---|---|---|---|
| 长度 `x,t_ox,W_ch,L_ch,L_n,L_p` | m | `1 μm = 1×10⁻⁶ m`；`1 nm = 1×10⁻⁹ m` | 用于电场、耗尽层和沟道几何。 |
| 面积 `A` | m² | `1 cm² = 1×10⁻⁴ m²` | 只用于 PN 结面积。 |
| 掺杂/载流子浓度 `N_A,N_D,n_i,n,p` | m⁻³ | `1 cm⁻³ = 1×10⁶ m⁻³`；例：`1×10¹⁵ cm⁻³ = 1×10²¹ m⁻³` | 这是最容易错六个数量级的地方；统一转成 m⁻³ 后再参与公式。 |
| 电压 `V_D,V_bi,V_a,V_GS,V_DS,V_th` | V | mV 转 V：乘 `10⁻³` | thermal voltage 与 MOS threshold 分开命名。 |
| 电流 `I_D,I_S` | A | mA=`10⁻³ A`；μA=`10⁻⁶ A` | 输出是解析模型值，不是测试结果。 |
| 迁移率 `μ_n,μ_p` | m²/(V·s) | `1 cm²/(V·s)=1×10⁻⁴ m²/(V·s)` | 例如 `1448 cm²/(V·s)=0.1448 m²/(V·s)`。 |
| 扩散系数 `D_n,D_p` | m²/s | `cm²/s` 乘 `10⁻⁴` 转为 `m²/s` | 同迁移率的长度平方换算。 |
| 时间/寿命 `τ_n,τ_p` | s | μs=`10⁻⁶ s`；ns=`10⁻⁹ s` | 不是本第一版一定要输入的参数。 |
| 温度 `T,T_0` | K | 摄氏度转 K：`T(K)=T(°C)+273.15` | 热力学公式必须使用开尔文。 |
| 介电率 `ε_s,ε_ox,ε_0` | F/m | 相对介电常数 `ε_r` 无量纲；`ε=ε_r ε_0` | 材料相对介电率不能直接当成 F/m。 |
| 单位面积电容 `C_ox` | F/m² | 若使用 F/cm²，需换算 | 公式 `C_ox=ε_ox/t_ox`。 |
| 能量 `E_g` | J | 若来源写 eV，乘 `q` 转 J | 指数项 `E_g/(k_B T)` 必须无量纲。 |
| 自然对数 `ln(·)`、指数 `exp(·)` | 无单位函数 | 函数输入必须无量纲 | 例如 `N_A N_D/n_i²`、`V_D/(n_d V_thermal)` 均无量纲。 |

### 代码输入约定

1. 输入表和 Python 内部计算一律用 SI 单位；若来源用 cm、μm、cm⁻³ 或 cm²/(V·s)，在读取时做显式转换，并保留原值、原单位和换算值。
2. 所有对数或指数的参数必须无量纲；所有平方根里的量必须满足物理定义域。
3. 参数表必须区分“官方常数/材料资料参数/论文参数/教学假设”；本项目不导入论文器件曲线来拟合模型。
4. `V_thermal` 与 `V_th` 绝不可用同一变量名；建议代码用 `v_thermal` 与 `vth_mos`。
5. 由于 PN 模型和 MOS 模型都是教学解析模型，曲线标题需标明“解析教学模型”，不能标注“实测”或“产品仿真”。

## 5. 本步交付与下一步

本表记录模型所用关系式、符号和单位。当前最小可复现模型已按冻结参数实现：先计算 PN 结耗尽区及理想二极管 I–V，再计算长沟道 nMOS 转移与输出特性。已有的自动检查用于发现单位换算、边界和连续性错误，不是实验验证或产品精度证明。下一步是扩展结果合理性核查与敏感性分析。

## 6. 来源清单

- **MIT 6.012 OpenCourseWare（Microelectronic Devices and Circuits）**：Lecture 1《Introduction to Semiconductors》用于掺杂、平衡载流子和迁移率基础；Lecture 4《p-n Junctions: Electrostatics》用于耗尽近似和 PN 结静电；Lecture 5–6 用于载流子注入与理想 PN 结 I–V；Lecture 9–10 用于 MOS 电容和阈值关系；Lecture 10–11 用于渐变沟道近似及长沟道 MOSFET 大信号 I–V 模型。链接见下方。
- **NIST CODATA 2022**：元电荷、Boltzmann 常数及真空介电率。`q=1.602176634×10⁻¹⁹ C`，`k_B=1.380649×10⁻²³ J/K`，`ε_0≈8.8541878188×10⁻¹² F/m`。
- **COMSOL 官方 Semiconductor Module 文档**：只用来交叉检查 SI 单位、硅相对介电率/迁移率参考值和“完整器件模型需要考虑温度、掺杂、复合等因素”的边界；不将 COMSOL 文档说成实验数据，也不把本项目模型说成 COMSOL 求解。
- **Kubulus et al. (2025), IEEE Transactions on Power Electronics**：属于 P02 的 SiC 紧凑模型研究背景，不是本表基础 PN/MOS 方程的唯一来源，也不代表本项目复现其 SPICE 模型。

### 直达资料

- [MIT 6.012 Lecture 1 — Introduction to Semiconductors](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/resources/mit6_012f09_lec01/)
- [MIT 6.012 Lecture 4 — p-n Junctions: Electrostatics](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/resources/mit6_012f09_lec04/)
- [MIT 6.012 Lecture 5 — p-n Junction Injection and Flow](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/resources/mit6_012f09_lec05/)
- [MIT 6.012 Lecture 6 — p-n Junctions: I-V Relationship](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/resources/mit6_012f09_lec06/)
- [MIT 6.012 Lecture 9 — MOS Capacitors I](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/resources/mit6_012f09_lec09/)
- [MIT 6.012 Lecture 10 — MOS Caps II; MOSFETs I](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/resources/mit6_012f09_lec10/)
- [MIT 6.012 Lecture 11 — MOSFETs II; Large Signal Models](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/resources/mit6_012f09_lec11/)
- [NIST CODATA 2022 constant values (including elementary charge, Boltzmann constant, and vacuum electric permittivity)](https://www.physics.nist.gov/cuu/pdf/wall_2022.pdf)
- [COMSOL semiconductor material properties](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_ref_materials.25.47.html)
- [COMSOL power-law mobility model](https://doc.comsol.com/6.3/doc/com.comsol.help.semicond/semicond_ug_semiconductor.6.13.html)
- [COMSOL 6.4 P–N Junction 1D official example](https://doc.comsol.com/6.4/doc/com.comsol.help.models.semicond.pn_junction_1d/pn_junction_1d.html)
- [Kubulus et al., DOI 10.1109/TPEL.2024.3510037](https://doi.org/10.1109/TPEL.2024.3510037)
