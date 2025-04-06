// Ensure unique user and session identifiers
if (!localStorage.getItem("user_id")) {
    localStorage.setItem("user_id", Math.floor(Math.random() * 100000));
}
if (!sessionStorage.getItem("session_id")) {
    sessionStorage.setItem("session_id", Date.now());
}

let entryTime = new Date();
let clickCount = parseInt(sessionStorage.getItem("click_count")) || 0;

// Function to send tracking data
function sendTrackingData(sectionOverride = null) {
    const exitTime = new Date();
    const timeSpent = Math.round((exitTime - entryTime) / 1000); // time in seconds

    const path = window.location.pathname.replace("/", "") || "home";
    const section = sectionOverride || path;

    // Update click count if it's a navigation click
    if (sectionOverride) {
        clickCount++;
        sessionStorage.setItem("click_count", clickCount);
    }

    const avgTimeSpent = clickCount > 0 ? Math.round(timeSpent / clickCount) : timeSpent;

    const data = {
        user_id: localStorage.getItem("user_id"),
        session_id: sessionStorage.getItem("session_id"),
        page: section,
        page_title: document.title, // ✅ Add page title
        clicks: clickCount,
        avg_time_spent: avgTimeSpent
    };

    navigator.sendBeacon("/track", new Blob([JSON.stringify(data)], { type: "application/json" }));
}

// Track initial page load
document.addEventListener("DOMContentLoaded", () => {
    sendTrackingData();

    const links = document.querySelectorAll("nav a");

    links.forEach(link => {
        link.addEventListener("click", (event) => {
            event.preventDefault();

            const href = link.getAttribute("href");
            let pageName = href.replace(".html", "").replace("/", "") || "home";
            pageName = pageName.toLowerCase();

            sendTrackingData(pageName);

            setTimeout(() => {
                window.location.href = href;
            }, 100);
        });
    });
});

// Track page unload
window.addEventListener("beforeunload", () => sendTrackingData());
