// ======================================
// FacilityOps AI - Common Script
// Shared by All Pages
// ======================================

// Load HTML Component
async function loadComponent(id, file) {

    try {

        const response = await fetch(file);

        if (!response.ok) {
            throw new Error(`Failed to load ${file}`);
        }

        const html = await response.text();

        const container = document.getElementById(id);

        if (container) {
            container.innerHTML = html;
        }

    }

    catch (error) {

        console.error(error);

    }

}

// ======================================
// Highlight Active Sidebar Menu
// ======================================

function highlightActiveMenu() {

    const currentPage = window.location.pathname
        .split("/")
        .pop()
        .toLowerCase();

    const items = document.querySelectorAll(".sidebar li[onclick]");

    items.forEach(item => {

        const onclickAttr = item.getAttribute("onclick");

        if (!onclickAttr) return;

        if (onclickAttr.toLowerCase().includes(currentPage)) {

            item.classList.add("active");

        }

    });

}

// ======================================
// Initialize Common Layout
// ======================================

async function initializeLayout() {

    await loadComponent(
        "sidebar-container",
        "../components/sidebar.html"
    );

    await loadComponent(
        "header-container",
        "../components/header.html"
    );

    highlightActiveMenu();

}