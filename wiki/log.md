# Wiki Log

## [2026-11-12] revise | M42 延长筒外径实测回填与座孔派生更新
- Measured: 用户实测 M42×0.75、长 10 mm 延长筒的筒身外径 44 mm；F-02 由 42／待定 改为 44／已确认
- Updated: F-03 座孔由 42.3 派生为 44.3，F-04 旧反推依据作废；同步总体派生尺寸链、首轮接口冻结、T11 详细设计、T16 排版与 T08a 试片记录、FM-05 采集清单
- Risk: 座孔 44.3 时孔壁至两条调节槽内缘仅余约 0.6 mm（由 F-09 槽距 50 与槽宽 4.5 决定，加宽板宽无效）；进入座孔的实际段落（筒身 44 或螺纹段约 42）仍需 FM-05 台阶与螺纹长度数据
- Not written back: `FocuserMountPlate.FCStd` 与契约 `if_top_m42_hole_d` 仍为 42.3，整板 DXF 与 T08a 试片未重生成；T11／T16／T08a 保持待验证

## [2026-11-07] refactor | CAD 模块正式分层
- Moved: 模块专属零件进入 `Parts/`，下一级总成进入 `SubAssemblies/`；公共件与契约改为 `90_CommonParts/`、`91_Interfaces/`；试片和套合试环进入 `tests/fixtures/cad/`
- Added: 根目录与 `cad/` README；13 份 DXF 归入 `exports/drawings/`；本地备份移至根目录 `backup/` 并保持 Git 忽略
- Updated: 32 份 FCStd 的内部相对文件链接，以及备份监控、VS Code、AGENTS、建模技能和当前文档路径
- Verified: 38 份模型只读重开和 recompute 无错误，148 个文件引用、Link、实体、草图和 ZIP 完整性通过；Markdown、Python、JSON 和备份归档样例通过
- Scope: 保留所有 FCStd 文件名，未修改设计参数、几何或 T09～T17 状态

## [2026-11-07] refactor | 仓库目录结构迁移
- Moved: 正式模型模块与契约迁入 `cad/`，模型备份迁入 `cad/backup/`；备份监控迁入 `src/tools/`；建立 `tests/` 与 `tests/fixtures/cad/` 测试边界
- Updated: VS Code 任务、AGENTS、freecad-modeling 技能、当前文档模型链接、项目概览、命名规范、模块清单与 wiki 索引
- Verified: 38 份现行 FCStd 只读重开和 recompute 无迁移错误，XLink／Link、实体、草图及 ZIP 完整性通过，SHA-256 不变；Markdown 链接、Python 语法、JSON 和备份监控临时样例通过
- Note: 计划时位于 `.pi/` 的 5 个临时 T10 脚本在执行前已不存在，未重建或迁移；设计参数和 T09～T17 状态不变

## [2026-11-07] design | T13 摇架榫接与方位支承闭合
- Added: A-13～A-22；侧板双 30×16 mm 榫、底板四通槽、双 341.5 mm 底板、M8 中心枢轴和四块 PTFE 滑动垫
- Created: `GroundBasePlate.FCStd`；总装增至 35 Link，收纳增至 36 Link，并增加独立地面板层
- Derived: 箱内高 244.036 mm、箱外高 276.036 mm；侧板带榫平面长度 451.4162 mm
- Verified: 新增草图完全约束，源件单实体；总装非设计干涉为 0；榫宽与垫厚回归未保存；九份 DXF 重导入 mm、1:1
- Status: T13／T15／T16 保持待验证；胶合、摩擦、配重和稳定性待整批加工后试验

## [2026-11-07] design | 底座箱、拆解收纳与生产图闭合
- Created: `01_Base/StorageBox/` 六个独立板件、6 Link 箱体装配与 35 Link 收纳装配；箱内 460×345.5×226.036 mm，箱外 492×377.5×258.036 mm
- Verified: 内容物均在箱内边界，35 Link 两两干涉为 0；新增两份箱体 DXF 和重建夹块 DXF 均重导入为 mm、1:1
- Corrected: 两种夹块的矩形端点约束、外侧开口与横向夹紧孔；副镜环源件变换；弧臂和摇架侧板的旋转／侧向偏移
- Verified: 总装 30 Link 全量检查仅保留调焦板设计嵌入，其他干涉为 0；25→30 mm 杆插入回归通过且未保存
- Status: T10／T15／T16 保持待验证；实物加工、试装、装箱与观测在整批加工后集中执行

## [2026-11-07] revise | 草图命名约束中文化
- Rule: 草图命名约束（尺寸标注名称）必须使用自描述中文，改名时同步更新表达式引用；参数 Alias 仍按既有英文规则维护
- Changed: 5 份模型中的 34 个英文约束名已改为中文，包括 LowerRodEndZ → 下杆端轴向位置、MAJOR → 副镜椭圆长轴
- Verified: 20 份 FCStd 经 freecadcmd 全部重开和强制 recompute；128 个命名约束均为中文，无旧引用、错误、断链或草图冲突／冗余，实体几何与关键约束值不变

## [2026-11-07] revise | 既有模型 Label 中文化清理
- Changed: 检查 20 份 FCStd、728 个对象，将 591 个不合规对象 Label 改为中文自描述名称；文件名、内部 Name、参数 Alias 和设计参数保持不变
- Verified: 全部关闭重开和强制 recompute 无错误；ZIP 完整性、链接、草图、Body 有效性及关键参数回归通过，无实体数量或关键尺寸变化
- Scope: FCStd 文档显示名由文件名派生，不作为可持久化对象 Label 批量改名；规范文档已同步明确该边界

## [2026-11-07] revise | 模型 Label 中文自描述命名约束
- Rule: 模型中所有对象的 Label 必须使用中文并自描述，能直接识别对象及其用途；不得使用无语义默认名或晦涩缩写
- Scope: Label 面向阅读与维护；内部 Name 和参数 Alias 不受此中文化约束，仍按各自规则维护
- Updated: AGENTS、freecad-modeling 技能、结构设计与 FreeCAD 建模指南及 wiki 索引同步；未修改既有 FCStd

