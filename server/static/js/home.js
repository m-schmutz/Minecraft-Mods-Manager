let allMods = [];

async function loadModList() {
    const res = await fetch("/api/info/mod-display-list");
    const data = await res.json();
    allMods = data["mod-list"];

    renderModList(allMods);
}

function renderModList(mods) {
    const container = document.getElementById("mod-list");
    container.innerHTML = ""; // clear existing cards

    mods.forEach(mod => {
        const card = document.createElement("div");
        card.className = "mod-card";

        card.innerHTML = `
            <h3>${mod.name} <small>v${mod.version}</small></h3>
            <p>${mod.description}</p>
            <p><strong>Type:</strong> ${mod.type}</p>
            <p><strong>Role:</strong> ${mod.role}</p>
            <p><strong>Link:</strong> <a href="${mod.link}" target="_blank">CurseForge Page</a></p>
            <p><strong>Dependencies:</strong></p>
            <ul class="deps">
                ${mod.dependancies.length > 0
                    ? mod.dependancies.map(d => `<li>${d}</li>`).join("")
                    : "<li>None</li>"
                }
            </ul>
        `;

        container.appendChild(card);
    });
}


document.getElementById("sort-role").addEventListener("change", applySorting);
document.getElementById("sort-type").addEventListener("change", applySorting);

function applySorting() {
    const role = document.getElementById("sort-role").value;
    const type = document.getElementById("sort-type").value;

    let filtered = [...allMods];

    if (role !== "All") {
        filtered = filtered.filter(mod => mod.role === role);
    }

    if (type !== "All") {
        filtered = filtered.filter(mod => mod.type === type);
    }

    renderModList(filtered);
}


loadModList();
