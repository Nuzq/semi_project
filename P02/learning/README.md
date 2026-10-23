# P02 学习页面｜PN 结与 MOSFET 基础

本目录包含面向初学者的讲义和零依赖交互教学页面，讲解 P02 第一步的三个部分：PN 结、nMOSFET、参数与 SI 单位。方程来源表和完整讲义已预先编译为本地 HTML，点击页面底部按钮后会在当前页面的原生对话框中排版显示。

## 打开与目录

直接用现代浏览器打开 index.html，不需要安装依赖或连接网络。

- 第一步_初学者讲义.md：详细概念、公式、参数含义、缩写全称和适用边界。
- docs/equation_source_table.html、docs/first_step_handout.html：由 Markdown 生成的独立 HTML 文档，供页面弹窗中的 iframe 离线读取。
- build_docs.py：当任一 Markdown 源文档更新时，重新生成上述 HTML。运行前需安装 Python-Markdown：python -m pip install Markdown；然后在本目录运行 python build_docs.py。
- index.html：页面结构和文字内容。
- styles.css：页面外观、响应式布局、键盘焦点和减少动态效果支持。
- app.js：PN 结、偏置、理想二极管 I–V 反算示例、MOSFET、热电压随绝对温度变化的教学演示、单位换算和术语提示交互。页面滑块是独立的概念示意，不调用冻结参数集或运行器件特性计算；模型数据由项目根目录的 Python 脚本生成。

## 嵌入个人主页

最隔离、最省事的集成方式是 iframe。将整个 learning 文件夹部署到个人主页可访问的静态资源目录，按实际部署路径修改 src：

~~~html
<iframe
  src="/projects/p02-learning/index.html"
  title="P02 半导体器件基础交互讲解"
  loading="lazy"
  style="width:100%;min-height:1100px;border:0;border-radius:16px"
></iframe>
~~~

如果以后希望直接使用主页的导航、字体和主题，可以把页面的 lesson sections、styles.css 和 app.js 拆入主页组件。本页面不依赖外部库，交互限制在本目录内；作为单页静态资源可直接部署，嵌入时由 iframe 隔离样式与脚本。

## 教学边界

- PN 滑块只表现趋势：反偏时耗尽区变宽，正偏时变窄；没有用项目参数计算真实耗尽层。
- 热电压滑块只按 SI 常数展示 Vthermal = kB·T/q 与绝对温度的比例关系，不涵盖 ni、迁移率等温度依赖，也不是器件温度模型。
- 二极管电压估算器将理想二极管 I–V 方程代数反解；演示用电流、反向饱和电流和理想因子可编辑，但这些假设值不能替代器件数据。
- MOSFET 滑块使用演示用过驱动电压和漏源电压展示区间切换；电流显示为归一化趋势，不是安培值，也不代表 `P02-EDU-V1` 的计算结果。
- 单位换算器只做单位换算。
- 本目录没有实现器件空间分布数值求解、产品拟合、实测数据驱动模型、COMSOL 或 TCAD 求解；页面中的二极管计算只是理想方程反算，概念动画不能写成器件仿真结果。
- 页面支持键盘操作、窄屏布局，并遵循 prefers-reduced-motion（减少动态效果）系统偏好。

方程技术底稿见 ../equation_source_table.md，进度见 ../status.md。

## 文档弹窗与本地部署

- 直接打开 index.html 时无需启动本地服务器；弹窗读取同目录中的预生成 HTML 文件，不通过浏览器 fetch 读取 Markdown，因此 file:// 打开也可用。
- 修改方程来源表或初学者讲义后，运行 build_docs.py 更新 docs/ 下的 HTML；提交/部署时应同时包含 Markdown 源文档和 docs/ 中的生成文件。
- 弹窗支持关闭按钮、Escape 键和点击遮罩关闭；关闭后焦点返回触发按钮。HTML 文档以 iframe 隔离样式，避免污染教学页面。

## 交互与动画约定

- 参数下标、指数使用 HTML sub/sup；SVG 图内的下标采用 tspan。
- 模态弹窗进入/退出使用 360 ms 的 opacity 与轻微位移过渡；按钮反馈使用 180 ms；PN 耗尽区和电荷符号使用 280 ms，帮助观察变量变化。
- 偏置滑块只用于解释趋势。耗尽区内正、负固定离子符号各自定位于区域左右两半，即使正向偏置达到教学刻度上限也不会互相覆盖。
- 遵循系统减少动态效果偏好；器件运动示意的连续动画会被关闭。
