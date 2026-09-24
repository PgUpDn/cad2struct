"""Print triangle count, watertightness, body count and bounding box of STL files."""
import sys, trimesh, numpy as np
for f in sys.argv[1:]:
    m = trimesh.load(f, force='mesh', process=True)
    b = m.bounds; ext = b[1]-b[0]
    parts = m.split(only_watertight=False)
    print(f"{f}\n  tris={len(m.faces)} watertight={m.is_watertight} winding={m.is_winding_consistent} bodies={len(parts)} wt_bodies={sum(p.is_watertight for p in parts)}\n  min={np.round(b[0],3)} max={np.round(b[1],3)} extent={np.round(ext,3)}")
