# เพิ่มฉาก "บ้าน" (ค่าเริ่มต้น) คู่กับ "โรงงาน" ใน home.src.html — รันครั้งเดียว
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = 'home.src.html'
s = open(P, encoding='utf8').read()

def R(a, b, cnt=1):
    global s
    assert a in s, 'MISSING: ' + a[:90]
    s = s.replace(a, b, cnt)

# ================= HTML: site selector, labels, panel starts folded
R('''        <div class="grp">
          <span class="gl-l" id="lMode">ชนิดระบบ</span>''', '''        <div class="grp">
          <span class="gl-l" id="lSite">สถานที่</span>
          <div class="seg3" id="siteRow" role="group" aria-labelledby="lSite">
            <button type="button" id="sHome" data-v="house" aria-pressed="true"><span class="ms">home</span>บ้าน</button>
            <button type="button" id="sFac" data-v="factory" aria-pressed="false"><span class="ms">factory</span>โรงงาน</button>
          </div>
        </div>
        <div class="grp">
          <span class="gl-l" id="lMode">ชนิดระบบ</span>''')
R('<input type="range" id="size" min="1" max="10" step="1" value="6">', '<input type="range" id="size" min="3" max="10" step="1" value="5">')
R('<div class="size-out"><b id="sizeKwp">160 kWp</b><span id="sizePanels">276 แผง</span></div>', '<div class="size-out"><b id="sizeKwp">5 kW</b><span id="sizePanels">8 แผง</span></div>')
R('<button type="button" class="fold-h" id="designFold" aria-expanded="true">', '<button type="button" class="fold-h" id="designFold" aria-expanded="false">')
R('<aside class="design" aria-label="ออกแบบระบบ">', '<aside class="design collapsed" aria-label="ออกแบบระบบ">')
s = re.sub(r'(<div class="gl" id="gl" role="img" aria-label=")[^"]*"', r'\1ภาพสามมิติจำลองบ้านและโรงงานติดโซล่าเซลล์ ปรับสถานที่ เวลา ขนาดติดตั้ง และชนิดระบบได้"', s, count=1)
R('<i class="d-grid"></i>การไฟฟ้า<b id="hGrid">', '<i class="d-grid"></i><span id="hGridL">การไฟฟ้า</span><b id="hGrid">')
s = re.sub(r'<div class="mix-l">[^<]*<b id="hLoad">', '<div class="mix-l"><span id="hLoadL">บ้านใช้ไฟ</span> <b id="hLoad">', s, count=1)
# panel folded by default on every screen (tap / click the header to open)
R("    if (overlay.matches) later(8000); else set(true);           // จอแคบ: เริ่มแบบพับไว้ แตะเพื่อเปิด",
  "    set(true);                                                  // เริ่มแบบพับไว้ทุกจอ แตะ/คลิกหัวแผงเพื่อเปิด")

# ================= groups: factory vs house
R("  function add(geo, mat, x, y, z, o){", "  var factoryG = new THREE.Group(), houseG = new THREE.Group(), CUR = scene;\n  scene.add(factoryG); scene.add(houseG);\n  function add(geo, mat, x, y, z, o){")
R("    (o.parent || scene).add(m); return m;", "    (o.parent || CUR).add(m); return m;")
R("  add(new THREE.PlaneGeometry(112, 70), M.conc, -6, .03, 6, { rx: -Math.PI / 2, cast: false });",
  "  add(new THREE.PlaneGeometry(112, 70), M.conc, -6, .03, 6, { rx: -Math.PI / 2, cast: false, parent: factoryG });")
R("  // ---------- factory\n", "  // ---------- factory\n  CUR = factoryG;\n")
R("var m = new THREE.Mesh(g, M.gable); m.castShadow = true; m.receiveShadow = true; scene.add(m);",
  "var m = new THREE.Mesh(g, M.gable); m.castShadow = true; m.receiveShadow = true; factoryG.add(m);")
