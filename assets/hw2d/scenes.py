from iso import Scene, box, C, S
import random

def floor(sc, x0, y0, x1, y1, step=2):
    lines = []
    for x in range(x0, x1 + 1, step):
        a, b = sc.P(x, y0, 0), sc.P(x, y1, 0); lines.append(f'M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}')
    for y in range(y0, y1 + 1, step):
        a, b = sc.P(x0, y, 0), sc.P(x1, y, 0); lines.append(f'M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}')
    pts = ' '.join(f'{p[0]:.1f},{p[1]:.1f}' for p in [sc.P(x0,y0,0), sc.P(x1,y0,0), sc.P(x1,y1,0), sc.P(x0,y1,0)])
    cx, cy = sc.P((x0+x1)/2, (y0+y1)/2, 0)
    sc.add(-1000, f'<g mask="url(#floorMask)"><polygon points="{pts}" fill="#0a1020"/>'
                  f'<path d="{"".join(lines)}" stroke="#6ee7b7" stroke-opacity=".09" stroke-width="1" fill="none"/></g>'
                  f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{sc.W*0.36:.0f}" ry="{sc.H*0.2:.0f}" fill="url(#floorGlow)"/>')

def switch_face(u0, v0, w, h=0.6, ports=16, lit=0.7, rnd=None):
    rnd = rnd or random.Random(1)
    out = [f'<rect x="{u0}" y="{v0}" width="{w}" height="{h}" rx=".05" fill="url(#plateDark)"/>',
           f'<rect x="{u0}" y="{v0}" width="{w}" height=".05" fill="#fff" fill-opacity=".12"/>']
    pw = (w - 1.0) / ports
    for i in range(ports):
        px = u0 + 0.7 + i * pw
        out.append(f'<rect x="{px:.3f}" y="{v0+h*0.28:.3f}" width="{pw*0.72:.3f}" height="{h*0.42:.3f}" fill="#05070c" stroke="#3b475c" stroke-width=".02"/>')
        if rnd.random() < lit:
            out.append(f'<rect x="{px:.3f}" y="{v0+h*0.12:.3f}" width="{pw*0.3:.3f}" height=".06" class="led {"ledb" if rnd.random()<.3 else ""}"/>')
    out.append(f'<circle cx="{u0+0.35}" cy="{v0+h/2}" r=".09" class="led"/>')
    return ''.join(out)

def node_face(u0, v0, w, h, rnd, led=True):
    out = [f'<rect x="{u0}" y="{v0}" width="{w}" height="{h}" rx=".08" fill="url(#plate)"/>',
           f'<rect x="{u0+0.35}" y="{v0+0.3}" width="{w-0.7}" height="{h-0.9}" fill="url(#perfG)"/>',
           f'<rect x="{u0}" y="{v0}" width="{w}" height=".06" fill="#fff" fill-opacity=".18"/>',
           f'<rect x="{u0+0.35}" y="{v0+h-0.45}" width="{w-0.7}" height=".22" fill="#0a0e16"/>']
    # handles
    for hu in (u0 + 0.12, u0 + w - 0.22):
        out.append(f'<rect x="{hu}" y="{v0+0.5}" width=".1" height="{h-1.3}" rx=".05" fill="#5b6a85"/>')
    if led:
        for k in range(4):
            out.append(f'<rect x="{u0+0.55+k*0.35:.2f}" y="{v0+h-0.39}" width=".22" height=".1" class="led {"ledb" if rnd.random()<.35 else ("ledb2" if rnd.random()<.3 else "")}"/>')
    return ''.join(out)

def rack(sc, x, y, w=6, d=11, h=22, rnd=None, missing=None, depth=None):
    rnd = rnd or random.Random(x)
    f = [f'<rect width="{w}" height="{h}" fill="#0b0f17"/>', f'<rect x=".35" y=".35" width="{w-0.7}" height="{h-0.7}" fill="#05070c"/>']
    f.append(switch_face(0.45, 0.8, w - 0.9, rnd=rnd)); f.append(switch_face(0.45, 1.5, w - 0.9, rnd=rnd))
    v = 2.5
    for i in range(4):
        if missing != i: f.append(node_face(0.45, v, w - 0.9, 4.0, rnd))
        else: f.append(f'<rect x=".45" y="{v}" width="{w-0.9}" height="4" fill="#020306"/><rect x=".45" y="{v}" width="{w-0.9}" height="4" fill="none" stroke="#34d399" stroke-opacity=".35" stroke-width=".05" stroke-dasharray=".25 .2"/>')
        v += 4.2
    f.append(switch_face(0.45, v + 0.1, w - 0.9, ports=10, lit=0.5, rnd=rnd))
    # side panel vents + top cable cutouts
    s_ = (f'<rect x=".6" y="1" width="{d-1.2}" height="{h-2}" fill="url(#mSide)"/>'
          f'<rect x="{d/2-0.03:.2f}" y="1" width=".06" height="{h-2}" fill="#000" fill-opacity=".35"/>'
          f'<rect x="0" y="0" width=".12" height="{h}" fill="#6ee7b7" fill-opacity=".12"/>'
          f'<rect x=".6" y="1" width="{d-1.2}" height=".05" fill="#fff" fill-opacity=".06"/>')
    t_ = f'<rect x="1" y="1.5" width="{w-2}" height="1.2" fill="#0a0e16"/><rect x="1" y="{d-2.7}" width="{w-2}" height="1.2" fill="#0a0e16"/>'
    box(sc, x, y, 0, w, d, h, fdetail=''.join(f[2:]) if False else ''.join(f), sdetail=s_, tdetail=t_, depth=depth)

def scene_rack_stack():
    sc = Scene(s=15.5, ox=560, oy=440)
    rnd = random.Random(7)
    floor(sc, -8, -6, 40, 30)
    xs = [-2, 4.6, 11.2, 17.8]
    for i, x in enumerate(xs):
        rack(sc, x, 0, rnd=rnd, missing=(2 if i == 2 else None), depth=i)
    # node being slid into rack 3 slot 2: pulled out along +y
    x = xs[2]; slot_top = 22 - (2.5 + 2 * 4.2)  # v from top -> z
    z0 = slot_top - 4.0
    nd = random.Random(3)
    node_front = node_face(0, 0, 5.1, 4.0, nd)
    top_d = '<rect x=".3" y=".4" width="4.5" height="6.2" fill="#0d121c"/>' + ''.join(f'<rect x="{0.6+k*0.55:.2f}" y="1" width=".4" height="2.2" fill="#1f2b40" stroke="#34d399" stroke-opacity=".5" stroke-width=".03"/>' for k in range(8)) + '<rect x=".6" y="3.6" width="3.9" height="1.4" fill="#16202f"/><rect x="1.4" y="3.85" width=".9" height=".9" fill="#273448" stroke="#6ee7b7" stroke-opacity=".6" stroke-width=".03"/><rect x="2.7" y="3.85" width=".9" height=".9" fill="#273448" stroke="#6ee7b7" stroke-opacity=".6" stroke-width=".03"/>'
    box(sc, x + 0.45, 11 + 3.2, z0, 5.1, 7.0, 4.0, front='url(#plate)', fdetail=node_front, tdetail=top_d, depth=10)
    # guide arrow + label
    a, b = sc.P(x + 3, 11 + 2.6, z0 + 2), sc.P(x + 3, 11.2, z0 + 2)
    sc.overlay.append(f'<path d="M{a[0]:.0f} {a[1]:.0f}L{b[0]:.0f} {b[1]:.0f}" stroke="#6ee7b7" stroke-width="2" stroke-dasharray="4 5" fill="none" class="flowpx"/>')
    # overhead cable tray with cables dropping into racks
    tray = []
    for k in range(6):
        p1, p2 = sc.P(-4, 4 + k * 0.25, 25.5), sc.P(28, 4 + k * 0.25, 25.5)
        col = ['#34d399', '#6ee7b7', '#10b981', '#a7f3d0', '#2dd4bf', '#5eead4'][k]
        tray.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f}L{p2[0]:.1f} {p2[1]:.1f}" stroke="{col}" stroke-width="2.2" stroke-opacity=".85"/>')
    for x_ in xs:
        for k in range(3):
            p1, p2 = sc.P(x_ + 1.5 + k * 0.6, 4.5, 25.5), sc.P(x_ + 1.5 + k * 0.6, 4.5, 22)
            tray.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f}L{p2[0]:.1f} {p2[1]:.1f}" stroke="#34d399" stroke-width="1.6" stroke-opacity=".7"/>')
    q = [sc.P(-4, 3.6, 25.2), sc.P(28, 3.6, 25.2), sc.P(28, 5.8, 25.2), sc.P(-4, 5.8, 25.2)]
    sc.add(-500, '')
    sc.add(500, f'<polygon points="{" ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in q)}" fill="#1b2232" stroke="#3b475c" stroke-width="1"/>' + ''.join(tray))
    return sc.render(extra_style='.flowpx{animation:fpx 1.2s linear infinite}@keyframes fpx{to{stroke-dashoffset:-18}}')

exec(open('scenes2.py').read())

if __name__ == '__main__':
    open('out/01-rack-stack.svg', 'w').write(scene_rack_stack())
    open('out/02-power-cooling.svg', 'w').write(scene_cooling())
    open('out/03-fabric.svg', 'w').write(scene_fabric())
    open('out/04-bring-up.svg', 'w').write(scene_bringup())
    open('out/05-acceptance.svg', 'w').write(scene_accept())