## [2026-11-06] ingest | 项目概览
- Updated: 命名与文档规范

## [2026-11-06] ingest | 命名与文档规范

## [2026-11-06] ingest | 模块与文档清单

## [2026-11-06] ingest | 光学合焦与调焦座参数

## [2026-11-06] ingest | Interfaces 契约层

## [2026-11-06] init | wiki 初始化（raw/ + wiki/ 骨架，批量导入 README / 光学方案 / 契约表 / 文档清单四份源材料，编译 5 篇文章）

## [2026-11-06] ingest | 目录与文件改名（词汇体系对齐）
- Updated: 项目概览
- Updated: 命名与文档规范
- Updated: 模块与文档清单
- Updated: Interfaces 契约层

## [2026-11-06] ingest | 契约项 if_rod_socket_depth 移除
- Updated: Interfaces 契约层
- Updated: 模块与文档清单

## [2026-11-06] ingest | 结构设计与 FreeCAD 建模指南（用户原文，项目化修订）
- Created: 结构设计与 FreeCAD 建模指南（修正 Fillet/Chamfer/Draft 术语错配，补契约层两层制、项目工艺与公差挂钩）

## [2026-11-06] revise | 结构设计与 FreeCAD 建模指南合并审校
- Updated: 合并设计输入、基准链、公差配合、连接与标准件、特征选择、参数回归和工程交付原则
- Updated: 将绝对化建模禁令改为稳健默认策略；修正桁架纯拉压、叠层闭口截面、统一留间隙及固定深径比等不严谨表述
- Updated: 对齐 App::Link 组装规范，明确 App::Part、Assembly 与干涉检查的职责边界

## [2026-11-06] revise | 补充未知尺寸的参数探索原则
- Updated: 结构设计与 FreeCAD 建模指南（先范围后定值、先粗后细、固定指标对比、保留候选与结果、验证后冻结）
- Updated: 明确探索值与跨模块契约真值的边界，要求参数调整可控、可比、可追溯、可回退

## [2026-11-06] ingest | 道布森望远镜需求基线与旧尺寸审核
- Created: 需求与旧尺寸审核（确认已有实物、四种观测/摄影组合、附件需求、免工具拆装、未来 GoTo/赤道平台接口和制造条件）
- Created: 33 项旧结构尺寸审核表，统一默认“待定”，提供确认值与审核备注栏
- Updated: 项目概览和 Interfaces 契约层增加本轮重审口径；不修改 FCStd 契约或模型

## [2026-11-06] revise | 建立 docs 唯一参数表并统一木板厚度
- Created: `docs/telescope-parameters.md`，集中维护实物、光学、结构参数、公式与审核状态
- Confirmed: `board_t=16 mm`；通用环、下环单层、主镜箱环、底座箱和俯仰弧臂的木板厚度统一引用该参数
- Updated: wiki 需求页改为定性需求与审核入口，不再复制参数值；光学页和索引同步指向唯一参数表

## [2026-11-06] revise | 明确无主镜箱的主镜座支撑方案
- Confirmed: 主镜自带镜座，由两个八角环直接套合；桁架杆直接安装到八角环，不设独立主镜箱
- Updated: 参数表新增 H-13；项目概览、需求页、README、命名规范和模块清单同步区分当前结构与历史 MirrorBox 文件名
- Scope: 仅修订文档和参数状态，未重命名目录或修改 FCStd

## [2026-11-06] revise | 闭合圆用直径、未闭合圆弧用半径
- Rule: 闭合圆、圆环、圆孔和圆杆以直径表示，模型所需半径按 `r=d/2` 派生；未闭合圆弧直接用半径表示
- Updated: 八角环旧候选改为 `bjh_d=237.5`、`bjh_r=118.75`（派生）；弧臂支承内缘保持 `arm_support_r=245`（R245），两者仍待定
- Confirmed: 主镜座圆环外径 193.5 mm 标记为当前唯一实物实测尺寸；其他标称或设计确认值不冒充实测值

## [2026-11-06] revise | CNC 三档误差假设与镜座固定容错
- Confirmed: CNC 误差目标 ≤1 mm；按 1/2/3 mm 三档假设进行容错设计，2/3 mm 不视为加工目标
- Added: M-02～M-06，分离加工误差、最小装入间隙、套合孔直径和孔切大后的单边空间；三档开孔候选为 Ø195.5/196.5/197.5 mm
- Confirmed: 镜座已有定位螺丝孔，孔偏大时可用于固定；孔位、规格、数量和螺纹待实测

## [2026-11-06] revise | CNC 整板一次走刀与连接桥交付约束
- Confirmed: CNC 一次走刀、整板雕刻；大件切透后可脱落，小件通过连接桥连接且不得掉落
- Added: M-07～M-10；连接桥的宽度、厚度、数量和位置留作后续待定参数
- Delivery: CNC 图纸必须体现整板排版、一次走刀和小件连接桥，不能只交付独立零件轮廓

## [2026-11-06] ingest | 手工装配间隙与过孔规则
- Confirmed: M-11～M-14；普通手工装配默认单边间隙 0.5 mm，并按固定、频繁拆装、受潮／涂层等工况分档
- Added: 16 mm 木板榫槽宽度派生规则及 M4/M5/M6/M8 普通过孔候选
- Rule: 间隙只负责装入，不承担定位；实际板厚与 CNC 误差通过试切校核

## [2026-11-06] create | 望远镜实施计划与跨会话进度跟踪
- Created: `docs/telescope-implementation-plan.md`，按需求基准、三条总体设计线、接口冻结、高风险验证、模块细化、总装交付划分任务
- Status: T00 已完成；T01 实物接口测量与 T02 总体基准定义为可并行开始的下一任务，其余未开始
- Rule: 每次工作更新任务状态、最近更新日期和进展日志；暂停、待验证与阻塞均保留真实状态

## [2026-11-06] create | T01 原始输入采集清单
- Created: `docs/measurement-log.md`，按 P0/P1/P2 列出主镜与镜座、副镜、调焦、铝杆和附件的测量项
- Added: 测量起止面、来源、工具、照片和无法测量原因记录栏；明确光学表面保护与禁止猜值
- Status: T01 改为“进行中”，当前等待分批实测；T02 可并行开展

