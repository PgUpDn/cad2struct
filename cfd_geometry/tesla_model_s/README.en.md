# Tesla Model S — CFD Geometry

[中文](README.md) | **English**

Two sources, same coordinate system (both derive from the same public Model S model; vehicle length 4.97 m, width 2.166 m):

- x axis: nose at x≈0.013, tail at x≈4.98, **freestream direction is +x**
- y axis: y=0 is the symmetry plane
- z axis points up
- Units: **meters** (all STLs have been converted to meters)

| Subdirectory | Source | License | Solver |
|---|---|---|---|
| [`polimi_openfoam/`](polimi_openfoam) | [alejandro-rivera-miguez/CFD-analysis-of-Tesla-Model-S-Rear-Wing-Attachment-Aerodynamics](https://github.com/alejandro-rivera-miguez/CFD-analysis-of-Tesla-Model-S-Rear-Wing-Attachment-Aerodynamics) | MIT | OpenFOAM (ESI), simpleFoam + k-ω SST |
| [`fluent_spoiler/`](fluent_spoiler) | [MohamedSamer1/tesla-model-s-spoiler-cfd-analysis](https://github.com/MohamedSamer1/tesla-model-s-spoiler-cfd-analysis) | MIT | ANSYS Fluent, standard k-ε |

---

## A. `polimi_openfoam/` — with wheels, baseline + 4 rear-wing configurations (ready to run in OpenFOAM)

The original files are ASCII STLs exported from CATIA, packed in `Geometry.rar`. They have been extracted here and converted to binary STL (about 1/4 of the original size, geometry unchanged).

| File | Configuration | Triangles | Shells | Notes |
|---|---|---:|---:|---|
| `stl/baseline.stl` | Baseline | 203,204 | 1 | Wheels included; tires penetrate 14 mm into the ground (z_min = −0.014) |
| `stl/rearwing_standard_pylons.stl` | Rear wing + standard pylons | 212,806 | 2 | |
| `stl/rearwing_swan_neck.stl` | Rear wing + swan-neck mounts | 212,754 | 4 | |
| `stl/rearwing_swan_neck_back.stl` | Rear wing + rearward-extended swan-neck mounts | 212,450 | 4 | Mounts extend past the tail, x_max = 5.045 |
| `stl/rearwing_floating_no_mounts.stl` | Floating rear wing, no mounts | 211,810 | 2 | Original file was in **mm**; scaled by 0.001 to m |

| baseline | standard_pylons | swan_neck | swan_neck_back | floating_no_mounts |
|---|---|---|---|---|
| ![](previews/baseline.png) | ![](previews/rearwing_standard_pylons.png) | ![](previews/rearwing_swan_neck.png) | ![](previews/rearwing_swan_neck_back.png) | ![](previews/rearwing_floating_no_mounts.png) |

All files are watertight with consistent normals. The rear wing and mounts are separate closed shells that intersect the body; snappyHexMesh handles them directly.

### Running

`openfoam_case/` is the `Simulation_setup/` directory of the original repository. The outdated `0.orig/` (a leftover from the motorBike tutorial that does not match this case) was removed, and an `Allrun` script was added:

```bash
cd polimi_openfoam/openfoam_case
./Allrun rearwing_swan_neck 8     # variant name = file name under stl/; 8 = number of cores
./Allclean                        # clean up (also removes constant/triSurface)
```

`Allrun` copies the selected STL to `constant/triSurface/TeslaModelS_RearWing_front.stl` (this name is hard-coded in all dictionaries), then runs blockMesh → surfaceFeatureExtract → parallel snappyHexMesh → checkMesh → parallel simpleFoam.

Case setup: half-car model (y ∈ [0, 4] m, y=0 is a symmetryPlane); domain x ∈ [−15, 40] m, z ∈ [0, 7] m; U∞ = 55 m/s; ground is fixedValue U=U∞ (moving ground); k-ω SST; 1500 iterations in total.

**Tested**: `./Allrun rearwing_swan_neck 4` was run with OpenFOAM v1912 (for this test only, the decomposition method was switched to `simple`, because the Debian v1912 package does not ship scotch). snappyHexMesh reported "Finished meshing without any errors" and produced 5.12 million cells (including 5 prism layers), taking about 40 minutes on 4 cores. checkMesh flagged only 29 highly skewed faces (max skewness 6.75). simpleFoam ran for 3 iterations with residuals decreasing normally. The dictionary headers state **v2406**; under v1912 the `forceCoeffs` function object fails, so the case only runs with `-noFunctionObjects`. v2406 or later is recommended.

> ⚠️ `Aref 2.2` in `system/forceCoeffs` corresponds to the full-car frontal area (the measured projection of `baseline.stl` is about 2.37 m²), but the domain covers only half the car and therefore only half the force, so the reported Cd/Cl are about half the true values. Either set Aref to the half-car area (1.1 from the author's estimate; about 1.18 m² measured) or multiply the results by 2.

---

## B. `fluent_spoiler/` — body without wheels + spoiler

| File | Notes |
|---|---|
| `step/tesla_model_s_base.stp` | Original STEP (exported from Autodesk, single solid, mm). **No wheels**; the wheel arches are simply closed off, and the underbody sits 154 mm above z=0. |
| `step/rear_spoiler_part.step` | SolidWorks spoiler part, **in its own local coordinate system, not assembled onto the car**. Span 2.855 m, wider than the car. The original author scaled and positioned it in SpaceClaim (`.scdocx`) and did not export an assembled STEP. |
| `stl/baseline_from_step.stl` | Triangulated from the STEP above with gmsh (304,720 faces, m, watertight). **The best no-wing geometry for remeshing.** |
| `stl/with_spoiler_fluent_surface.stl` | Extracted from the `car` wall of the Fluent mesh `car-with-spoiler/FFF.msh.h5`: originally a half car, mirrored into a full car and translated back to the STEP coordinate system (96,242 faces, watertight). **This is the only geometry with the spoiler in its installed position**, i.e. the shape Fluent actually computed. Accuracy is limited by the Fluent surface mesh. |
| `stl/baseline_fluent_surface.stl` | Same as above, from the no-wing mesh `FFF 1.msh.h5` (89,518 faces). |
| `stl/rear_spoiler_part_from_step.stl` | Triangulation of the spoiler part (local coordinate system, not positioned). |

| baseline_from_step | with_spoiler_fluent_surface |
|---|---|
| ![](previews/baseline_from_step.png) | ![](previews/with_spoiler_fluent_surface.png) |

Original Fluent setup: half-car symmetry model, velocity inlet / pressure outlet, stationary ground at z = −0.046 m (in the STEP coordinate system), pressure-based steady solver, standard k-ε, SIMPLE algorithm. There are no ready-made OpenFOAM dictionaries for these geometries. The `openfoam_case` from section A can be reused directly: just copy the STL to `constant/triSurface/TeslaModelS_RearWing_front.stl`. Note that this car has no wheels and is suspended above the ground.

The Fluent `.cas.h5` / `.dat.h5` / `.msh.h5` files in the original repository are large (about 100 MB) and were not copied here; download them from the original repository if needed.