R("    [glassIM, frameIM].forEach(function(m){ m.castShadow = true; m.receiveShadow = true; scene.add(m); });",
  "    [glassIM, frameIM].forEach(function(m){ m.castShadow = true; m.receiveShadow = true; factoryG.add(m); });")
R("    scene.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0x2b2b2b })));",
  "    factoryG.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0x2b2b2b })));")
R("  var bess = new THREE.Group(); scene.add(bess);", "  var bess = new THREE.Group(); factoryG.add(bess);")

# ================= house scene
HOUSE = r'''
  // ---------- house (2 storeys, gable roof facing south, carport, fence, PEA pole + meter)
  CUR = houseG;
  var hM = { wall: std({ color: 0xf0e9dd, roughness: .85 }), trim: std({ color: 0x8a7a66, roughness: .8 }), tile: std({ color: 0x4b525c, roughness: .62, metalness: .12 }),
             fence: std({ color: 0xf4f4f2, roughness: .9 }), car: std({ color: 0xb8bec6, roughness: .3, metalness: .6 }) };
  var HL = 11, HD = 8, HH = 6.2, HZ = -1, HP = Math.PI / 6, HRISE = (HD / 2) * Math.tan(HP), HSL = (HD / 2) / Math.cos(HP), HOV = .7;
  add(new THREE.PlaneGeometry(26, 22), M.conc, 2, .025, 1, { rx: -Math.PI / 2, cast: false });
  add(new THREE.PlaneGeometry(14, 5), M.grass, -2, .04, 7.3, { rx: -Math.PI / 2, cast: false });
  add(B(HL, HH, HD), hM.wall, 0, HH / 2, HZ);
  add(B(HL + .2, .35, HD + .2), hM.trim, 0, 3.1, HZ);                                  // floor band
  (function(){
    var g = new THREE.BufferGeometry(), hw = HD / 2, x = HL / 2;
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array([x, HH, HZ - hw, x, HH, HZ + hw, x, HH + HRISE, HZ, -x, HH, HZ + hw, -x, HH, HZ - hw, -x, HH + HRISE, HZ]), 3));
    g.computeVertexNormals();
    var m = new THREE.Mesh(g, hM.wall); m.castShadow = true; m.receiveShadow = true; houseG.add(m);
  })();
  [1, -1].forEach(function(sign){
    add(new THREE.PlaneGeometry(HL + 1.2, HSL + HOV), hM.tile, 0, HH + HRISE / 2 - HOV * Math.sin(HP) / 2, HZ + sign * (HD / 4 + HOV * Math.cos(HP) / 2), { rx: -Math.PI / 2 + sign * HP });
  });
  add(B(HL + 1.25, .22, .35), hM.tile, 0, HH + HRISE + .05, HZ);
  // windows + door (south face z = HZ + HD/2), glow at night via M.win
  var zf = HZ + HD / 2 + .05;
  [-3.6, -1.2, 1.2, 3.6].forEach(function(x){ add(B(1.5, 1.3, .1), M.win, x, 4.6, zf, { cast: false }); });
  [-3.6, 3.6].forEach(function(x){ add(B(1.6, 1.5, .1), M.win, x, 1.6, zf, { cast: false }); });
  add(B(1.2, 2.3, .1), hM.trim, 0, 1.15, zf, { cast: false });
  add(B(1.3, .08, 1.4), hM.fence, -1.2, 3.25, zf + .7);                                // balcony slab
  add(B(3.4, .9, .06), M.glass, -1.2, 3.75, zf + 1.38, { cast: false });
  // carport + car
  add(B(5.2, .2, 6.4), hM.fence, 8.4, 2.9, 2.2);
  [[6.1, -.7], [10.7, -.7], [6.1, 5.1], [10.7, 5.1]].forEach(function(p){ add(B(.18, 2.8, .18), hM.fence, p[0], 1.4, p[1]); });
  add(B(1.8, .75, 4.3), hM.car, 8.4, .75, 2.3); add(B(1.6, .6, 2.2), M.glass, 8.4, 1.4, 2.1);
  [[7.6, 1], [9.2, 1], [7.6, 3.6], [9.2, 3.6]].forEach(function(p){ add(new THREE.CylinderGeometry(.33, .33, .22, 14), M.dark, p[0], .33, p[1]).rotation.z = Math.PI / 2; });
  // fence (gap for the gate at the front)
  [[2, -10, 26, .15], [-11, 1, .15, 22], [15, 1, .15, 22]].forEach(function(f){ add(B(f[2], 1.2, f[3]), hM.fence, f[0], .6, f[1]); });
  add(B(9, 1.2, .15), hM.fence, -6.5, .6, 12); add(B(5.5, 1.2, .15), hM.fence, 12.25, .6, 12);
  // PEA pole + meter at the front, service wire to the house
  add(new THREE.CylinderGeometry(.13, .17, 8, 10), M.pole, 13.2, 4, 13);
  add(B(.4, .55, .22), M.white, 13.2, 1.5, 12.82);
  houseG.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(13.2, 7.6, 13), new THREE.Vector3(9.5, 6.9, 7), new THREE.Vector3(5.6, 5.8, 2.4)]), new THREE.LineBasicMaterial({ color: 0x2b2b2b })));
  // inverter + consumer unit on the east wall (x = HL/2)
  var xe = HL / 2;
  add(B(.18, .62, .46), M.white, xe + .09, 1.75, 1.3); add(B(.02, .06, .06), M.led, xe + .19, 1.95, 1.3, { cast: false });
  add(B(.14, .5, .42), M.steel, xe + .07, 1.45, 2.35);
  var hBess = new THREE.Group(); houseG.add(hBess);
  add(B(.24, 1.1, .7), M.bess, xe + .12, .75, -.2, { parent: hBess }); add(B(.02, .5, .08), M.purple, xe + .25, 1, -.2, { parent: hBess, cast: false });
  // panels on the south roof plane: bottom row first, each row filled from the middle outwards
  var HCOLS = 8, HROWS = 2, HMAX = HCOLS * HROWS, HPW = 1.13, HPL = 2.28;
  var hGlass = new THREE.InstancedMesh(B(HPW, .04, HPL), M.panel, HMAX), hFrame = new THREE.InstancedMesh(B(HPW + .04, .035, HPL + .04), M.frame, HMAX);
  (function(){
    var d = new THREE.Object3D(), k = 0, order = [3, 4, 2, 5, 1, 6, 0, 7];
    var normal = new THREE.Vector3(0, Math.cos(HP), Math.sin(HP)), down = new THREE.Vector3(0, -Math.sin(HP), Math.cos(HP));
    for (var r = HROWS - 1; r >= 0; r--) order.forEach(function(c){
      var u = (c - (HCOLS - 1) / 2) * (HPW + .06), v = .45 + HPL / 2 + r * (HPL + .05);
      d.position.set(u, HH + HRISE, HZ).addScaledVector(down, v).addScaledVector(normal, .14);
      d.rotation.set(HP, 0, 0); d.updateMatrix(); hGlass.setMatrixAt(k, d.matrix);
      d.position.addScaledVector(normal, -.02); d.updateMatrix(); hFrame.setMatrixAt(k, d.matrix); k++;
    });
    [hGlass, hFrame].forEach(function(m){ m.castShadow = true; m.receiveShadow = true; houseG.add(m); });
  })();
  function hRoofY(z){ return HH + HRISE - (z - HZ) * Math.tan(HP); }
  CUR = scene;
'''
R("  // night lights (no shadows, cheap)\n", HOUSE + "\n  // night lights (no shadows, cheap)\n")

