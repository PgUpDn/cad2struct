"""Tessellate a STEP solid to STL with gmsh, output in metres.

Usage: step2stl.py in.step out.stl hmax_m [hmin_m]
"""
import sys, gmsh
src, out, hmax = sys.argv[1], sys.argv[2], float(sys.argv[3])
gmsh.initialize(); gmsh.option.setNumber("General.Terminal", 0)
gmsh.option.setString("Geometry.OCCTargetUnit", "M")  # read directly in metres
gmsh.model.occ.importShapes(src); gmsh.model.occ.synchronize()
gmsh.option.setNumber("Mesh.MeshSizeMax", hmax)
gmsh.option.setNumber("Mesh.MeshSizeMin", float(sys.argv[4]) if len(sys.argv)>4 else hmax/50)
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 24)
gmsh.option.setNumber("Mesh.Algorithm", 6)
gmsh.option.setNumber("Mesh.Binary", 1)
gmsh.option.setNumber("Mesh.StlOneSolidPerSurface", 0)
gmsh.model.mesh.generate(2)
gmsh.write(out); gmsh.finalize()
