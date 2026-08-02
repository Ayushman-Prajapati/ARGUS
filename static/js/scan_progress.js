// ARGUS Scan Progress Tracker
// Handles polling the scan progress API and updating the UI

(function() {
    'use strict';

    const STAGES = [
        { key: 'upload_received', label: 'Upload received', progress: 5 },
        { key: 'preparing', label: 'Preparing scan', progress: 15 },
        { key: 'engines_running', label: 'Running security engines', progress: 30 },
        { key: 'bandit', label: 'Running Bandit...', progress: 40 },
        { key: 'semgrep', label: 'Running Semgrep...', progress: 50 },
        { key: 'ast', label: 'Running ARGUS AST...', progress: 65 },
        { key: 'safety', label: 'Running Safety...', progress: 75 },
        { key: 'pip_audit', label: 'Running pip-audit...', progress: 85 },
        { key: 'aggregating', label: 'Aggregating findings', progress: 90 },
        { key: 'report', label: 'Generating report', progress: 95 },
        { key: 'completed', label: 'Completed', progress: 100 },
    ];

    const ENGINE_ORDER = ['bandit', 'semgrep', 'ast', 'safety', 'pip_audit'];

    const ENGINE_DISPLAY = {
        bandit: { name: 'Bandit', icon: 'shield-lock' },
        semgrep: { name: 'Semgrep', icon: 'search' },
        ast: { name: 'ARGUS AST', icon: 'cpu' },
        safety: { name: 'Safety', icon: 'shield-check' },
        pip_audit: { name: 'pip-audit', icon: 'box-seam' },
    };

    const STATUS_CONFIG = {
        queued: { label: 'Queued', class: 'bg-info', icon: 'hourglass-split', textClass: 'text-info' },
        running: { label: 'Running', class: 'bg-warning', icon: 'play-circle-fill', textClass: 'text-warning' },
        completed: { label: 'Completed', class: 'bg-success', icon: 'check-circle-fill', textClass: 'text-success' },
        failed: { label: 'Failed', class: 'bg-danger', icon: 'x-circle-fill', textClass: 'text-danger' },
        cancelled: { label: 'Cancelled', class: 'bg-secondary', icon: 'stop-circle', textClass: 'text-secondary' },
        skipped: { label: 'Skipped', class: 'bg-secondary', icon: 'dash-circle', textClass: 'text-secondary' },
    };

    class ScanProgress {
        constructor(projectId, statusUrl) {
            this.projectId = projectId;
            this.statusUrl = statusUrl;
            this.pollInterval = 1500; // 1.5s
            this.maxPolls = 200; // ~5 minutes max
            this.pollCount = 0;
            this.currentStageIndex = 0;
            this.simulatedProgress = 0;
            this.lastServerProgress = 0;
            this.consoleEvents = [];

            // Cache DOM elements
            this.elements = {
                bar: document.getElementById('progress-bar'),
                percent: document.getElementById('progress-percent'),
                stage: document.getElementById('progress-stage'),
                message: document.getElementById('progress-message'),
                details: document.getElementById('progress-details'),
                spinner: document.getElementById('progress-spinner'),
                engineStatus: document.getElementById('engine-status'),
                engineCards: document.getElementById('engine-cards'),
                completionActions: document.getElementById('completion-actions'),
                consoleLines: document.getElementById('console-lines'),
                consoleEventCount: document.getElementById('console-event-count'),
                consoleStatus: document.getElementById('console-status'),
            };

            this.startPolling();
        }

        startPolling() {
            this.poll();
        }

        async poll() {
            this.pollCount++;

            try {
                const response = await fetch(this.statusUrl);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                const data = await response.json();

                this.handleServerResponse(data);

                // Continue polling if not complete
                if (data.status !== 'completed' && data.status !== 'failed') {
                    if (this.pollCount < this.maxPolls) {
                        setTimeout(() => this.poll(), this.pollInterval);
                    } else {
                        this.handleTimeout();
                    }
                }
            } catch (error) {
                console.warn('Progress poll failed:', error);
                // On error, simulate progress to keep UI responsive
                this.simulateProgress();
                if (this.pollCount < this.maxPolls) {
                    setTimeout(() => this.poll(), this.pollInterval);
                }
            }
        }

        handleServerResponse(data) {
            const { status, progress, stage, message, details, engines, console: consoleEvents } = data;

            // Update progress bar
            const targetProgress = Math.min(100, Math.max(0, progress || 0));
            this.animateProgress(targetProgress);

            // Update percentage
            if (this.elements.percent) {
                this.elements.percent.textContent = `${Math.round(targetProgress)}%`;
            }

            // Update stage label
            if (this.elements.stage && stage) {
                this.elements.stage.textContent = stage;
            } else if (this.elements.stage) {
                // Fallback to stage from progress
                const stageInfo = this.getStageForProgress(targetProgress);
                this.elements.stage.textContent = stageInfo.label;
            }

            // Update message
            if (this.elements.message && message) {
                this.elements.message.textContent = message;
            }

            // Update details
            if (this.elements.details && details) {
                this.elements.details.textContent = details;
            }

            // Update engine status if provided
            if (engines && this.elements.engineCards) {
                this.renderEngineStatus(engines);
                if (this.elements.engineStatus) {
                    this.elements.engineStatus.style.display = 'block';
                }
            }

            // Update console if provided
            if (consoleEvents && this.elements.consoleLines) {
                this.renderConsoleEvents(consoleEvents);
            }

            // Update console status badge
            if (this.elements.consoleStatus) {
                if (status === 'running' || status === 'queued') {
                    this.elements.consoleStatus.textContent = 'LIVE';
                    this.elements.consoleStatus.className = 'badge bg-warning text-dark';
                } else if (status === 'completed') {
                    this.elements.consoleStatus.textContent = 'COMPLETE';
                    this.elements.consoleStatus.className = 'badge bg-success';
                } else if (status === 'failed') {
                    this.elements.consoleStatus.textContent = 'FAILED';
                    this.elements.consoleStatus.className = 'badge bg-danger';
                } else if (status === 'cancelled') {
                    this.elements.consoleStatus.textContent = 'CANCELLED';
                    this.elements.consoleStatus.className = 'badge bg-secondary';
                } else {
                    this.elements.consoleStatus.textContent = 'WAITING';
                    this.elements.consoleStatus.className = 'badge bg-info';
                }
            }

            // Update console event count
            if (this.elements.consoleEventCount && consoleEvents) {
                this.elements.consoleEventCount.textContent = `${consoleEvents.length} events`;
            }

            // Handle completion
            if (status === 'completed' || status === 'failed' || status === 'cancelled') {
                this.handleCompletion(status);
                return;
            }

            this.lastServerProgress = targetProgress;
        }

        animateProgress(target) {
            if (!this.elements.bar) return;

            const current = parseFloat(this.elements.bar.style.width) || 0;
            // Only animate forward, never backward
            if (target > current) {
                this.elements.bar.style.width = `${target}%`;
                this.elements.bar.setAttribute('aria-valuenow', Math.round(target));
            }
        }

        getStageForProgress(progress) {
            for (let i = STAGES.length - 1; i >= 0; i--) {
                if (progress >= STAGES[i].progress) {
                    return STAGES[i];
                }
            }
            return STAGES[0];
        }

        simulateProgress() {
            // Gentle progress simulation when server isn't responding
            // Only simulate up to 90% - wait for real completion for 100%
            const maxSimulated = 90;
            if (this.simulatedProgress < maxSimulated) {
                // Increment by 1-3% per poll
                this.simulatedProgress += Math.random() * 2 + 1;
                this.simulatedProgress = Math.min(this.simulatedProgress, maxSimulated);

                this.animateProgress(this.simulatedProgress);
                if (this.elements.percent) {
                    this.elements.percent.textContent = `${Math.round(this.simulatedProgress)}%`;
                }

                const stageInfo = this.getStageForProgress(this.simulatedProgress);
                if (this.elements.stage) {
                    this.elements.stage.textContent = stageInfo.label;
                }
            }
        }

        renderEngineStatus(engines) {
            if (!this.elements.engineCards) return;

            const cards = ENGINE_ORDER.map(engineKey => {
                const engine = engines[engineKey];
                if (!engine) return '';

                const status = engine.status || 'pending';
                const statusConfig = STATUS_CONFIG[status] || STATUS_CONFIG.pending;

                const displayInfo = ENGINE_DISPLAY[engineKey] || { name: engineKey, icon: 'gear' };

                return `
                    <div class="col-12 col-md-6 col-lg-4">
                        <div class="d-flex align-items-center gap-2 p-2 bg-transparent border rounded"
                             style="border-color: var(--argus-border);">
                            <i class="bi bi-${statusConfig.icon} ${statusConfig.textClass} fs-5"></i>
                            <div class="flex-grow-1">
                                <div class="fw-medium small">${displayInfo.name}</div>
                                <span class="badge ${statusConfig.class}">${statusConfig.label}</span>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');

            this.elements.engineCards.innerHTML = cards;
        }

        renderConsoleEvents(events) {
            if (!this.elements.consoleLines) return;

            // Keep track of already rendered events by timestamp + message
            const existingKeys = new Set();
            this.elements.consoleLines.querySelectorAll('.console-line').forEach(el => {
                existingKeys.add(el.dataset.key);
            });

            events.forEach(event => {
                const key = `${event.timestamp}-${event.message}`;
                if (existingKeys.has(key)) return;

                const typeConfig = {
                    info: { class: 'text-info', icon: 'info-circle' },
                    success: { class: 'text-success', icon: 'check-circle' },
                    warning: { class: 'text-warning', icon: 'exclamation-triangle' },
                    error: { class: 'text-danger', icon: 'x-circle' },
                }[event.type] || { class: 'text-muted', icon: 'circle' };

                const line = document.createElement('div');
                line.className = 'console-line d-flex align-items-start gap-2 small py-1 border-bottom';
                line.style.borderColor = 'var(--argus-border)';
                line.dataset.key = key;
                line.innerHTML = `
                    <span class="text-muted fw-mono" style="min-width: 45px;">${event.timestamp}</span>
                    <i class="bi bi-${typeConfig.icon} ${typeConfig.class} me-1" style="margin-top: 1px;"></i>
                    <span class="fw-medium ${typeConfig.class}">${event.message}</span>
                    ${event.details ? `<span class="text-muted ms-auto small">${event.details}</span>` : ''}
                `;
                this.elements.consoleLines.appendChild(line);
                existingKeys.add(key);
            });

            // Auto-scroll to bottom
            this.elements.consoleLines.scrollTop = this.elements.consoleLines.scrollHeight;
        }

        handleCompletion(status) {
            // Stop spinner
            if (this.elements.spinner) {
                this.elements.spinner.classList.remove('spinner-border');
                this.elements.spinner.classList.remove('text-warning');
                if (status === 'completed') {
                    this.elements.spinner.classList.add('bi', 'bi-check-circle-fill', 'text-success', 'fs-4');
                } else if (status === 'cancelled') {
                    this.elements.spinner.classList.add('bi', 'bi-stop-circle', 'text-secondary', 'fs-4');
                } else {
                    this.elements.spinner.classList.add('bi', 'bi-x-circle-fill', 'text-danger', 'fs-4');
                }
            }

            // Ensure progress bar is at 100%
            this.animateProgress(100);
            if (this.elements.percent) {
                this.elements.percent.textContent = '100%';
            }
            if (this.elements.stage) {
                this.elements.stage.textContent = status.charAt(0).toUpperCase() + status.slice(1);
            }

            // Show completion message
            if (this.elements.message) {
                if (status === 'completed') {
                    this.elements.message.textContent = 'Scan completed successfully!';
                } else if (status === 'cancelled') {
                    this.elements.message.textContent = 'Scan was cancelled by the user.';
                } else {
                    this.elements.message.textContent = 'Scan encountered an error. See details below.';
                }
            }

            // Show completion actions
            if (this.elements.completionActions) {
                this.elements.completionActions.style.display = 'flex';
            }

            // Update page status badge if present
            const statusBadge = document.querySelector('.scan-status-badge');
            if (statusBadge) {
                statusBadge.className = `scan-status-badge scan-status-${status}`;
                statusBadge.textContent = status.charAt(0).toUpperCase() + status.slice(1);
            }
        }

        handleTimeout() {
            if (this.elements.message) {
                this.elements.message.textContent = 'Scan is taking longer than expected. Please check the results page.';
            }
            if (this.elements.completionActions) {
                this.elements.completionActions.style.display = 'flex';
            }
        }
    }

    // Expose globally
    window.ScanProgress = {
        init: (projectId, statusUrl) => new ScanProgress(projectId, statusUrl),
    };
})();