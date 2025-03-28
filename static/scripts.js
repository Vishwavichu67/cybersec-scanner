document.addEventListener("DOMContentLoaded", function() {
    const scanForm = document.querySelector("form");
    const scanBtn = document.querySelector("button");
    const targetInput = document.getElementById("target");

    // 🚀 Start Scan Button Animation
    scanForm.addEventListener("submit", function() {
        scanBtn.innerHTML = "Scanning...";
        scanBtn.disabled = true;
        scanBtn.style.boxShadow = "0 0 15px #ff0000, 0 0 30px #ff0000";
    });

    // 🔥 Glitch Effect on Input Fields
    targetInput.addEventListener("focus", function() {
        targetInput.style.boxShadow = "0 0 10px #ff00ff, 0 0 20px #ff00ff";
    });

    targetInput.addEventListener("blur", function() {
        targetInput.style.boxShadow = "0 0 5px #00ffcc";
    });

    // 🛠️ Moving Cybersecurity Tool Containers
    let tools = document.querySelectorAll(".moving-container");
    let speed = 0.3;

    function moveContainers() {
        tools.forEach((tool, index) => {
            let x = Math.sin(Date.now() * 0.001 + index) * 5;
            let y = Math.cos(Date.now() * 0.001 + index) * 5;
            tool.style.transform = `translate(${x}px, ${y}px)`;
        });
        requestAnimationFrame(moveContainers);
    }
    moveContainers();
});
