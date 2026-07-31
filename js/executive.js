// ======================================
// FacilityOps AI - Executive Dashboard
// ======================================

const API_BASE_URL = "http://127.0.0.1:8000";

// ======================================
// Load Facility Intelligence Data
// ======================================

async function loadFacilityIntelligence() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/api/facility-intelligence/`
        );

        const result = await response.json();

        if (result.status !== "success") {
            console.error("Facility Intelligence Engine returned an error.");
            return;
        }

        // Top KPI cards
        document.getElementById("fi-health-score").textContent =
            `${result.facility_health_score} / 100`;

        document.getElementById("fi-score-maintenance").textContent =
            `${result.score_breakdown.maintenance} / 100`;

        document.getElementById("fi-score-security").textContent =
            `${result.score_breakdown.security} / 100`;

        document.getElementById("fi-score-cost").textContent =
            `${result.score_breakdown.cost} / 100`;

        document.getElementById("fi-score-occupancy").textContent =
            `${result.score_breakdown.occupancy} / 100`;

        document.getElementById("fi-score-energy").textContent =
            `${result.score_breakdown.energy} / 100`;
        // Score breakdown table
        const breakdownBody = document.getElementById("fi-breakdown-body");

        breakdownBody.innerHTML = Object.entries(result.score_breakdown)
            .map(([agent, score]) => `
                <tr>
                    <td style="text-transform: capitalize;">${agent}</td>
                    <td>${score}</td>
                    <td>${(result.score_weights[agent] * 100).toFixed(0)}%</td>
                </tr>
            `).join("");

        // Cross-agent summary table
        const agentsBody = document.getElementById("fi-agents-body");

        const agents = result.agents;

        agentsBody.innerHTML = `
            <tr>
                <td>Energy</td>
                <td>${agents.energy.status}</td>
                <td>${agents.energy.summary.total_buildings} buildings monitored</td>
            </tr>
            <tr>
                <td>Maintenance</td>
                <td>${agents.maintenance.status}</td>
                <td>${agents.maintenance.summary.critical_assets} critical assets</td>
            </tr>
            <tr>
                <td>Occupancy</td>
                <td>${agents.occupancy.status}</td>
                <td>${agents.occupancy.summary.occupancy_rate_pct}% occupancy rate</td>
            </tr>
            <tr>
                <td>Security</td>
                <td>${agents.security.status}</td>
                <td>${agents.security.summary.unauthorized_attempts} unauthorized attempts</td>
            </tr>
            <tr>
                <td>Cost</td>
                <td>${agents.cost.status}</td>
                <td>${agents.cost.summary.over_budget_reports} over-budget reports</td>
            </tr>
        `;

    }

    catch (error) {

        console.error("Failed to load Facility Intelligence:", error);

    }

}

// ======================================
// Initialize Executive Dashboard Page
// ======================================

async function initializeExecutivePage() {

    await initializeLayout();

    await loadFacilityIntelligence();

}

initializeExecutivePage();