# ================= flows per site
R("  function flow(points, color){", "  function flow(points, color, parent){")
R("    scene.add(base); scene.add(glow);", "    (parent || scene).add(base); (parent || scene).add(glow);")
old_F = re.search(r"  var F = \{\n    roof: flow\(.*?\n  \};\n", s, re.S)
assert old_F, 'flows block'
fac = old_F.group(0).replace("  var F = {", "  var FL = {};\n  FL.factory = {").replace(", 0xffb020)", ", 0xffb020, factoryG)") \
    .replace(", 0x2bd576)", ", 0x2bd576, factoryG)").replace(", 0x3b9cff)", ", 0x3b9cff, factoryG)").replace(", 0xa77bff)", ", 0xa77bff, factoryG)")
fac += '''  FL.house = {
    roof: flow([[3.2, hRoofY(1.3) + .38, 1.3], [xe + .35, hRoofY(1.3) - .1, 1.3], [xe + .35, 2.1, 1.3]], 0xffb020, houseG),
    inv: flow([[xe + .35, 1.5, 1.55], [xe + .35, 1.5, 2.1]], 0xffb020, houseG),
    load: flow([[xe + .35, 1.2, 2.6], [xe + .35, 1.2, HZ + HD / 2 + .35], [xe - 1.2, 1.2, HZ + HD / 2 + .35]], 0x2bd576, houseG),
    grid: flow([[13.2, 6.6, 13.15], [13.2, .3, 13.15], [11.4, .3, 13.15], [11.4, .3, 6.2], [xe + .45, .3, 6.2], [xe + .45, .3, 2.35], [xe + .45, 1.2, 2.35]], 0x3b9cff, houseG),
    bat: flow([[xe + .35, 1.05, 2.1], [xe + .35, 1.05, .2]], 0xa77bff, houseG)
  };
  var F = FL.house;
'''
s = s[:old_F.start()] + fac + s[old_F.end():]

