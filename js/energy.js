// ======================================
// FacilityOps AI - Energy Page
// ======================================

const API_BASE_URL = "http://127.0.0.1:8000";

// ======================================
// Load HTML Component
// ======================================

async function loadComponent(id, file) {

    const response = await fetch(file);
    const html = await response.text();

    const container = document.getElementById(id);

    if (container) {
        container.innerHTML = html;
    }

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

        document.getElementById("energy-saving-value").textContent =
            `${summary.energy_savings}%`;

        document.getElementById("cost-saving-value").textContent =
            `₹${summary.cost_savings.toLocaleString()}`;

        document.getElementById("forecast-value").textContent =
            `${summary.forecast_accuracy}%`;

    } catch (error) {

        console.error("Failed to load Energy Analytics:", error);

    }

}

// ======================================
// Load AI Recommendations
// ======================================

async function loadRecommendations() {

    const listEl = document.getElementById("recommendations-list");
    const countEl = document.getElementById("recommendations-count");

    if (!listEl || !countEl) return;

    try {

        const response = await fetch(
            `${API_BASE_URL}/api/energy/recommendations`
        );

        const result = await response.json();

        if (result.status !== "success") {

            listEl.innerHTML =
                "<p class='rec-loading'>Unable to load recommendations.</p>";

            return;

        }

        const recommendations = result.summary.recommendations;

        countEl.textContent = `${recommendations.length} Insights`;

        listEl.innerHTML = recommendations.map(rec => `
            <div class="rec-item">

                <div class="rec-item-left">

                    <div class="rec-item-title">

                        <h4>Building ${rec.building_id}</h4>

                        <span class="rec-meter-badge">
                            ${rec.meter_type}
                        </span>

                    </div>

                    <p class="rec-item-text">
                        ${rec.recommendation}
                    </p>

                </div>

                <div class="rec-item-right">

                    <p class="rec-savings-label">
                        Estimated Daily Savings
                    </p>

                    <p class="rec-savings-value">
                        ₹${rec.estimated_daily_savings.toLocaleString()}
                    </p>

                </div>

            </div>
        `).join("");

    } catch (error) {

        console.error(error);

        listEl.innerHTML =
            "<p class='rec-loading'>Unable to load recommendations.</p>";

    }

}

// ======================================
// Load Anomaly Detection
// ======================================

async function loadAnomalyDetection() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/api/energy/anomaly-detection`
        );

        const result = await response.json();

        if (result.status !== "success") {
            console.error(result.message);
            return;
        }

        const summary = result.summary;

        document.getElementById("anomaly-method-text").textContent =
            `${summary.method}. ${summary.validation_method}.`;

        document.getElementById("anomaly-accuracy").textContent =
            `${summary.accuracy_pct}%`;

        document.getElementById("anomaly-precision").textContent =
            `${summary.precision_pct}%`;

        document.getElementById("anomaly-recall").textContent =
            `${summary.recall_pct}%`;

        document.getElementById("anomaly-count").textContent =
            summary.real_anomalies_detected_in_dataset.toLocaleString();

        const sampleBody = document.getElementById("anomaly-sample-body");

        sampleBody.innerHTML = result.sample_flagged_anomalies.map(item => `
            <tr>
                <td>${item.building_id}</td>
                <td>${item.meter}</td>
                <td>${item.timestamp}</td>
                <td>${item.meter_reading}</td>
            </tr>
        `).join("");

    }

    catch (error) {

        console.error("Failed to load Anomaly Detection:", error);

    }

}

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

                    fill: true

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

            }

        }

    });

}

// ======================================
// Initialize Energy Page
// ======================================

async function initializeEnergyPage() {

    await initializeLayout();

    await loadComponent(
        "energy-agent-container",
        "../components/energyAgent.html"
    );

    await loadComponent(
        "recommendations-container",
        "../components/recommendations.html"
    );

    initializeEnergyChart();

    await loadEnergyAnalytics();

    await loadRecommendations();

    await loadAnomalyDetection();

}

initializeEnergyPage();