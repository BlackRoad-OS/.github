/* ============================================
   BlackRoad OS - Pixel Art Scene Renderer
   ============================================ */

const PixelScenes = {
  // Draw a pixel (scaled block) on canvas
  px(ctx, x, y, color, size = 1) {
    ctx.fillStyle = color;
    ctx.fillRect(x * size, y * size, size, size);
  },

  // Draw rectangle of pixels
  rect(ctx, x, y, w, h, color, size = 1) {
    ctx.fillStyle = color;
    ctx.fillRect(x * size, y * size, w * size, h * size);
  },

  // --- COMMAND CENTER ---
  drawCommand(ctx, w, h) {
    const s = Math.max(1, Math.floor(w / 96));
    const gw = Math.floor(w / s);
    const gh = Math.floor(h / s);
    // Background
    this.rect(ctx, 0, 0, gw, gh, '#0a0a1a', s);
    this.rect(ctx, 0, gh * 0.6, gw, gh * 0.4, '#0d1b2a', s);
    // Floor
    for (let x = 0; x < gw; x += 4) {
      this.rect(ctx, x, gh - 8, 2, 8, '#151530', s);
      this.rect(ctx, x + 2, gh - 8, 2, 8, '#1a1a3a', s);
    }
    // Central holo table
    const cx = Math.floor(gw / 2);
    this.rect(ctx, cx - 12, gh - 20, 24, 4, '#1a3050', s);
    this.rect(ctx, cx - 10, gh - 22, 20, 2, '#0d4060', s);
    // Hologram effect
    for (let i = 0; i < 8; i++) {
      const alpha = 0.1 + Math.random() * 0.15;
      ctx.fillStyle = `rgba(0, 212, 255, ${alpha})`;
      ctx.fillRect((cx - 8 + i * 2) * s, (gh - 38 + i) * s, 2 * s, (16 - i * 2) * s);
    }
    // Top screens
    const screens = [
      { x: cx - 30, c: '#1a237e' }, { x: cx - 10, c: '#004d40' }, { x: cx + 10, c: '#4a148c' }
    ];
    screens.forEach(sc => {
      this.rect(ctx, sc.x, 8, 18, 12, sc.c, s);
      this.rect(ctx, sc.x + 1, 9, 16, 10, '#0a1020', s);
      // Screen content lines
      for (let i = 0; i < 4; i++) {
        this.rect(ctx, sc.x + 2, 10 + i * 2, 8 + Math.floor(Math.random() * 6), 1, sc.c, s);
      }
    });
    // Bottom consoles
    for (let i = 0; i < 5; i++) {
      const bx = cx - 24 + i * 10;
      this.rect(ctx, bx, gh - 12, 8, 6, '#1a2030', s);
      this.rect(ctx, bx + 1, gh - 11, 6, 4, '#0a1520', s);
      this.rect(ctx, bx + 2, gh - 10, 3, 1, i % 2 === 0 ? '#00d4ff' : '#7ed321', s);
    }
    // Stars
    for (let i = 0; i < 20; i++) {
      const sx = Math.floor(Math.random() * gw);
      const sy = Math.floor(Math.random() * gh * 0.5);
      this.px(ctx, sx, sy, `rgba(255,255,255,${0.3 + Math.random() * 0.5})`, s);
    }
  },

  // --- OFFICE ---
  drawOffice(ctx, w, h) {
    const s = Math.max(1, Math.floor(w / 96));
    const gw = Math.floor(w / s);
    const gh = Math.floor(h / s);
    // Walls
    this.rect(ctx, 0, 0, gw, gh * 0.4, '#d4c5a0', s);
    // Floor
    this.rect(ctx, 0, gh * 0.4, gw, gh * 0.6, '#c8a86e', s);
    // Floor tiles
    for (let x = 0; x < gw; x += 6) {
      for (let y = Math.floor(gh * 0.4); y < gh; y += 6) {
        this.rect(ctx, x, y, 3, 3, '#c09860', s);
        this.rect(ctx, x + 3, y + 3, 3, 3, '#c09860', s);
      }
    }
    // Sign
    this.rect(ctx, cx(gw) - 16, 4, 32, 6, '#ffffff', s);
    this.rect(ctx, cx(gw) - 14, 5, 28, 4, '#f0f0f0', s);
    // Desks
    for (let i = 0; i < 3; i++) {
      const dx = 8 + i * 28;
      const dy = Math.floor(gh * 0.5) + 4;
      this.rect(ctx, dx, dy, 20, 8, '#b8860b', s);
      this.rect(ctx, dx + 2, dy + 1, 8, 5, '#2a2a4a', s); // monitor
      this.rect(ctx, dx + 3, dy + 2, 6, 3, '#1a3050', s);
      // Chair
      this.rect(ctx, dx + 6, dy + 8, 6, 4, '#333355', s);
      // Person
      this.rect(ctx, dx + 7, dy + 4, 4, 4, '#8B6914', s); // head
      this.rect(ctx, dx + 7, dy + 8, 4, 3, '#4466aa', s); // body
    }
    // Server rack
    this.rect(ctx, gw - 14, 6, 10, 20, '#222244', s);
    for (let i = 0; i < 5; i++) {
      this.rect(ctx, gw - 12, 8 + i * 3, 6, 2, '#1a1a3a', s);
      this.px(ctx, gw - 5, 8 + i * 3, i % 2 === 0 ? '#7ed321' : '#f5a623', s);
    }
    // Plants
    this.rect(ctx, 2, gh * 0.4 - 6, 3, 6, '#2e7d32', s);
    this.rect(ctx, 1, gh * 0.4 - 3, 5, 3, '#4caf50', s);
    this.rect(ctx, 2, gh * 0.4, 3, 2, '#8B4513', s);

    function cx(gw) { return Math.floor(gw / 2); }
  },

  // --- CAMPUS ---
  drawCampus(ctx, w, h) {
    const s = Math.max(1, Math.floor(w / 96));
    const gw = Math.floor(w / s);
    const gh = Math.floor(h / s);
    // Sky
    this.rect(ctx, 0, 0, gw, gh * 0.3, '#87CEEB', s);
    // Ground
    this.rect(ctx, 0, gh * 0.3, gw, gh * 0.7, '#4caf50', s);
    // Paths
    this.rect(ctx, gw / 2 - 2, gh * 0.3, 4, gh * 0.7, '#d4c5a0', s);
    this.rect(ctx, 0, gh * 0.55, gw, 3, '#d4c5a0', s);
    // Main building
    const bx = Math.floor(gw / 2) - 10;
    this.rect(ctx, bx, gh * 0.1, 20, 24, '#1a237e', s);
    this.rect(ctx, bx + 2, gh * 0.12, 16, 3, '#0d47a1', s);
    // Windows
    for (let row = 0; row < 4; row++) {
      for (let col = 0; col < 4; col++) {
        this.rect(ctx, bx + 2 + col * 4, gh * 0.18 + row * 4, 3, 2, '#4fc3f7', s);
      }
    }
    // Small buildings
    [[4, 12], [gw - 16, 10], [4, gh * 0.45], [gw - 18, gh * 0.45]].forEach(([x, y]) => {
      this.rect(ctx, x, y, 12, 8, '#37474f', s);
      this.rect(ctx, x + 1, y + 1, 4, 3, '#4fc3f7', s);
      this.rect(ctx, x + 7, y + 1, 4, 3, '#4fc3f7', s);
    });
    // Trees
    for (let i = 0; i < 8; i++) {
      const tx = 2 + Math.floor(Math.random() * (gw - 4));
      const ty = gh * 0.35 + Math.floor(Math.random() * (gh * 0.3));
      this.rect(ctx, tx, ty - 4, 3, 4, '#2e7d32', s);
      this.rect(ctx, tx - 1, ty - 6, 5, 3, '#388e3c', s);
      this.rect(ctx, tx + 1, ty, 1, 2, '#5D4037', s);
    }
    // Fountain
    this.rect(ctx, gw / 2 - 3, gh * 0.52, 6, 4, '#90a4ae', s);
    this.rect(ctx, gw / 2 - 1, gh * 0.48, 2, 4, '#4fc3f7', s);
  },

  // --- MUSEUM ---
  drawMuseum(ctx, w, h) {
    const s = Math.max(1, Math.floor(w / 96));
    const gw = Math.floor(w / s);
    const gh = Math.floor(h / s);
    // Walls
    this.rect(ctx, 0, 0, gw, gh, '#e8e0d0', s);
    // Floor
    this.rect(ctx, 0, gh * 0.65, gw, gh * 0.35, '#c8b898', s);
    // Dinosaur skeleton
    this.rect(ctx, gw - 24, gh * 0.3, 16, 2, '#d7ccc8', s);
    this.rect(ctx, gw - 22, gh * 0.25, 2, 5, '#d7ccc8', s);
    this.rect(ctx, gw - 14, gh * 0.22, 8, 3, '#bcaaa4', s);
    this.rect(ctx, gw - 10, gh * 0.32, 2, 16, '#d7ccc8', s);
    this.rect(ctx, gw - 18, gh * 0.32, 2, 16, '#d7ccc8', s);
    this.rect(ctx, gw - 8, gh * 0.19, 6, 4, '#bcaaa4', s);
    // Globe
    this.rect(ctx, 12, gh * 0.35, 8, 8, '#1565c0', s);
    this.rect(ctx, 13, gh * 0.36, 3, 3, '#4caf50', s);
    this.rect(ctx, 17, gh * 0.39, 2, 2, '#4caf50', s);
    this.rect(ctx, 15, gh * 0.43, 2, 4, '#5D4037', s);
    // Solar system display
    this.rect(ctx, gw / 2 - 14, 4, 28, 16, '#1a237e', s);
    this.rect(ctx, gw / 2 - 2, 10, 4, 4, '#ffeb3b', s); // sun
    this.px(ctx, gw / 2 - 8, 12, '#2196f3', s); // planet
    this.px(ctx, gw / 2 + 6, 8, '#f44336', s); // planet
    this.px(ctx, gw / 2 + 10, 14, '#ff9800', s); // planet
    // Visitors
    for (let i = 0; i < 6; i++) {
      const vx = 8 + i * 14;
      const vy = gh * 0.6;
      this.rect(ctx, vx, vy, 3, 3, '#' + ['8B6914', '5D4037', '455a64', 'b71c1c', '1565c0', '2e7d32'][i], s);
      this.rect(ctx, vx, vy + 3, 3, 4, '#' + ['4466aa', '66bb6a', 'ff7043', '7e57c2', 'ffa726', 'ef5350'][i], s);
    }
    // Telescope
    this.rect(ctx, 4, gh * 0.5, 2, 8, '#455a64', s);
    this.rect(ctx, 2, gh * 0.48, 6, 3, '#546e7a', s);
  },

  // --- STORE ---
  drawStore(ctx, w, h) {
    const s = Math.max(1, Math.floor(w / 96));
    const gw = Math.floor(w / s);
    const gh = Math.floor(h / s);
    // Background
    this.rect(ctx, 0, 0, gw, gh, '#f5f0e8', s);
    // Floor
    this.rect(ctx, 0, gh * 0.3, gw, gh * 0.7, '#e8dcc8', s);
    // Shelves
    for (let i = 0; i < 4; i++) {
      const sx = 4 + i * 22;
      this.rect(ctx, sx, gh * 0.35, 18, 3, '#8B6914', s);
      this.rect(ctx, sx, gh * 0.5, 18, 3, '#8B6914', s);
      // Products
      for (let j = 0; j < 5; j++) {
        const colors = ['#f44336', '#2196f3', '#4caf50', '#ff9800', '#9c27b0'];
        this.rect(ctx, sx + 1 + j * 3, gh * 0.32, 2, 3, colors[j], s);
        this.rect(ctx, sx + 1 + j * 3, gh * 0.47, 2, 3, colors[(j + 2) % 5], s);
      }
    }
    // Sign "STORE"
    this.rect(ctx, gw / 2 - 10, 2, 20, 6, '#ff9800', s);
    // Registers
    for (let i = 0; i < 3; i++) {
      const rx = gw / 2 - 16 + i * 12;
      this.rect(ctx, rx, gh * 0.65, 8, 5, '#5D4037', s);
      this.rect(ctx, rx + 1, gh * 0.63, 6, 3, '#333', s);
      // Person at register
      this.rect(ctx, rx + 2, gh * 0.58, 3, 3, '#8B6914', s);
      this.rect(ctx, rx + 2, gh * 0.61, 3, 3, '#4466aa', s);
    }
    // Electronics section sign
    this.rect(ctx, gw - 20, 2, 18, 5, '#1565c0', s);
  },

  // --- LOUNGE ---
  drawLounge(ctx, w, h) {
    const s = Math.max(1, Math.floor(w / 96));
    const gw = Math.floor(w / s);
    const gh = Math.floor(h / s);
    // Background
    this.rect(ctx, 0, 0, gw, gh, '#e0d8c8', s);
    // Floor
    this.rect(ctx, 0, gh * 0.3, gw, gh * 0.7, '#c8b898', s);
    // Sofas
    const sofaColors = ['#d32f2f', '#1565c0', '#2e7d32', '#f57c00'];
    for (let i = 0; i < 4; i++) {
      const sx = 4 + i * 22;
      const sy = gh * 0.4 + (i % 2) * 16;
      this.rect(ctx, sx, sy, 16, 6, sofaColors[i], s);
      this.rect(ctx, sx, sy + 1, 2, 4, sofaColors[i], s);
      this.rect(ctx, sx + 14, sy + 1, 2, 4, sofaColors[i], s);
    }
    // Round tables
    for (let i = 0; i < 3; i++) {
      const tx = 12 + i * 28;
      const ty = gh * 0.55;
      this.rect(ctx, tx, ty, 8, 8, '#8B6914', s);
      this.rect(ctx, tx + 1, ty + 1, 6, 6, '#a0842c', s);
      // Chairs around
      this.rect(ctx, tx - 2, ty + 2, 2, 4, '#455a64', s);
      this.rect(ctx, tx + 8, ty + 2, 2, 4, '#455a64', s);
    }
    // Plants
    for (let i = 0; i < 5; i++) {
      const px = 6 + i * 18;
      this.rect(ctx, px, gh * 0.28, 4, 6, '#2e7d32', s);
      this.rect(ctx, px - 1, gh * 0.25, 6, 4, '#4caf50', s);
      this.rect(ctx, px + 1, gh * 0.34, 2, 2, '#5D4037', s);
    }
    // Screens on wall
    this.rect(ctx, 8, 4, 14, 10, '#222', s);
    this.rect(ctx, 9, 5, 12, 8, '#1a3050', s);
    this.rect(ctx, gw - 22, 4, 14, 10, '#222', s);
    this.rect(ctx, gw - 21, 5, 12, 8, '#1a3050', s);
  },

  // --- WORLD MAP ---
  drawMap(ctx, w, h) {
    const s = Math.max(1, Math.floor(w / 96));
    const gw = Math.floor(w / s);
    const gh = Math.floor(h / s);
    // Ocean
    this.rect(ctx, 0, 0, gw, gh, '#1565c0', s);
    // Continents (simplified)
    // North America
    this.rect(ctx, 8, 8, 24, 20, '#4caf50', s);
    this.rect(ctx, 12, 6, 16, 4, '#66bb6a', s);
    this.rect(ctx, 14, 28, 12, 8, '#4caf50', s);
    // South America
    this.rect(ctx, 18, 38, 10, 18, '#66bb6a', s);
    this.rect(ctx, 20, 36, 6, 4, '#4caf50', s);
    // Europe/Africa
    this.rect(ctx, 40, 6, 14, 12, '#81c784', s);
    this.rect(ctx, 42, 20, 10, 24, '#ffb74d', s);
    this.rect(ctx, 40, 18, 14, 4, '#81c784', s);
    // Asia
    this.rect(ctx, 54, 4, 28, 20, '#a5d6a7', s);
    this.rect(ctx, 60, 24, 16, 10, '#81c784', s);
    // Australia
    this.rect(ctx, 72, 44, 14, 10, '#ffb74d', s);
    // BlackRoad HQ marker
    const hx = 20, hy = 16;
    this.rect(ctx, hx, hy, 6, 8, '#1a237e', s);
    this.rect(ctx, hx + 1, hy + 1, 4, 2, '#4fc3f7', s);
    this.px(ctx, hx + 2, hy - 1, '#ff6b9d', s);
    // Mountains
    this.rect(ctx, 10, 10, 2, 3, '#fff', s);
    this.rect(ctx, 58, 8, 2, 3, '#fff', s);
    // Cities
    const cities = [[28, 14], [44, 10], [62, 12], [48, 28], [76, 48]];
    cities.forEach(([x, y]) => {
      this.px(ctx, x, y, '#ffeb3b', s);
      this.px(ctx, x + 1, y, '#ffeb3b', s);
    });
  },

  // --- COTTAGE ---
  drawCottage(ctx, w, h) {
    const s = Math.max(1, Math.floor(w / 96));
    const gw = Math.floor(w / s);
    const gh = Math.floor(h / s);
    // Sky
    this.rect(ctx, 0, 0, gw, gh * 0.4, '#87CEEB', s);
    // Grass
    this.rect(ctx, 0, gh * 0.4, gw, gh * 0.6, '#4caf50', s);
    // Grass detail
    for (let x = 0; x < gw; x += 3) {
      this.rect(ctx, x, gh * 0.4, 2, 1, '#388e3c', s);
    }
    // House body
    const hx = Math.floor(gw / 2) - 12;
    const hy = Math.floor(gh * 0.25);
    this.rect(ctx, hx, hy, 24, 18, '#ffe0b2', s);
    // Roof
    for (let i = 0; i < 14; i++) {
      this.rect(ctx, hx - 2 + i, hy - i - 1, 28 - i * 2, 1, '#bf360c', s);
    }
    // Door
    this.rect(ctx, hx + 10, hy + 10, 4, 8, '#5D4037', s);
    this.px(ctx, hx + 13, hy + 14, '#ffeb3b', s);
    // Windows
    this.rect(ctx, hx + 3, hy + 4, 5, 5, '#4fc3f7', s);
    this.rect(ctx, hx + 16, hy + 4, 5, 5, '#4fc3f7', s);
    this.rect(ctx, hx + 5, hy + 4, 1, 5, '#8B6914', s);
    this.rect(ctx, hx + 18, hy + 4, 1, 5, '#8B6914', s);
    // Chimney
    this.rect(ctx, hx + 18, hy - 10, 3, 6, '#795548', s);
    this.rect(ctx, hx + 17, hy - 11, 5, 2, '#8d6e63', s);
    // Smoke
    this.px(ctx, hx + 19, hy - 13, 'rgba(200,200,200,0.6)', s);
    this.px(ctx, hx + 18, hy - 15, 'rgba(200,200,200,0.4)', s);
    // Fence
    for (let x = 2; x < gw - 2; x += 4) {
      this.rect(ctx, x, gh * 0.7, 1, 5, '#fff', s);
      this.rect(ctx, x - 1, gh * 0.72, 3, 1, '#fff', s);
    }
    // Flowers
    const flowerColors = ['#f44336', '#ff9800', '#ffeb3b', '#e91e63', '#9c27b0'];
    for (let i = 0; i < 12; i++) {
      const fx = 4 + Math.floor(Math.random() * (gw - 8));
      const fy = gh * 0.6 + Math.floor(Math.random() * (gh * 0.08));
      this.rect(ctx, fx, fy - 2, 1, 2, '#2e7d32', s);
      this.px(ctx, fx, fy - 3, flowerColors[i % flowerColors.length], s);
    }
    // Trees
    [[4, gh * 0.3], [gw - 8, gh * 0.28]].forEach(([tx, ty]) => {
      this.rect(ctx, tx + 1, ty + 4, 2, 4, '#5D4037', s);
      this.rect(ctx, tx - 1, ty, 6, 5, '#2e7d32', s);
      this.rect(ctx, tx, ty - 2, 4, 3, '#388e3c', s);
    });
    // Path
    for (let y = Math.floor(gh * 0.43); y < gh * 0.7; y += 2) {
      this.rect(ctx, gw / 2 - 2, y, 4, 1, '#d4c5a0', s);
    }
    // Mailbox
    this.rect(ctx, gw / 2 - 8, gh * 0.62, 3, 4, '#d32f2f', s);
    this.rect(ctx, gw / 2 - 7, gh * 0.6, 1, 6, '#5D4037', s);
  },

  // Render a scene to a canvas
  render(canvas, sceneName) {
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    switch (sceneName) {
      case 'command': this.drawCommand(ctx, w, h); break;
      case 'office': this.drawOffice(ctx, w, h); break;
      case 'campus': this.drawCampus(ctx, w, h); break;
      case 'museum': this.drawMuseum(ctx, w, h); break;
      case 'store': this.drawStore(ctx, w, h); break;
      case 'lounge': this.drawLounge(ctx, w, h); break;
      case 'map': this.drawMap(ctx, w, h); break;
      case 'cottage': this.drawCottage(ctx, w, h); break;
    }
  },

  // Render all thumbnails
  renderThumbnails() {
    document.querySelectorAll('.thumb-item').forEach(item => {
      const canvas = item.querySelector('.thumb-canvas');
      if (canvas) {
        this.render(canvas, item.dataset.scene);
      }
    });
  },

  // Render main scene canvas
  renderMainScene(sceneName) {
    const canvas = document.getElementById('scene-canvas');
    if (!canvas) return;
    const parent = canvas.parentElement;
    canvas.width = parent.offsetWidth;
    canvas.height = parent.offsetHeight;
    this.render(canvas, sceneName);
  }
};
