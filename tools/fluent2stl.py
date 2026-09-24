"""Extract one face zone of a Fluent .msh.h5 mesh as a triangulated STL.

Usage: fluent2stl.py mesh.msh.h5 <zone name> out.stl
Polygon faces are fan-triangulated; coordinates are written as stored (Fluent: metres).
"""
import sys, h5py, numpy as np, trimesh
def extract(fn, zone_name):
    f = h5py.File(fn, "r"); m = f["meshes/1"]
    zt = m["faces/zoneTopology"]; names = zt["name"][0].decode().split(";")
    coords = np.vstack([m[f"nodes/coords/{k}"][:] for k in sorted(m["nodes/coords"].keys(), key=int)])
    sec = m[f"faces/nodes/{names.index(zone_name)+1}"]
    nn = sec["nnodes"][:].astype(np.int64); idx = sec["nodes"][:].astype(np.int64) - 1
    starts = np.concatenate([[0], np.cumsum(nn)[:-1]])
    tris = [ [idx[s], idx[s+k], idx[s+k+1]] for s, n in zip(starts, nn) for k in range(1, n-1) ]  # fan triangulation
    mesh = trimesh.Trimesh(coords, np.array(tris), process=True)
    mesh.remove_unreferenced_vertices()
    return mesh
if __name__ == "__main__":
    fn, zone, out = sys.argv[1:4]
    m = extract(fn, zone); m.export(out)
    print(out, len(m.faces), m.bounds.round(4).tolist())