## [2026-11-06] revise | docs 文件名统一为日期前缀加中文名称
- Renamed: 参数表、实施计划、原始输入清单和既有光学方案统一采用 `YYYY-MM-DD_中文名称.md`
- Updated: AGENTS、wiki 索引及活动文档内部链接同步到新文件名；raw 中的历史来源路径保持不变
- Rule: 日期表示创建日期，后续内容修改不反复更改前缀；目录占位文件例外

## [2026-11-06] create | TODO 用户手工事项统一入口
- Created: `TODO/2026-11-06_用户待办.md`，集中提供需要用户测量、采购、试装和确认事项的入口
- Moved: T01 原始输入采集清单由 docs 移至 TODO；实施计划继续跟踪项目状态，TODO 只承载用户操作
- Updated: AGENTS、wiki 索引、实施计划和清单内部链接已同步

## [2026-11-06] remove | 删除 README.md
- Removed: 根目录 `README.md`——项目转为面向 AI 助手开发，入口由 `AGENTS.md` + `wiki/index.md` 承担
- Moved: README 中的五金件采购清单并入 `TODO/2026-11-06_用户待办.md`
- Note: README 原文快照留存于 `raw/project/2026-11-06_strock6自述文件.md`，各 wiki 文章的 raw 溯源链接不受影响

## [2026-11-06] remove | docs 移除已编译的光学方案原文
- Removed: `docs/2026-11-06_160mm牛反望远镜光学合焦与调焦座设计参数方案.md`——内容与 `raw/optics/2026-11-06_160mm牛反光学合焦与调焦座设计方案.md` 快照逐字一致，已编译为 [光学合焦与调焦座参数](optics/光学合焦与调焦座参数.md)，数值已入参数表 O-01～O-11
- Note: raw 快照与 wiki 文章的溯源链不受影响；`docs/` 保留运行态真值（参数表、实施计划）

## [2026-11-06] rename | wiki 与 raw 文件名中文化
- Renamed: raw/ 6 份快照改为 `YYYY-MM-DD_中文名称.md`（与 docs 一致），wiki/ 7 篇文章改为 `中文名称.md`
- Kept: `wiki/index.md`、`wiki/log.md` 为知识库技能约定的结构入口，保持原名
- Updated: 全部 front-matter 溯源链接、See Also、wiki 索引、TODO/docs/AGENTS 引用已同步；raw 文件内容未动
- Rule: AGENTS 命名约定已扩展至 raw/ 与 wiki/ 文章

## [2026-11-06] create | 项目技能 freecad-modeling
- Created: `.agents/skills/freecad-modeling/SKILL.md`——从本指南与 AGENTS 蒸馏的建模强制操作规范（参数三层制、结构边界、文档组织、骨架/TNP/Sketcher 规则、验证闭环、CNC 交付约束）
- Updated: 本指南顶部与 See Also 增加技能指引；AGENTS 同步登记
- Rule: 本页 = 方法论知识（为什么），技能 = 操作指令（必须怎么做）；修改建模规范时两处同步

## [2026-11-06] revise | 技能去除与 AGENTS 重复的开工前必读节
- Updated: `freecad-modeling`——删除"开工前必读（强制顺序）"整节（阅读顺序与参数状态纪律已在 AGENTS.md「每次开始工作」「参数与状态纪律」规定，会话开场已执行）；数值来源一句话并入参数三层制开头，章节重排为 1～6
- Rule: 技能只写建模专属操作指令，与 AGENTS.md 不重复维护

## [2026-11-06] rename | 技能 strock6-freecad-modeling → freecad-modeling
- Renamed: 技能目录与 `name` 字段去除项目前缀，为跨项目复用与将来升为用户级技能做准备
- Updated: description 改为项目中立表述；新增复用说明（〔项目特定〕章节跨项目复用时整体替换）；AGENTS、wiki 索引与指南引用同步

## [2026-11-06] rename | 02_MirrorBox → 02_PrimarySupport
- Renamed: 目录 `02_MirrorBox/` → `02_PrimarySupport/`，`MirrorBoxAssembly.FCStd` → `PrimarySupportAssembly.FCStd`，文档 Label 同步内改
- Verified: 模块间无互相引用；全部 XLink 仅指向 `interfaces/` 且相对路径深度不变、无需重连；FCStd zip 完整性校验通过、0 残留旧名
- Updated: 项目概览、模块与文档清单、命名与文档规范、接口契约层、AGENTS、freecad-modeling 技能同步
- Note: raw 快照与历史 log 条目中的旧名按惯例保留作历史记录

## [2026-11-06] revise | 参数表列结构拆分与参数英文名直白化
- Restructured: 参数表“参数”列拆为「英文名」「中文名」两列；备注扩充为完整说明（定义、公式、上下游关系、历史值与待办）
- Renamed: 英文参数名统一为小写下划线全词，去除拼音（bjh→oct_ring）和晦涩缩写（S_prim_to_sec→primary_to_sec_dist、ring_pitch→top_bottom_ring_dist、tab_geometry→link_bridge_params 等约 40 项，旧名保留在备注中）；参数 ID 全部稳定不变
- Rule: 新增命名规则条目（全词、固定后缀 _d/_od/_id/thick/gap，不用拼音和晦涩简写）
- Updated: AGENTS、freecad-modeling 技能、wiki 需求页和光学页的 `board_t`、`R_axis` 等引用同步为新名；契约层 if_* 名称本次未动

## [2026-11-06] revise | 参数表引入工程默认状态
- Added: `工程默认` 状态定义（实测/审核前的工作值，仅推进设计，不作加工依据）；AGENTS 状态纪律同步
- Promoted: G-01／G-02／G-03／R-01／R-03／R-06／T-02／F-01／R-07 九项 待定/待实测 → 工程默认，打通 T02 骨架链
- Flagged: B-01 底座箱内净尺寸——契约层页记载 2026-11-04 用户确认与参数表 `待定` 标记冲突，待用户裁决
- Updated: 实施计划（T01 转暂缓、下一任务=T02）、TODO 用户待办同步
- Rule: 工程默认被实测/审核取代时显式改状态并记录依据

