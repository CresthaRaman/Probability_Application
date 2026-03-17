/* ─────────────────────────────────────────────
   Cardiac Health Analytics – Interactive JS
   ───────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    initNavbar();
    initCounters();
    initLightbox();
    initScrollAnimations();
    initCharts();
});

/* ── Theme Toggle ── */
function initTheme() {
    const toggle = document.getElementById("themeToggle");
    const icon = toggle.querySelector(".theme-icon");
    const saved = localStorage.getItem("theme");
    if (saved === "dark") {
        document.documentElement.setAttribute("data-theme", "dark");
        icon.textContent = "\u2600";
    }
    toggle.addEventListener("click", () => {
        const isDark = document.documentElement.getAttribute("data-theme") === "dark";
        document.documentElement.setAttribute("data-theme", isDark ? "light" : "dark");
        icon.textContent = isDark ? "\u263E" : "\u2600";
        localStorage.setItem("theme", isDark ? "light" : "dark");
        recolorCharts(!isDark);
    });
}

/* ── Navbar ── */
function initNavbar() {
    const navbar = document.getElementById("navbar");
    const toggle = document.getElementById("navToggle");
    const links = document.getElementById("navLinks");
    const anchors = links.querySelectorAll("a");

    window.addEventListener("scroll", () => {
        navbar.classList.toggle("scrolled", window.scrollY > 40);
        highlightNav();
    });

    toggle.addEventListener("click", () => links.classList.toggle("open"));

    anchors.forEach(a => a.addEventListener("click", () => links.classList.remove("open")));
}

function highlightNav() {
    const sections = document.querySelectorAll("section[id]");
    const anchors = document.querySelectorAll(".nav-links a");
    let current = "";
    sections.forEach(s => {
        if (window.scrollY >= s.offsetTop - 120) current = s.id;
    });
    anchors.forEach(a => {
        a.classList.toggle("active", a.getAttribute("href") === "#" + current);
    });
}

/* ── Animated Counters ── */
function initCounters() {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                animateCounter(e.target);
                observer.unobserve(e.target);
            }
        });
    }, { threshold: 0.5 });
    document.querySelectorAll(".hero-stat").forEach(el => observer.observe(el));
}

function animateCounter(el) {
    const target = parseInt(el.dataset.count, 10);
    const numEl = el.querySelector(".stat-number");
    const duration = 1600;
    const start = performance.now();
    function step(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        numEl.textContent = Math.floor(eased * target);
        if (progress < 1) requestAnimationFrame(step);
        else numEl.textContent = target;
    }
    requestAnimationFrame(step);
}

/* ── Lightbox ── */
function initLightbox() {
    const lb = document.getElementById("lightbox");
    const lbImg = document.getElementById("lightboxImg");
    const lbTitle = document.getElementById("lightboxTitle");
    const lbClose = document.getElementById("lightboxClose");

    document.querySelectorAll(".gallery-item").forEach(item => {
        item.addEventListener("click", () => {
            lbImg.src = item.dataset.chart;
            lbTitle.textContent = item.dataset.title || "";
            lb.classList.add("active");
            document.body.style.overflow = "hidden";
        });
    });

    function closeLb() {
        lb.classList.remove("active");
        document.body.style.overflow = "";
    }
    lbClose.addEventListener("click", closeLb);
    lb.addEventListener("click", e => { if (e.target === lb) closeLb(); });
    document.addEventListener("keydown", e => { if (e.key === "Escape") closeLb(); });
}

/* ── Scroll Animations ── */
function initScrollAnimations() {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.classList.add("visible");
                observer.unobserve(e.target);
            }
        });
    }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });

    document.querySelectorAll(
        ".feature-card, .stat-card, .chart-panel, .gallery-item, .unit-header, .prob-laws-container"
    ).forEach(el => {
        el.classList.add("fade-in");
        observer.observe(el);
    });
}

/* ── Charts ── */
const chartInstances = [];

function getChartColors() {
    const dark = document.documentElement.getAttribute("data-theme") === "dark";
    return {
        text: dark ? "#e4e7f1" : "#1a1d2e",
        grid: dark ? "#2a2d42" : "#e2e6ef",
        accent: "#e74c3c",
        blue: "#3498db",
        green: "#2ecc71",
        orange: "#e67e22",
        purple: "#9b59b6",
        teal: "#1abc9c",
    };
}

function recolorCharts(isDark) {
    chartInstances.forEach(c => {
        const colors = getChartColors();
        if (c.options.scales) {
            Object.values(c.options.scales).forEach(scale => {
                if (scale.ticks) scale.ticks.color = colors.text;
                if (scale.grid) scale.grid.color = colors.grid;
                if (scale.title) scale.title.color = colors.text;
            });
        }
        if (c.options.plugins && c.options.plugins.legend && c.options.plugins.legend.labels) {
            c.options.plugins.legend.labels.color = colors.text;
        }
        c.update();
    });
}

