document.addEventListener("DOMContentLoaded", () => {

    console.log("Website Loaded");

    const circles = document.querySelectorAll(".circle-score");

    circles.forEach(circle => {

        const value = parseFloat(circle.dataset.value);

        if (isNaN(value)) return;

        const percent = Math.max(0, Math.min(value, 100));

        const degree = (percent / 100) * 360;

        circle.style.setProperty("--progress", degree + "deg");

    });

});