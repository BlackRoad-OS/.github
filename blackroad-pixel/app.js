/* ============================================
   BlackRoad OS - Main Application Logic
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ==========================================
  //  DATA
  // ==========================================

  const agents = [
    { name: 'Cecilia', cls: 'cecilia', color: '#ff6b9d', role: 'System Orchestrator', task: 'Coordinating multi-agent pipeline', cpu: 72, mem: 58 },
    { name: 'Cadence', cls: 'cadence', color: '#f5a623', role: 'Build Engineer', task: 'Running CI/CD pipeline for v2.4', cpu: 88, mem: 65 },
    { name: 'Lucidia', cls: 'lucidia', color: '#00d4ff', role: 'Documentation Specialist', task: 'Generating API reference docs', cpu: 34, mem: 42 },
    { name: 'Octavia', cls: 'octavia', color: '#7ed321', role: 'Security Analyst', task: 'Scanning dependencies for CVEs', cpu: 56, mem: 71 },
    { name: 'Aria', cls: 'aria', color: '#c44dff', role: 'DevOps Engineer', task: 'Provisioning staging environment', cpu: 91, mem: 78 },
    { name: 'Anastasia', cls: 'anastasia', color: '#ff8a65', role: 'Database Architect', task: 'Optimizing query performance', cpu: 45, mem: 53 },
    { name: 'Alice', cls: 'alice', color: '#64b5f6', role: 'Test Engineer', task: 'Running integration test suite', cpu: 67, mem: 44 },
    { name: 'Gematria', cls: 'gematria', color: '#ce93d8', role: 'Analytics Engineer', task: 'Processing telemetry data batch', cpu: 39, mem: 62 },
    { name: 'Codex', cls: 'codex', color: '#4db6ac', role: 'API Developer', task: 'Implementing REST endpoints', cpu: 81, mem: 55 },
    { name: 'Silas', cls: 'silas', color: '#90a4ae', role: 'Infrastructure Monitor', task: 'Monitoring cluster health', cpu: 28, mem: 36 },
    { name: 'Alexandria', cls: 'alexandria', color: '#aed581', role: 'Knowledge Engineer', task: 'Indexing documentation corpus', cpu: 52, mem: 83 },
    { name: 'Alexa Louise', cls: 'alexa-louise', color: '#ff6b9d', role: 'Lead Coordinator', task: 'Synchronizing all agent outputs', cpu: 60, mem: 47 }
  ];

  const repos = [
    { name: 'blackroad-os/core', desc: 'Core operating system framework and runtime', lang: 'Rust', langColor: '#dea584', stars: 2847, forks: 312, issues: 23,
      branches: ['main', 'develop', 'feature/agent-v3', 'hotfix/memory-leak'],
      commits: [
        { hash: 'f7f38e2', msg: 'Add BlackRoad OS pixel-art desktop UI', time: '2h ago' },
        { hash: '2dc092a', msg: 'Deploy Intelligent Auto-PR System', time: '5h ago' },
        { hash: '2c41f07', msg: 'Autonomy deployment - Push to 100!', time: '8h ago' },
        { hash: '3f451de', msg: 'Add organization-wide security policy', time: '1d ago' },
        { hash: '005008c', msg: 'Sync files via br-sync', time: '2d ago' }
      ]},
    { name: 'blackroad-os/agents', desc: 'Multi-agent orchestration and communication layer', lang: 'Python', langColor: '#3572A5', stars: 1923, forks: 187, issues: 12,
      branches: ['main', 'develop', 'feature/swarm-protocol'],
      commits: [
        { hash: 'a1b2c3d', msg: 'Implement agent swarm communication', time: '3h ago' },
        { hash: 'e4f5a6b', msg: 'Add agent health monitoring', time: '12h ago' },
        { hash: 'c7d8e9f', msg: 'Refactor message queue', time: '1d ago' }
      ]},
    { name: 'blackroad-os/pixel-ui', desc: 'Pixel art themed user interface components', lang: 'TypeScript', langColor: '#3178c6', stars: 867, forks: 94, issues: 8,
      branches: ['main', 'develop', 'feature/dark-mode'],
      commits: [
        { hash: 'b2c3d4e', msg: 'Add scene renderer module', time: '1h ago' },
        { hash: 'f5a6b7c', msg: 'Implement thumbnail canvas system', time: '6h ago' }
      ]},
    { name: 'blackroad-os/infra', desc: 'Infrastructure as code, deployment, and monitoring', lang: 'Go', langColor: '#00ADD8', stars: 534, forks: 67, issues: 5,
      branches: ['main', 'staging', 'production'],
      commits: [
        { hash: 'd4e5f6a', msg: 'Update Kubernetes manifests', time: '4h ago' },
        { hash: 'a7b8c9d', msg: 'Add Prometheus alerting rules', time: '1d ago' }
      ]},
    { name: 'blackroad-os/knowledge', desc: 'Knowledge base indexing and semantic search engine', lang: 'Python', langColor: '#3572A5', stars: 412, forks: 43, issues: 3,
      branches: ['main', 'feature/vector-search'],
      commits: [
        { hash: 'e1f2a3b', msg: 'Add vector embedding pipeline', time: '2h ago' }
      ]},
    { name: 'blackroad-os/sdk', desc: 'Developer SDK for building BlackRoad extensions', lang: 'TypeScript', langColor: '#3178c6', stars: 678, forks: 89, issues: 11,
      branches: ['main', 'v2', 'v3-beta'],
      commits: [
        { hash: 'c4d5e6f', msg: 'Release SDK v3 beta', time: '6h ago' },
        { hash: 'a8b9c0d', msg: 'Add plugin lifecycle hooks', time: '1d ago' }
      ]}
  ];

  const tools = [
    { name: 'Build Runner', icon: '&#9881;', iconBg: '#1a3d2b', desc: 'Automated build and compilation pipeline with caching', status: 'active',
      config: [
        { label: 'Build Target', type: 'input', value: 'production' },
        { label: 'Cache Enabled', type: 'toggle', value: true },
        { label: 'Parallel Jobs', type: 'input', value: '8' }
      ]},
    { name: 'Code Analyzer', icon: '&#128269;', iconBg: '#2a1a3d', desc: 'Static analysis, linting, and code quality metrics', status: 'active',
      config: [
        { label: 'Ruleset', type: 'input', value: 'strict' },
        { label: 'Auto-fix', type: 'toggle', value: false }
      ]},
    { name: 'Test Suite', icon: '&#9989;', iconBg: '#1a2a3d', desc: 'Unit, integration, and end-to-end test execution', status: 'active',
      config: [
        { label: 'Test Pattern', type: 'input', value: '**/*.test.*' },
        { label: 'Coverage Threshold', type: 'input', value: '80%' },
        { label: 'Watch Mode', type: 'toggle', value: false }
      ]},
    { name: 'Deploy Manager', icon: '&#128640;', iconBg: '#3d2a1a', desc: 'Deployment orchestration for staging and production', status: 'idle',
      config: [
        { label: 'Target Environment', type: 'input', value: 'staging' },
        { label: 'Rolling Update', type: 'toggle', value: true }
      ]},
    { name: 'Security Scanner', icon: '&#128274;', iconBg: '#1a3d1a', desc: 'Vulnerability scanning and dependency auditing', status: 'active',
      config: [
        { label: 'Scan Depth', type: 'input', value: 'deep' },
        { label: 'Block on Critical', type: 'toggle', value: true }
      ]},
    { name: 'Package Manager', icon: '&#128230;', iconBg: '#3d1a2a', desc: 'Dependency management and package publishing', status: 'idle',
      config: [
        { label: 'Registry', type: 'input', value: 'https://registry.blackroad.dev' },
        { label: 'Lock File', type: 'toggle', value: true }
      ]},
    { name: 'Doc Generator', icon: '&#128196;', iconBg: '#1a2a2a', desc: 'Automatic API documentation generation from source', status: 'idle',
      config: [
        { label: 'Output Format', type: 'input', value: 'markdown' },
        { label: 'Include Private', type: 'toggle', value: false }
      ]},
    { name: 'Performance Profiler', icon: '&#9889;', iconBg: '#2a2a1a', desc: 'Runtime performance profiling and bottleneck detection', status: 'active',
      config: [
        { label: 'Sample Rate', type: 'input', value: '1000ms' },
        { label: 'Flame Graph', type: 'toggle', value: true }
      ]}
  ];

  const fileTree = [
    { name: 'blackroad-os', type: 'folder', depth: 0, children: [
      { name: 'src', type: 'folder', depth: 1, children: [
        { name: 'core', type: 'folder', depth: 2, children: [
          { name: 'runtime.rs', type: 'file', depth: 3, lang: 'rust' },
          { name: 'scheduler.rs', type: 'file', depth: 3, lang: 'rust' },
          { name: 'memory.rs', type: 'file', depth: 3, lang: 'rust' },
        ]},
        { name: 'agents', type: 'folder', depth: 2, children: [
          { name: 'orchestrator.py', type: 'file', depth: 3, lang: 'python' },
          { name: 'protocol.py', type: 'file', depth: 3, lang: 'python' },
          { name: 'swarm.py', type: 'file', depth: 3, lang: 'python' },
        ]},
        { name: 'ui', type: 'folder', depth: 2, children: [
          { name: 'app.tsx', type: 'file', depth: 3, lang: 'typescript' },
          { name: 'dashboard.tsx', type: 'file', depth: 3, lang: 'typescript' },
          { name: 'theme.css', type: 'file', depth: 3, lang: 'css' },
        ]},
      ]},
      { name: 'config', type: 'folder', depth: 1, children: [
        { name: 'blackroad.toml', type: 'file', depth: 2, lang: 'toml' },
        { name: 'agents.yaml', type: 'file', depth: 2, lang: 'yaml' },
      ]},
      { name: 'README.md', type: 'file', depth: 1, lang: 'markdown' },
      { name: 'package.json', type: 'file', depth: 1, lang: 'json' },
    ]}
  ];

  const fileContents = {
    'welcome.md': `# Welcome to BlackRoad OS
#
# Your intelligent development environment
# powered by a network of 12 specialized agents.
#
# Getting Started:
# 1. Open the Dashboard to monitor agent activity
# 2. Use the Terminal for direct system access
# 3. Browse Repositories for your codebase
# 4. Configure Tools for your workflow
#
# Agent Network Status: All 12 agents online
# System Version: BlackRoad OS v2.4.0
# Build: 2026.02.03-stable`,
    'runtime.rs': `use std::sync::Arc;
use tokio::runtime::Runtime;

pub struct BlackRoadRuntime {
    scheduler: Arc<Scheduler>,
    agents: Vec<AgentHandle>,
    config: RuntimeConfig,
}

impl BlackRoadRuntime {
    pub fn new(config: RuntimeConfig) -> Self {
        let scheduler = Arc::new(Scheduler::new(
            config.max_threads,
            config.priority_queue_size,
        ));
        Self {
            scheduler,
            agents: Vec::new(),
            config,
        }
    }

    pub async fn start(&mut self) -> Result<()> {
        log::info!("Starting BlackRoad OS Runtime v2.4");
        self.scheduler.initialize().await?;
        for agent in &mut self.agents {
            agent.activate().await?;
        }
        Ok(())
    }
}`,
    'orchestrator.py': `from typing import List, Dict
from blackroad.agents import Agent, Message
from blackroad.protocol import SwarmProtocol

class Orchestrator:
    """Central orchestrator for the BlackRoad agent network."""

    def __init__(self, config: Dict):
        self.agents: List[Agent] = []
        self.protocol = SwarmProtocol(config)
        self.task_queue = []

    async def register_agent(self, agent: Agent):
        """Register a new agent in the network."""
        await agent.initialize()
        self.agents.append(agent)
        await self.protocol.announce(agent)

    async def dispatch(self, task: Task):
        """Dispatch a task to the best available agent."""
        agent = self._select_agent(task)
        result = await agent.execute(task)
        await self.protocol.broadcast(
            Message(type="task_complete", data=result)
        )
        return result`,
    'app.tsx': `import React from 'react';
import { Dashboard } from './dashboard';
import { AgentProvider } from '../agents/context';
import { ThemeProvider } from './theme';

export const App: React.FC = () => {
  return (
    <ThemeProvider theme="pixel-dark">
      <AgentProvider>
        <div className="blackroad-app">
          <Navigation />
          <MainContent>
            <Dashboard />
          </MainContent>
          <StatusBar />
        </div>
      </AgentProvider>
    </ThemeProvider>
  );
};`,
    'blackroad.toml': `[blackroad]
name = "BlackRoad OS"
version = "2.4.0"
edition = "2026"

[runtime]
max_threads = 16
priority_queue_size = 1024
gc_interval = "30s"

[agents]
count = 12
swarm_protocol = "v3"
heartbeat_interval = "5s"

[security]
tls_enabled = true
audit_log = true
scan_on_commit = true`,
  };

  const chatResponses = [
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
    'Deploying to staging cluster.',
    'All systems nominal.',
    'Pipeline execution complete.',
    'Agent consensus reached.',
    'Memory optimization in progress.',
  ];

  const terminalCommands = {
    help: `Available commands:
  help      Show this help message
  status    Show system status
  agents    List all agents
  clear     Clear terminal
  ls        List files
  pwd       Print working directory
  whoami    Show current user
  uptime    Show system uptime
  version   Show OS version
  neofetch  Show system info`,
    status: `\x1b[32mBlackRoad OS v2.4.0\x1b[0m
  Agents Online:  12/12
  CPU Usage:      47.3%
  Memory:         6.2 GB / 16 GB
  Uptime:         14d 7h 23m
  Tasks Active:   8
  Build Status:   Passing`,
    agents: agents.map(a => `  ${a.name.padEnd(14)} ${a.role.padEnd(24)} [Online]`).join('\n'),
    ls: `blackroad.toml  config/  src/  tests/  README.md  package.json  .github/`,
    pwd: `/home/blackroad/projects/blackroad-os`,
    whoami: `blackroad`,
    uptime: `14 days, 7 hours, 23 minutes`,
    version: `BlackRoad OS v2.4.0 (build 2026.02.03-stable)`,
    neofetch: `
  ██████╗ ██╗      █████╗  ██████╗██╗  ██╗
  ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝
  ██████╔╝██║     ███████║██║     █████╔╝
  ██╔══██╗██║     ██╔══██║██║     ██╔═██╗
  ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗
  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
  ROAD OS

  OS:       BlackRoad OS v2.4.0
  Kernel:   br-kernel 6.2.0
  Shell:    br-shell 3.1
  Agents:   12 online
  CPU:      BR-X1 (16 cores)
  Memory:   6.2 GB / 16 GB
  Theme:    Pixel Dark`
  };

  // ==========================================
  //  TAB NAVIGATION
  // ==========================================

  const navItems = document.querySelectorAll('.nav-item');
  const tabContents = document.querySelectorAll('.tab-content');
  let currentScene = 'command';

  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const tab = item.dataset.tab;
      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');
      tabContents.forEach(t => t.classList.remove('active'));
      const target = document.getElementById(`tab-${tab}`);
      if (target) target.classList.add('active');

      // Focus terminal input when switching to terminal
      if (tab === 'terminal') {
        setTimeout(() => document.getElementById('terminal-input')?.focus(), 100);
      }
    });
  });

  // ==========================================
  //  SIDEBAR
  // ==========================================

  document.querySelectorAll('.sidebar-icon').forEach(icon => {
    icon.addEventListener('click', () => {
      document.querySelectorAll('.sidebar-icon').forEach(i => i.classList.remove('active'));
      icon.classList.add('active');
    });
  });

  // ==========================================
  //  COLOR PALETTE
  // ==========================================

  document.querySelectorAll('.color-dot').forEach(dot => {
    dot.addEventListener('click', () => {
      document.querySelectorAll('.color-dot').forEach(d => d.classList.remove('active'));
      dot.classList.add('active');
    });
  });

  // ==========================================
  //  CLOCK
  // ==========================================

  function updateClock() {
    const now = new Date();
    const h = String(now.getHours()).padStart(2, '0');
    const m = String(now.getMinutes()).padStart(2, '0');
    const s = String(now.getSeconds()).padStart(2, '0');
    document.getElementById('clock').textContent = `${h}:${m}:${s}`;
  }
  updateClock();
  setInterval(updateClock, 1000);

  // ==========================================
  //  DASHBOARD - CHAT
  // ==========================================

  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');

  chatInput?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && chatInput.value.trim()) {
      const msg = chatInput.value.trim();
      appendChat('You', msg, '#fff');
      chatInput.value = '';
      setTimeout(() => {
        const agent = agents[Math.floor(Math.random() * agents.length)];
        const resp = chatResponses[Math.floor(Math.random() * chatResponses.length)];
        appendChat(agent.name, resp, agent.color);
      }, 300 + Math.random() * 700);
    }
  });

  function appendChat(name, text, color) {
    const div = document.createElement('div');
    div.className = 'chat-msg';
    div.innerHTML = `<span class="agent-name" style="color:${color}">${esc(name)}:</span> ${esc(text)}`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Animate initial messages
  document.querySelectorAll('#chat-messages .chat-msg').forEach((msg, i) => {
    msg.style.opacity = '0';
    msg.style.transform = 'translateY(8px)';
    msg.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    setTimeout(() => { msg.style.opacity = '1'; msg.style.transform = 'translateY(0)'; }, 80 + i * 100);
  });

  // ==========================================
  //  DASHBOARD - SCENE THUMBNAILS
  // ==========================================

  const thumbItems = document.querySelectorAll('.thumb-item');
  const sceneOverlay = document.getElementById('scene-overlay');

  const sceneNames = {
    command: 'COMMAND CENTER', office: 'HQ OFFICE', campus: 'BLACKROAD CAMPUS',
    museum: 'SCIENCE MUSEUM', store: 'MEGA STORE', lounge: 'AGENT LOUNGE',
    map: 'WORLD MAP', cottage: 'PIXEL COTTAGE'
  };

  thumbItems.forEach(item => {
    item.addEventListener('click', () => {
      const scene = item.dataset.scene;
      currentScene = scene;
      thumbItems.forEach(t => t.classList.remove('active'));
      item.classList.add('active');
      sceneOverlay.textContent = sceneNames[scene] || scene.toUpperCase();
      PixelScenes.renderMainScene(scene);
    });
  });

  // Initial render
  setTimeout(() => {
    PixelScenes.renderThumbnails();
    PixelScenes.renderMainScene('command');
  }, 100);

  window.addEventListener('resize', () => {
    PixelScenes.renderMainScene(currentScene);
  });

  // ==========================================
  //  REPOSITORIES TAB
  // ==========================================

  const repoList = document.getElementById('repo-list');
  const repoDetail = document.getElementById('repo-detail');

  repos.forEach((repo, idx) => {
    const el = document.createElement('div');
    el.className = 'repo-item';
    el.innerHTML = `
      <div class="repo-item-name">${esc(repo.name)}</div>
      <div class="repo-item-desc">${esc(repo.desc)}</div>
      <div class="repo-item-meta">
        <span><span class="repo-lang-dot" style="background:${repo.langColor}"></span>${repo.lang}</span>
        <span>&#9733; ${repo.stars}</span>
        <span>&#9906; ${repo.forks}</span>
      </div>`;
    el.addEventListener('click', () => {
      document.querySelectorAll('.repo-item').forEach(r => r.classList.remove('active'));
      el.classList.add('active');
      showRepoDetail(repo);
    });
    repoList.appendChild(el);
  });

  // Repo search
  document.querySelector('.repo-search-input')?.addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    document.querySelectorAll('.repo-item').forEach(item => {
      const name = item.querySelector('.repo-item-name').textContent.toLowerCase();
      item.style.display = name.includes(q) ? '' : 'none';
    });
  });

  function showRepoDetail(repo) {
    repoDetail.innerHTML = `
      <div class="repo-detail-header">
        <div class="repo-detail-name">${esc(repo.name)}</div>
        <div class="repo-detail-desc">${esc(repo.desc)}</div>
        <div class="repo-detail-stats">
          <div class="repo-stat"><div class="repo-stat-value">${repo.stars}</div><div class="repo-stat-label">Stars</div></div>
          <div class="repo-stat"><div class="repo-stat-value">${repo.forks}</div><div class="repo-stat-label">Forks</div></div>
          <div class="repo-stat"><div class="repo-stat-value">${repo.issues}</div><div class="repo-stat-label">Issues</div></div>
          <div class="repo-stat"><div class="repo-stat-value">${repo.branches.length}</div><div class="repo-stat-label">Branches</div></div>
        </div>
      </div>
      <div class="repo-detail-section">
        <h3>Branches</h3>
        <div class="repo-branch-list">
          ${repo.branches.map(b => `<div class="repo-branch"><span class="repo-branch-icon">&#9588;</span> ${esc(b)}</div>`).join('')}
        </div>
      </div>
      <div class="repo-detail-section">
        <h3>Recent Commits</h3>
        <div class="repo-commit-list">
          ${repo.commits.map(c => `<div class="repo-commit"><span class="commit-hash">${c.hash}</span><span class="commit-msg">${esc(c.msg)}</span><span class="commit-time">${c.time}</span></div>`).join('')}
        </div>
      </div>`;
  }

  // ==========================================
  //  FILES TAB
  // ==========================================

  const fileTreeContent = document.getElementById('file-tree-content');
  const codeArea = document.getElementById('code-area');
  const lineNumbers = document.getElementById('line-numbers');

  function renderTree(items, container) {
    items.forEach(item => {
      const el = document.createElement('div');
      el.className = `tree-item ${item.type === 'folder' ? 'folder' : ''}`;
      let indent = '';
      for (let i = 0; i < item.depth; i++) indent += '<span class="tree-indent"></span>';
      const icon = item.type === 'folder' ? '&#128193;' : '&#128196;';
      el.innerHTML = `${indent}<span class="tree-icon">${icon}</span> ${esc(item.name)}`;

      if (item.type === 'file') {
        el.addEventListener('click', () => {
          document.querySelectorAll('.tree-item').forEach(t => t.classList.remove('active'));
          el.classList.add('active');
          openFile(item.name);
        });
      }
      container.appendChild(el);

      if (item.children) {
        renderTree(item.children, container);
      }
    });
  }

  renderTree(fileTree, fileTreeContent);

  function openFile(name) {
    const content = fileContents[name] || `// ${name}\n// File content not available in demo`;
    const lines = content.split('\n');
    lineNumbers.innerHTML = lines.map((_, i) => i + 1).join('\n');
    codeArea.textContent = content;

    // Update editor tab
    const editorTabs = document.getElementById('editor-tabs');
    editorTabs.innerHTML = `<div class="editor-tab active" data-file="${esc(name)}"><span>${esc(name)}</span><button class="tab-close">&times;</button></div>`;
  }

  // Load welcome file by default
  openFile('welcome.md');

  // ==========================================
  //  TERMINAL TAB
  // ==========================================

  const terminalInput = document.getElementById('terminal-input');
  const terminalOutput = document.getElementById('terminal-output');
  let termHistory = [];
  let historyIdx = -1;

  // Welcome message
  terminalOutput.innerHTML = `<span style="color:#00d4ff">BlackRoad OS v2.4.0 Terminal</span>
<span style="color:#8888aa">Type "help" for available commands.</span>
`;

  terminalInput?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const cmd = terminalInput.value.trim();
      if (!cmd) return;
      termHistory.unshift(cmd);
      historyIdx = -1;
      terminalInput.value = '';

      terminalOutput.innerHTML += `\n<span style="color:#7ed321">blackroad@os</span> <span style="color:#4a90d9">~/projects</span> $ ${esc(cmd)}\n`;

      if (cmd === 'clear') {
        terminalOutput.innerHTML = '';
      } else if (terminalCommands[cmd]) {
        terminalOutput.innerHTML += terminalCommands[cmd] + '\n';
      } else {
        terminalOutput.innerHTML += `<span style="color:#d0021b">command not found: ${esc(cmd)}</span>\n<span style="color:#8888aa">Type "help" for available commands.</span>\n`;
      }
      terminalOutput.scrollTop = terminalOutput.scrollHeight;
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (historyIdx < termHistory.length - 1) {
        historyIdx++;
        terminalInput.value = termHistory[historyIdx];
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIdx > 0) {
        historyIdx--;
        terminalInput.value = termHistory[historyIdx];
      } else {
        historyIdx = -1;
        terminalInput.value = '';
      }
    }
  });

  // Click anywhere in terminal body to focus input
  document.getElementById('terminal-body')?.addEventListener('click', () => {
    terminalInput?.focus();
  });

  // ==========================================
  //  TOOLS TAB
  // ==========================================

  const toolsGrid = document.getElementById('tools-grid');
  const toolDetail = document.getElementById('tool-detail');

  tools.forEach(tool => {
    const el = document.createElement('div');
    el.className = 'tool-card';
    el.innerHTML = `
      <div class="tool-card-header">
        <div class="tool-card-icon" style="background:${tool.iconBg}">${tool.icon}</div>
        <div class="tool-card-name">${esc(tool.name)}</div>
      </div>
      <div class="tool-card-desc">${esc(tool.desc)}</div>
      <span class="tool-card-status ${tool.status === 'active' ? 'tool-status-active' : 'tool-status-idle'}">${tool.status}</span>`;
    el.addEventListener('click', () => {
      document.querySelectorAll('.tool-card').forEach(c => c.classList.remove('active'));
      el.classList.add('active');
      showToolDetail(tool);
    });
    toolsGrid.appendChild(el);
  });

  function showToolDetail(tool) {
    let configHTML = tool.config.map(c => {
      if (c.type === 'toggle') {
        return `<div class="tool-config-row">
          <div class="tool-config-toggle" onclick="this.querySelector('.toggle-track').classList.toggle('on')">
            <div class="toggle-track ${c.value ? 'on' : ''}"><div class="toggle-thumb"></div></div>
            <span class="tool-config-label">${esc(c.label)}</span>
          </div>
        </div>`;
      }
      return `<div class="tool-config-row">
        <label class="tool-config-label">${esc(c.label)}</label>
        <input class="tool-config-input" value="${esc(c.value)}" />
      </div>`;
    }).join('');

    toolDetail.innerHTML = `
      <div class="tool-detail-header">
        <div class="tool-detail-title">${esc(tool.name)}</div>
        <div class="tool-detail-description">${esc(tool.desc)}</div>
      </div>
      <div class="tool-config">${configHTML}</div>`;
  }

  // ==========================================
  //  AGENTS TAB
  // ==========================================

  const agentsGrid = document.getElementById('agents-grid');

  agents.forEach(agent => {
    const el = document.createElement('div');
    el.className = 'agent-card';
    el.innerHTML = `
      <div class="agent-card-top">
        <div class="agent-avatar" style="background:${agent.color}">${agent.name[0]}</div>
        <div class="agent-info">
          <div class="agent-card-name">${esc(agent.name)}</div>
          <div class="agent-card-role">${esc(agent.role)}</div>
        </div>
        <span class="agent-status-badge agent-status-online">Online</span>
      </div>
      <div class="agent-card-task"><strong>Current:</strong> ${esc(agent.task)}</div>
      <div class="agent-card-metrics">
        <div class="agent-metric">
          <div class="agent-metric-bar"><div class="agent-metric-fill" style="width:${agent.cpu}%;background:${agent.cpu > 80 ? '#d0021b' : agent.cpu > 50 ? '#f5a623' : '#7ed321'}"></div></div>
          <div class="agent-metric-label">CPU ${agent.cpu}%</div>
        </div>
        <div class="agent-metric">
          <div class="agent-metric-bar"><div class="agent-metric-fill" style="width:${agent.mem}%;background:${agent.mem > 80 ? '#d0021b' : agent.mem > 50 ? '#f5a623' : '#4a90d9'}"></div></div>
          <div class="agent-metric-label">MEM ${agent.mem}%</div>
        </div>
      </div>`;
    agentsGrid.appendChild(el);
  });

  // ==========================================
  //  UTILITY
  // ==========================================

  function esc(text) {
    const el = document.createElement('span');
    el.textContent = text;
    return el.innerHTML;
  }

});
