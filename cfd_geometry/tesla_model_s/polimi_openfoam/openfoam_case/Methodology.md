# 🏎️ Tesla Model S – OpenFOAM Aerodynamic Simulation Workflow

This document describes the complete workflow followed for the preparation, meshing, and aerodynamic simulation of a Tesla Model S using OpenFOAM.

> 🎓 **Academic Context**  
> This project represents my first practical hands-on experience with OpenFOAM. Documenting this process step-by-step was essential to understand the architecture and workflow of the software, transitioning from manually executing commands in the terminal to fully automating the simulation pipeline using Bash scripts.

---

# 1. Geometry Preparation and Domain Sizing 📐

Before meshing, it is critical to ensure that the geometry exported from CATIA® is correctly formatted and scaled.

## STL Verification

The exported STL file must be in ASCII format.

This can be verified by opening the file with a text editor. The file should start with:

```
solid <name>
```

## Scale Conversion

OpenFOAM and ParaView operate in meters. If the CAD geometry was created in millimeters, a scale conversion must be applied:

```bash
surfaceConvert TeslaModelS_baseCaseSinEscalar.stl TeslaModelS_baseCase.stl -clean -scale 0.001
```

## Virtual Wind Tunnel Dimensions (blockMesh)

To ensure that the boundary conditions do not artificially interfere with the vehicle wake, the computational domain was sized using the vehicle length \(L\) and height \(H\) as references.

| Region | Recommended Size |
|------|------|
| Inlet (front) | 3L – 5L ahead of the vehicle |
| Outlet (rear) | 8L – 10L behind the vehicle |
| Sides | 2L – 3L on each side |
| Top | 3H – 5H above the vehicle |

---

# 2. Meshing Strategy (snappyHexMesh) 🕸️

The mesh was generated using the `snappyHexMesh` utility, executed in parallel to optimize computational resources.

---

## 2.1 Base Mesh and Feature Extraction

First, the background grid is generated and the geometric features of the model are extracted:

```bash
blockMesh
surfaceFeaturesExtract
```

The `surfaceFeaturesExtract` dictionary was configured with:

```
includedAngle 180;
```

---

## 2.2 snappyHexMeshDict Configuration

Mesh parameters were selected considering the available hardware resources (8-core CPU environment).

### Surface Refinement

```
refinementSurfaces
{
    TeslaModelS
    {
        level (5 6);
    }
}
```

Ideally this could be increased to refinement levels **7–8** on more powerful computing clusters.

### Feature Angle Resolution

```
resolveFeatureAngle 30;
```

This allows the mesh to properly capture curved surfaces and geometric details.

### Refinement Regions

Volumetric refinement boxes were defined around:

- The vehicle body
- The downstream wake region

### Boundary Layer Resolution

To properly resolve the boundary layer, **6 prism layers** were generated on the relevant surfaces:

```
layers
{
    "(lowerWall|TeslaModelS_baseCase).*"
    {
        nSurfaceLayers 6;
    }
}
```

---

## 2.3 Parallel Meshing Execution

The mesh generation process was executed in parallel.

```bash
decomposePar
mpirun -np 2 snappyHexMesh -overwrite -parallel
reconstructParMesh -constant
rm -r processor*
```

The `scotch` decomposition method was used for automatic load balancing.

### Visualization Tip

An empty `.foam` file can be created to easily open the case in ParaView:

```bash
touch foam.foam
```

---

# 3. CFD Simulation (simpleFoam) 🚀

The case was solved using the steady-state incompressible solver `simpleFoam`, applying the **k-ω SST turbulence model**.

To automate the workflow, a Bash script was created.

## Simulation Script

```bash
#!/bin/bash

decomposePar
mpirun -np 2 simpleFoam -parallel > log.simple &
```

Make the script executable with:

```bash
chmod +x go
```

Run the simulation with:

```bash
./go
```

---

## Live Monitoring

The solver progress and residual evolution can be monitored in real time by reading the log file:

```bash
tail -f log.simple
```

---

## Resource Monitoring

Linux commands such as the following were used to monitor CPU and memory usage:

```bash
top
```

or

```bash
ps wux
```

---

## Process Control

If a background simulation needs to be terminated manually:

```bash
kill -9 <PID_NUMBER>
```

---

# 4. Post-Processing and Results 📊

Once the simulation converged (or reached acceptable residual levels), post-processing was performed.

---

## 4.1 Case Reconstruction

If the simulation was executed in parallel, the decomposed domains must be reconstructed:

```bash
reconstructPar
rm -r processor*
```

---

## 4.2 Boundary Layer Verification (y+)

To ensure that the near-wall mesh resolution is appropriate for the selected turbulence model:

```bash
simpleFoam -postProcess -func yPlus
```

Inside ParaView it is necessary to click **"Reload Files"** to visualize the newly generated field.

---

## 4.3 Advanced Visualization

The aerodynamic flow field was analyzed in ParaView, focusing on:

- Streamlines
- Pressure coefficient \(C_p\)
- Wake vortex structures

Alternatively, simulation data can be exported to standard VTK format:

```bash
foamToVTK
```

---

## 4.4 Residual Monitoring

Residual convergence was analyzed using **gnuplot** to evaluate the stability and convergence behavior of the simulation.

---

# Troubleshooting ⚠️

If permission issues arise when running OpenFOAM in WSL/Ubuntu, the user password can be reset by launching the distribution as root:

```bash
wsl -d Ubuntu -u root
```

Then run:

```bash
passwd <username>
```

---

# Skills Demonstrated

- OpenFOAM workflow setup
- snappyHexMesh meshing strategy
- Parallel CFD execution
- Bash workflow automation
- Boundary layer validation using \(y^+\)
- Aerodynamic post-processing with ParaView

---

# Tools Used

- OpenFOAM  
- ParaView  
- GNU/Linux (WSL Ubuntu)  
- GNUplot  
- CATIA