## [2026-11-06] revise | 参数组织原则：工艺量为基础输入，总体尺寸一律派生
- Added: 参数表与 AGENTS 写入原则——基础输入只设「实物实测尺寸＋用户可直观判断的工艺量（板厚、最小壁宽、间隙）」，抽象总体尺寸（环径、环距、箱体外廓）全部经派生链推出，不要求用户直接确认
- Reworked: R-01 八角环内切圆直径 工程默认 → 派生（= M-05 套合孔径 ＋ 2×R-09 孔到边最小宽度）；新增 R-09 `oct_ring_wall_min` = 20 mm 工程默认（用户可用手比划判断的量；旧值 237.5 反推恰为壁宽 20）
- Rule: 后续 G/T/F/B/A 各链在 T02 按同原则逐项改造成派生

## [2026-11-06] revise | 参数表新增「参数类型」列
- Added: 全部 79 行增加参数类型列——`基础`（直接设定：实测/决策/规则）67 项、`派生`（公式或引用计算）12 项（M-05、M-06、M-13、O-03、H-09、R-01、R-02、R-04、R-05、B-02、B-03、A-01）
- Rule: 类型与状态相互独立（如 R-02 派生＋已确认＝『引用 M-01』规则已确认）；填写规则已注明

## [2026-11-06] create | T02 总体基准与派生尺寸链（文字阶段）
- Created: `docs/2026-11-06_总体基准与派生尺寸链.md`，定义主镜顶点原点、Z 光轴、X 调焦轴、环功能面、杆端和俯仰轴基准
- Reworked: G/T/F/B/A 总体尺寸改为派生公式；光学间距 1073.25、杆连接面环距 1200、下环组中面 −25 mm；查明旧链 10 mm 为未分配杆长，−8 mm 为隐含环面偏移
- Pending: 底座箱内净由 T04 收纳排版派生，俯仰轴坐标和弧臂半径由 T05 计算；未伪造缺失数值
- Status: T02 保持进行中，待文字定义审阅后建立总体 FreeCAD 骨架；本轮未修改任何 FCStd
- Updated: 参数表、实施计划、wiki 索引、光学说明和 T01 PM-08 测量备注同步

## [2026-11-06] complete | T02 总体 FreeCAD 骨架
- Confirmed: 用户确认整机坐标系、功能基准和派生尺寸链文字定义
- Created: `00_TotalAssembly/TotalSkeleton.FCStd`，含原点/光轴、L0/LM/U0/UM/F0/FP、副镜中心、调焦轴、俯仰轴方向基准及完全约束主控草图；无制造零件或固体
- Contract: Interfaces 新增 T02 专用 XLink 派生项；旧模块别名保持原值，留待 T07 统一切换，避免意外改形历史零件
- Verified: FCStd 重新打开无错误；草图 0 自由度、无冲突/冗余；杆端闭合 1250 mm；杆插入 25→30、板厚 16→18 的内存回归通过且未保存
- Status: T02 已完成；后续 T03/T04/T05 可分别从光学、杆端包络和重心基准挂载

## [2026-11-06] complete | T03 光学尺寸链与四模态合焦检查
- Corrected: O-06=226.75 mm 是巴洛后光程，不能与主镜焦距直接相减；G-01 恢复为 1121 mm 工程默认，新增 O-43 固有焦平面 179 mm，骨架同步为 G-02=71 mm 并通过回归
- Reworked: 旧矩阵隐含设备偏移显式化为 O-19～O-22；目视延长筒改 40 mm、相机直插改 35 mm，四模式调焦高度 47.25/53/51/48.25 mm 均在行程内
- Checked: 35 mm 副镜短轴对 22.0308 mm 轴上光束有名义余量；全视场渐晕和实物合焦不冒充已验证
- Created: `docs/2026-11-06_光学尺寸链与四模态合焦检查.md`；参数表新增 O-18～O-43，wiki 和 FM-09～FM-13 测量提示同步
- Status: T03 已完成；T08d 保留实物试装，下一任务 T04

## [2026-11-06] complete | T04 机械包络、桁架长度链与收纳布局
- Created: `docs/2026-11-06_机械包络与收纳布局.md`，闭合环位置、杆端、杆孔边距和已知结构包络；已知轴向包络 1259 mm，上杆端外伸 9 mm
- Added: R-11/R-12 八角环外接圆与边长，T-06～T-10 杆孔和接口包络，B-06～B-09 装箱间隙与环组下界
- Storage: 2 mm 单边装箱间隙为工程默认；仅环组箱内下界 240.5×240.5×56 mm，旧箱宽 237.5 mm 少 3 mm，不再作为当前候选
- Boundary: 主副镜座、附件和底座件完整排版仍待实测；未虚构附件尺寸，未修改 FCStd
- Status: T04 已完成；下一任务 T05 质量、重心、俯仰轴和底座粗布局

## [2026-11-06] complete | T05 质量、重心、俯仰轴和底座粗布局
- Created: `docs/2026-11-06_质量重心与底座粗布局.md`；参数表新增 W-01～W-23 质量与底座估算链
- Estimated: 工作总质量 6.08293 kg（区间 4.756～7.710），Z 向重心 343.6223 mm，X 向重心 21.8275 mm；全部标明非实测
- Derived: 俯仰轴 Z=333.6223、天顶轴高 415.6223、弧臂 R177.9929、底座支承面下界 309.5×309.5 mm；静态投影余量 132.9225 mm
- Corrected: 弧臂半径改由环旋转包络＋径向余量派生，不再由地面高度反推
- Boundary: 1.3025 N·m 侧向不平衡、配重和抗倾覆留 T08e/T13；未修改 FCStd，下一任务 T06

