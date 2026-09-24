# cad2struct

## CFD 车辆几何库

[`cfd_geometry/`](cfd_geometry/README.md)：从公开仓库中提取、可直接用于外流场 CFD 的车辆几何，按车型整理。

- **Tesla Model S**：带车轮的 5 种尾翼配置（OpenFOAM 算例），以及无车轮的 STEP 原始 CAD 和带扰流板的车身
- **Tesla Cybertruck**：4 种配置（标准 / 货箱敞开 / 行李架 / 行李箱），每种都是完整的 OpenFOAM 12 算例，带 MRF 旋转车轮

转换和检查脚本在 [`tools/`](tools/)。
