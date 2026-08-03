// ARGUS Homepage Demo Scan Driver
// Runs the entire demo scan on the homepage, entirely client-side:
// - Renders a realistic vulnerable Python file in a code viewer.
// - Streams a live terminal feed as "engines" detect findings.
// - Highlights each vulnerable line with its severity color as it's detected.
// - Animates the homepage stat cards on completion and shows "Demo Complete".
// - "Run Demo Again" resets and replays.
// No page navigation and no database writes are involved.

(function () {
    'use strict';

    // Mirrors the platform severity colors (see custom.css).
    const SEVERITY = {
        critical: '#e0472a',
        high: '#f5a623',
        medium: '#c98a2e',
        low: '#8a7a4a',
    };

    const LINE_MS = 1000; // ms per terminal line / detection step

    class HomeDemo {
        constructor(config) {
            this.config = config || {};
            // Static dataset injected from the view (see demo_service.py).
            this.data = this.config.data || {
                code: [], vulnerabilities: [], terminal: [], stats: {},
            };
            this.running = false;

            this.elements = {
                triggerBtn: document.getElementById('trigger-demo-btn'),
                stagePanel: document.getElementById('demo-stage-panel'),
                stageLabel: document.getElementById('demo-stage-label'),
                stageProgress: document.getElementById('demo-stage-progress'),
                stageSpinner: document.getElementById('demo-stage-spinner'),
                completeState: document.getElementById('demo-complete-state'),
                runAgainBtn: document.getElementById('demo-run-again-btn'),
                codeLines: document.getElementById('demo-code-lines'),
                activeEngine: document.getElementById('demo-active-engine'),
                terminalStatus: document.getElementById('demo-terminal-status'),
                terminalLines: document.getElementById('demo-terminal-lines'),
            };

            this.timers = [];
            this.bind();
        }

        bind() {
            if (this.elements.triggerBtn) {
                this.elements.triggerBtn.addEventListener('click', () => this.start());
            }
            if (this.elements.runAgainBtn) {
                this.elements.runAgainBtn.addEventListener('click', () => this.start());
            }
            if (this.config.autoStart) {
                this.start();
            }
        }

        clearTimers() {
            this.timers.forEach((t) => clearTimeout(t));
            this.timers = [];
        }

        start() {
            // Reset any in-flight run.
            this.clearTimers();
            this.running = true;
            this.animFrame = null;

            // Reset trigger button + show stage panel, hide completion.
            if (this.elements.triggerBtn) {
                this.elements.triggerBtn.disabled = true;
                this.elements.triggerBtn.innerHTML =
                    '<span class="spinner-border spinner-border-sm me-1"></span> Scanning...';
            }
            if (this.elements.completeState) this.elements.completeState.style.display = 'none';
            if (this.elements.stagePanel) this.elements.stagePanel.style.display = 'block';
            if (this.elements.stageSpinner) {
                this.elements.stageSpinner.className = 'spinner-border spinner-border-sm text-warning';
            }

            // Render the code viewer.
            this.renderCode();

            // Reset terminal.
            if (this.elements.terminalLines) this.elements.terminalLines.innerHTML = '';
            if (this.elements.terminalStatus) {
                this.elements.terminalStatus.textContent = 'RUNNING';
                this.elements.terminalStatus.className = 'text-warning';
            }

            // Play the terminal feed, one line per step.
            const lines = this.data.terminal || [];
            lines.forEach((line, index) => {
                this.timers.push(setTimeout(() => this.appendTerminal(line), index * LINE_MS));
            });

            // Each detection highlights a vulnerable line right as its
            // terminal message appears.
            const vulns = this.data.vulnerabilities || [];
            // Terminal indices where detections are announced:
            //  index 2 -> Bandit, 3 -> Semgrep, 4 & 5 -> ARGUS AST.
            vulns.forEach((vuln, idx) => {
                const atLine = 3 + idx; // lines 3..6 in terminal correspond
                this.timers.push(setTimeout(() => this.highlight(vuln), atLine * LINE_MS));
            });

            // Finish after the last terminal line + a short beat.
            this.timers.push(setTimeout(() => this.finish(), (lines.length + 1) * LINE_MS));
        }

        renderCode() {
            if (!this.elements.codeLines) return;
            const code = this.data.code || [];
            // Build line-by-line so each line can be targeted for highlight.
            const frag = document.createDocumentFragment();
            code.forEach((text, i) => {
                const span = document.createElement('span');
                span.className = 'demo-code-line';
                span.dataset.line = i + 1; // 1-based
                span.textContent = text;
                frag.appendChild(span);
                frag.appendChild(document.createTextNode('\n'));
            });
            this.elements.codeLines.innerHTML = '';
            this.elements.codeLines.appendChild(frag);
        }

        lineEl(lineNum) {
            return this.elements.codeLines
                ? this.elements.codeLines.querySelector(`.demo-code-line[data-line="${lineNum}"]`)
                : null;
        }

        highlight(vuln) {
            const el = this.lineEl(vuln.line);
            if (!el) return;
            const color = SEVERITY[vuln.severity] || SEVERITY.medium;
            // Clear any prior highlight state.
            el.classList.remove('demo-flash');
            el.classList.remove('demo-line-highlight');
            // Force reflow so the flash animation restarts on replay.
            void el.offsetWidth;
            el.classList.add('demo-flash');
            el.style.setProperty('--sev-color', color);
            // ~20% alpha fill for the persistent highlight (hex + alpha suffix).
            el.style.backgroundColor = color + '33';
            el.dataset.severity = vuln.severity;

            // Move to persistent highlight after the flash is out.
            this.timers.push(setTimeout(() => {
                el.classList.remove('demo-flash');
                el.classList.add('demo-line-highlight');
            }, 650));

            // Reflect the detecting engine in the viewer header.
            if (this.elements.activeEngine) {
                this.elements.activeEngine.textContent = vuln.engine;
            }
        }

        appendTerminal(line) {
            if (!this.elements.terminalLines) return;
            const div = document.createElement('div');
            div.className = 'console-code-line active';
            div.textContent = line;
            this.elements.terminalLines.appendChild(div);
            // Auto-scroll to keep the latest line visible.
            this.elements.terminalLines.scrollTop = this.elements.terminalLines.scrollHeight;
        }

        finish() {
            this.running = false;

            // Final terminal status.
            if (this.elements.terminalStatus) {
                this.elements.terminalStatus.textContent = 'COMPLETE';
                this.elements.terminalStatus.className = 'text-success';
            }

            // Stage label → Complete, 100%.
            if (this.elements.stageLabel) this.elements.stageLabel.textContent = 'Complete';
            if (this.elements.stageProgress) this.elements.stageProgress.textContent = '100%';
            if (this.elements.stageSpinner) {
                this.elements.stageSpinner.className = 'bi bi-check-circle-fill text-success fs-5';
            }

            // Restore the trigger button.
            if (this.elements.triggerBtn) {
                this.elements.triggerBtn.disabled = false;
                this.elements.triggerBtn.innerHTML = '<i class="bi bi-play-fill me-1"></i> Run Demo Scan';
            }

            // Show "Demo Complete" + single "Run Demo Again" action.
            if (this.elements.completeState) this.elements.completeState.style.display = 'flex';

            // Animate stats to their temporary demo values.
            this.animateCounters();
        }

        animateCounters() {
            const values = document.querySelectorAll('.stat-value');
            if (typeof anime === 'undefined') return;
            values.forEach((stat) => {
                const demoTarget = stat.getAttribute('data-demo-target');
                if (demoTarget === null) return;
                const targetVal = parseInt(demoTarget, 10) || 0;
                const countObj = { value: 0 };
                anime({
                    targets: countObj,
                    value: targetVal,
                    round: 1,
                    duration: 1200,
                    easing: 'easeOutExpo',
                    update: () => {
                        stat.textContent = countObj.value;
                    },
                });
            });
        }
    }

    window.HomeDemo = {
        init: (config) => new HomeDemo(config),
    };
})();