## [2026-11-06] complete | T06 总体方案集成与候选比较
- Created: `docs/2026-11-06_总体方案集成与候选比较.md`，记录环壁宽 20/25/30、杆插入 20/25/30、俯仰下移 0/−10/−20 的单变量比较与取舍
- Integrated: TotalSkeleton 新增估算重心点，俯仰轴定位到 Z=333.6223 mm；契约新增质量、环几何和底座公式，旧模块别名不变
- Verified: 21 对象、无固体；草图完全约束；环壁宽 20→25 回归驱动质量/重心/俯仰轴/弧臂/底座全部正确，回归未保存
- Baseline: 保留 R-09=20、T-02=25、B-04=−10 工程默认，不作最终制造冻结
- Status: T06 已完成；下一任务 T07 首轮模块接口审核与冻结

## [2026-11-07] complete | T07 首轮模块接口审核与冻结
- Created: `docs/2026-11-07_首轮模块接口冻结.md`，明确镜座/环、杆/环、调焦/上环、俯仰/底座、收纳和未来扩展接口的责任参数与冻结等级
- Migration: 建立旧新契约别名迁移表；历史模块保持只读，T09～T13 逐项切换并回归，不在 T07 批量改形
- Verified: 5 份历史模块和 TotalSkeleton 相对 XLink 完整，FreeCAD 重开/recompute 均无对象错误；未保存修改
- Status: T07 已完成；工程默认项为条件冻结，下一任务 T08a CNC 试片

## [2026-11-07] prepare | T08a CNC 试片（待实切验证）
- Added: M-15 试切刀具 Ø6 mm 工程默认；M-09 增加试片桥宽 10、剩余厚 3、双桥工作值
- Created: `99_CommonParts/CNCTestCoupon.FCStd` 与 `exports/T08a_CNCTestCoupon.dxf`；300×220×16 mm 整板含杆孔、M42 孔、6 档槽和小件双桥
- Verified: 单一有效实体；DXF 重导入 64 实体，mm、1:1；FCStd 相对 XLink 和压缩包完整
- Created: `TODO/2026-11-07_CNC试片记录.md`，区分切透与桥位 13 mm 减薄，提供实测回填表
- Status: T08a 待验证；实切、测量和参数复核未完成，不标记完成

## [2026-11-07] prepare | T08b 主镜座套合与固定试验（待验证）
- Created: `99_CommonParts/MirrorCellFitRings.FCStd`、`exports/T08b_MirrorCellFitRings.dxf` 和 `TODO/2026-11-07_主镜座套合试验记录.md`
- Coverage: Ø195.5/196.5/197.5 三档套合孔，记录装入、端面定位、定位螺钉、防脱落和重复拆装
- Verified: 基准板单实体有效；DXF 重导入 55 实体，mm、1:1；外环释放轮廓仅作 CNC 刀路，不交付错误布尔结果
- Status: T08b 待验证，实物试验未完成

## [2026-11-07] prepare | T08c 桁架接头与重复定位试验（待验证）
- Created: `TODO/2026-11-07_桁架接头试验记录.md`，定义现有 T 接头与手拧夹紧两类候选的对比试验
- Coverage: 免工具、端面定位、预紧松动、10 次拆装、重复定位极差、上端 9 mm 操作空间和 1250 mm 杆端闭合
- Boundary: 鱼眼轴承／夹紧件未选型，不生成接头加工尺寸；无确认重复定位阈值，必须记录实测极差
- Status: T08c 待验证；未修改 FCStd

## [2026-11-07] prepare | T08d 四种调焦组合实物试装（待验证）
- Created: `TODO/2026-11-07_四模态合焦试装记录.md`，使用 T03 修正后的 40/15/0/35 mm 延长筒组合
- Coverage: 预测高度 47.25/53/51/48.25 mm，记录实际合焦高度、低/高端余量、接口与操作空间
- Boundary: 目镜/相机偏移仍需厂家或实测；巴洛未采购的 M2/M3 明确保持未验证
- Status: T08d 待验证；未修改 FCStd，下一任务 T08e

## [2026-11-07] prepare | T08e 重心与俯仰配重试验（待验证）
- Created: `TODO/2026-11-07_重心与俯仰配重试验记录.md`，将 T05 估算转为称重、三姿态漂移、配重和摩擦实测
- Safety: 先支撑再逐步释放，明显失衡不得放手；配重先可调临时固定，不侵入运动包络
- Boundary: 估算 6.08293 kg 和 1.3025 N·m 不是验收值；实测后回填 W/B/A 参数
- Status: T08e 待验证；未修改 FCStd

## [2026-11-07] design | T09 下环与主镜座支撑（待验证）
- Added: R-13 下层杆孔盲深 7 mm，T-11 下环 8 孔 45° 等分工作值；契约新增对应派生项
- Created: `02_PrimarySupport/LowerRing/` 下 LowerRingTop/Bottom 独立源件和 LowerRingAssembly；装配仅 App::Link
- Verified: 源件单实体有效，装配层间 2 mm、总厚 34 mm、下层背面余料 9 mm；重开/recompute、相对 XLink 和 FCStd 完整性通过
- Boundary: 镜座定位孔、防脱落和实际拆装待 T08b；T09 不标完成

## [2026-11-07] design | T10 桁架杆与接头（待验证）
- Created: `03_Truss/Members/TrussRod.FCStd` 和 `MembersAssembly.FCStd`；Ø12/Ø10×1250 mm 源件及 8 杆平行参考 Link 布置
- Generalized: G-03 改为由杆件中点长度和横向偏移开方派生；当前 q=0 时仍 1200 mm，最终斜杆不得沿用纯轴向公式
- Verified: 杆件与 8 Link 重开无错误，骨架完全约束；修复契约行覆盖底座参数的问题并恢复验证
- Status: T10 待验证；最终接头、预紧和三角化待 T08c

## [2026-11-07] design | T11 上环与调焦座安装（待验证）
- Created: `04_TopEnd/UpperRing/UpperRing.FCStd` 独立源件及 `docs/2026-11-07_上环与调焦座安装详细设计.md`
- Checked: 16 mm 单实体、中央孔与 8 杆孔、相对 XLink；上杆端外伸 9 mm
- Interface: F0 与中档环边仅差 0.5 mm，不得任意叠加 16 mm 外置板；FM-03/07 未测前不生成孔位或操作包络
- Status: T11 待验证；M42 和四模态公式保留，实际安装与合焦待 T08d