# ================= energy model (site aware; houses may export surplus in On-Grid)
old_E = re.search(r"  // ---------- energy model.*?\n  function drawChart\(\)\{.*?\n  \}\n", s, re.S)
assert old_E, 'energy block'
s = s[:old_E.start()] + r'''  // ---------- energy model (illustrative; factory load stays above PV so nothing is exported, a house may export its daytime surplus)
  var site = 'house', mode = 'ongrid', sizeBy = { house: 5, factory: 6 }, KWP, NP, PEAK, CAP, PMAX, LREF, sim = [];
  var STEP = 1 / 12;                                   // 5-minute steps
  function pvAt(t){ var a = (t - 6) / 12; return a <= 0 || a >= 1 ? 0 : PEAK * Math.pow(Math.sin(Math.PI * a), 1.2); }
  function loadAt(t){
    if (site === 'house'){
      if (t < 6) return .8; if (t < 8) return 1.5; if (t < 17) return 1.6; if (t < 18) return 2.2; if (t < 23) return 3.2; return 1.2;
    }
    var day = 250, night = 90;
    if (t >= 8 && t < 17) return day;
    if (t >= 6 && t < 8) return night + (day - night) * (t - 6) / 2;
    if (t >= 17 && t < 20) return day - (day - night) * (t - 17) / 3;
    return night;
  }
  function simulate(){
    var v = sizeBy[site];
    if (site === 'house'){ KWP = v; NP = Math.min(HMAX, Math.ceil(v * 1000 / 640)); PEAK = KWP * .85; CAP = KWP * 2; PMAX = KWP * .6; LREF = 3.2; }
    else { NP = v * COLS; KWP = Math.round(NP * .58); PEAK = KWP * .88; CAP = Math.round(KWP * 1.5); PMAX = CAP * .3; LREF = 250; }
    var soc = .1, out = [];
    for (var day = 0; day < 3; day++) for (var s = 0; s <= 288; s++){
      var t = s * STEP, pv = pvAt(t), ld = loadAt(t), bat = 0;
      if (mode === 'hybrid'){
        if (site === 'house'){
          if (pv > ld && soc < 1) bat = Math.min(pv - ld, PMAX, (1 - soc) * CAP / STEP);          // charge from surplus
          else if (pv < ld && soc > .1) bat = -Math.min(ld - pv, PMAX, (soc - .1) * CAP / STEP);  // cover the evening
        } else {
          if (pv > 1 && soc < 1){ bat = Math.min(pv * .5, PMAX, (1 - soc) * CAP / STEP); }
          else if (pv < 5 && soc > .1){ bat = -Math.min(PMAX, ld * .5, (soc - .1) * CAP / STEP); }
        }
        soc = Math.min(1, Math.max(.1, soc + bat * STEP / CAP));
      }
      var pvUse = Math.min(pv - Math.max(bat, 0), ld), fromBat = Math.max(-bat, 0);
      var grid = Math.max(0, ld - pvUse - fromBat), exp = Math.max(0, pv - pvUse - Math.max(bat, 0));
      if (day === 2) out.push({ pv: pv, ld: ld, use: pvUse, bat: bat, grid: grid, exp: exp, soc: soc });
    }
    sim = out;
    var house = site === 'house';
    (house ? hGlass : glassIM).count = (house ? hFrame : frameIM).count = NP;
    if (renderer) renderer.shadowMap.needsUpdate = true;
    $('sizeKwp').textContent = house ? KWP + ' kW' : KWP + ' kWp'; $('sizePanels').textContent = NP + ' แผง';
    $('hKwp').textContent = 'ระบบตัวอย่าง ' + (house ? 'บ้าน ' + KWP + ' kW' : 'โรงงาน ' + KWP + ' kWp') + ' · ' + (mode === 'hybrid' ? 'Hybrid' : 'On-Grid');
    $('hLoadL').textContent = house ? 'บ้านใช้ไฟ' : 'โรงงานใช้ไฟ';
    bess.visible = hBess.visible = mode === 'hybrid';
    $('rowBat').hidden = $('socRow').hidden = mode !== 'hybrid';
    PINS[4].el.style.visibility = mode === 'hybrid' ? '' : 'hidden';
    $('modeDesc').textContent = house
      ? (mode === 'hybrid' ? 'ไฟที่เหลือตอนกลางวันเก็บลงแบตเตอรี่ แล้วนำมาใช้ตอนค่ำที่เปิดแอร์' : 'กลางวันใช้ไฟจากแผงก่อน ไฟส่วนที่เหลือไหลเข้าระบบการไฟฟ้า กลางคืนใช้ไฟการไฟฟ้าตามปกติ')
      : (mode === 'hybrid' ? 'แผงชาร์จแบตเตอรี่ช่วงกลางวัน แล้วแบตจ่ายไฟให้โรงงานตอนเย็นและกลางคืน' : 'ไฟจากแผงเข้าโรงงานโดยตรงช่วงกลางวัน ส่วนที่ไม่พอใช้ไฟจากการไฟฟ้า');
    PINS[0].d = (house ? KWP + ' kW' : KWP + ' kWp') + ' · ' + NP + ' แผง ' + (house ? 'บนหลังคาบ้านด้านรับแดด' : 'บนหลังคาเมทัลชีท') + ' กระจกแผงสะท้อนท้องฟ้าตามเวลาในฉาก';
    PINS[4].d = 'ความจุ ' + CAP + ' kWh เก็บไฟจากแผงช่วงกลางวัน จ่ายให้' + (house ? 'บ้าน' : 'โรงงาน') + 'ตอนแดดหมด';
    drawChart();
  }
  function at(t){ var i = Math.min(287, Math.max(0, Math.floor(t / STEP))), f = t / STEP - i, a = sim[i], b = sim[i + 1] || a, o = {};
    for (var k in a) o[k] = a[k] + (b[k] - a[k]) * f; return o; }
  var CHART_MAX = 1;
  function drawChart(){
    CHART_MAX = Math.max(PEAK, LREF) * 1.05;
    var pv = [], ld = [];
    for (var i = 0; i <= 288; i += 3){ var x = (4 + 152 * i / 288).toFixed(1); pv.push(x + ' ' + (40 - sim[i].pv / CHART_MAX * 34).toFixed(1)); ld.push(x + ' ' + (40 - sim[i].ld / CHART_MAX * 34).toFixed(1)); }
    $('hCurve').setAttribute('d', 'M' + pv.join(' L')); $('hArea').setAttribute('d', 'M' + pv.join(' L') + ' L156 40 L4 40 Z');
    $('hLoadC').setAttribute('d', 'M' + ld.join(' L'));
  }
''' + s[old_E.end():]

