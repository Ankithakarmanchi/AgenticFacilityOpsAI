// ======================================
// FacilityOps AI - AI Agents Page
// ======================================

async function loadComponent(id, file) {

    try {

        const response = await fetch(file);
        const html = await response.text();

        const container = document.getElementById(id);

        if (container) {
            container.innerHTML = html;
        }

    }

    catch (error) {

        console.error("Failed to load component:", error);

    }

}

// ======================================
// Initialize AI Agents Page
// ======================================

async function initializeAIAgentsPage() {

    await initializeLayout();
}

initializeAIAgentsPage();