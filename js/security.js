// ======================================
// FacilityOps AI - Security Page
// ======================================

const API_BASE_URL = "http://127.0.0.1:8000";

// ======================================
// Load Security Data
// ======================================

async function loadSecurityData() {

    try {

        // Summary
        const summaryResponse = await fetch(
            `${API_BASE_URL}/api/security/`
        );

        const result = await summaryResponse.json();

        if (result.status !== "success") {
            console.error(result.message);
            return;
        }

        const summary = result.summary;

        document.getElementById("security-total-events").textContent =
            summary.total_events.toLocaleString();

        document.getElementById("security-buildings-monitored").textContent =
            summary.buildings_monitored;

        document.getElementById("security-unique-employees").textContent =
            summary.unique_employees;

        document.getElementById("security-unauthorized-attempts").textContent =
            summary.unauthorized_attempts;

        const severityBody = document.getElementById("security-severity-body");

        severityBody.innerHTML = Object.entries(summary.severity_breakdown)
            .map(([severity, count]) => `
                <tr>
                    <td>${severity}</td>
                    <td>${count}</td>
                </tr>
            `).join("");

        // Alerts
        const alertsResponse = await fetch(
            `${API_BASE_URL}/api/security/alerts`
        );

        const alerts = await alertsResponse.json();

        const alertsBody = document.getElementById("security-alerts-body");

        alertsBody.innerHTML = alerts.map(alert => `
            <tr>
                <td>${alert.timestamp}</td>
                <td>${alert.building}</td>
                <td>${alert.zone}</td>
                <td>${alert.door}</td>
                <td>${alert.severity}</td>
            </tr>
        `).join("");

    }

    catch (error) {

        console.error("Failed to load Security Analytics:", error);

    }

}

// ======================================
// Initialize Security Page
// ======================================

async function initializeSecurityPage() {

    await initializeLayout();

    await loadSecurityData();

}

initializeSecurityPage();