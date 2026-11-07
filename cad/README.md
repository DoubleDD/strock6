# FreeCAD 模型目录

`cad/` 只保存正式产品模型和跨模块契约。测试专用模型位于 `tests/fixtures/cad/`，自动备份位于项目根目录 `backup/`。

## 组织规则

- `00_TotalAssembly/`：总体骨架与整机总装；总装只链接各模块，不绘制新的制造零件。
- `01_Dob/`～`06_GoTo/`：功能模块。模块装配放模块根部，专属零件放 `Parts/`，下一级总成放 `SubAssemblies/`，TechDraw 源文件放 `Drawings/`。
- `90_CommonParts/Standard/`：螺栓、螺母、轴承等标准件。
- `90_CommonParts/SharedParts/`：被多个模块复用的自制通用件。
- `91_Interfaces/Interfaces.FCStd`：跨模块尺寸契约，不属于普通公共件。

一个零件一份 FCStd 文件；装配通过 App::Link 引用源件。现有 FCStd 文件名和内部对象 Name 不因目录整理而改变。没有实际文件的可选目录无需提前创建。

## 引用与修改

跨模块尺寸必须通过 `91_Interfaces/Interfaces.FCStd` 分发。移动文件或调整层级后，必须同步处理 App::Link、XLink、文档和脚本路径，并重新执行模型回归。

## 默认可见性

模型默认显示所有零件 Body、最终特征和装配 `App::Link`；非最终草图、基准和中间特征保持隐藏，骨架与 CNC 排版等草图交付物除外。批量修正工具为 `src/tools/freecad_set_default_visibility.py`，须在 FreeCAD GUI 中运行，并通过保存后重开检查 `GuiDocument.xml` 和实际视图状态。

具体参数纪律、建模规则和验证要求见根目录 `AGENTS.md` 与 `.agents/skills/freecad-modeling/SKILL.md`。
