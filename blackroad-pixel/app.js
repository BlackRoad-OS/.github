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
    campus: 'BLACKROAD CAMPUS',
    museum: 'SCIENCE MUSEUM',
    store: 'MEGA STORE',
    lounge: 'AGENT LOUNGE',
    workshop: 'WORKSHOP',
    map: 'WORLD MAP',
    cottage: 'PIXEL COTTAGE'
  };

  const sceneGradients = {
    office: 'linear-gradient(180deg, #1a1008 0%, #2a1a0a 40%, #3d2b1f 100%)',
    campus: 'linear-gradient(180deg, #051a0d 0%, #0a2a1a 40%, #1a3d2b 100%)',
    museum: 'linear-gradient(180deg, #0a0a2a 0%, #1a1a3d 40%, #2b2b5e 100%)',
    store: 'linear-gradient(180deg, #1a0d05 0%, #3d2a1a 40%, #5e3b2b 100%)',
    lounge: 'linear-gradient(180deg, #050d1a 0%, #1a2a3d 40%, #2b3b5e 100%)',
    workshop: 'linear-gradient(180deg, #1a1a05 0%, #2a2a0a 40%, #3d3d1a 100%)',
    map: 'linear-gradient(180deg, #052a1a 0%, #0a3d2a 40%, #1a5e3b 100%)',
    cottage: 'linear-gradient(180deg, #0d1a05 0%, #2a3d0a 40%, #3b5e1a 100%)'
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
