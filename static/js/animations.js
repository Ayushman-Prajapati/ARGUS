// ARGUS UI animations, powered by anime.js
document.addEventListener("DOMContentLoaded", () => {
    if (typeof anime === "undefined") {
        console.warn("anime.js is not loaded.");
        return;
    }

    // 1. DYNAMIC GRID CELL GENERATION (14x10)
    const staggerGrid = document.getElementById("stagger-grid");
    const totalCells = 14 * 10;
    if (staggerGrid) {
        for (let i = 0; i < totalCells; i++) {
            const cell = document.createElement("div");
            cell.classList.add("grid-cell");
            cell.setAttribute("data-index", i);
            staggerGrid.appendChild(cell);
        }
    }

    // 2. INITIAL LOAD ENTRIES (STAGGERED)
    // Stagger in the grid cells on page load
    if (document.querySelectorAll(".grid-cell").length) {
        anime({
            targets: ".grid-cell",
            scale: [0.1, 1],
            opacity: [0, 1],
            delay: anime.stagger(15, {grid: [14, 10], from: 'center'}),
            easing: "easeOutBack",
            duration: 800
        });
    }

    // Hero content entrance
    anime({
        targets: ".argus-hero h1, .argus-hero p, .argus-hero .btn-argus-primary, .argus-hero .btn-argus-neon",
        translateY: [20, 0],
        opacity: [0, 1],
        delay: anime.stagger(120),
        easing: "easeOutQuad",
        duration: 800
    });

    // 3. STAT COUNTERS COUNT-UP ANIMATION
    const statCards = document.querySelectorAll(".argus-stat-card");
    const statValues = document.querySelectorAll(".stat-value");
    
    // Stagger the cards entrance
    if (statCards.length) {
        anime({
            targets: statCards,
            translateY: [30, 0],
            opacity: [0, 1],
            delay: anime.stagger(100),
            easing: "easeOutElastic(1, .8)",
            duration: 1000,
            complete: () => {
                // Once cards enter, count up the statistics values
                statValues.forEach(stat => {
                    const targetVal = parseInt(stat.getAttribute("data-target"), 10) || 0;
                    const countObj = { value: 0 };
                    anime({
                        targets: countObj,
                        value: targetVal,
                        round: 1,
                        duration: 1800,
                        easing: "easeOutExpo",
                        update: () => {
                            stat.textContent = countObj.value;
                        }
                    });
                });
            }
        });
    }

    // 4. INTERACTIVE GRID STAGGER RIPPLE
    const cells = document.querySelectorAll(".grid-cell");
    cells.forEach(cell => {
        cell.addEventListener("click", (e) => {
            const index = parseInt(e.target.getAttribute("data-index"), 10);
            
            // Ripple wave of scaling and color
            anime({
                targets: ".grid-cell",
                scale: [
                    {value: 0.5, easing: "easeOutSine", duration: 250},
                    {value: 1.1, easing: "easeInOutQuad", duration: 400},
                    {value: 1, easing: "easeOutQuad", duration: 300}
                ],
                backgroundColor: [
                    {value: "rgba(59, 130, 246, 0.8)", easing: "easeOutSine", duration: 250}, // Cyan/Blue
                    {value: "rgba(217, 70, 239, 0.8)", easing: "easeInOutQuad", duration: 400}, // Purple
                    {value: "rgba(35, 45, 69, 0.4)", easing: "easeOutQuad", duration: 500} // Restore default
                ],
                delay: anime.stagger(50, {grid: [14, 10], from: index})
            });
        });
    });

    // 5. SCROLL INTERSECTION OBSERVER FOR CARDS
    const scrollTargets = document.querySelectorAll(".argus-method-card, .argus-card, .finding-row, .chart-card");
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Trigger staggered entrance for child cards if it's a container or list
                if (entry.target.classList.contains("argus-method-card")) {
                    anime({
                        targets: entry.target,
                        translateY: [25, 0],
                        opacity: [0, 1],
                        easing: "easeOutCubic",
                        duration: 600
                    });
                } else if (entry.target.classList.contains("finding-row")) {
                    anime({
                        targets: entry.target,
                        translateX: [-20, 0],
                        opacity: [0, 1],
                        easing: "easeOutCubic",
                        duration: 500
                    });
                } else {
                    anime({
                        targets: entry.target,
                        translateY: [30, 0],
                        opacity: [0, 1],
                        easing: "easeOutCubic",
                        duration: 700
                    });
                }
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    });

    scrollTargets.forEach(target => {
        // Pre-set low opacity to avoid flash of content
        target.style.opacity = "0";
        observer.observe(target);
    });

    // 6. SCANNING SIMULATION PIPELINE
    const triggerBtn = document.getElementById("trigger-scan-btn");
    const scanConsole = document.getElementById("scan-console");
    const laserLine = document.getElementById("laser-line");
    const consoleCode = document.getElementById("console-code");
    const simAlert = document.getElementById("sim-alert");
    const scanStatusText = document.getElementById("scan-status-text");

    const simCodeLines = [
        "import os",
        "from django.db import connection",
        "",
        "def get_user(request):",
        "    user_id = request.GET.get('id')",
        "    # Vulnerability: raw concatenation",
        "    query = \"SELECT * FROM users WHERE id = \" + user_id",
        "    cursor = connection.cursor()",
        "    cursor.execute(query) # SQL Injection Vulnerability!",
        "    return cursor.fetchone()"
    ];

    let isSimulating = false;

    if (triggerBtn && scanConsole && laserLine && consoleCode) {
        triggerBtn.addEventListener("click", () => {
            if (isSimulating) return;
            isSimulating = true;
            triggerBtn.disabled = true;
            triggerBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> Running Demo...`;

            // Reset console html
            consoleCode.innerHTML = "";
            simCodeLines.forEach((line, index) => {
                const div = document.createElement("div");
                div.classList.add("console-code-line");
                // Escaping code tags
                div.textContent = `${index + 1}  ${line}`;
                consoleCode.appendChild(div);
            });

            // Make console visible
            scanConsole.classList.add("active");
            scanStatusText.textContent = "STATUS: INITIALIZING SCANNER...";
            scanStatusText.style.color = "var(--neon-cyan)";
            simAlert.style.opacity = "0";
            simAlert.style.transform = "translateY(10px) scale(0.95)";

            // Build sequence timeline
            const simTimeline = anime.timeline({
                complete: () => {
                    // Let scanner show COMPLETED status
                    scanStatusText.textContent = "STATUS: COMPLETED (1 ISSUE FOUND)";
                    scanStatusText.style.color = "var(--neon-pink)";
                    
                    // Hold screen for 4 seconds, then return to normal stagger-grid
                    setTimeout(() => {
                        anime({
                            targets: scanConsole,
                            opacity: [1, 0],
                            duration: 500,
                            easing: "easeOutQuad",
                            complete: () => {
                                scanConsole.classList.remove("active");
                                scanConsole.style.opacity = "";
                                triggerBtn.disabled = false;
                                triggerBtn.innerHTML = `<i class="bi bi-play-fill me-1"></i> Trigger Scan Demo`;
                                isSimulating = false;
                                
                                // Do a celebratory grid wave starting from center
                                anime({
                                    targets: ".grid-cell",
                                    scale: [
                                        {value: 0.5, duration: 200},
                                        {value: 1.1, duration: 300},
                                        {value: 1, duration: 300}
                                    ],
                                    backgroundColor: [
                                        {value: "var(--neon-green)", duration: 200},
                                        {value: "var(--neon-cyan)", duration: 300},
                                        {value: "rgba(35, 45, 69, 0.4)", duration: 400}
                                    ],
                                    delay: anime.stagger(25, {grid: [14, 10], from: 'center'}),
                                    easing: "easeOutQuad"
                                });
                            }
                        });
                    }, 4000);
                }
            });

            // 1. Reveal lines staggered (quick typing simulation)
            simTimeline.add({
                targets: ".console-code-line",
                opacity: [0.1, 0.4],
                delay: anime.stagger(80),
                duration: 500,
                easing: "easeOutQuad",
                changeBegin: () => {
                    scanStatusText.textContent = "STATUS: ANALYZING CODE SYSTEM...";
                    scanStatusText.style.color = "var(--neon-green)";
                }
            });

            // 2. Activate laser line scanning
            simTimeline.add({
                targets: laserLine,
                top: ["-5px", "100%"],
                opacity: [0, 1, 1, 0],
                easing: "easeInOutQuad",
                duration: 2500,
                offset: "-=200", // Start slightly early
                // Update callback to highlight lines as laser sweeps down
                update: (anim) => {
                    const progress = anim.progress; // 0 to 100
                    const lineCount = simCodeLines.length;
                    const activeIndex = Math.floor((progress / 100) * lineCount);
                    
                    const domLines = document.querySelectorAll(".console-code-line");
                    domLines.forEach((domLine, idx) => {
                        if (idx <= activeIndex) {
                            domLine.classList.add("active");
                        } else {
                            domLine.classList.remove("active");
                        }
                    });
                }
            });

            // 3. Flag vulnerabilities at target index 6 & 8
            simTimeline.add({
                targets: ".console-code-line:nth-child(7), .console-code-line:nth-child(9)",
                color: "var(--neon-pink)",
                backgroundColor: "rgba(244, 63, 94, 0.15)",
                opacity: 1,
                fontWeight: "700",
                duration: 300,
                easing: "easeInQuad",
                offset: "-=1000" // Trigger while laser is passing line 8
            });

            // 4. Elastic slide-in of alert box
            simTimeline.add({
                targets: simAlert,
                opacity: [0, 1],
                scale: [0.85, 1],
                translateY: [15, 0],
                easing: "easeOutElastic(1, .6)",
                duration: 800,
                offset: "-=400"
            });
        });
    }
});
