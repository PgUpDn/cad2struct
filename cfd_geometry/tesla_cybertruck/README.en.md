# Tesla Cybertruck — CFD Geometry (OpenFOAM 12, Four Configurations)

[中文](README.md) | **English**

Source: [liukushk-a/cybertruckAerodynamics](https://github.com/liukushk-a/cybertruckAerodynamics) (Politecnico di Milano student project)

> ⚠️ **The original repository has no license statement**, so all rights are reserved by default. It is collected here for internal research only. Contact the original author for permission before any public release or use in a paper.

Each subdirectory is a **complete, ready-to-run** OpenFOAM 12 case, with the geometry under `constant/triSurface/`. The only files removed were regenerable ones (`*.eMesh`, `extendedFeatureEdgeMesh/`), macOS `.DS_Store` files, and, in the standard directory, two gmsh draft files and one result image.

| Directory | Configuration | Body STL | Body triangles | Original Cd |
|---|---|---|---:|---:|
| [`standard_closed_bed/`](standard_closed_bed) | Standard (bed cover closed) | `bodyCassoneChiuso_mm.stl` | 1,106 | 0.312 |
| [`open_bed/`](open_bed) | Open bed | `bodyCassoneAperto_mm.stl` | 1,096 | 0.375 |
| [`roof_rack/`](roof_rack) | Roof rack | `bodyRoofrack_mm.stl` | 46,296 (3 shells) | 0.337 |
| [`roof_carrier_box/`](roof_carrier_box) | Roof rack + carrier box | `bodyCassoneChiusoPortapacchi_mm.stl` | 57,246 | 0.408 |

| standard_closed_bed | open_bed | roof_rack | roof_carrier_box |
|---|---|---|---|
| ![](previews/standard_closed_bed.png) | ![](previews/open_bed.png) | ![](previews/roof_rack.png) | ![](previews/roof_carrier_box.png) |

All four cases share the same wheels, `FR_mm.stl` (front wheel) and `RR_mm.stl` (rear wheel), each with 2,496 faces and 8 closed shells. All four cases use the same boundary conditions, meshing parameters and turbulence model. Apart from the body STL and its patch name, the original author's settings differ in a few small ways (all kept as is):

- `roof_rack/`, `roof_carrier_box/`: `system/fvSolution` has no `residualControl` (the standard case uses p 1e-4, U/k/ω 1e-5) and no `turbOnFinalIterOnly false`, so these cases always run the full 5000 iterations; `fieldAverage1` in `controlDict` is `enabled false`.
- `open_bed/`: `controlDict` uses `startFrom latestTime` (restart), and `timeStart 1000` in `fieldAverage1` is commented out, so averaging starts from iteration 0.

All STLs have been verified to be watertight with consistent normals. The original Cd values are taken from `postprocessing/cdBreak.py`.

## Coordinates and units

- The file names contain `_mm`, but **the actual unit is meters** (vehicle length 5.683 m). Use them as is; do not rescale.
- The vehicle front points toward +x (x = 2.841); **the freestream direction is −x** (inlet U = (−30, 0, 0) m/s).
- Half-car model: the domain spans y ∈ [−10, 0], and y=0 is a symmetry patch. The body STL is the full vehicle; wheels exist only on the −y side.
- The ground `tarmac` is at z = −0.8605; the bottoms of the wheels penetrate the ground by about 1 cm.
- Computational domain: x ∈ [−100, 20], z ∈ [−0.86, 20].

## Running

```bash
cd standard_closed_bed      # or any of the other three configurations
./Allrun.sh                 # blockMesh → surfaceFeatures → snappyHexMesh on 6 cores → topoSet (MRF zones) → foamRun on 6 cores
./Allclean.sh
```

The solver is `foamRun` + `incompressibleFluid` with k-ω SST, 5000 iterations in total. Wheel rotation is modeled with MRF zones (cylinders defined in `topoSetDict`) plus `rotatingWallVelocity` boundary conditions. `controlDict` already includes forces / forceCoeffs output (magUInf 30, lRef 5.683, Aref 1.60, commented "frontal area" in the original).

The original author reports a mesh of about 8 million cells. `Allrun.sh` hard-codes 6 cores; if you change this, also update `system/decomposeParDict`.

**Tested (meshing only)**: the local machine has only OpenFOAM v1912, not OF12, so only whether the geometry can be meshed was checked; foamRun was not run. The surface refinement levels were lowered from (5 7) to (3 4) and prism layers were disabled, with everything else unchanged. All four configurations reported "Finished meshing without any errors", with about 4.54 million cells each, and checkMesh returned `Mesh OK` for all of them.

## Notes

- **The MRF rotation-speed unit appears to be wrong**: `constant/MRFProperties` specifies `rpm 67.887126`, but the wheel wall boundary condition uses `omega 67.8871` (rad/s), and 30 m/s ÷ 0.442 m wheel radius = 67.9 rad/s. In other words, the rad/s value was written under the `rpm` key, so the MRF zones actually rotate at only 7.1 rad/s, which does not match the rotation rate imposed on the wheel walls. Changing `rpm 67.887126;` to `omega 67.887126;` is recommended. The original files are kept here unmodified.
- **Cd reference area and integration surface**: projecting the standard body plus the −y wheels (above the ground) onto the y-z plane gives a half-car frontal area of about 1.38 m², about 14% smaller than `Aref 1.60`. If Aref is meant to be the half-car frontal area, the reported Cd is about 14% low. In addition, the `patches` of forces / forceCoeffs contain only the body, **not the wheels** (`FR_mm`, `RR_mm`), so the original Cd values exclude wheel drag.
- In the original repository, `CAD modifications/roofrack_1_4pz.stl` is a standalone roof rack part (in mm, without the body). It has already been merged into the body STL in `roof_rack/`, so it was not copied over separately.

## Post-processing scripts

`postprocessing/` is `pythonCodes/` from the original repository:
- `cdBreak.py`: Cd comparison plot of the four configurations
- `gridConv.py`: grid convergence curve (interactive input)
- `mediumCoefficients.py`, `Autonomy.py`: coefficient averaging, range estimation
