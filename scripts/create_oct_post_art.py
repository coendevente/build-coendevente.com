"""Create original, schematic SVG artwork for the two OCT research posts."""
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1] / 'site/images'


def retina(width=1000, height=320, accent=False):
    """Stylized macular OCT: inner layers taper at the fovea; outer bands stay separate.

    Band order follows ILM/RNFL, GCL, IPL, INL, OPL, ONL, ELM, EZ,
    interdigitation zone, and RPE/Bruch's membrane. This is a schematic,
    not a clinical image or a depiction of a particular atrophy lesion.
    """
    light = '#f5e3d4' if accent else '#d9eeec'
    medium = '#bcaabf' if accent else '#83acb8'
    dark = '#68536e' if accent else '#456979'
    xs = list(range(0, width + 1, 5))

    def profile(layer, x):
        u = x / width
        pit = math.exp(-((u - .51) / .135) ** 2)
        curve = 3 * math.sin(u * math.pi)  # gentle curvature shared by outer retina
        # Inner retinal tissue displaces laterally at the foveal centre.
        inner = [45, 59, 88, 108, 134, 149]
        if layer < 6:
            return inner[layer] + (146 - inner[layer]) * pit + curve
        return [188, 204, 220, 235, 247, 287][layer - 6] + curve - 4 * pit

    def coords(layer):
        return [(x, profile(layer, x)) for x in xs]

    def points(coords):
        return ' '.join(f'{x:.1f},{y:.1f}' for x, y in coords)

    result = []
    # Alternate reflective plexiform bands and darker nuclear layers.
    for upper, lower, color, opacity in [
        (0,1,light,.38), (1,2,dark,.34), (2,3,medium,.48),
        (3,4,dark,.26), (4,5,light,.37), (5,6,dark,.18),
        (6,7,dark,.16), (7,8,medium,.12), (8,9,dark,.20),
        (10,11,dark,.19)]:
        polygon = coords(upper) + list(reversed(coords(lower)))
        result.append(f'<polygon points="{points(polygon)}" fill="{color}" opacity="{opacity}"/>')
    # Bright ILM, then thin ELM, stronger EZ, IZ, and the broad RPE complex.
    for layer, thickness, opacity in [(0,2,.8),(5,1.4,.4),(6,1.8,.65),
                                        (7,4,.88),(8,2.4,.6),(9,6,.95),(10,1.3,.4)]:
        result.append(f'<polyline points="{points(coords(layer))}" fill="none" stroke="{light}" stroke-width="{thickness}" opacity="{opacity}"/>')
    # Sparse, low-contrast OCT-like texture inside tissue, never uniform extra layers.
    import random
    rng = random.Random(17)
    for _ in range(1050):
        x = rng.uniform(0, width)
        y = rng.uniform(profile(0, x), profile(11, x))
        if profile(5, x) < y < profile(6, x):
            opacity = rng.uniform(.025,.10)  # hyporeflective ONL
        else:
            opacity = rng.uniform(.04,.20)
        result.append(f'<path d="M{x:.1f} {y:.1f}h{rng.uniform(1,4):.1f}" stroke="{light}" stroke-width=".8" opacity="{opacity:.2f}"/>')
    return ''.join(result)


def artwork(slug, thumb):
    w,h = (900,675) if thumb else (1600,900)
    defs = '''<defs>
      <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#163c50"/><stop offset="1" stop-color="#122332"/></linearGradient>
      <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0.35" stop-color="#102530" stop-opacity="0"/><stop offset="1" stop-color="#0a1827" stop-opacity=".98"/></linearGradient>
      <linearGradient id="glass"><stop stop-color="#51d0c6" stop-opacity=".1"/><stop offset="1" stop-color="#b1f4e9" stop-opacity=".22"/></linearGradient>
      <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0H0V60" fill="none" stroke="#9dc8cf" stroke-opacity=".07"/></pattern>
    </defs>'''
    if slug == 'ubix':
        defs = (defs.replace('#163c50', '#42334e').replace('#122332', '#211e33')
                .replace('#102530', '#302439').replace('#0a1827', '#191625')
                .replace('#9dc8cf', '#cbb6d4'))
    body = f'<rect width="{w}" height="{h}" fill="url(#bg)"/><rect width="{w}" height="{h}" fill="url(#grid)"/>'
    if slug == 'irora-crora':
        # Two feature bands over a stylized retina; conceptual, not a clinical segmentation.
        tx,ty,scale = (50,95,.8) if thumb else (400,150,.8)
        body += f'<g transform="translate({tx} {ty}) scale({scale})">'
        body += '<path d="M0 305 Q500 345 1000 305" stroke="#6e99a9" stroke-width="1" fill="none"/>'
        body += retina()
        for x,width,color in [(250,105,'#66ead4'),(590,220,'#ccacf5')]:
            body += f'<rect x="{x}" y="40" width="{width}" height="250" fill="{color}" opacity=".12"/>'
            body += f'<path d="M{x} 48v230m{width} -230v230" stroke="{color}" stroke-width="2" stroke-dasharray="5 7"/>'
            body += f'<path d="M{x} 322v12h{width}v-12" fill="none" stroke="{color}" stroke-width="5"/>'
        body += '<g fill="none" stroke-width="13" stroke-linecap="round"><path d="M250 367h105" stroke="#66ead4"/><path d="M590 367h220" stroke="#ccacf5"/></g>'
        body += '</g>'
    else:
        tx,ty,scale = (110,100,1) if thumb else (590,215,.65)
        body += f'<g transform="translate({tx} {ty}) scale({scale})">'
        # A stack of image planes, with an amber displaced plane that is excluded.
        for i in reversed(range(5)):
            excluded = i == 2
            x,y = i*64, i*47
            if excluded: x+=65
            color = '#f3a295' if excluded else '#dbc4b2'
            body += f'<g transform="translate({x} {y}) skewY(-12)">'
            body += f'<rect width="380" height="205" rx="5" fill="#332c43" stroke="{color}" stroke-width="2"/>'
            body += f'<g transform="translate(12 5) scale(.355 .61)" opacity="{.3 if excluded else .9}">{retina(accent=True)}</g>'
            if excluded:
                body += '<path d="M150 8v187m12-187v187m-26-187v187" stroke="#f3a295" stroke-width="9" opacity=".45"/>'
                body += '<circle cx="350" cy="24" r="15" fill="#f3a295"/><path d="M343 17l14 14m0-14l-14 14" stroke="#3a2945" stroke-width="3"/>'
            else:
                body += '<circle cx="350" cy="24" r="6" fill="#f4e0c7"/>'
            body += '</g>'
        body += '</g>'
    if not thumb: body += f'<rect width="{w}" height="{h}" fill="url(#fade)"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{"Retinal layers and atrophy feature regions" if slug == "irora-crora" else "OCT slice stack with one uncertain slice excluded"}</title><desc>Original conceptual illustration; not a patient scan or model prediction.</desc>{defs}{body}</svg>\n'


for slug in ['irora-crora','ubix']:
    folder=ROOT/slug
    folder.mkdir(exist_ok=True)
    for thumb in [False,True]:
        (folder/('thumbnail.svg' if thumb else 'cover.svg')).write_text(artwork(slug,thumb))
