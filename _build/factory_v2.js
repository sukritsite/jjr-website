  // truck: cab-over tractor + box trailer backed onto dock 2
  (function(){
    var x = -10;
    add(B(2.5, 2.9, 12), M.white, x, 2.4, 22.6);                                            // trailer box
    add(B(2.2, .3, 12.4), M.dark, x, .82, 22.6);                                            // chassis
    add(B(2.3, .08, 12.05), M.fascia, x, 3.82, 22.6, { cast: false });                      // roof trim stripe
    [17.4, 18.5, 26.2].forEach(function(z){ [-1.05, 1.05].forEach(function(dx){ add(new THREE.CylinderGeometry(.48, .48, .36, 18), M.dark, x + dx, .48, z).rotation.z = Math.PI / 2; }); });
    add(B(2.45, 2.55, 2.3), M.cab, x, 2.05, 30.25);                                         // cab
    add(B(2.3, 1.05, .06), M.glass, x, 2.65, 31.42, { cast: false });                       // windscreen
    add(B(2.46, .35, .25), M.dark, x, .78, 31.35);                                          // bumper
    [-.85, .85].forEach(function(dx){ add(B(.36, .16, .05), M.lamp, x + dx, 1.0, 31.49, { cast: false }); });
    [29.9, 28.6].forEach(function(z){ [-1.05, 1.05].forEach(function(dx){ add(new THREE.CylinderGeometry(.48, .48, .36, 18), M.dark, x + dx, .48, z).rotation.z = Math.PI / 2; }); });
  })();

  // ---------- factory detailing (kept deliberately sparse)
  var fM = {
    plinth: std({ color: 0xb4b8bb, roughness: .9 }), pil: std({ color: 0xcfd4d8, roughness: .6, metalness: .3 }),
    rubber: std({ color: 0x1e2124, roughness: .95 }), yellow: std({ color: 0xf2b705, roughness: .6 }),
    line: new THREE.MeshBasicMaterial({ color: 0xf4f4f0 }), leaf: std({ color: 0xffffff, roughness: .95 }), trunk: std({ color: 0x6b5543, roughness: .95 }),
    booth: std({ color: 0xf3f3f1, roughness: .8 })
  };
  // concrete plinth + structural pilasters give the long walls rhythm
  add(B(L + .14, 1.0, WD + .14), fM.plinth, 0, .5, 0);
  [-28, -15, -5, 5, 15, 21, 27].forEach(function(x){ add(B(.4, H - .7, .28), fM.pil, x, (H - .7) / 2, WD / 2 + .14); });
  [-12.5, -8.5, 3, 10, 13.5].forEach(function(z){ add(B(.28, H - .7, .4), fM.pil, L / 2 + .14, (H - .7) / 2, z); });
  // dock shelters + bumpers on the four loading doors
  [-20, -10, 0, 10].forEach(function(x){
    add(B(.45, 5.5, .5), fM.rubber, x - 2.55, 2.75, WD / 2 + .3); add(B(.45, 5.5, .5), fM.rubber, x + 2.55, 2.75, WD / 2 + .3);
    add(B(5.55, .55, .5), fM.rubber, x, 5.25, WD / 2 + .3);
    [-1.7, 1.7].forEach(function(d){ add(B(.3, .45, .25), fM.yellow, x + d, 1.05, WD / 2 + .2, { cast: false }); });
  });
  // office: entrance canopy, steps, sign band
  add(B(6.4, .28, 3.2), M.white, -48, 3.45, 19.6);
  [-50.9, -45.1].forEach(function(x){ add(B(.25, 3.4, .25), fM.pil, x, 1.7, 21.0); });
  add(B(6.4, .16, 1.2), fM.plinth, -48, .08, 18.7, { cast: false });
  add(B(20.4, .95, .22), M.fascia, -48, 8.75, 18.2);
  // car park with painted bays + a few cars
  add(new THREE.PlaneGeometry(26, 13), M.asph, -49, .045, 27.5, { rx: -Math.PI / 2, cast: false });
  for (var bx = -61; bx <= -37; bx += 3) add(B(.12, .01, 5), fM.line, bx, .06, 29.6, { cast: false });
  add(B(24, .01, .12), fM.line, -49, .06, 32.1, { cast: false });
  function car(x, z, color){
    var body = std({ color: color, roughness: .28, metalness: .55 });
    add(B(1.8, .6, 4.3), body, x, .62, z); add(B(1.6, .55, 2.2), M.glass, x, 1.2, z + .1); add(B(1.62, .07, 2.1), body, x, 1.5, z + .1);
    [[-.9, 1.35], [.9, 1.35], [-.9, -1.4], [.9, -1.4]].forEach(function(p){ add(new THREE.CylinderGeometry(.33, .33, .22, 16), M.dark, x + p[0], .33, z + p[1]).rotation.z = Math.PI / 2; });
  }
  car(-59.5, 29.6, 0xf2f2f0); car(-56.5, 29.6, 0x9aa3ab); car(-50.5, 29.6, 0x1f2f45); car(-41.5, 29.6, 0xb22a2a);
  // guard booth + barrier at the entrance from the road
  add(B(2.6, 2.7, 2.6), fM.booth, 47.5, 1.35, 21.2); add(B(3.2, .22, 3.2), M.white, 47.5, 2.8, 21.2);
  add(B(1.8, 1.0, .06), M.glass, 47.5, 1.7, 22.52, { cast: false });
  add(B(.3, 1.1, .3), fM.yellow, 46.3, .55, 23.4); add(B(.12, .12, 6.5), fM.yellow, 46.3, 1.05, 26.8);
  // low planting: hedges along the car park edge + a handful of trees by the office (not a forest)
  (function(){
    var shrubs = [], trees = [[-60.5, 21.5], [-35.5, 21.5], [-60.5, 35.2], [-35.5, 35.2], [-34, -4]];
    for (var x = -61.5; x <= -36.5; x += 1.6) shrubs.push([x, 34.5]);
    for (var z = 21; z <= 33; z += 1.6) shrubs.push([-34.6, z]);
    var im = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), fM.leaf, shrubs.length + trees.length * 3), d = new THREE.Object3D(), col = new THREE.Color(), k = 0;
    var greens = ['#3e7a35', '#4f8c3c', '#2f6a2c', '#5c9a44'];
    shrubs.forEach(function(p, i){ d.position.set(p[0], .45, p[1]); d.scale.set(.85, .6, .85); d.rotation.y = i; d.updateMatrix(); im.setMatrixAt(k, d.matrix); im.setColorAt(k++, col.set(greens[i % 4])); });
    trees.forEach(function(p, i){
      add(new THREE.CylinderGeometry(.16, .24, 3.2, 8), fM.trunk, p[0], 1.6, p[1]);
      [[0, 4.1, 0, 1.9], [-.9, 3.6, .5, 1.3], [.8, 3.7, -.4, 1.4]].forEach(function(c){ d.position.set(p[0] + c[0], c[1], p[1] + c[2]); d.scale.setScalar(c[3]); d.updateMatrix(); im.setMatrixAt(k, d.matrix); im.setColorAt(k++, col.set(greens[(i + 1) % 4])); });
    });
    im.count = k; im.castShadow = true; im.receiveShadow = true; factoryG.add(im);
  })();