## [2026-11-07] design | T12 副镜座总成集成（待验证）
- Created: `docs/2026-11-07_副镜座总成集成设计.md`，闭合 S=1121、U0 间距 71 mm 和 35×49.4975 mm 椭圆包络
- Interface: 明确 SM-03～SM-08 的中心、偏心、叶片和调角输入；旧 M6×40 与 Ø17.5 斜杆仅作历史候选
- Boundary: 轴上通光通过不等于全视场或无干涉；调角行程和蜘蛛架包络未测，不生成虚构几何
- Status: T12 待验证；未修改 FCStd，下一任务 T13

## [2026-11-07] design | T13 俯仰轴承与底座（待验证）
- Added: A-09 弧臂毛坯径向宽度 50 mm 工程默认；契约新增对应项
- Created: `01_Base/AltitudeBearing/AltitudeArm.FCStd` 半环毛坯和 `01_Base/BasePlate.FCStd` 309.5 mm 支承板，均为独立单实体
- Boundary: 不含枢轴孔、减重孔、PTFE 支承、方位轴和配重座；静态投影不冒充抗倾覆验收
- Status: T13 待验证；下一任务 T14

## [2026-11-07] design | T14 附件与未来扩展接口（待验证）
- Created: `docs/2026-11-07_附件与未来扩展接口.md`，明确寻星、导星、遮光罩安装分区、附件收纳和 AM-01～03 输入
- Reserved: GoTo 仅保留方位/俯仰运动中心；赤道平台仅保留支承面下方接口，不生成未知孔位或电机尺寸
- Boundary: 附件质量、侧向重心、干涉和实际装箱待验证；本轮未修改 FCStd
- Status: T14 待验证；下一任务 T15 总装与回归准备

## [2026-11-07] design | T15 当前结构核心总装（待验证）
- Created: `00_TotalAssembly/TotalAssembly.FCStd` 与 `docs/2026-11-07_总装与参数回归验证.md`；14 个 App::Link，无总装内新实体
- Verified: 环/杆/底板/弧臂基准对齐；杆插入 25→30 回归正确，重开恢复基线，XLink/FCStd 完整
- Boundary: 最终副镜、调焦、接头、定位件和附件未纳入，不宣称完整干涉或运动验收
- Status: T15 待验证；下一任务 T16 CNC 排版与交付准备

## [2026-11-07] prepare | T16 CNC 整板排版与交付（待验证）
- Created: `99_CommonParts/CNCCurrentCoreLayout.FCStd` 及 exports 下 T16_RingBoard/ArmBoard/BasePlate.dxf
- Coverage: 三环板 789.5×276.5、弧臂板 496×516、底板 309.5 方形；下层杆孔 7 mm 盲切单列，当前均为大件无需桥
- Verified: DXF 重导入分别 55/12/4 实体，mm、1:1；修复导出前 recompute 缺失导致的空 DXF 后重新生成
- Status: T16 待验证，非最终生产版；下一任务 T17 实物装配与观测验证准备

## [2026-11-07] prepare | T17 整机装配、观测验证与设计回写（待验证）
- Created: `TODO/2026-11-07_整机装配与观测验证记录.md`，覆盖实物装配、光轴、四模态观测、运动、拆解收纳和问题回写
- Boundary: 前置 T08/T09～T16 未关闭；不以模型准直或“能装上”替代实际观测
- Status: T17 待验证；所有剩余任务均需实物输入或试验才能最终关闭

## [2026-11-07] revise | 实物试验改为设计后整批加工验证
- Condition: 当前仅有主副镜、调焦座和 8 根桁架杆；试件、接头、五金、配重和附件均无现成实物
- Workflow: T08a～T08e 转“暂缓”，不再阻塞详细设计；T09～T16 继续用明确工程默认完成设计，T08/T17 在统一加工后集中验证与回写
- Naming: 用户已完成现有模型中文自描述 Label 与命名约束清理；本轮不修改 FCStd，不覆盖这些修改

## [2026-11-07] confirm | 桁架杆采用 4 组 M 型杆系
- Confirmed: 8 根桁架杆按 4 组 M 型杆系组装；参数表新增 T-14，H-05／T-12 和 T10 文档同步
- Boundary: 平行 MembersAssembly 仅为杆件／孔位参考，不是最终装配；M 型孔位、接头和空间长度链在 T10 详细设计中闭合
- Scope: 未修改 FCStd，不覆盖用户已完成的中文 Label 和命名约束清理

## [2026-11-07] design | T09 镜座三点压持与防脱落设计完成
- Added: R-14～R-17 镜座压持端面、3 个压持扣、Ø4.5 过孔和 60° 角向偏移；压持不依赖未知镜座定位孔
- Created: `MirrorCellRetainer.FCStd` L 形源件；上下环新增 3 点过孔，LowerRingAssembly 新增 3 个 Link
- Verified: 全部源件单实体有效，压持面回归正确，重开/XLink 无错误；实物夹紧与光学安全间隙待 T08b
- Status: T09 待验证；下一任务继续 T10 的 M 型杆系详细设计

## [2026-11-07] design | T10 M 型杆系参数化闭合
- Derived: 4 组上接头位于相邻下孔角向中点；接头双孔径向内缩 13、切向 ±9 mm；横向偏移 70.0866、环距 1197.9515、G-02=68.9515 mm
- Updated: MembersAssembly 与 TotalAssembly 杆件位置和旋转均由表达式驱动；UpperRing 8 个 M 型接头孔完全约束
- Verified: 每杆端点矢量 1250 mm，插入量 25→30 回归保持杆长并联动方向；重开无错误
- Synchronized: 总体基准、机械包络、质量重心、候选比较、接口、副镜和总装文档更新到当前 M 型数值
- Status: T10 待验证；接头实体、预紧与重复定位待整批加工后试验

## [2026-11-07] design | T11 插槽定位调焦安装板完成
- Added: F-06～F-10 安装板 60×180、30 mm 调节槽、50 mm 槽距与 M4 槽宽；F0 光学基准不被板厚外推
- Created: `FocuserMountPlate.FCStd` 独立源件；UpperRing 新增表达式驱动插槽，M42 盲孔 10 mm
- Verified: 两件单实体有效，插槽完全约束，板厚回归正确，重开/XLink/中文 Label 通过
- Status: T11 待验证；实际孔位、手轮、接头和四模态空间待整批加工后试装

