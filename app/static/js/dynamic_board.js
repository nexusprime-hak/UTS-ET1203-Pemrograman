document.getElementById("satellite").addEventListener("change", function () {
    const selectedSatellite = this.value;

    // Send selected satellite name via AJAX
    fetch("/get_satellite_info", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ satellite: selectedSatellite })
    })
    .then(response => response.json())
    .then(data => {
        // Update satellite info dynamically
        const infoDiv = document.getElementById("satellite-info");
        infoDiv.innerHTML = "";

        if (data) {
            const displayOrder = [
            { key: "norad_id", label: "NORAD ID" },
            { key: "intl_code", label: "Int'l Code" },
            { key: "perigee", label: "Perigee" },
            { key: "apogee", label: "Apogee" },
            { key: "inclination", label: "Inclination" },
            { key: "period", label: "Period" },
            { key: "semi_major_axis", label: "Semi Major Axis" },
            { key: "rcs", label: "RCS" },
            { key: "launch_date", label: "Launch Date" },
            { key: "source", label: "Source" },
            { key: "launch_site", label: "Launch Site" },
            { key: "description", label: "Description" }
        ];
        
        displayOrder.forEach(item => {
            const value = data[item.key];
            if (value !== undefined && value !== 0) {
                const content = document.createElement("p");
                content.innerHTML = `<strong>${item.label}:</strong> ${value}`;
                infoDiv.appendChild(content);
            }
        });
        } else {
            infoDiv.innerHTML = "<p>No satellite information available.</p>";
        }
    })
    .catch(error => console.error("Error fetching satellite data:", error));
});