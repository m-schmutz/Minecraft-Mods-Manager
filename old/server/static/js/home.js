let modList = [];

// fetch the full list of mods 
async function loadModList() {
    const res = await fetch("/api/info/modlist");
    modList = await res.json();
    
    renderModList(modList);
}

// render the mod list on the webpage
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
            <p><strong>Filename:</strong> ${mod.filename}</p>
            <p><strong>Filehash:</strong> ${mod.filehash}</p>
            <p><strong>Dependencies:</strong></p>
            <ul class="deps">
                ${mod.dependencies.length > 0
                    ? mod.dependencies.map(d => `<li>${d}</li>`).join("")
                    : "<li>None</li>"
                }
            </ul>
        `;

        container.appendChild(card);
    });
}


// detect when the user attempts to sort the mods
document.getElementById("sort-role").addEventListener("change", applySorting);
document.getElementById("sort-type").addEventListener("change", applySorting);


// apply sorting requested by the user
function applySorting() {
    const role = document.getElementById("sort-role").value;
    const type = document.getElementById("sort-type").value;

    let filtered = [...modList];

    if (role !== "All") {
        filtered = filtered.filter(mod => mod.role === role);
    }

    if (type !== "All") {
        filtered = filtered.filter(mod => mod.type === type);
    }

    renderModList(filtered);
}


loadModList();
