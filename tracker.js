if (!localStorage.getItem("user_id")) {
    localStorage.setItem("user_id", Math.floor(Math.random() * 100000));
}
if (!sessionStorage.getItem("session_id")) {
    sessionStorage.setItem("session_id", Date.now());
}

let entryTime = new Date();
let clickCount = parseInt(sessionStorage.getItem("click_count")) || 0;

function sendTrackingData(sectionOverride = null) {
    const exitTime = new Date();
    const timeSpent = Math.round((exitTime - entryTime) / 1000);

    const path = window.location.pathname.replace("/", "") || "home";
    const section = sectionOverride || path;

    if (sectionOverride) {
        clickCount++;
        sessionStorage.setItem("click_count", clickCount);
    }

    const avgTimeSpent = clickCount > 0 ? Math.round(timeSpent / clickCount) : timeSpent;

    const data = {
        user_id: localStorage.getItem("user_id"),
        session_id: sessionStorage.getItem("session_id"),
        page: section,
        page_title: document.title,
        clicks: clickCount,
        avg_time_spent: avgTimeSpent
    };

    navigator.sendBeacon("/track", new Blob([JSON.stringify(data)], { type: "application/json" }));
}

document.addEventListener("DOMContentLoaded", () => {
    entryTime = new Date();
    sendTrackingData();

    document.querySelectorAll("nav a").forEach(link => {
        link.addEventListener("click", (e) => {
            const href = link.getAttribute("href");
            const pageName = href.replace("/", "") || "home";
            sendTrackingData(pageName);
        });
    });
});

window.addEventListener("beforeunload", () => sendTrackingData());
