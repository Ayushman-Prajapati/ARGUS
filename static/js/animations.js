// ARGUS UI animations, powered by Motion (motion.dev - formerly Framer Motion)
document.addEventListener("DOMContentLoaded", () => {
    if (typeof Motion === "undefined") return;
    const { animate, stagger, inView } = Motion;

    // Fade + rise in alert messages
    const alerts = document.querySelectorAll(".argus-fade-in");
    if (alerts.length) {
        animate(alerts, { opacity: [0, 1], y: [-8, 0] }, { duration: 0.4, delay: stagger(0.08) });
    }

    // Stagger the method / stat cards on the home page as they enter view
    const cards = document.querySelectorAll(".argus-method-card, .argus-stat-card");
    if (cards.length) {
        animate(cards, { opacity: [0, 1], y: [16, 0] }, { duration: 0.45, delay: stagger(0.07), easing: "ease-out" });
    }

    // Hero heading + subtitle
    const heroTitle = document.querySelector(".argus-hero h1");
    const heroSub = document.querySelector(".argus-hero p");
    if (heroTitle) {
        animate(heroTitle, { opacity: [0, 1], y: [14, 0] }, { duration: 0.5 });
    }
    if (heroSub) {
        animate(heroSub, { opacity: [0, 1], y: [14, 0] }, { duration: 0.5, delay: 0.1 });
    }

    // Risk gauge pop-in
    const gauge = document.querySelector(".risk-gauge");
    if (gauge) {
        animate(gauge, { scale: [0.7, 1], opacity: [0, 1] }, { duration: 0.5, easing: [0.34, 1.56, 0.64, 1] });
    }

    // Finding rows: fade in as they scroll into view, staggered
    const findingRows = document.querySelectorAll(".finding-row");
    findingRows.forEach((row, i) => {
        inView(row, () => {
            animate(row, { opacity: [0, 1], x: [-10, 0] }, { duration: 0.35, delay: Math.min(i * 0.02, 0.3) });
        }, { margin: "0px 0px -10% 0px" });
    });

    // Panel entrance for forms/detail panels
    const panels = document.querySelectorAll(".argus-panel");
    if (panels.length) {
        animate(panels, { opacity: [0, 1], y: [10, 0] }, { duration: 0.4 });
    }

    // Subtle hover lift on buttons
    document.querySelectorAll(".btn-argus").forEach((btn) => {
        btn.addEventListener("mouseenter", () => animate(btn, { scale: 1.03 }, { duration: 0.15 }));
        btn.addEventListener("mouseleave", () => animate(btn, { scale: 1 }, { duration: 0.15 }));
    });
});