## [2026-11-07] design | T12 副镜座与当前总装静态干涉闭合
- Integrated: 复用 SecondaryAssembly 的环与光学子装配，经右手坐标旋转变换接入 TotalAssembly；加入 T11 调焦安装板，总计 17 个 Link
- Derived: S-03 杆／副镜环间隙 1.5 mm 驱动 T-15 径向内缩 4 mm；当前环距 1197.7772、G-02=68.7772 mm
- Verified: 副镜环／光学件与上环、调焦板、8 根 M 杆布尔交集全为 0；插入回归后仍为 0；重开无错误
- Status: T12 待验证；调角、光轴复位、附件和观测待整批加工后验证

## [2026-11-07] revise | 建立参数正向发布与逆向回收流程
- Workflow: 正向发布从用户确认并更新 docs 参数表开始，经用户要求后由 AI 回写契约和模型；逆向回收允许模型 Sheet 试参，经差异审查和用户确认后再进入全局基线
- Constraint: 实验值不自动覆盖全局；派生结果不独立回收；并发冲突交用户裁决；模型验证通过不自动升级为已确认
- Synchronized: `AGENTS.md`、项目 `freecad-modeling` 技能与方法论指南已同步；本轮未修改参数数值或 FCStd

## [2026-11-07] design | T13 俯仰支承与底座结构闭合
- Created: 带轮毂/腹板和 Ø9 枢轴孔的 AltitudeArm、RockerSidePanel、PTFESupportBlock；底板更新为 341.5 mm 方形
- Corrected: 环→侧隙→弧臂→摇架侧板实际叠放；摇架外廓 301.5 mm，重心投影余量 148.9225 mm；侧板高=轴高+20 mm
- Verified: 源件单实体、轮毂连续、枢轴联动、总装 19 Link、中文 Label；底板与带轮毂弧臂 DXF 已同步重导入验证
- Status: T13 待验证；支承位置、方位、配重和抗倾覆待整批加工后试验

## [2026-11-07] design | T14 通用附件板与遮光罩展开完成
- Added: E-01～E-07 定义 2 件 80×40×16 mm 附件板、双 4.5×30 mm 调节槽、50 mm 搭接与 120 mm 罩高；展开长 833.6921 mm
- Created: `04_TopEnd/Accessories/AccessoryMount.FCStd`、`LightShadeStrip.FCStd` 及两份 T14 DXF；对象 Label 均为自描述中文
- Verified: 附件板 DXF 重导入 12 实体，遮光罩 5 线（含搭接线）；mm、1:1，无不支持实体
- Boundary: 附件板进入 CNC 整板时须按 M-09 加连接桥；柔性罩不套用木板厚度，实际设备、扣件、材料、干涉和收纳仍待验证
- Status: T14 待验证；下一任务 T15 总装与回归闭合

## [2026-11-07] verify | T15 总装补入压持扣并修正杆件干涉
- Integrated: TotalAssembly 新增 3 个镜座压持扣 Link，总计 22 Link；所有对象保持中文自描述 Label
- Corrected: 旧 60° 方案与 M 杆相交；R-17 改为 15°，压持扣位于 15°/135°/255°，上下环固定孔与 Link 共用公式并补齐草图全约束
- Verified: 三件至 8 杆最小名义间隙约 9.80 mm，压持扣与双环/8 杆布尔交集为 0；端面 0→2 mm、杆插入 25→30 mm 回归通过，重开恢复基线
- Boundary: 接头、附件设备、支承接触和完整运动验收未关闭；R-17 环孔变化须在 T16 重导出环板 DXF
- Status: T15 待验证；下一任务 T16 生产图同步

## [2026-11-07] manufacture | T16 当前设计板件整板排版扩展
- Updated: 环板加入 6 个 R-17 压持扣固定孔和上环调焦板插槽；弧臂、底板保持当前已验证轮廓
- Created: 新增摇架侧板整板与调焦/附件小件整板；后者含 1 调焦板、2 附件板、3 压持扣，共 6 件双桥小件
- Process: 压持扣拉伸厚度统一为 16 mm；侧形切出后垂直钻 Ø4.5 固定孔；M42 盲切 10 mm、桥位切深 13 mm 保留 3 mm
- Verified: 5 份 DXF 重导入 65/30/4/14/107 实体，mm、1:1，无不支持实体；排版重算与中文 Label 通过
- Status: T16 待验证；接头、底座箱和实切复核未关闭，不作为无条件最终加工放行

## [2026-11-07] design | T10 完整杆端矢量与斜杆槽修正
- Corrected: G-03 改为由 1250 mm 完整杆端矢量开方并扣除插入量；当前环距 1197.8662 mm，消除旧链约 0.089 mm 误差
- Derived: T-17～T-20；杆倾角 3.3482°，贯穿槽 13.1569×12.2209 mm，盲槽 12.6509×12.2209 mm、盲深 7.3504 mm
- Fixed: 24 个槽分别使用独立全约束草图和 Pocket；修正旧 Pocket 方向、盲槽杆端补偿及后建特征深度表达式
- Verified: 8 杆长度均 1250 mm，与三层环板布尔干涉为 0；插入 25→30 mm 回归通过；环板 DXF 重导入 137 实体
- Boundary: 杆槽只负责装入，免工具夹紧接头仍未完成；T10/T16 保持待验证

## [2026-11-07] design | T10 双杆节点与免工具夹块闭合
- Corrected: 下节点双杆按相反符号切向错位 9 mm，消除共点管体重叠；杆位置与旋转使用同一端点公式
- Created: 上/下双杆夹块源件各一，实际共 8 件 24×44×16 mm，配 16 个 M4 手拧螺钉；上夹块盲槽深 9.3110 mm
- Verified: 杆长、杆杆、杆环、夹块与杆/环/副镜/调焦板/压持扣干涉均为 0；25→30 mm 回归通过；总装 30 Link
- Updated: 压持扣改为 50°/155°/305°，最小杆及夹块间隙约 11.16 mm；新增夹块整板 DXF，重导入 228 实体
- Status: T10 待实物夹持和重复定位验证；T16 新增夹块整板，底座箱仍待设计

