  // ---------- house v2: modern Thai 2-storey home (gable roof to the south), single-storey wing, carport, garden, fence, PEA pole
  CUR = houseG;
  function ctex(w, h, draw, rep){ return tex(w, h, draw, { srgb: true, repeat: rep }); }
  var tileTex = ctex(64, 64, function(ctx, w, h){
    ctx.fillStyle = '#4a5058'; ctx.fillRect(0, 0, w, h);
    for (var y = 0; y < h; y += 16){
      var g = ctx.createLinearGradient(0, y, 0, y + 16); g.addColorStop(0, '#5a616a'); g.addColorStop(.8, '#454b53'); g.addColorStop(1, '#2f343a');
      ctx.fillStyle = g; ctx.fillRect(0, y, w, 16);
      for (var x = (y / 16) % 2 ? 0 : 16; x < w; x += 32){ ctx.fillStyle = 'rgba(0,0,0,.18)'; ctx.fillRect(x, y, 1.5, 16); }
    }
  }, [22, 10]);
  var stoneTex = ctex(128, 128, function(ctx, w, h){
    ctx.fillStyle = '#b9b2a6'; ctx.fillRect(0, 0, w, h);
    for (var y = 0; y < h; y += 16) for (var x = -Math.random() * 30; x < w; x += 22 + Math.random() * 24){
      var l = 150 + Math.random() * 60 | 0; ctx.fillStyle = 'rgb(' + l + ',' + (l - 6) + ',' + (l - 16) + ')'; ctx.fillRect(x + 1, y + 1, 20 + Math.random() * 22, 14);
    }
  }, [3, 1]);
  var woodTex = ctex(128, 16, function(ctx, w, h){
    for (var x = 0; x < w; x += 8){ var l = 120 + Math.random() * 30 | 0; ctx.fillStyle = 'rgb(' + (l + 40) + ',' + (l + 5) + ',' + (l - 40) + ')'; ctx.fillRect(x, 0, 6, h); ctx.fillStyle = '#3b2a1c'; ctx.fillRect(x + 6, 0, 2, h); }
  }, [2, 1]);
  var paverTex = ctex(64, 64, function(ctx, w, h){
    ctx.fillStyle = '#9d9a93'; ctx.fillRect(0, 0, w, h);
    for (var y = 0; y < h; y += 16) for (var x = (y / 16) % 2 ? -16 : 0; x < w; x += 32){ var l = 170 + Math.random() * 25 | 0; ctx.fillStyle = 'rgb(' + l + ',' + (l - 4) + ',' + (l - 10) + ')'; ctx.fillRect(x + 1, y + 1, 30, 14); }
  }, [6, 12]);
  var hM = {
    wall: std({ color: 0xf5f3ee, roughness: .92 }), wall2: std({ color: 0xdedbd4, roughness: .9 }),
    stone: std({ map: stoneTex, roughness: .95 }), wood: std({ map: woodTex, roughness: .7 }),
    tile: std({ map: tileTex, roughness: .6, metalness: .1 }), fascia: std({ color: 0xfbfbfa, roughness: .6 }), soffit: std({ color: 0xeceae5, roughness: .9 }),
    frame: std({ color: 0x33373c, roughness: .45, metalness: .6 }), rail: new THREE.MeshStandardMaterial({ color: 0xbfd4df, roughness: .05, metalness: .2, transparent: true, opacity: .35 }),
    pave: std({ map: paverTex, roughness: .95 }), fence: std({ color: 0xe9e7e2, roughness: .9 }), cap: std({ color: 0x6f6a63, roughness: .8 }),
    gate: std({ color: 0x2b2f33, roughness: .5, metalness: .5 }), sheet: std({ color: 0xc9ced3, roughness: .4, metalness: .7 }),
    car: std({ color: 0xf2f2f0, roughness: .25, metalness: .55 }), tint: std({ color: 0x1b2430, roughness: .08, metalness: .8 }), rubber: std({ color: 0x161616, roughness: .9 }),
    leaf: std({ color: 0xffffff, roughness: .95 }), trunk: std({ color: 0x6b5543, roughness: .95 }), door: std({ color: 0x5b3d26, roughness: .6 })
  };
  var HL = 11, HD = 8.5, HH = 6.4, HZ = -1.5, HP = 25 * Math.PI / 180, HRISE = (HD / 2) * Math.tan(HP), HOV = .95, HGO = .7;
  var zf = HZ + HD / 2, xe = HL / 2;

  // lot, lawn, driveway, path
  add(new THREE.PlaneGeometry(29, 23), M.conc, 1.5, .025, .5, { rx: -Math.PI / 2, cast: false });
  add(new THREE.PlaneGeometry(11.5, 7.5), M.grass, -5.5, .035, 7.9, { rx: -Math.PI / 2, cast: false });
  add(new THREE.PlaneGeometry(5.6, 11.5), hM.pave, 8.6, .04, 6.2, { rx: -Math.PI / 2, cast: false });
  add(new THREE.PlaneGeometry(1.6, 8.6), hM.pave, 1.2, .04, 7.4, { rx: -Math.PI / 2, cast: false }).material = hM.pave;

  // main 2-storey block + details
  add(B(HL, HH, HD), hM.wall, 0, HH / 2, HZ);
  add(B(HL + .12, .28, HD + .12), hM.wall2, 0, 3.25, HZ);                                   // floor line
  add(B(2.4, 3.1, .12), hM.wood, 1.9, 1.55, zf + .07, { cast: false });                     // wood slat accent by the door
  add(B(1.05, 2.3, .1), hM.door, 1.25, 1.15, zf + .12);
  add(B(2.6, .16, 1.5), hM.fascia, 1.5, 2.85, zf + .75); [.35, 2.65].forEach(function(x){ add(B(.1, 2.8, .1), hM.frame, x, 1.4, zf + 1.4); });
  add(B(HL + .02, .7, HD + .02), hM.stone, 0, .35, HZ, { cast: false });                    // stone plinth

  // gable end walls
  (function(){
    var g = new THREE.BufferGeometry(), hw = HD / 2, x = HL / 2;
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array([x, HH, HZ - hw, x, HH, HZ + hw, x, HH + HRISE, HZ, -x, HH, HZ + hw, -x, HH, HZ - hw, -x, HH + HRISE, HZ]), 3));
    g.computeVertexNormals(); var m = new THREE.Mesh(g, hM.wall); m.castShadow = true; m.receiveShadow = true; houseG.add(m);
  })();
  // roof: thick slabs (tile top, soffit bottom, white fascia edges) + ridge cap + rake boards
  var HSL = (HD / 2 + HOV) / Math.cos(HP);
  [1, -1].forEach(function(sign){
    var m = new THREE.Mesh(new THREE.BoxGeometry(HL + 2 * HGO, .16, HSL), [hM.fascia, hM.fascia, hM.tile, hM.soffit, hM.fascia, hM.fascia]);
    m.position.set(0, HH + HRISE - (HSL / 2) * Math.sin(HP) + .02, HZ + sign * (HSL / 2) * Math.cos(HP));
    m.rotation.x = sign * HP; m.castShadow = true; m.receiveShadow = true; houseG.add(m);
    var gut = add(B(HL + 2 * HGO, .22, .18), hM.fascia, 0, HH + HRISE - HSL * Math.sin(HP) - .02, HZ + sign * (HSL * Math.cos(HP) + .02));
  });
  add(B(HL + 2 * HGO + .05, .2, .42), hM.tile, 0, HH + HRISE + .12, HZ);

  // windows: glass (glows at night) with dark aluminium frames
  function win(x, y, z, w, h, axis, mull){
    var gl = axis === 'x' ? add(B(.06, h, w), M.win, x, y, z, { cast: false }) : add(B(w, h, .06), M.win, x, y, z, { cast: false });
    var t = .07, o = axis === 'x' ? [1, 0] : [0, 1];
    [[0, h / 2], [0, -h / 2]].forEach(function(p){ axis === 'x' ? add(B(.1, t, w + t), hM.frame, x, y + p[1], z, { cast: false }) : add(B(w + t, t, .1), hM.frame, x, y + p[1], z, { cast: false }); });
    [-w / 2, w / 2].concat(mull ? [0] : []).forEach(function(d){ axis === 'x' ? add(B(.1, h, t), hM.frame, x, y, z + d, { cast: false }) : add(B(t, h, .1), hM.frame, x + d, y, z, { cast: false }); });
  }
  win(-2.6, 1.55, zf + .04, 3.4, 2.5, 'z', true);                 // living room sliding door
  win(4.1, 1.8, zf + .04, 1.6, 1.4, 'z', false);
  win(-2.6, 4.75, zf + .04, 3.2, 2.3, 'z', true);                 // upper sliding door to balcony
  win(2.4, 5.0, zf + .04, 1.5, 1.4, 'z', false); win(4.3, 5.0, zf + .04, 1.2, 1.4, 'z', false);
  win(xe + .04, 5.0, -3.4, 1.4, 1.2, 'x', false); win(xe + .04, 5.0, -.4, 1.4, 1.2, 'x', false);
  win(-xe - .04, 5.0, -1.5, 1.8, 1.2, 'x', false);
  // balcony: slab + glass railing
  add(B(4.2, .2, 1.5), hM.fascia, -2.6, 3.42, zf + .75);
  add(B(4.2, 1.0, .04), hM.rail, -2.6, 4.02, zf + 1.48, { cast: false }); add(B(4.2, .05, .06), hM.frame, -2.6, 4.53, zf + 1.48, { cast: false });
  [-1.52, 1.52].forEach(function(d){ add(B(.04, 1.0, 1.45), hM.rail, -2.6 + d * 1.38, 4.02, zf + .77, { cast: false }); });

  // single-storey wing (west) with flat roof + parapet
  var wx0 = -xe - 5.2, wx1 = -xe, wz0 = HZ - 2.8, wz1 = zf + .6;
  add(B(wx1 - wx0, 3.5, wz1 - wz0), hM.wall, (wx0 + wx1) / 2, 1.75, (wz0 + wz1) / 2);
  add(B(wx1 - wx0 + .6, .45, wz1 - wz0 + .6), hM.fascia, (wx0 + wx1) / 2, 3.72, (wz0 + wz1) / 2);
  add(B(wx1 - wx0 - .4, 1.0, .1), hM.stone, (wx0 + wx1) / 2, .5, wz1 + .06, { cast: false });
  win((wx0 + wx1) / 2, 2.0, wz1 + .05, 3.8, 1.9, 'z', true);

  // carport (east): steel posts + metal-sheet roof + car
  add(B(5.8, .09, 6.8), hM.sheet, 8.6, 3.0, 2.4).rotation.x = -.05;
  add(B(5.9, .22, .12), hM.fascia, 8.6, 2.95, 5.8);
  [[6.0, -.8], [11.2, -.8], [6.0, 5.6], [11.2, 5.6]].forEach(function(p){ add(B(.14, 2.95, .14), hM.frame, p[0], 1.47, p[1]); });
  (function(){
    var cx = 8.6, cz = 2.5;
    add(B(1.85, .62, 4.5), hM.car, cx, .62, cz); add(B(1.75, .12, 4.3), hM.car, cx, .98, cz);
    add(B(1.6, .55, 2.3), hM.tint, cx, 1.3, cz - .15); add(B(1.62, .08, 2.2), hM.car, cx, 1.6, cz - .15);
    [[-.93, 1.45], [.93, 1.45], [-.93, -1.5], [.93, -1.5]].forEach(function(p){ add(new THREE.CylinderGeometry(.34, .34, .24, 18), hM.rubber, cx + p[0], .34, cz + p[1]).rotation.z = Math.PI / 2; });
    [-.6, .6].forEach(function(d){ add(B(.28, .12, .05), M.lamp, cx + d, .72, cz + 2.26, { cast: false }); });
  })();

  // fence with posts + caps, sliding gate at the driveway
  function wall(x0, z0, x1, z1){
    var len = Math.hypot(x1 - x0, z1 - z0), ax = Math.abs(x1 - x0) > Math.abs(z1 - z0);
    add(ax ? B(len, 1.5, .18) : B(.18, 1.5, len), hM.fence, (x0 + x1) / 2, .75, (z0 + z1) / 2);
    add(ax ? B(len, .08, .26) : B(.26, .08, len), hM.cap, (x0 + x1) / 2, 1.54, (z0 + z1) / 2, { cast: false });
    for (var i = 0, n = Math.max(1, Math.round(len / 3)); i <= n; i++){ var f = i / n; add(B(.34, 1.72, .34), hM.fence, x0 + (x1 - x0) * f, .86, z0 + (z1 - z0) * f); }
  }
  wall(-13, -10.9, 16, -10.9); wall(-13, -10.9, -13, 12); wall(16, -10.9, 16, 12); wall(-13, 12, 5.8, 12); wall(11.4, 12, 16, 12);
  for (var gx = 0; gx < 14; gx++) add(B(.12, 1.5, .06), hM.gate, 6.0 + gx * .4, .85, 12);
  add(B(5.6, .1, .1), hM.gate, 8.6, 1.58, 12); add(B(5.6, .1, .1), hM.gate, 8.6, .12, 12);

  // garden: shrubs + one frangipani-style tree
  (function(){
    var spots = [[-10.8, 11.2, .7], [-9.4, 11.3, .6], [-7.9, 11.2, .75], [-6.3, 11.3, .6], [-4.6, 11.2, .7], [-3.0, 11.3, .55], [4.7, 11.3, .6],
                 [-10.9, 5.0, .65], [-10.9, 6.6, .55], [-0.1, 3.9, .45], [2.9, 3.8, .45], [-12.2, -9.6, .8], [14.6, -9.6, .8], [14.8, 10.9, .6]];
    var im = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), hM.leaf, spots.length), d = new THREE.Object3D(), col = new THREE.Color();
    var greens = ['#3e7a35', '#4f8c3c', '#2f6a2c', '#5c9a44'];
    spots.forEach(function(p, i){ d.position.set(p[0], p[2] * .8, p[1]); d.scale.set(p[2] * 1.2, p[2], p[2] * 1.2); d.rotation.y = i; d.updateMatrix(); im.setMatrixAt(i, d.matrix); im.setColorAt(i, col.set(greens[i % greens.length])); });
    im.castShadow = true; im.receiveShadow = true; houseG.add(im);
    add(new THREE.CylinderGeometry(.12, .18, 2.2, 8), hM.trunk, -7.5, 1.1, 7.4);
    [[-7.5, 2.7, 7.4, 1.3], [-8.3, 2.4, 7.0, .9], [-6.8, 2.5, 7.9, .95], [-7.4, 3.2, 8.1, .8]].forEach(function(c){ var m = add(new THREE.IcosahedronGeometry(c[3], 1), hM.leaf, c[0], c[1], c[2]); m.material = std({ color: 0x4d8a3a, roughness: .95 }); });
  })();

  // PEA pole + meter outside the gate, service wire to the house
  add(new THREE.CylinderGeometry(.13, .18, 8.5, 10), M.pole, 13.2, 4.25, 13);
  add(B(1.4, .12, .14), M.pole, 13.2, 7.9, 13);
  add(B(.42, .58, .24), M.white, 13.2, 1.55, 12.82);
  houseG.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(13.2, 7.95, 13), new THREE.Vector3(9.8, 7.1, 7.5), new THREE.Vector3(xe + .05, 6.1, 2.2)]), new THREE.LineBasicMaterial({ color: 0x2b2b2b })));

  // inverter + consumer unit on the east wall (under the carport), battery for Hybrid
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
      var u = (c - (HCOLS - 1) / 2) * (HPW + .06), v = .5 + HPL / 2 + r * (HPL + .05);
      d.position.set(u, HH + HRISE + .02, HZ).addScaledVector(down, v).addScaledVector(normal, .2);
      d.rotation.set(HP, 0, 0); d.updateMatrix(); hGlass.setMatrixAt(k, d.matrix);
      d.position.addScaledVector(normal, -.02); d.updateMatrix(); hFrame.setMatrixAt(k, d.matrix); k++;
    });
    [hGlass, hFrame].forEach(function(m){ m.castShadow = true; m.receiveShadow = true; houseG.add(m); });
  })();
  function hRoofY(z){ return HH + HRISE - (z - HZ) * Math.tan(HP); }
  CUR = scene;
