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
                    const targetAttr = stat.getAttribute("data-target");
                    if (targetAttr === null) return;
                    const targetVal = parseInt(targetAttr, 10) || 0;
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
                    {value: "rgba(245, 166, 35, 0.85)", easing: "easeOutSine", duration: 250}, // Amber
                    {value: "rgba(201, 138, 46, 0.85)", easing: "easeInOutQuad", duration: 400}, // Deep amber
                    {value: "rgba(42, 42, 31, 0.4)", easing: "easeOutQuad", duration: 500} // Restore default
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
});
