// ======================================
// FacilityOps AI - Cost Page
// ======================================

const API_BASE_URL = "http://127.0.0.1:8000";

// ======================================
// Load Cost Data
// ======================================

async function loadCostData() {

    try {

        // Summary
        const summaryResponse = await fetch(
            `${API_BASE_URL}/api/cost/`
        );

        const result = await summaryResponse.json();

        if (result.status !== "success") {
            console.error(result.message);
            return;
        }

        const summary = result.summary;

        document.getElementById("cost-total-reports").textContent =
            summary.total_reports.toLocaleString();

        document.getElementById("cost-total-spent").textContent =
            `₹${summary.total_amount_spent.toLocaleString()}`;

        document.getElementById("cost-over-budget").textContent =
            summary.over_budget_reports;

        document.getElementById("cost-vendors-engaged").textContent =
            summary.vendors_engaged;

        const categoryBody = document.getElementById("cost-category-body");

        categoryBody.innerHTML = Object.entries(summary.category_breakdown)
            .map(([category, amount]) => `
                <tr>
                    <td>${category}</td>
                    <td>₹${Number(amount).toLocaleString()}</td>
                </tr>
            `).join("");

        // Recommendations
        const recResponse = await fetch(
            `${API_BASE_URL}/api/cost/recommendations`
        );

        const recommendations = await recResponse.json();

        const recBody = document.getElementById("cost-recommendations-body");

        recBody.innerHTML = recommendations.map(rec => `
            <tr>
                <td>${rec.building}</td>
                <td>${rec.category}</td>
                <td>${rec.vendor}</td>
                <td>₹${Number(rec.variance).toLocaleString()}</td>
                <td>${rec.priority}</td>
            </tr>
        `).join("");

    }

    catch (error) {

        console.error("Failed to load Cost Analytics:", error);

    }

}

// ======================================
// Initialize Cost Page
// ======================================

async function initializeCostPage() {

    await initializeLayout();

    await loadCostData();

}

initializeCostPage();