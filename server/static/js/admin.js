async function loadAdminModList() {
    const res = await fetch("/api/info/mod-display-list");
    const data = await res.json();
    const mods = data["mod-list"];

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
        ${mod.dependancies.length > 0
                ? mod.dependancies.map(d => `<li>${d}</li>`).join("")
                : "<li>None</li>"
            }
    </ul>

    <button class="update-btn" data-mod="${mod.id}">Update</button>
    <button class="delete-btn" data-mod="${mod.id}">Delete</button>
`;


        container.appendChild(card);
    });
}


document.getElementById("add-mod-btn").onclick = () => {
    window.location.href = "/admin/add-mod";
};


loadAdminModList();
