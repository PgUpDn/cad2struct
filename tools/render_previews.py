"""Render README preview images for every packaged geometry.

Usage (headless):  xvfb-run -a python3 tools/render_previews.py
Needs: pyvista, pillow (and xvfb on a machine without a display).

Writes one PNG per configuration into cfd_geometry/<model>/previews/ and an
overview mosaic cfd_geometry/previews/overview.png.
"""
import os
import numpy as np
import pyvista as pv
from PIL import Image, ImageChops, ImageDraw, ImageFont

pv.OFF_SCREEN = True
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cfd_geometry")
MS = "tesla_model_s"
CT = "tesla_cybertruck"


def ct(case, body):
    tri = f"{CT}/{case}/constant/triSurface/"
    return [tri + body, tri + "FR_mm.stl", tri + "RR_mm.stl"]


# (model dir, preview name, label, STL paths relative to cfd_geometry/, rear direction along x)
# Model S drives towards -x (nose at x=0, tail at x=5); the Cybertruck drives towards +x.
ITEMS = [
    (MS, "baseline", "Model S · baseline", [f"{MS}/polimi_openfoam/stl/baseline.stl"], +1),
    (MS, "rearwing_standard_pylons", "Model S · wing, standard pylons", [f"{MS}/polimi_openfoam/stl/rearwing_standard_pylons.stl"], +1),
    (MS, "rearwing_swan_neck", "Model S · wing, swan neck", [f"{MS}/polimi_openfoam/stl/rearwing_swan_neck.stl"], +1),
    (MS, "rearwing_swan_neck_back", "Model S · wing, swan neck (back)", [f"{MS}/polimi_openfoam/stl/rearwing_swan_neck_back.stl"], +1),
    (MS, "rearwing_floating_no_mounts", "Model S · floating wing", [f"{MS}/polimi_openfoam/stl/rearwing_floating_no_mounts.stl"], +1),
    (MS, "baseline_from_step", "Model S · STEP body (no wheels)", [f"{MS}/fluent_spoiler/stl/baseline_from_step.stl"], +1),
    (MS, "with_spoiler_fluent_surface", "Model S · Fluent surface + spoiler", [f"{MS}/fluent_spoiler/stl/with_spoiler_fluent_surface.stl"], +1),
    (CT, "standard_closed_bed", "Cybertruck · standard", ct("standard_closed_bed", "bodyCassoneChiuso_mm.stl"), -1),
    (CT, "open_bed", "Cybertruck · open bed", ct("open_bed", "bodyCassoneAperto_mm.stl"), -1),
    (CT, "roof_rack", "Cybertruck · roof rack", ct("roof_rack", "bodyRoofrack_mm.stl"), -1),
    (CT, "roof_carrier_box", "Cybertruck · roof box", ct("roof_carrier_box", "bodyCassoneChiusoPortapacchi_mm.stl"), -1),
]


def autocrop(img, pad=10):
    bg = Image.new(img.mode, img.size, (255, 255, 255))
    x0, y0, x1, y1 = ImageChops.difference(img, bg).getbbox()
    return img.crop((max(x0 - pad, 0), max(y0 - pad, 0), min(x1 + pad, img.width), min(y1 + pad, img.height)))


def render(paths, rear, out):
    meshes = [pv.read(os.path.join(ROOT, p)) for p in paths]
    xmin, xmax, ymin, ymax, zmin, zmax = pv.merge(meshes).bounds
    length = xmax - xmin
    centre = np.array([(xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2])

    p = pv.Plotter(off_screen=True, window_size=(1400, 800))
    p.set_background("white")
    width = ymax - ymin
    floor = pv.Plane(center=(centre[0], centre[1], zmin), direction=(0, 0, 1),
                     i_size=length * 1.3, j_size=width * 2.2)
    p.add_mesh(floor, color="#f1f3f6", ambient=1.0, diffuse=0.0, specular=0.0)
    for m in meshes:
        p.add_mesh(m, color="#7f96ad", smooth_shading=True, split_sharp_edges=True,
                   specular=0.35, specular_power=20)
    # rear three-quarter view from the -y side (the Cybertruck only has -y wheels)
    eye = centre + np.array([rear * 0.95, -1.05, 0.55]) * length
    p.camera.position = tuple(eye)
    p.camera.focal_point = tuple(centre)
    p.camera.up = (0, 0, 1)
    p.camera.view_angle = 26
    p.enable_anti_aliasing("ssaa")
    img = Image.fromarray(p.screenshot(return_img=True)).convert("RGB")
    p.close()
    img = autocrop(img)
    img.thumbnail((900, 520), Image.LANCZOS)
    img.save(out, optimize=True)
    return img


def label_font(size):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def mosaic(tiles, out, cols=4, cell=(420, 215)):
    font = label_font(17)
    rows = -(-len(tiles) // cols)
    W, H = cols * cell[0], rows * (cell[1] + 34)
    sheet = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (label, img) in enumerate(tiles):
        if img is None:
            continue
        r, c = divmod(i, cols)
        t = img.copy()
        t.thumbnail((cell[0] - 16, cell[1] - 10), Image.LANCZOS)
        x0, y0 = c * cell[0], r * (cell[1] + 34)
        sheet.paste(t, (x0 + (cell[0] - t.width) // 2, y0 + (cell[1] - t.height) // 2))
        tw = draw.textlength(label, font=font)
        draw.text((x0 + (cell[0] - tw) / 2, y0 + cell[1] + 4), label, fill="#333333", font=font)
    sheet.save(out, optimize=True)


if __name__ == "__main__":
    tiles, prev_model = [], None
    for model, name, label, paths, rear in ITEMS:
        os.makedirs(os.path.join(ROOT, model, "previews"), exist_ok=True)
        out = os.path.join(ROOT, model, "previews", name + ".png")
        if tiles and model != prev_model and len(tiles) % 4:
            tiles += [("", None)] * (4 - len(tiles) % 4)  # start each vehicle on its own row
        prev_model = model
        tiles.append((label, render(paths, rear, out)))
        print(out)
    os.makedirs(os.path.join(ROOT, "previews"), exist_ok=True)
    mosaic(tiles, os.path.join(ROOT, "previews", "overview.png"))
    print(os.path.join(ROOT, "previews", "overview.png"))
