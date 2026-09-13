// ========================================
// Data Guardian AI
// MASTER SIDEBAR CONTROLLER
// ========================================

console.log("✅ sidebar.js loaded");

document.addEventListener("DOMContentLoaded", function () {

    const sidebar =
        document.getElementById("sidebar");

    const toggleButton =
        document.getElementById("sidebarToggle");

    if (!sidebar) {
        console.error("❌ Sidebar not found.");
        return;
    }

    if (!toggleButton) {
        console.error("❌ Sidebar toggle button not found.");
        return;
    }

    console.log("✅ Sidebar ready");

    toggleButton.addEventListener("click", function () {

        sidebar.classList.toggle("collapsed");

        console.log(
            sidebar.classList.contains("collapsed")
                ? "📦 Sidebar collapsed"
                : "📂 Sidebar expanded"
        );

    });

});