document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.querySelector('input[name="resume"]');

    if (!fileInput) return;

    fileInput.addEventListener("change", function () {

        if (this.files.length === 0) return;

        const file = this.files[0];

        document.getElementById("uploadIcon").className =
            "fa-solid fa-circle-check";

        document.getElementById("uploadIcon").style.color = "#22c55e";

        document.getElementById("uploadTitle").textContent =
            file.name;

        document.getElementById("uploadTitle").style.color =
            "#16a34a";

        document.getElementById("uploadText").textContent =
            "Resume Selected Successfully";

        document.getElementById("uploadSize").textContent =
            "PDF • " + (file.size / 1024 / 1024).toFixed(2) + " MB";

    });

});