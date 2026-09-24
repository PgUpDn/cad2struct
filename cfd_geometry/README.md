# 可直接跑 CFD 的车辆几何（按车型整理）

**中文** | [English](README.en.md)

从三个公开仓库中提取出能直接用于外流场 CFD 的几何，并按车型归类。所有 STL（包括 STEP 的三角化结果）都用 `tools/stlcheck.py` 检查过：全部水密（watertight）、法向一致，单位统一为**米**。

## 预览

![几何预览：7 种 Model S 配置 + 4 种 Cybertruck 配置](previews/overview.png)

**Tesla Model S**

| 原车 | 尾翼 + 标准立柱 | 尾翼 + 鹅颈吊挂 | 尾翼 + 后伸鹅颈吊挂 |
|---|---|---|---|
| ![](tesla_model_s/previews/baseline.png) | ![](tesla_model_s/previews/rearwing_standard_pylons.png) | ![](tesla_model_s/previews/rearwing_swan_neck.png) | ![](tesla_model_s/previews/rearwing_swan_neck_back.png) |
| **悬浮尾翼（无支架）** | **STEP 车身（无车轮）** | **Fluent 面网格：车身 + 扰流板** | |
| ![](tesla_model_s/previews/rearwing_floating_no_mounts.png) | ![](tesla_model_s/previews/baseline_from_step.png) | ![](tesla_model_s/previews/with_spoiler_fluent_surface.png) | |

**Tesla Cybertruck**

| 标准（货箱盖关闭） | 货箱敞开 | 车顶行李架 | 车顶行李箱 |
|---|---|---|---|
| ![](tesla_cybertruck/previews/standard_closed_bed.png) | ![](tesla_cybertruck/previews/open_bed.png) | ![](tesla_cybertruck/previews/roof_rack.png) | ![](tesla_cybertruck/previews/roof_carrier_box.png) |

预览图由 `tools/render_previews.py` 生成，统一从 −y 一侧的后上方看。Cybertruck 是半车模型，车轮只有 −y 一侧。

## 目录结构

```
cfd_geometry/
├── previews/overview.png           # 全部配置的预览拼图
├── tesla_model_s/
│   ├── polimi_openfoam/            # 来源①  MIT   带车轮，原车 + 4 种尾翼配置，OpenFOAM 算例
│   │   ├── stl/                    #   5 个 STL
│   │   └── openfoam_case/          #   blockMesh/snappy/simpleFoam 字典 + Allrun
│   └── fluent_spoiler/             # 来源②  MIT   无车轮车身 + 扰流板
│       ├── step/                   #   原始 STEP（重新划网格首选）
│       └── stl/                    #   STEP 三角化结果，以及从 Fluent 网格提取的壁面
└── tesla_cybertruck/               # 来源③  ⚠️ 无许可声明
    ├── standard_closed_bed/        #   每个目录都是完整的 OpenFOAM 12 算例
    ├── open_bed/
    ├── roof_rack/
    ├── roof_carrier_box/
    └── postprocessing/
```

## 总表

