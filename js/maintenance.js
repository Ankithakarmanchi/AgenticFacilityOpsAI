// ======================================
// FacilityOps AI - Maintenance Page
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
// Load Maintenance Analytics
// ======================================

async function loadMaintenanceAnalytics() {

    try {

        // Dashboard Summary
        const summaryResponse = await fetch(
            `${API_BASE_URL}/api/maintenance/`
        );

        const result = await summaryResponse.json();

        if (result.status !== "success") {
            console.error(result.message);
            return;
        }

        const summary = result.summary;

        document.getElementById("maintenance-total-assets").textContent =
            summary.total_assets;

        document.getElementById("maintenance-healthy-assets").textContent =
            summary.healthy_assets;

        document.getElementById("maintenance-warning-assets").textContent =
            summary.warning_assets;

        document.getElementById("maintenance-critical-assets").textContent =
            summary.critical_assets;

        document.getElementById("maintenance-health-score").textContent =
            summary.average_health_score;

        // Critical Assets
        const alertsResponse = await fetch(
            `${API_BASE_URL}/api/maintenance/alerts`
        );

        const alerts = await alertsResponse.json();

        document.getElementById("maintenance-alerts-body").innerHTML =
            alerts.map(alert => `
                <tr>
                    <td>${alert.asset}</td>
                    <td>${alert.health_score}</td>
                    <td>${alert.message}</td>
                </tr>
            `).join("");

        // AI Recommendations
        const recommendationsResponse = await fetch(
            `${API_BASE_URL}/api/maintenance/recommendations`
        );

        const recommendations = await recommendationsResponse.json();

        document.getElementById("maintenance-recommendations").innerHTML =
            recommendations.map(item => `
                <li>
                    <strong>${item.asset}</strong> - ${item.action}
                </li>
            `).join("");

    }

    catch (error) {

        console.error(
            "Failed to load Maintenance Analytics:",
            error
        );

    }

}

// ======================================
// Initialize Maintenance Page
// ======================================

async function initializeMaintenancePage() {

    await initializeLayout();

    await loadComponent(
        "maintenance-agent-container",
        "../components/maintenanceAgent.html"
    );

    await loadMaintenanceAnalytics();

}

initializeMaintenancePage();