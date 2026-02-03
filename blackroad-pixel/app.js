/* ============================================
   BlackRoad OS - Interactive UI Logic
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ---- Navigation ----
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');
    });
  });

  // ---- Color Palette ----
  const colorDots = document.querySelectorAll('.color-dot');
  colorDots.forEach(dot => {
    dot.addEventListener('click', () => {
      colorDots.forEach(d => d.classList.remove('active'));
      dot.classList.add('active');
      const color = dot.dataset.color;
      document.documentElement.style.setProperty('--accent-active', color);
    });
  });

  // ---- Thumbnail Click ----
  const thumbItems = document.querySelectorAll('.thumb-item');
  const sceneOverlay = document.querySelector('.scene-overlay');

  const sceneNames = {
    office: 'HQ OFFICE',
    apartment: 'APARTMENT',
    home: 'HOME',
    dataport: 'DATA PORT',
    farm: 'FARM',
    town: 'TOWN',
    museum: 'SCIENCE MUSEUM',
    store: 'MEGA STORE',
    lounge: 'AGENT LOUNGE',
    cottage: 'PIXEL COTTAGE',
    garage: 'CYBER GARAGE',
    dock: 'STAR DOCK',
    lab: 'NEON LAB',
    vault: 'THE VAULT',
    garden: 'PIXEL GARDEN',
    bullpen: 'THE BULLPEN',
    summit: 'THE SUMMIT',
    campus: 'HQ CAMPUS',
    metro: 'PIXEL METRO',
    nation: 'THE NATION',
    arena: 'PIXEL ARENA',
    shrine: 'THE SHRINE',
    outpost: 'STAR OUTPOST',
    harbor: 'NEON HARBOR',
    citadel: 'THE CITADEL',
    bunker: 'THE BUNKER',
    tavern: 'PIXEL TAVERN',
    skyport: 'SKY PORT',
    canyon: 'CYBER CANYON',
    fortress: 'THE FORTRESS'
  };

  const sceneGradients = {
    office: 'linear-gradient(180deg, #1a1008 0%, #2a1a0a 40%, #3d2b1f 100%)',
    apartment: 'linear-gradient(180deg, #5a3a10 0%, #8b6914 40%, #c4956a 100%)',
    home: 'linear-gradient(180deg, #6b5530 0%, #a0855a 40%, #d4b896 100%)',
    dataport: 'linear-gradient(180deg, #051a3a 0%, #0a3a7a 40%, #1a6abf 100%)',
    farm: 'linear-gradient(180deg, #0a3a0a 0%, #2a6b1a 40%, #5a9e3b 100%)',
    town: 'linear-gradient(180deg, #1a4a0a 0%, #3a7a2a 40%, #6ab04a 100%)',
    museum: 'linear-gradient(180deg, #0a0a2a 0%, #1a1a3d 40%, #2b2b5e 100%)',
    store: 'linear-gradient(180deg, #1a0d05 0%, #3d2a1a 40%, #5e3b2b 100%)',
    lounge: 'linear-gradient(180deg, #050d1a 0%, #1a2a3d 40%, #2b3b5e 100%)',
    cottage: 'linear-gradient(180deg, #0d1a05 0%, #2a3d0a 40%, #3b5e1a 100%)',
    garage: 'linear-gradient(180deg, #1a0808 0%, #3d1a1a 40%, #5e2b2b 100%)',
    dock: 'linear-gradient(180deg, #10051a 0%, #2a0a3d 40%, #5e1a6b 100%)',
    lab: 'linear-gradient(180deg, #051a10 0%, #0a3d2a 40%, #1a5e4a 100%)',
    vault: 'linear-gradient(180deg, #1a1905 0%, #3d3a0a 40%, #5e5510 100%)',
    garden: 'linear-gradient(180deg, #1a050d 0%, #3d0a2a 40%, #6b1a5e 100%)',
    bullpen: 'linear-gradient(180deg, #1a1408 0%, #3d3020 40%, #6b5a3a 100%)',
    summit: 'linear-gradient(180deg, #0a0f1a 0%, #1a2840 40%, #2a3d5e 100%)',
    campus: 'linear-gradient(180deg, #0a1a0a 0%, #1a4a1a 40%, #2a7a3a 100%)',
    metro: 'linear-gradient(180deg, #0a1a0d 0%, #1a3a2a 40%, #2a6a4a 100%)',
    nation: 'linear-gradient(180deg, #051020 0%, #0a2a4a 40%, #1a4a7a 100%)',
    arena: 'linear-gradient(180deg, #1a0a05 0%, #4a1a0a 40%, #8a3a1a 100%)',
    shrine: 'linear-gradient(180deg, #0d0520 0%, #2a1050 40%, #5a2a8a 100%)',
    outpost: 'linear-gradient(180deg, #0a1510 0%, #1a3a2a 40%, #2a5a4a 100%)',
    harbor: 'linear-gradient(180deg, #050a1a 0%, #0a2040 40%, #1a3a6a 100%)',
    citadel: 'linear-gradient(180deg, #1a0d0a 0%, #3a2010 40%, #6a4020 100%)',
    bunker: 'linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 40%, #2a2a2a 100%)',
    tavern: 'linear-gradient(180deg, #1a0a00 0%, #3a2a10 40%, #6a4a20 100%)',
    skyport: 'linear-gradient(180deg, #0a1020 0%, #1a3050 40%, #3a5080 100%)',
    canyon: 'linear-gradient(180deg, #1a0800 0%, #4a2010 40%, #7a3820 100%)',
    fortress: 'linear-gradient(180deg, #10100a 0%, #2a2a1a 40%, #4a4a2a 100%)'
  };

  thumbItems.forEach(item => {
    item.addEventListener('click', () => {
      const scene = item.dataset.scene;
      const commandCenter = document.querySelector('.command-center');

      if (sceneGradients[scene]) {
        commandCenter.style.background = sceneGradients[scene];
      }
      if (sceneNames[scene]) {
        sceneOverlay.textContent = sceneNames[scene];
      }

      // Highlight selected thumb
      thumbItems.forEach(t => t.style.borderColor = '');
      item.style.borderColor = 'var(--accent-cyan)';
    });
  });

  // ---- Chat Input ----
  const chatInput = document.querySelector('.chat-input');
  const chatMessages = document.querySelector('.chat-messages');

  const agents = [
    { name: 'Cecilia', class: 'cecilia' },
    { name: 'Cadence', class: 'cadence' },
    { name: 'Lucidia', class: 'lucidia' },
    { name: 'Octavia', class: 'octavia' },
    { name: 'Aria', class: 'aria' },
    { name: 'Anastasia', class: 'anastasia' },
    { name: 'Alice', class: 'alice' },
    { name: 'Gematria', class: 'gematria' },
    { name: 'Codex', class: 'codex' },
    { name: 'Silas', class: 'silas' },
    { name: 'Alexandria', class: 'alexandria' },
    { name: 'Alexa Louise', class: 'alexa-louise' }
  ];

  const responses = [
    'Acknowledged. Processing request...',
    'Task queued and prioritized.',
    'Analyzing parameters now.',
    'Cross-referencing with knowledge base.',
    'Executing in sandboxed environment.',
    'Running diagnostic sweep.',
    'Compiling updated modules.',
    'Syncing with distributed nodes.',
    'Optimizing resource allocation.',
    'Generating comprehensive report.',
    'Validating data integrity.',
    'Deploying to staging cluster.'
  ];

  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && chatInput.value.trim()) {
      const userMsg = chatInput.value.trim();

      // Add user message
      const userDiv = document.createElement('div');
      userDiv.className = 'chat-msg';
      userDiv.innerHTML = `<span class="agent-name" style="color: #fff;">You:</span> ${escapeHtml(userMsg)}`;
      chatMessages.appendChild(userDiv);

      chatInput.value = '';

      // Random agent response
      setTimeout(() => {
        const agent = agents[Math.floor(Math.random() * agents.length)];
        const response = responses[Math.floor(Math.random() * responses.length)];
        const respDiv = document.createElement('div');
        respDiv.className = 'chat-msg';
        respDiv.innerHTML = `<span class="agent-name ${agent.class}">${agent.name}:</span> ${response}`;
        chatMessages.appendChild(respDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }, 300 + Math.random() * 700);

      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  });

  // ---- Sidebar Icons ----
  const sidebarIcons = document.querySelectorAll('.sidebar-icon');
  sidebarIcons.forEach(icon => {
    icon.addEventListener('click', () => {
      sidebarIcons.forEach(i => i.style.color = '');
      icon.style.color = 'var(--accent-cyan)';
    });
  });

  // ---- Typing animation for initial messages ----
  const msgs = document.querySelectorAll('.chat-msg');
  msgs.forEach((msg, i) => {
    msg.style.opacity = '0';
    msg.style.transform = 'translateY(8px)';
    msg.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    setTimeout(() => {
      msg.style.opacity = '1';
      msg.style.transform = 'translateY(0)';
    }, 100 + i * 120);
  });

  // ---- Helper ----
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
});