## [2026-11-07] maintenance | 模型默认可见性与批量处理工具
- Changed: 现行及测试共 38 份 FCStd 默认显示零件 Body、最终特征和装配 App::Link；非最终草图、基准和中间特征隐藏，骨架与 CNC 排版草图除外
- Tool: 新增 `src/tools/freecad_set_default_visibility.py`，在 FreeCAD GUI 中批量保存并逐份重开验证；包含完整载入检查、几何签名、实体、草图、链接及 GuiDocument 检查
- Verified: GUI 抽检 BasePlate、PrimarySupportAssembly、TotalAssembly 无隐藏零件；38 份 ZIP／GuiDocument 完整，Body／Link 可见性检查通过
- Synchronized: `AGENTS.md`、项目建模技能、方法论指南与 `cad/README.md` 已同步默认可见性规则；不改变设计参数和阶段任务状态

## [2026-11-07] fix | 隐藏装配链接源件的 Origin 基准
- Cause: `PartDesign::Body.Group` 不包含 `Origin`，仅遍历 Body.Group 会漏掉原点、XYZ 基准轴和基准面
- Updated: `src/tools/freecad_set_default_visibility.py` 已显式隐藏 `App::Origin` 及 `OriginFeatures`，并重新保存全部 38 份现行及测试模型
- Verified: TotalAssembly 重开后无可见 Origin、无隐藏零件；全部 FCStd 的基准隐藏、Body／Link 显示、ZIP 与 GuiDocument 检查通过

## [2026-11-14] prototype | 下环外置单夹块与向边中点收拢斜孔
- Checked: 既有 OctBaseB 孔轴基本仅在径向竖直平面内倾斜，缺少朝向所在边中点的切向分量；通过 MCP 只读检查现行模型，未修改既有 FCStd 或契约
- Derived: 参数表新增 T-30～T-34；按 25 mm 下孔距、当前上端 ±9 mm 错位和 4.5 mm 径向内缩、1250 mm 杆长计算，总倾角 4.088852°，径向／切向分量分别 1.818877°／3.664478°
- Created: `cad/02_PrimarySupport/Parts/LowerRingClampPrototype.FCStd` 与 `src/freecad/lower_ring_clamp_prototype.py`；同一文档含八角环和 25×20×16 mm 夹块两个 Body，4 个缺口、8 个环孔及 2 个同轴夹块槽
- Geometry: 原 20 mm 环壁不能直接再切 20 mm 深缺口，故将缺口放在原实际外轮廓之外新增区域，保留连续环壁；两孔圆心位于夹块靠环体长边两端
- Verified: MCP GUI 保存重开和独立 freecadcmd 重算通过；两 Body 单一有效实体，10 个槽均实际去料，方向点积 1、孔心误差 0、孔距 25 mm、环块重叠 0；草图全约束且无冲突／冗余，孔深 25→26→25 mm 回归恢复，ZIP／GuiDocument 完整
- Status: T09／T10／T08c 保持待验证；夹紧开口、紧固件、实物夹持和重复定位未关闭。`pytest tests/` 因环境未安装 pytest 无法执行，不记为测试通过


## [2026-11-15] inspect | 主镜座总成只读干涉检查与防尘盖建议
- Checked: 用户修改后的 PrimarySupportAssembly 含 11 个实体 Link；55 组两两检查无体积干涉，GUI 与独立 freecadcmd 磁盘重开均为有效实体，无无效对象；未修改或保存模型
- Dimensions: 上环／镜座径向单边间隙 2 mm；光学面最高点至上环顶面约 3.7728 mm；支撑板高 48 mm；底托对镜座名义径向承托宽度 3 mm
- Boundary: 支撑板实际紧固／胶合和镜座真实底面接触需核实；CLI 有 TopoShapeExpansion hasher mismatch 警告但本轮实体检查通过；实物调角螺钉最高点未纳入现有模型
- Cover: 推荐上环顶面承托的轻量浅盖，不调整上环内孔或支撑板高度；Ø220 mm 为候选而非确认参数，额外净高由盖子隆起或垫圈解决
- Status: T09 保持待验证；盖子正式尺寸待实物最高点和连接结构测量

- Decision: M-16 确认普通 M4 孔不进入 CNC 模型／DXF，到货后按实物手工钻孔；辅助定位孔为例外。既有模型和历史 DXF 未自动清理，T16 生产输出时执行
- Decision: R-19／R-20 确认底托内孔 Ø173.5 mm，镜座径向承托宽度 10 mm，主镜口径外径向余量 6.75 mm；未修改模型
- Decision: E-12 选定完整八角薄板防尘盖＋磁吸防滑，覆盖环面、夹块与杆孔；不改上环内孔或支撑板高度。磁铁防脱、板厚和中央刚度待设计验证

- Cover revision: 圆形浅沉台候选的 5 mm 径向托边可保留同一 CNC 刀具，但 5 mm 深沉台＋5 mm 齐平薄盖会使盖底低于当前光学面最高点约 1.2272 mm；E-12 转为圆形薄盖待定，沉台深度待实物净高校核，未修改模型

- Model: R-21 确认支撑板高度50 mm；OctBaseB 高度约束已修改并命名，PrimarySupportAssembly 上环与夹块联动抬高2 mm。磁盘重开、55组干涉、上下接触和实体检查通过；5 mm齐平沉台的镜面名义余量0.7728 mm。T09待验证，pytest环境仍不可用

- Clarified: 防尘盖名义链60／50／16 mm对应沉台前6 mm、5 mm沉台后1 mm；球面模型60.2272 mm对应5.7728／0.7728 mm，结论一致，未修改模型

- Fix: TotalAssembly 磁盘保存版已移除错误嵌套的 Dob底座 AssemblyLink，Group 10→9；无关节或爆炸图直接依赖，源 DobAssembly 未改。独立重开无残留或无效对象；旧GUI进程未强制结束，卡死会话未保存改动不在离线结果中