| 车型 | 配置 | 几何文件 | 格式 | 三角面 | 车轮 | 现成求解设置 |
|---|---|---|---|---:|---|---|
| **Model S** | 原车 | `tesla_model_s/polimi_openfoam/stl/baseline.stl` | STL | 203 k | ✅ | OpenFOAM (ESI) |
| | 尾翼 + 标准立柱 | `…/stl/rearwing_standard_pylons.stl` | STL | 213 k | ✅ | OpenFOAM (ESI) |
| | 尾翼 + 鹅颈吊挂 | `…/stl/rearwing_swan_neck.stl` | STL | 213 k | ✅ | OpenFOAM (ESI) |
| | 尾翼 + 后伸鹅颈吊挂 | `…/stl/rearwing_swan_neck_back.stl` | STL | 212 k | ✅ | OpenFOAM (ESI) |
| | 悬浮尾翼（无支架） | `…/stl/rearwing_floating_no_mounts.stl` | STL | 212 k | ✅ | OpenFOAM (ESI) |
| **Model S** | 原车（CAD） | `tesla_model_s/fluent_spoiler/step/tesla_model_s_base.stp` | STEP | — | ❌ | Fluent（仅在原仓库） |
| | 原车 | `…/stl/baseline_from_step.stl` | STL | 305 k | ❌ | — |
| | 带扰流板（已定位） | `…/stl/with_spoiler_fluent_surface.stl` | STL | 96 k | ❌ | — |
| | 原车（Fluent 面网格） | `…/stl/baseline_fluent_surface.stl` | STL | 90 k | ❌ | — |
| | 扰流板零件（未定位） | `…/step/rear_spoiler_part.step` | STEP | — | — | — |
| **Cybertruck** | 标准（货箱盖关闭） | `tesla_cybertruck/standard_closed_bed/constant/triSurface/` | STL | 1.1 k + 轮 | ✅ | OpenFOAM 12，MRF 旋转轮 |
| | 货箱敞开 | `tesla_cybertruck/open_bed/constant/triSurface/` | STL | 1.1 k + 轮 | ✅ | OpenFOAM 12，MRF 旋转轮 |
| | 车顶行李架 | `tesla_cybertruck/roof_rack/constant/triSurface/` | STL | 46 k + 轮 | ✅ | OpenFOAM 12，MRF 旋转轮 |
| | 车顶行李箱 | `tesla_cybertruck/roof_carrier_box/constant/triSurface/` | STL | 57 k + 轮 | ✅ | OpenFOAM 12，MRF 旋转轮 |

各车型的坐标系、工况、运行方法和已知问题，见 [`tesla_model_s/README.md`](tesla_model_s/README.md) 和 [`tesla_cybertruck/README.md`](tesla_cybertruck/README.md)。

## 怎么选

- **要现成、带车轮、能一键跑的 Model S**：用 `polimi_openfoam/`，运行 `./Allrun <变体名>`。
- **要干净的 CAD 自己划网格（Fluent / STAR-CCM+ / OpenFOAM）**：用 `fluent_spoiler/step/tesla_model_s_base.stp`。注意这份几何没有车轮。
- **要带旋转车轮（MRF）的模型，或做配置对比**：用 Cybertruck 的四个算例。

## 来源与许可

| # | 仓库 | 许可 |
|---|---|---|
| ① | [alejandro-rivera-miguez/CFD-analysis-of-Tesla-Model-S-Rear-Wing-Attachment-Aerodynamics](https://github.com/alejandro-rivera-miguez/CFD-analysis-of-Tesla-Model-S-Rear-Wing-Attachment-Aerodynamics) | MIT（见 `tesla_model_s/polimi_openfoam/LICENSE`） |
| ② | [MohamedSamer1/tesla-model-s-spoiler-cfd-analysis](https://github.com/MohamedSamer1/tesla-model-s-spoiler-cfd-analysis) | MIT（见 `tesla_model_s/fluent_spoiler/LICENSE`） |
| ③ | [liukushk-a/cybertruckAerodynamics](https://github.com/liukushk-a/cybertruckAerodynamics) | **未声明**：公开发布或发表前请先联系作者 |

## 转换工具（`tools/`）

| 脚本 | 用途 |
|---|---|
| `stlcheck.py <stl…>` | 输出三角面数、是否水密、实体数和包围盒 |
| `step2stl.py <in.step> <out.stl> <hmax_m> [hmin_m]` | 用 gmsh 把 STEP 三角化成 STL（单位 mm → m） |
| `fluent2stl.py <mesh.msh.h5> <zone> <out.stl>` | 从 Fluent HDF5 网格中提取一个面区域，输出 STL |
| `render_previews.py` | 重新生成所有预览图和 `previews/overview.png`（无显示器时用 `xvfb-run -a python3 tools/render_previews.py`） |

依赖：`pip install trimesh numpy scipy h5py gmsh pyvista pillow`（gmsh 还需要系统库 `libglu1-mesa`；无显示器的机器渲染需要 `xvfb`）。
