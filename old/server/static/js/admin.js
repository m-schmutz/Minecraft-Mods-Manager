async function loadAdminModList() {
    const res = await fetch("/api/info/mods");
    const data = await res.json();
    const mods = data["mods"];

    const container = document.getElementById("admin-mod-list");
    container.innerHTML = "";

    mods.forEach(mod => {
        const card = document.createElement("div");
        card.className = "admin-mod-card";

        card.innerHTML = `
    <h3>${mod.name} <small>v${mod.version}</small></h3>
    <p>${mod.description}</p>
    <p><strong>Type:</strong> ${mod.type}</p>
    <p><strong>Role:</strong> ${mod.role}</p>

    <p><strong>Dependencies:</strong></p>
    <ul class="deps">
        ${mod.dependencies.length > 0
                ? mod.dependencies.map(d => `<li>${d}</li>`).join("")
                : "<li>None</li>"
            }
    </ul>

    <button class="edit-btn" data-mod="${mod.id}">Edit</button>
    <button class="delete-btn" data-mod="${mod.id}">Delete</button>
`;


        container.appendChild(card);
    });
}


document.getElementById("add-mod-btn").onclick = () => {
    window.location.href = "/admin/add-mod";
};


document.addEventListener("click", e => {
    if (e.target.classList.contains("edit-btn")) {
        const id = e.target.dataset.mod;
        window.location.href = `/admin/edit-mod?id=${id}`;
    }
});






loadAdminModList();
