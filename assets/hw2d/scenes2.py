def line3(sc, pts, cls='', stroke='#34d399', width=2.0, opacity=1.0, extra=''):
    d = 'M' + ' L'.join(f'{sc.P(*p)[0]:.1f} {sc.P(*p)[1]:.1f}' for p in pts)
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-opacity="{opacity}" stroke-linejoin="round" stroke-linecap="round" class="{cls}" {extra}/>'

def pipe(sc, pts, grad='#34d399', core='#a7f3d0', w=7, flow=True):
    out = line3(sc, pts, stroke='#04070d', width=w + 3) + line3(sc, pts, stroke=grad, width=w) + line3(sc, pts, stroke=core, width=w * 0.28, opacity=.7)
    if flow: out += line3(sc, pts, cls='pflow', stroke='#ecfdf5', width=w * 0.35, opacity=.9)
    return out

PFLOW = '.pflow{stroke-dasharray:6 22;animation:pf 1.4s linear infinite}@keyframes pf{to{stroke-dashoffset:-28}}.pflow.rev{animation-direction:reverse}'

def busway(sc, x0, x1, y, z):
    box(sc, x0, y, z, x1 - x0, 1.2, 0.9, front='url(#plateDark)', side='url(#mSide)', depth=400,
        fdetail=''.join(f'<rect x="{0.6+i*0.9:.1f}" y=".3" width=".5" height=".3" fill="#0a0e16"/>' for i in range(int((x1-x0)/0.9)-1)))

def scene_cooling():
    sc = Scene(s=15, ox=520, oy=430)
    rnd = random.Random(11)
    floor(sc, -8, -6, 40, 30)
    for i, x in enumerate([-2, 4.6]):
        rack(sc, x, 0, rnd=rnd, depth=i)
    # CDU to the right
    cdu_front = ('<rect x=".5" y=".6" width="4.2" height="2.4" rx=".1" fill="#05080f" stroke="#34d399" stroke-opacity=".5" stroke-width=".05"/>'
                 '<text x=".85" y="1.45" class="txt" font-size=".5" fill="#6ee7b7" letter-spacing=".05">CDU-01</text>'
                 '<rect x=".85" y="1.9" width="2.6" height=".18" fill="#0f2a22"/><rect x=".85" y="1.9" width="1.9" height=".18" fill="#34d399" class="ledb2"/>'
                 '<rect x=".85" y="2.35" width="2.6" height=".18" fill="#0f2a22"/><rect x=".85" y="2.35" width="2.3" height=".18" fill="#34d399"/>'
                 '<circle cx="1.4" cy="4.4" r=".75" fill="#0a0f19" stroke="#5b6a85" stroke-width=".08"/><path d="M1.4 4.4 L1.85 3.95" stroke="#6ee7b7" stroke-width=".08"/>'
                 '<circle cx="3.6" cy="4.4" r=".75" fill="#0a0f19" stroke="#5b6a85" stroke-width=".08"/><path d="M3.6 4.4 L3.2 3.9" stroke="#93c5fd" stroke-width=".08"/>'
                 '<rect x=".5" y="5.8" width="4.2" height="5.4" fill="url(#vents)"/>')
    cdu_top = ''.join(f'<circle cx="{1.4+k*2.4}" cy="2.2" r="1.0" fill="#0a0e16" stroke="#3b475c" stroke-width=".06"/><circle cx="{1.4+k*2.4}" cy="2.2" r=".25" fill="#5b6a85"/>' for k in range(2))
    box(sc, 17, 2, 0, 5.2, 5, 12, front='url(#plate)', fdetail=cdu_front, tdetail=cdu_top, depth=5)
    # manifold on rack 2 side face (x = 10.6), supply green + return blue down the side, hoses to CDU
    xs = 10.6 + 0.05
    sup = [(xs, 2.0, 21), (xs, 2.0, 3), (xs + 2.0, 2.0, 1.2), (17, 3.2, 1.2)]
    ret = [(xs, 3.6, 21), (xs, 3.6, 4.5), (xs + 2.5, 3.6, 2.6), (17, 4.4, 2.6)]
    taps = ''.join(line3(sc, [(xs, 2.0, z), (xs + 0.6, 2.0, z)], stroke='#34d399', width=3) + line3(sc, [(xs, 3.6, z - .4), (xs + 0.6, 3.6, z - .4)], stroke='#60a5fa', width=3) for z in (18.5, 14.3, 10.1, 5.9))
    sc.add(4, pipe(sc, ret, grad='#2563eb', core='#93c5fd', w=7).replace('class="pflow"', 'class="pflow rev"') + pipe(sc, sup) + taps)
    # overhead busway + tap-off cables to racks
    busway(sc, -4, 24, -2.5, 25)
    po = ''.join(line3(sc, [(x + 3, -1.5, 25), (x + 3, -1.5, 22)], stroke='#fbbf24', width=1.6, opacity=.0) for x in (-2, 4.6))
    for x in (-2, 4.6):
        box(sc, x + 2.2, -2.2, 23.6, 1.6, 1.0, 1.4, front='url(#plateDark)', fdetail='<circle cx=".8" cy=".7" r=".18" class="led"/>', depth=401)
    sc.add(402, ''.join(line3(sc, [(x + 3.0, -1.2, 23.6), (x + 3.0, 1.5, 22.0)], stroke='#6ee7b7', width=2, opacity=.75) for x in (-2, 4.6)))
    # flow labels
    p = sc.P(17.5, 3.2, 1.2); q = sc.P(17.5, 4.4, 2.6)
    sc.overlay.append(f'<g class="txt" font-size="13" letter-spacing="2"><text x="{p[0]-150:.0f}" y="{p[1]+40:.0f}" fill="#6ee7b7">SUPPLY</text><text x="{q[0]-150:.0f}" y="{q[1]+70:.0f}" fill="#93c5fd">RETURN</text></g>')
    return sc.render(extra_style=PFLOW)

