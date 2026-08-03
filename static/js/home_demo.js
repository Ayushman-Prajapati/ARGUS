// ARGUS Homepage Demo Scan Driver
//
// Fully self-contained client-side demo. Static demo data lives here — no
// fetch, no page navigation, and no database writes of any kind. Nothing here
// ever creates a Scan / Project / Finding / Report, and the demo never shows up
// in Scan History.
//
// Behavior:
// - "Run Demo Scan" shows a temporary code-viewer + terminal overlay on top of
//   the idle animated grid. The grid keeps animating underneath (laser sweep +
//   severity pulses) while detections flash the vulnerable lines.
// - When the demo ends the overlay fades out, the grid returns to its idle
//   animated state, and the button reverts to "Run Demo Scan".
// - No "Demo Complete" state, no "Run Demo Again", no report buttons.

(function () {
    'use strict';

    // Platform severity colors (see custom.css).
    const SEVERITY_COLORS = {
        critical: '#e0472a',
        high: '#f5a623',
        medium: '#c98a2e',
        low: '#8a7a4a',
    };

    // The "vulnerable" file shown in the demo code viewer.
    const DEMO_CODE = [
        'import sqlite3',
        'import subprocess',
        'import pickle',
        '',
        'def login(username, password):',
        '    query = f"SELECT * FROM users WHERE username=\'{username}\'"',
        '    cursor.execute(query)',
        '',
        'def run(command):',
        '    subprocess.run(command, shell=True)',
        '',
        'secret_key = "sk_live_demo_secret"',
        '',
        'password = "admin123"',
        '',
        'data = pickle.loads(user_input)',
    ];

    // Detections in the order they are announced. ``step`` is the index into
    // DEMO_TERMINAL at which the finding is revealed; ``line`` is 1-based and
    // matches DEMO_CODE.
    const DEMO_VULNERABILITIES = [
        {
            step: 2,
            line: 10,
            engine: 'Bandit',
            severity: 'high',
            label: 'subprocess.run(command, shell=True)',
        },
        {
            step: 3,
            line: 7,
            engine: 'Semgrep',
            severity: 'critical',
            label: 'cursor.execute(query)',
        },
        {
            step: 4,
            line: 12,
            engine: 'ARGUS AST',
            severity: 'critical',
            label: 'secret_key = "sk_live_demo_secret"',
        },
        {
            step: 5,
            line: 16,
            engine: 'ARGUS AST',
            severity: 'high',
            label: 'pickle.loads(user_input)',
        },
    ];

    // Terminal feed, paced 1 line per second. Ends on a plain completion line —
    // there is no "Demo Complete" state in the UI.
    const DEMO_TERMINAL = [
        '[00:01] Loading project...',
        '[00:02] Parsing AST...',
        '[00:03] Bandit detected insecure subprocess usage.',
        '[00:04] Semgrep detected SQL Injection.',
        '[00:05] ARGUS AST detected Hardcoded Secret.',
        '[00:06] ARGUS AST detected Unsafe Deserialization.',
        '[00:07] Aggregating findings...',
        '[00:08] Scan complete — 4 vulnerabilities found.',
    ];

    const LINE_MS = 1000;

    class HomeDemo {
        constructor() {
            this.running = false;
            this.timers = [];
            this.overlay = null;
            this.laser = null;
            this.sweepAnim = null;

            this.triggerBtn = document.getElementById('trigger-demo-btn');
            this.container = document.querySelector('.grid-visualizer-container');

            this.bind();
        }

        bind() {
            if (this.triggerBtn) {
                this.triggerBtn.addEventListener('click', () => this.start());
            }
        }

        clearTimers() {
            this.timers.forEach((t) => clearTimeout(t));
            this.timers = [];
        }

        start() {
            if (this.running) return;
            this.clearTimers();
            this.teardown(); // Remove any leftover overlay/laser from a prior run.

            if (!this.container || !this.triggerBtn) return;
            this.running = true;

            this.setButtonScanning();

            // Build the overlay (code viewer + terminal) above the grid.
            this.buildOverlay();
            this.renderCode();

            // Reset the terminal feed.
            if (this.terminalLines) this.terminalLines.innerHTML = '';
            if (this.terminalStatus) {
                this.terminalStatus.textContent = 'SCANNING';
                this.terminalStatus.className = 'text-warning';
            }
            if (this.activeEngine) this.activeEngine.textContent = 'Demo';

            // The grid keeps animating underneath: start a looping laser sweep.
            this.startLaserSweep();

            // Stream the terminal feed, one line per step.
            DEMO_TERMINAL.forEach((line, index) => {
                this.timers.push(setTimeout(() => this.appendTerminal(line), index * LINE_MS));
            });

            // Reveal each detection as its terminal line lands.
            DEMO_VULNERABILITIES.forEach((vuln) => {
                this.timers.push(setTimeout(() => this.onDetect(vuln), vuln.step * LINE_MS));
            });

            // Finish after the feed ends + a short beat.
            this.timers.push(setTimeout(() => this.finish(), DEMO_TERMINAL.length * LINE_MS + 500));
        }

        buildOverlay() {
            const overlay = document.createElement('div');
            overlay.className = 'demo-scan-overlay';
            overlay.innerHTML = `
                <div class="demo-code-panel cyber-panel">
                    <div class="code-viewer-header">
                        <div class="d-flex align-items-center gap-2 min-width-0">
                            <i class="bi bi-file-earmark-code"></i>
                            <span class="code-viewer-filename text-truncate">demo_app.py</span>
                            <span class="code-viewer-engine-badge" id="demo-active-engine">Demo</span>
                        </div>
                    </div>
                    <div class="demo-code-body">
                        <pre class="code-viewer-pre"><code id="demo-code-lines"></code></pre>
                    </div>
                </div>
                <div class="demo-terminal cyber-panel">
                    <div class="console-header">
                        <span>ARGUS DEMO TERMINAL</span>
                        <span id="demo-terminal-status" class="text-warning">SCANNING</span>
                    </div>
                    <div class="console-body" id="demo-terminal-lines"></div>
                </div>
            `;
            this.container.appendChild(overlay);
            this.overlay = overlay;

            this.codeLines = overlay.querySelector('#demo-code-lines');
            this.terminalLines = overlay.querySelector('#demo-terminal-lines');
            this.terminalStatus = overlay.querySelector('#demo-terminal-status');
            this.activeEngine = overlay.querySelector('#demo-active-engine');

            // Slide the overlay in.
            if (typeof anime !== 'undefined') {
                anime({
                    targets: overlay,
                    opacity: [0, 1],
                    translateY: [12, 0],
                    duration: 350,
                    easing: 'easeOutQuad',
                });
            }
        }

        renderCode() {
            if (!this.codeLines) return;
            const frag = document.createDocumentFragment();
            DEMO_CODE.forEach((text, i) => {
                const span = document.createElement('span');
                span.className = 'demo-code-line';
                span.dataset.line = i + 1; // 1-based
                span.textContent = text;
                frag.appendChild(span);
                frag.appendChild(document.createTextNode('\n'));
            });
            this.codeLines.innerHTML = '';
            this.codeLines.appendChild(frag);
        }

        lineEl(lineNum) {
            return this.codeLines
                ? this.codeLines.querySelector(`.demo-code-line[data-line="${lineNum}"]`)
                : null;
        }

        startLaserSweep() {
            if (typeof anime === 'undefined') return;
            const laser = document.createElement('div');
            laser.className = 'laser-sweep';
            laser.style.zIndex = '2100';
            this.container.appendChild(laser);
            this.laser = laser;

            this.sweepAnim = anime({
                targets: laser,
                top: ['-5px', '100%'],
                opacity: [0, 1, 1, 0],
                easing: 'easeInOutQuad',
                duration: 2000,
                loop: true,
            });
        }

        onDetect(vuln) {
            // Flash the matching code line with its severity color.
            const el = this.lineEl(vuln.line);
            if (el) {
                const color = SEVERITY_COLORS[vuln.severity] || SEVERITY_COLORS.medium;
                el.classList.remove('demo-flash', 'demo-line-highlight');
                void el.offsetWidth; // Force reflow so the flash restarts on replay.
                el.classList.add('demo-flash');
                el.style.setProperty('--sev-color', color);
                el.style.backgroundColor = color + '33';
                el.dataset.severity = vuln.severity;

                this.timers.push(setTimeout(() => {
                    el.classList.remove('demo-flash');
                    el.classList.add('demo-line-highlight');
                }, 650));
            }

            // Reflect the detecting engine in the overlay header.
            if (this.activeEngine) this.activeEngine.textContent = vuln.engine;

            // Pulse the grid underneath with the severity color.
            this.pulseGrid(SEVERITY_COLORS[vuln.severity] || SEVERITY_COLORS.medium);
        }

        appendTerminal(line) {
            if (!this.terminalLines) return;
            const div = document.createElement('div');
            div.className = 'console-code-line active';
            div.textContent = line;
            this.terminalLines.appendChild(div);
            this.terminalLines.scrollTop = this.terminalLines.scrollHeight;
        }

        pulseGrid(color) {
            const cells = document.querySelectorAll('.grid-cell');
            if (!cells.length || typeof anime === 'undefined') return;
            anime({
                targets: cells,
                scale: [
                    { value: 0.5, easing: 'easeOutSine', duration: 250 },
                    { value: 1.15, easing: 'easeInOutQuad', duration: 400 },
                    { value: 1, easing: 'easeOutQuad', duration: 300 },
                ],
                backgroundColor: [
                    { value: color, easing: 'easeOutSine', duration: 250 },
                    { value: 'rgba(245, 166, 35, 0.5)', easing: 'easeInOutQuad', duration: 400 },
                    { value: 'rgba(42, 42, 31, 0.45)', easing: 'easeOutQuad', duration: 400 },
                ],
                delay: anime.stagger(20, { grid: [14, 10], from: 'center' }),
                easing: 'easeOutQuad',
            });
        }

        finish() {
            this.running = false;
            this.clearTimers();

            // Stop the laser sweep and fade the overlay out, revealing the idle grid.
            if (this.sweepAnim) this.sweepAnim.pause();
            if (this.laser) {
                this.laser.style.opacity = '0';
                this.laser.remove();
                this.laser = null;
            }
            if (this.overlay) {
                const overlay = this.overlay;
                if (typeof anime !== 'undefined') {
                    anime({
                        targets: overlay,
                        opacity: 0,
                        translateY: [0, 8],
                        duration: 400,
                        easing: 'easeOutQuad',
                        complete: () => overlay.remove(),
                    });
                } else {
                    overlay.remove();
                }
                this.overlay = null;
            }

            // Back to the idle grid.
            this.pulseGrid(null);

            // Restore the trigger button.
            this.setButtonIdle();
        }

        setButtonScanning() {
            if (!this.triggerBtn) return;
            this.triggerBtn.disabled = true;
            this.triggerBtn.innerHTML =
                '<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Scanning...';
        }

        setButtonIdle() {
            if (!this.triggerBtn) return;
            this.triggerBtn.disabled = false;
            this.triggerBtn.innerHTML = '<i class="bi bi-play-fill me-1"></i> Run Demo Scan';
        }

        // Remove any leftover overlay / laser from a previous run.
        teardown() {
            if (this.sweepAnim) this.sweepAnim.pause();
            this.sweepAnim = null;
            if (this.laser) {
                this.laser.remove();
                this.laser = null;
            }
            if (this.overlay) {
                this.overlay.remove();
                this.overlay = null;
            }
        }
    }

    window.HomeDemo = {
        init: () => {
            if (!window.HomeDemo._instance) {
                window.HomeDemo._instance = new HomeDemo();
            }
            return window.HomeDemo._instance;
        },
    };
})();
