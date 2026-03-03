document.getElementById("add-mod-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const res = await fetch("/api/admin/add-mod", {
        method: "POST",
        body: formData
    });

    if (res.ok) {
        alert("Mod added successfully");
        window.location.href = "/admin";
    } else {
        alert("Failed to add mod");
    }
});

