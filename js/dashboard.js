// ======================================
// FacilityOps AI Dashboard
// ======================================

// Backend API
const API_BASE_URL = "http://127.0.0.1:8000";

// ======================================
// Load HTML Components
// ======================================

async function loadComponent(id, file) {

    const response = await fetch(file);

    const html = await response.text();

    document.getElementById(id).innerHTML = html;

}

// ======================================
// Load Energy Analytics
// ======================================

async function loadEnergyAnalytics() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/api/energy/`
        );

        const result = await response.json();

        if (result.status !== "success") {

            console.error(result.message);

            return;

        }

        const summary = result.summary;

        // ======================================
        // Summary Cards
        // ======================================

        document.getElementById("total-buildings").textContent =
            summary.total_buildings.toLocaleString();

        document.getElementById("total-records").textContent =
            summary.total_records.toLocaleString();

        document.getElementById("average-meter-reading").textContent =
            summary.average_meter_reading.toLocaleString();

        document.getElementById("maximum-meter-reading").textContent =
            summary.maximum_meter_reading.toLocaleString();

        // ======================================
        // Energy Agent Card
        // ======================================

        document.getElementById("energy-saving-value").textContent =
            `${summary.energy_savings}%`;

        document.getElementById("cost-saving-value").textContent =
            `₹${summary.cost_savings.toLocaleString()}`;

        document.getElementById("forecast-value").textContent =
            `${summary.forecast_accuracy}%`;

    }

    catch (error) {

        console.error(
            "Failed to load Energy Analytics:",
            error
        );

    }

}

// ======================================
// Initialize Dashboard
// ======================================

async function initializeDashboard() {

    await loadComponent(
        "sidebar-container",
        "../components/sidebar.html"
    );

    await loadComponent(
        "header-container",
        "../components/header.html"
    );

    await loadComponent(
        "summary-cards-container",
        "../components/summaryCards.html"
    );

    await loadComponent(
        "energy-agent-container",
        "../components/energyAgent.html"
    );

    await loadComponent(
        "workflow-container",
        "../components/workflow.html"
    );

    initializeEnergyChart();

    await loadEnergyAnalytics();

}

initializeDashboard();

// ======================================
// Energy Chart
// ======================================

function initializeEnergyChart() {

    const canvas = document.getElementById("energyChart");

    if (!canvas) return;

    new Chart(canvas, {

        type: "line",

        data: {

            labels: [

                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"

            ],

            datasets: [

                {

                    label: "Energy Usage",

                    data: [

                        78,
                        72,
                        75,
                        69,
                        73,
                        68,
                        66

                    ],

                    borderColor: "#22C55E",

                    backgroundColor: "rgba(34,197,94,0.15)",

                    borderWidth: 3,

                    tension: 0.4,

                    fill: true,

                    pointRadius: 4,

                    pointBackgroundColor: "#22C55E"

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: false,

                    grid: {

                        color: "#E5E7EB"

                    }

                },

                x: {

                    grid: {

                        display: false

                    }

                }

            }

        }

    });

}