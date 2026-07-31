// ======================================
// FacilityOps AI - Occupancy Page
// ======================================

const API_BASE_URL = "http://127.0.0.1:8000";

// ======================================
// Load Occupancy Data
// ======================================

async function loadOccupancyData() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/api/occupancy/`
        );

        const result = await response.json();

        if (result.status !== "success") {
            console.error(result.message);
            return;
        }

        const summary = result.summary;

        document.getElementById("occupancy-total-records").textContent =
            summary.total_records.toLocaleString();

        document.getElementById("occupancy-rate").textContent =
            `${summary.occupancy_rate_pct}%`;

        document.getElementById("occupancy-occupied-records").textContent =
            summary.occupied_records.toLocaleString();

        document.getElementById("occupancy-vacant-records").textContent =
            summary.vacant_records.toLocaleString();

        document.getElementById("occupancy-co2-occupied").textContent =
            summary.average_co2_when_occupied;

        document.getElementById("occupancy-co2-vacant").textContent =
            summary.average_co2_when_vacant;

        document.getElementById("occupancy-peak-co2").textContent =
            summary.peak_co2_level;

        document.getElementById("occupancy-avg-light").textContent =
            summary.average_light_when_occupied;

    }

    catch (error) {

        console.error("Failed to load Occupancy Analytics:", error);

    }

}
// ======================================
// Load Forecast Accuracy
// ======================================

async function loadForecastAccuracy() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/api/occupancy/forecast-accuracy`
        );

        const result = await response.json();

        if (result.status !== "success") {
            console.error(result.message);
            return;
        }

        const summary = result.summary;

        document.getElementById("forecast-method-text").textContent =
            `${summary.method}. ${summary.validation_method}.`;

        document.getElementById("forecast-accuracy").textContent =
            `${summary.accuracy_pct}%`;

        document.getElementById("forecast-precision").textContent =
            `${summary.precision_pct}%`;

        document.getElementById("forecast-recall").textContent =
            `${summary.recall_pct}%`;

        document.getElementById("forecast-training-records").textContent =
            summary.training_records.toLocaleString();

        document.getElementById("forecast-test-records").textContent =
            summary.test_records.toLocaleString();

    }

    catch (error) {

        console.error("Failed to load Forecast Accuracy:", error);

    }

}

// ======================================
// Initialize Occupancy Page
// ======================================

async function initializeOccupancyPage() {

    await initializeLayout();

    await loadOccupancyData();

}
async function initializeOccupancyPage() {

    await initializeLayout();

    await loadOccupancyData();

    await loadForecastAccuracy();

}

initializeOccupancyPage();