function initCharts() {
    const C = getChartColors();
    Chart.defaults.font.family = "'Inter', sans-serif";

    // 1. Diagnosis Doughnut
    chartInstances.push(new Chart(document.getElementById("diagnosisChart"), {
        type: "doughnut",
        data: {
            labels: ["Healthy (534)", "Disease (66)"],
            datasets: [{
                data: [534, 66],
                backgroundColor: [C.green, C.accent],
                borderWidth: 3,
                borderColor: getComputedStyle(document.documentElement).getPropertyValue('--surface').trim() || '#fff',
                hoverOffset: 12,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom", labels: { color: C.text, padding: 16, font: { size: 13, weight: 500 } } },
            },
            cutout: "55%",
        }
    }));

    // 2. Feature Importance (horizontal bar)
    const featLabels = ["age", "resting_bp", "cholesterol", "fasting_blood_sugar", "max_heart_rate", "oldpeak", "bmi"];
    const featCorr = [0.167, 0.141, 0.054, 0.100, -0.119, 0.118, 0.070];
    chartInstances.push(new Chart(document.getElementById("featureImportanceChart"), {
        type: "bar",
        data: {
            labels: featLabels,
            datasets: [{
                label: "Pearson r with Heart Disease",
                data: featCorr,
                backgroundColor: featCorr.map(v => v >= 0 ? C.accent : C.blue),
                borderRadius: 6,
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: C.grid }, ticks: { color: C.text }, title: { display: true, text: "Pearson r", color: C.text } },
                y: { grid: { display: false }, ticks: { color: C.text, font: { weight: 500 } } },
            }
        }
    }));

    // 3. Probability Laws (grouped bar)
    chartInstances.push(new Chart(document.getElementById("probLawsChart"), {
        type: "bar",
        data: {
            labels: ["P(HD)", "P(HighBP)", "P(HD \u2229 HighBP)", "P(HD \u222A HighBP)", "P(HD|HighBP)", "P(HighBP|HD)", "Bayes P(HD|HighBP)"],
            datasets: [{
                label: "Probability",
                data: [0.40, 0.35, 0.22, 0.53, 0.629, 0.55, 0.629],
                backgroundColor: [C.accent, C.blue, C.purple, C.orange, C.green, C.teal, "#e84393"],
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, max: 1, grid: { color: C.grid }, ticks: { color: C.text } },
                x: { grid: { display: false }, ticks: { color: C.text, font: { size: 11 }, maxRotation: 25 } },
            }
        }
    }));

    // 4. Distribution Probabilities (radar)
    chartInstances.push(new Chart(document.getElementById("distProbChart"), {
        type: "radar",
        data: {
            labels: ["Binomial", "Poisson", "Neg. Binomial", "Normal", "Gamma", "Chi-Square"],
            datasets: [{
                label: "Probability",
                data: [0.438, 0.195, 0.084, 0.711, 0.753, 0.875],
                backgroundColor: "rgba(231, 76, 60, 0.15)",
                borderColor: C.accent,
                borderWidth: 2,
                pointBackgroundColor: C.accent,
                pointRadius: 5,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: C.text } } },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 1,
                    ticks: { color: C.text, backdropColor: "transparent", stepSize: 0.25 },
                    grid: { color: C.grid },
                    pointLabels: { color: C.text, font: { size: 12, weight: 500 } },
                }
            }
        }
    }));

    // 5. CLT comparison (bar)
    chartInstances.push(new Chart(document.getElementById("cltChart"), {
        type: "bar",
        data: {
            labels: ["Population Mean", "Sampling Mean", "Population Std", "Sampling Std", "Theoretical SE"],
            datasets: [{
                label: "Value",
                data: [130.48, 130.53, 58.64, 9.33, 9.27],
                backgroundColor: [C.blue, C.green, C.orange, C.purple, C.accent],
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: C.grid }, ticks: { color: C.text } },
                x: { grid: { display: false }, ticks: { color: C.text, font: { size: 11 }, maxRotation: 20 } },
            }
        }
    }));

    // 6. Hypothesis Tests (horizontal bar with alpha line)
    const htLabels = ["1-Sample t", "2-Sample t", "Paired t", "Kruskal-Wallis", "Chi-Square", "Shapiro"];
    const htPvals = [0.0000, 0.0003, 0.0000, 0.0362, 0.0596, 0.0557];
    chartInstances.push(new Chart(document.getElementById("hypothesisChart"), {
        type: "bar",
        data: {
            labels: htLabels,
            datasets: [{
                label: "p-value",
                data: htPvals,
                backgroundColor: htPvals.map(p => p < 0.05 ? C.accent : C.green),
                borderRadius: 6,
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                annotation: {
                    annotations: {
                        alpha: { type: "line", xMin: 0.05, xMax: 0.05, borderColor: "#333", borderWidth: 2, borderDash: [6, 4] }
                    }
                }
            },
            scales: {
                x: { grid: { color: C.grid }, ticks: { color: C.text }, title: { display: true, text: "p-value", color: C.text } },
                y: { grid: { display: false }, ticks: { color: C.text, font: { weight: 500 } } },
            }
        }
    }));

    // 7. ANOVA decomposition (pie)
    chartInstances.push(new Chart(document.getElementById("anovaChart"), {
        type: "pie",
        data: {
            labels: ["SSR (Explained): 33,731", "SSE (Unexplained): 945,656"],
            datasets: [{
                data: [33731, 945656],
                backgroundColor: [C.blue, C.orange],
                borderWidth: 3,
                borderColor: getComputedStyle(document.documentElement).getPropertyValue('--surface').trim() || '#fff',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom", labels: { color: C.text, padding: 14, font: { size: 12 } } },
            }
        }
    }));

    // 8. Regression Coefficients (horizontal bar)
    chartInstances.push(new Chart(document.getElementById("coefChart"), {
        type: "bar",
        data: {
            labels: ["age", "resting_bp", "bmi", "smoking_status"],
            datasets: [{
                label: "Coefficient",
                data: [0.437, 0.128, 0.238, -1.98],
                backgroundColor: [C.blue, C.green, C.orange, C.accent],
                borderRadius: 6,
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: C.grid }, ticks: { color: C.text }, title: { display: true, text: "Coefficient", color: C.text } },
                y: { grid: { display: false }, ticks: { color: C.text, font: { weight: 500 } } },
            }
        }
    }));

    // 9. P-Chart Interactive (line)
    const pCenter = 0.11;
    const pUcl = 0.407;
    const pLcl = 0.0;
    const pData = [0.1,0.2,0.1,0.0,0.2,0.1,0.0,0.1,0.2,0.0,0.1,0.1,0.3,0.0,0.1,0.2,0.0,0.1,0.1,0.2,0.0,0.2,0.1,0.0,0.1,0.1,0.2,0.0,0.3,0.1,0.0,0.2,0.1,0.0,0.1,0.1,0.2,0.0,0.1,0.1,0.2,0.0,0.1,0.1,0.3,0.0,0.1,0.2,0.0,0.1,0.1,0.2,0.0,0.2,0.1,0.0,0.1,0.1,0.0,0.1];
    chartInstances.push(new Chart(document.getElementById("pChartInteractive"), {
        type: "line",
        data: {
            labels: pData.map((_, i) => i + 1),
            datasets: [
                { label: "Proportion", data: pData, borderColor: C.blue, backgroundColor: "rgba(52,152,219,0.1)", fill: true, pointRadius: 2, tension: 0.1 },
                { label: "CL", data: Array(pData.length).fill(pCenter), borderColor: C.green, borderDash: [6, 4], pointRadius: 0 },
                { label: "UCL", data: Array(pData.length).fill(pUcl), borderColor: C.accent, borderDash: [6, 4], pointRadius: 0 },
                { label: "LCL", data: Array(pData.length).fill(pLcl), borderColor: C.accent, borderDash: [6, 4], pointRadius: 0 },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: C.text, usePointStyle: true } } },
            scales: {
                x: { grid: { color: C.grid }, ticks: { color: C.text }, title: { display: true, text: "Subgroup", color: C.text } },
                y: { grid: { color: C.grid }, ticks: { color: C.text }, title: { display: true, text: "Proportion", color: C.text }, min: 0, max: 0.5 },
            }
        }
    }));

    // 10. Sigma Gauge (doughnut)
    const sigmaLevel = 0.96;
    chartInstances.push(new Chart(document.getElementById("sigmaGauge"), {
        type: "doughnut",
        data: {
            labels: ["Sigma Level", "Remaining to 6\u03C3"],
            datasets: [{
                data: [sigmaLevel, 6 - sigmaLevel],
                backgroundColor: [C.accent, C.grid],
                borderWidth: 0,
                circumference: 270,
                rotation: 225,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "75%",
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true },
            },
        },
        plugins: [{
            id: "gaugeText",
            afterDraw(chart) {
                const { ctx, chartArea: { left, right, top, bottom } } = chart;
                const cx = (left + right) / 2;
                const cy = (top + bottom) / 2 + 20;
                ctx.save();
                ctx.textAlign = "center";
                ctx.fillStyle = C.text;
                ctx.font = "bold 32px Inter";
                ctx.fillText(sigmaLevel.toFixed(2) + "\u03C3", cx, cy);
                ctx.font = "14px Inter";
                ctx.fillStyle = C.accent;
                ctx.fillText("DPMO: 110,000", cx, cy + 28);
                ctx.restore();
            }
        }]
    }));
}