# ================= pins per site
old_P = re.search(r"  var PINS = \[\n.*?\n  \];\n", s, re.S)
assert old_P, 'pins'
fac_pins = old_P.group(0).replace("  var PINS = [", "  var PIN_SETS = {};\n  PIN_SETS.factory = [")
s = s[:old_P.start()] + fac_pins + '''  PIN_SETS.house = [
    { p: [0, hRoofY(1.1) + .8, 1.1], t: 'แผงโซล่าเซลล์ Tier 1', d: '' },
    { p: [xe + .3, 2.45, 1.3], t: 'อินเวอร์เตอร์', d: 'แปลงไฟ DC จากแผงเป็นไฟ AC ที่เครื่องใช้ไฟฟ้าในบ้านใช้ได้' },
    { p: [xe + .3, 2.05, 2.5], t: 'ตู้ไฟในบ้าน', d: 'รวมไฟจากแผง แบตเตอรี่ และการไฟฟ้า บ้านใช้ไฟจากแผงก่อนเสมอ' },
    { p: [13.2, 8.4, 13], t: 'มิเตอร์และระบบการไฟฟ้า', d: 'กลางคืนบ้านใช้ไฟจากการไฟฟ้าตามปกติ ส่วนกลางวันไฟที่เหลือจากแผงไหลกลับเข้าระบบ' },
    { p: [xe + .3, 1.7, -.2], t: 'แบตเตอรี่ (Hybrid)', d: '', cls: 'bat' }
  ];
  var PINS = PIN_SETS.house.map(function(p){ return { p: p.p, t: p.t, d: p.d, cls: p.cls }; });
''' + s[old_P.end():]