def switch_box(sc, x, y, z, w=7, d=4, rnd=None, depth=None, ports=16):
    box(sc, x, y, z, w, d, 0.9, front='url(#plateDark)', fdetail=switch_face(0.1, 0.1, w - 0.2, h=0.7, ports=ports, lit=.9, rnd=rnd), depth=depth)

def scene_fabric():
    sc = Scene(s=11.5, ox=560, oy=560)
    rnd = random.Random(5)
    floor(sc, -14, -10, 40, 30)
    xs = [-6, 0.6, 7.2, 13.8]
    for i, x in enumerate(xs):
        rack(sc, x, 2, rnd=rnd, depth=i)
    # leaf switches above each rack, spines further back and higher
    leafs = [(x - 0.5, 4.5, 25.5) for x in xs]
    spines = [(-4, -6, 34), (9, -6, 34)]
    for i, (x, y, z) in enumerate(spines):
        switch_box(sc, x, y, z, w=8, d=5, rnd=rnd, depth=100 + i, ports=20)
    for i, (x, y, z) in enumerate(leafs):
        switch_box(sc, x, y, z, rnd=rnd, depth=200 + i)
    links = []
    for li, (lx, ly, lz) in enumerate(leafs):
        for si, (sx, sy, sz) in enumerate(spines):
            a = (lx + 3.5, ly + 1.5, lz + 0.9); b = (sx + 4, sy + 2.5, sz)
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, max(a[2], b[2]) + 3)
            pts = [a, ((a[0]+mid[0])/2, (a[1]+mid[1])/2, mid[2] - 0.6), mid, ((b[0]+mid[0])/2, (b[1]+mid[1])/2, mid[2] - 0.6), b]
            col = '#34d399' if (li + si) % 2 == 0 else '#5eead4'
            links.append(line3(sc, pts, stroke=col, width=2.2, opacity=.55) + line3(sc, pts, cls='pk', stroke='#ecfdf5', width=2.6, extra=f'style="animation-delay:-{(li*2+si)*0.37:.2f}s"'))
        # leaf to rack drop
        links.append(line3(sc, [(lx + 3.5, ly + 1, lz), (lx + 3.5, ly + 1, 22)], stroke='#34d399', width=1.6, opacity=.6))
    sc.add(150, ''.join(links))
    sc.overlay.append('<g class="txt" font-size="13" letter-spacing="2.5" fill="#94a3b8">'
                      f'<text x="{sc.P(-2,-10,33)[0]:.0f}" y="{sc.P(-2,-10,33)[1]-6:.0f}">SPINE</text>'
                      f'<text x="{sc.P(-6.5,4.5,27.5)[0]-40:.0f}" y="{sc.P(-6.5,4.5,27.5)[1]:.0f}">LEAF</text></g>')
    return sc.render(extra_style='.pk{stroke-dasharray:3 60;animation:pk 2.2s linear infinite}@keyframes pk{to{stroke-dashoffset:-63}}')

