// ARGUS Toast Notification System
// Reusable toast notifications for user feedback

(function() {
    'use strict';

    const TOAST_TYPES = {
        success: { icon: 'check-circle-fill', class: 'bg-success', textClass: 'text-white' },
        error: { icon: 'x-circle-fill', class: 'bg-danger', textClass: 'text-white' },
        warning: { icon: 'exclamation-triangle-fill', class: 'bg-warning', textClass: 'text-dark' },
        info: { icon: 'info-circle-fill', class: 'bg-info', textClass: 'text-white' },
    };

    const DEFAULT_DURATION = 5000; // 5 seconds

    class ToastManager {
        constructor() {
            this.container = document.getElementById('argus-toast-container');
            if (!this.container) {
                this.container = document.createElement('div');
                this.container.id = 'argus-toast-container';
                this.container.className = 'toast-container position-fixed top-0 end-0 p-3';
                this.container.style.zIndex = '4000';
                document.body.appendChild(this.container);
            }
        }

        show(message, type = 'info', options = {}) {
            const { duration = DEFAULT_DURATION, title, actionText, actionCallback } = options;
            const toastConfig = TOAST_TYPES[type] || TOAST_TYPES.info;

            const toastEl = document.createElement('div');
            toastEl.className = `toast ${toastConfig.class} ${toastConfig.textClass} align-items-center`;
            toastEl.role = 'alert';
            toastEl.ariaLive = 'assertive';
            toastEl.ariaAtomic = 'true';
            toastEl.style.minWidth = '300px';
            toastEl.style.maxWidth = '450px';

            let actionBtn = '';
            if (actionText && actionCallback) {
                actionBtn = `
                    <div class="toast-footer mt-2 pt-2 border-top border-white border-opacity-25">
                        <button type="button" class="btn btn-sm btn-light" data-toast-action>${actionText}</button>
                    </div>
                `;
            }

            toastEl.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body d-flex align-items-center gap-2">
                        <i class="bi bi-${toastConfig.icon} fs-5"></i>
                        <div>
                            ${title ? `<div class="fw-semibold small">${title}</div>` : ''}
                            <div class="small">${message}</div>
                        </div>
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                ${actionBtn}
            `;

            if (actionBtn) {
                toastEl.querySelector('[data-toast-action]').addEventListener('click', () => {
                    actionCallback();
                    bootstrap.Toast.getInstance(toastEl).hide();
                });
            }

            this.container.appendChild(toastEl);

            const toast = new bootstrap.Toast(toastEl, {
                autohide: true,
                delay: duration,
            });
            toast.show();

            toastEl.addEventListener('hidden.bs.toast', () => {
                toastEl.remove();
            });

            return toast;
        }

        success(message, options = {}) {
            return this.show(message, 'success', options);
        }

        error(message, options = {}) {
            return this.show(message, 'error', options);
        }

        warning(message, options = {}) {
            return this.show(message, 'warning', options);
        }

        info(message, options = {}) {
            return this.show(message, 'info', options);
        }
    }

    window.ArgusToast = new ToastManager();
})();