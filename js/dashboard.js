// ======================================
// FacilityOps AI Dashboard
// ======================================

const API_BASE_URL = "http://127.0.0.1:8000";

// ======================================
// Load HTML Components
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
// Load Energy Summary
// ======================================

async function loadEnergyAnalytics() {

    try {

        const response = await fetch(`${API_BASE_URL}/api/energy/`);
        const result = await response.json();

        if (result.status !== "success") return;

        const summary = result.summary;

        document.getElementById("total-buildings").textContent =
            summary.total_buildings.toLocaleString();

        document.getElementById("total-records").textContent =
            summary.total_records.toLocaleString();

        document.getElementById("average-meter-reading").textContent =
            summary.average_meter_reading.toLocaleString();

        document.getElementById("maximum-meter-reading").textContent =
            summary.maximum_meter_reading.toLocaleString();

    } catch (error) {

        console.error("Failed to load dashboard summary:", error);

    }

}

// ======================================
// Dashboard Initialization
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
        "workflow-container",
        "../components/workflow.html"
    );

    await loadEnergyAnalytics();

}

initializeDashboard();