/* jshint esversion: 8 */

// load DOM
document.addEventListener("DOMContentLoaded", function () {
    const surfSpotsList = document.getElementById(surf-spots-list);

    // fetch surf spots from the backend
    async function fetchSurfSpots() {
        try {
            const response = await fetch("/api/surf_spots/list/");
            if (!response.ok) {
                throw new Error("Failed to fetchsurf spots");
            }
            const spots = await response.json();

            //clear the surf spots list
            surfSpotsList.innerHTML = "";

            //populate the list with fetched data
            spots.forEach((spot) => {
                const spotDiv = document.createElement("div");
                spotDiv.classList.add("surf-spot");
                //dynamic content insertion
                spotDiv.innerHTML = `
                    <h3>${spot.title}</h3>
                    <p class="label">Location: <span>${spot.location}</span></p>
                    <p class="label">Description: <span>${spot.description}</span></p>
                    <p class="label">Best seasons: <span>${spot.best_seasons}</span></p>
                    <p class="label">Posted by: <span>${spot.user}</span></p>
                    <p class="label">Date: <span>${new Date(spot.created_at).toLocaleString()}</span></p>
                `;

                surfSpotsList.appendChild(spotDiv);
            });
        } catch (error) {
            surfSpotsList.innerHTML = `<p class="error">Error loadingsurf spots: ${error.message}</p>`;
        }
    }

    //call the fetch function to load surf spots on page load
    fetchSurfSpots();
});
