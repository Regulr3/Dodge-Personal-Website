import math
C, S = math.cos(math.radians(30)), math.sin(math.radians(30))

class Scene:
    def __init__(self, W=1200, H=900, s=14, ox=600, oy=520):
        self.W, self.H, self.s, self.ox, self.oy = W, H, s, ox, oy
        self.items = []   # (depth, svg)
        self.defs = []
        self.overlay = []
        self.uid = 0
    def P(self, x, y, z):
        s = self.s
        return (self.ox + (x - y) * C * s, self.oy + (x + y) * S * s - z * s)
    def id(self, p='g'):
        self.uid += 1; return f'{p}{self.uid}'
    # face transforms: local (u right, v down) in units
    def m_front(self, x0, y, z1):   # plane y=const, u along +x, v along -z (top-left at x0,z1)
        s = self.s; X, Y = self.P(x0, y, z1)
        return f'matrix({C*s:.4f},{S*s:.4f},0,{s:.4f},{X:.2f},{Y:.2f})'
    def m_side(self, x, y0, z1):    # plane x=const, u along +y?? we want u going toward viewer-left: along +y
        s = self.s; X, Y = self.P(x, y0, z1)
        return f'matrix({-C*s:.4f},{S*s:.4f},0,{s:.4f},{X:.2f},{Y:.2f})'
    def m_top(self, x0, y0, z):     # u along +x, v along +y
        s = self.s; X, Y = self.P(x0, y0, z)
        return f'matrix({C*s:.4f},{S*s:.4f},{-C*s:.4f},{S*s:.4f},{X:.2f},{Y:.2f})'
    def add(self, depth, svg): self.items.append((depth, svg))
    def render(self, extra_style=''):
        body = ''.join(svg for _, svg in sorted(self.items, key=lambda t: t[0]))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.W} {self.H}" width="{self.W}" height="{self.H}">'
                f'<defs>{COMMON_DEFS}{"".join(self.defs)}</defs><style>{STYLE}{extra_style}</style>'
                '<rect width="100%" height="100%" fill="url(#bgG)"/>' + body + ''.join(self.overlay) +
                '<rect width="100%" height="100%" fill="url(#vig)" pointer-events="none"/></svg>')

COMMON_DEFS = '''
<radialGradient id="bgG" cx=".5" cy=".45" r=".75"><stop offset="0" stop-color="#0d1628"/><stop offset=".55" stop-color="#070b16"/><stop offset="1" stop-color="#03050b"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".72"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#01020a" stop-opacity=".75"/></radialGradient>
<radialGradient id="floorFade" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff"/><stop offset=".7" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="floorMask" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#floorFade)"/></mask>
<linearGradient id="mTop" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a566d"/><stop offset="1" stop-color="#2c3445"/></linearGradient>
<linearGradient id="mFront" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#232b3a"/><stop offset="1" stop-color="#151a25"/></linearGradient>
<linearGradient id="mSide" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#151a24"/><stop offset="1" stop-color="#0c1018"/></linearGradient>
<linearGradient id="plate" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2b3547"/><stop offset=".5" stop-color="#3a475e"/><stop offset="1" stop-color="#28313f"/></linearGradient>
<linearGradient id="plateDark" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#121722"/><stop offset=".5" stop-color="#1b2230"/><stop offset="1" stop-color="#111520"/></linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="pipeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a7f3d0"/><stop offset=".45" stop-color="#34d399"/><stop offset="1" stop-color="#065f46"/></linearGradient>
<linearGradient id="pipeB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#93c5fd"/><stop offset=".45" stop-color="#2563eb"/><stop offset="1" stop-color="#1e3a8a"/></linearGradient>
<pattern id="perf" width=".5" height=".5" patternUnits="userSpaceOnUse"><rect width=".5" height=".5" fill="#1a2130"/><circle cx=".25" cy=".25" r=".13" fill="#070a10"/></pattern>
<pattern id="perfG" width=".5" height=".5" patternUnits="userSpaceOnUse"><rect width=".5" height=".5" fill="#22314a"/><circle cx=".25" cy=".25" r=".14" fill="#0a0f19"/></pattern>
<pattern id="vents" width=".35" height="1" patternUnits="userSpaceOnUse"><rect width=".35" height="1" fill="#141a26"/><rect x=".1" width=".14" height="1" fill="#090c13"/></pattern>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glowBig" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .05 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<radialGradient id="floorGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#34d399" stop-opacity=".16"/><stop offset=".6" stop-color="#0b3b5e" stop-opacity=".10"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
'''
STYLE = '''
.led{fill:#34d399;filter:url(#glow)}
.ledb{animation:blink 1.6s steps(2,end) infinite}
.ledb2{animation:blink 2.3s steps(2,end) infinite .4s}
@keyframes blink{50%{opacity:.25}}
.flow{fill:none;stroke-linecap:round;stroke-dasharray:.6 1.4;animation:flow 1.6s linear infinite}
@keyframes flow{to{stroke-dashoffset:-2}}
.edge{fill:none;stroke:#fff;stroke-opacity:.09;stroke-width:.05}
.txt{font-family:ui-sans-serif,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
'''

def box(sc, x, y, z, w, d, h, top='url(#mTop)', front='url(#mFront)', side='url(#mSide)', fdetail='', sdetail='', tdetail='', depth=None, edge=True):
    """front = plane y=y+d (faces viewer-left), side = plane x=x+w (faces viewer-right)."""
    g = []
    # top
    g.append(f'<g transform="{sc.m_top(x, y, z+h)}"><rect width="{w}" height="{d}" fill="{top}"/>{tdetail}<rect width="{w}" height="{d}" fill="url(#sheen)"/>' + (f'<rect width="{w}" height="{d}" class="edge"/>' if edge else '') + '</g>')
    # front (y+d plane)
    g.append(f'<g transform="{sc.m_front(x, y+d, z+h)}"><rect width="{w}" height="{h}" fill="{front}"/>{fdetail}' + (f'<rect width="{w}" height="{h}" class="edge"/>' if edge else '') + '</g>')
    # side (x+w plane): u along +y from y.. we draw from y to y+d
    g.append(f'<g transform="{sc.m_side(x+w, y, z+h)}"><rect width="{d}" height="{h}" fill="{side}"/>{sdetail}' + (f'<rect width="{d}" height="{h}" class="edge"/>' if edge else '') + '</g>')
    sc.add(depth if depth is not None else (x + y + z + (w + d) * 0.5), ''.join(g))