def scene_bringup():
    sc = Scene(s=20, ox=430, oy=430)
    rnd = random.Random(9)
    floor(sc, -10, -8, 30, 24, step=2)
    W, D, H = 14, 18, 5.5
    # chassis walls (open lid): draw box without top detail, top as interior
    gpus = ''
    for r in range(2):
        for k in range(4):
            gx, gy = 0.9 + k * 3.1, 1.0 + r * 4.6
            gpus += (f'<rect x="{gx}" y="{gy}" width="2.6" height="4.0" rx=".1" fill="#1a2232" stroke="#3b475c" stroke-width=".05"/>'
                     + ''.join(f'<rect x="{gx+0.2}" y="{gy+0.25+j*0.32:.2f}" width="2.2" height=".16" fill="#2c3850"/>' for j in range(11))
                     + f'<rect x="{gx+0.3}" y="{gy+3.75}" width="2.0" height=".12" class="led {"ledb" if (r+k)%3==0 else ""}"/>')
    sw = ''.join(f'<rect x="{3.2+k*4.6}" y="10.6" width="3" height="2" rx=".1" fill="#121a28" stroke="#34d399" stroke-opacity=".7" stroke-width=".06"/><rect x="{3.6+k*4.6}" y="10.95" width="2.2" height="1.3" fill="#22304a"/>' for k in range(2))
    nics = ''.join(f'<rect x="{0.8+k*1.6}" y="14.2" width="1.2" height="2.6" rx=".08" fill="#0f1726" stroke="#6ee7b7" stroke-opacity=".55" stroke-width=".05"/><circle cx="{1.4+k*1.6}" cy="16.3" r=".13" class="led"/>' for k in range(8))
    top = f'<rect width="{W}" height="{D}" fill="#0a0f19"/><rect x=".4" y=".4" width="{W-0.8}" height="{D-0.8}" fill="#0f1522" stroke="#1f2a3d" stroke-width=".06"/>' + gpus + sw + nics
    front = node_face(0, 0, W, H, rnd)
    box(sc, 0, 0, 0, W, D, H, top='#0a0f19', front='url(#plate)', fdetail=front, tdetail=top, depth=1)
    # lifted lid floating above
    sc.overlay.append('')
    lid = sc
    # HUD checklist (flat overlay)
    items = [('Firmware baseline', 1.0, True), ('OS image', 1.0, True), ('Burn-in', 0.72, False), ('NCCL all-reduce', 0.46, False)]
    hud = ['<g class="txt" transform="translate(780 170)">',
           '<rect width="360" height="300" rx="14" fill="#060a14" fill-opacity=".82" stroke="#34d399" stroke-opacity=".35"/>',
           '<rect width="360" height="300" rx="14" fill="url(#sheen)"/>',
           '<text x="24" y="40" font-size="13" letter-spacing="3" fill="#6ee7b7">NODE BRING-UP</text>',
           '<text x="24" y="62" font-size="12" letter-spacing="1.5" fill="#64748b">HGX B300 · RACK 03 · U12</text>']
    for i, (label, pct, done) in enumerate(items):
        y = 100 + i * 48
        hud.append(f'<text x="24" y="{y}" font-size="15" fill="#e2e8f0">{label}</text>')
        hud.append(f'<text x="336" y="{y}" font-size="13" text-anchor="end" fill="{"#34d399" if done else "#94a3b8"}">{"PASS" if done else str(int(pct*100))+"%"}</text>')
        hud.append(f'<rect x="24" y="{y+10}" width="312" height="6" rx="3" fill="#13203a"/>')
        hud.append(f'<rect x="24" y="{y+10}" width="{312*pct:.0f}" height="6" rx="3" fill="#34d399" class="{"" if done else "grow"}" style="--w:{312*pct:.0f}px"/>')
    hud.append('</g>')
    sc.overlay.append(''.join(hud))
    # connector line from HUD to node
    a = sc.P(W, D * 0.35, H); sc.overlay.append(f'<path d="M780 300 L{a[0]+30:.0f} {a[1]-10:.0f}" stroke="#34d399" stroke-opacity=".5" stroke-dasharray="3 5" fill="none"/><circle cx="{a[0]+30:.0f}" cy="{a[1]-10:.0f}" r="4" fill="#34d399" filter="url(#glow)"/>')
    return sc.render(extra_style='.grow{animation:grow 3.5s ease-in-out infinite alternate}@keyframes grow{from{width:0}}')

def scene_accept():
    sc = Scene(s=11, ox=520, oy=500)
    rnd = random.Random(21)
    floor(sc, -16, -16, 50, 40)
    k = 0
    for row in range(2):
        for i in range(6):
            rack(sc, -10 + i * 6.6, -8 + row * 16, rnd=rnd, depth=row * 10 + i); k += 1
    # cables between rows
    sc.add(50, ''.join(line3(sc, [(-10 + i * 6.6 + 3, 3, 22), (-10 + i * 6.6 + 3, 5.5, 25), (-10 + i * 6.6 + 3, 8, 22)], stroke='#34d399', width=1.8, opacity=.7) for i in range(6)))
    badge = ('<g class="txt" transform="translate(800 150)">'
             '<circle cx="110" cy="110" r="96" fill="#34d399" fill-opacity=".08" filter="url(#glowBig)"/>'
             '<circle cx="110" cy="110" r="78" fill="#060a14" stroke="#34d399" stroke-width="2.5"/>'
             '<circle cx="110" cy="110" r="66" fill="none" stroke="#34d399" stroke-opacity=".35" stroke-dasharray="3 6" class="spin"/>'
             '<path d="M78 112 L101 135 L145 88" fill="none" stroke="#6ee7b7" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>'
             '<text x="110" y="232" text-anchor="middle" font-size="15" letter-spacing="4" fill="#e2e8f0">ACCEPTED</text>'
             '<text x="110" y="256" text-anchor="middle" font-size="11.5" letter-spacing="2" fill="#64748b">HANDED OVER WITH MONITORING</text></g>')
    sc.overlay.append(badge)
    return sc.render(extra_style='.spin{transform-origin:110px 110px;animation:spin 18s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}')
