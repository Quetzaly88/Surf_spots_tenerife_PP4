/* jshint esversion: 8 */

document.addEventListener("DOMContentLoaded", function () {
    const surfSpotsList = document.getElementById('surf-spots-list');

    async function fetchSurfSpots() {
        try {
            const response = await fetch("/surf_spots/list/");
            if (!response.ok) {
                throw new Error("Failed to fetch surf spots");
            }
            const spots = await response.json();

            //clear the surf spots list
            surfSpotsList.innerHTML = "";

            //populate the list with fetched data
            spots.forEach((spot) => {
                const spotDiv = document.createElement("div");
                spotDiv.classList.add("surf-spot");

                //handle null or undefined fields
                const bestSeasons = spot.best_seasons || "Not specified";
                const user = spot.user || "Anonymous";
                const date = spot.created_at ? new Date(spot.created_at).toLocaleString() : "Unknown date";

                //dynamic content insertion
                spotDiv.innerHTML = `
                    <h3>${spot.title}</h3>
                    <p class="label">Location: <span>${spot.location}</span></p>
                    <p class="label">Description: <span>${spot.description}</span></p>
                    <p class="label">Best seasons: <span>${spot.best_seasons}</span></p>
                    <p class="label">Posted by: <span>${spot.user}</span></p>
                    <p class="label">Date: <span>${date}</span></p>
                `;

                surfSpotsList.appendChild(spotDiv);
            });
        } catch (error) {
            console.error("Error loading surf spots:", error);
            const errorDiv = document.createElement("p");
            errorDiv.classList.add("error");
            errorDiv.textContent = `Error loading surf spots: ${error.message}`;
            surfSpotsList.appendChild(errorDiv);
        }
    }

    //call the fetch function to load surf spots on page load
    fetchSurfSpots();
});