# ================= site switching (camera, shadows, pins, flows, slider)
SITE = r'''
  var VIEWS = {
    house: { pos: new THREE.Vector3(21, 12.5, 26), target: new THREE.Vector3(1.5, 3.2, 1), min: 9, max: 60, sh: 22, sun: new THREE.Vector3(1.5, 0, 1) },
    factory: { pos: new THREE.Vector3(74, 30, 84), target: new THREE.Vector3(-2, 5, 3), min: 38, max: 190, sh: 78, sun: new THREE.Vector3(-8, 0, 6) }
  };
  function setSite(v, instant){
    site = v;
    factoryG.visible = v === 'factory'; houseG.visible = v === 'house';
    F = FL[v];
    var V = VIEWS[v];
    controls.minDistance = V.min; controls.maxDistance = V.max;
    HOME.pos.copy(V.pos); HOME.target.copy(V.target);
    controls.target.copy(V.target);
    if (instant) camera.position.copy(V.pos); else zoomTo = V.pos.clone();
    sc.left = -V.sh; sc.right = V.sh; sc.top = V.sh * .8; sc.bottom = -V.sh * .8; sc.updateProjectionMatrix();
    sun.target.position.copy(V.sun); sun.target.updateMatrixWorld();
    PIN_SETS[v].forEach(function(src, i){ var pin = PINS[i]; pin.t = src.t; pin.d = src.d; pin.v.fromArray(src.p); pin.el.setAttribute('aria-label', src.t); });
    var sz = $('size');
    if (v === 'house'){ sz.min = 3; sz.max = 10; } else { sz.min = 1; sz.max = 10; }
    sz.value = sizeBy[v];
    Object.keys(FL).forEach(function(k){ if (k !== v) for (var n in FL[k]) FL[k][n].base.visible = FL[k][n].glow.visible = false; });
    simulate(); kick();
  }
'''
R("  // ---------- UI\n", SITE + "\n  // ---------- UI\n")
R("  $('size').addEventListener('input', function(){ rows = +this.value; simulate(); kick(); });",
  "  $('size').addEventListener('input', function(){ sizeBy[site] = +this.value; simulate(); kick(); });\n"
  "  $('siteRow').addEventListener('click', function(e){ var b = e.target.closest('button'); if (!b || b.dataset.v === site) return; press(this, b); setSite(b.dataset.v); controls.autoRotate = false; clearTimeout(resumeTimer); resumeTimer = setTimeout(function(){ controls.autoRotate = playing && !reduce; kick(); }, 4000); });")

# ================= per-frame update: site-relative references, export direction, decimals for houses
R("""    drive(F.load, s.ld, 250, dt);
    drive(F.grid, s.grid, 250, dt);""", """    drive(F.load, s.ld, LREF, dt);
    var exporting = s.exp > s.grid;
    drive(F.grid, exporting ? s.exp : s.grid, LREF, dt, exporting ? -1 : 1);""")
R("  function drive(fl, kw, ref, dt, dir){\n    var on = kw >= .5;", "  function drive(fl, kw, ref, dt, dir){\n    var on = kw >= ref * .02;")
R("""    setTxt('hPow', String(Math.round(s.pv)));
    setTxt('hLoad', String(Math.round(s.ld) + ' kW'));
    setTxt('hUse', String(Math.round(s.use) + ' kW'));
    setTxt('hGrid', String(Math.round(s.grid) + ' kW'));""", """    var q = site === 'house' ? function(x){ return (Math.round(x * 10) / 10).toFixed(1); } : function(x){ return String(Math.round(x)); };
    setTxt('hPow', q(s.pv));
    setTxt('hLoad', q(s.ld) + ' kW');
    setTxt('hUse', q(s.use) + ' kW');
    setTxt('hGridL', exporting ? 'ส่งเข้าการไฟฟ้า' : 'การไฟฟ้า');
    setTxt('hGrid', q(exporting ? s.exp : s.grid) + ' kW');""")
R("      setTxt('hBat', String(s.bat > .5 ? '+' + Math.round(s.bat) + ' kW' : Math.round(fromBat) + ' kW'));",
  "      setTxt('hBat', s.bat > PMAX * .02 ? '+' + q(s.bat) + ' kW' : q(fromBat) + ' kW');")
R("      setTxt('hBatL', String(s.bat > .5 ? 'แบตเตอรี่ (กำลังชาร์จ)' : 'แบตเตอรี่'));",
  "      setTxt('hBatL', s.bat > PMAX * .02 ? 'แบตเตอรี่ (กำลังชาร์จ)' : 'แบตเตอรี่');")
R("$('hDot').setAttribute('cy', (40 - s.pv / 260 * 34).toFixed(1));", "$('hDot').setAttribute('cy', (40 - s.pv / CHART_MAX * 34).toFixed(1));")

# ================= boot: start on the house
R("  simulate(); resize(); setPlaying(playing);", "  setSite('house', true); resize(); setPlaying(playing);")
R("  var slider = $('clock'), out = $('clockOut'), playBtn = $('play');", "  var slider = $('clock'), out = $('clockOut'), playBtn = $('play');")
open(P, 'w', encoding='utf8').write(s)
print('ok; leftover rows refs:', len(re.findall(r'\brows\b', s)))
