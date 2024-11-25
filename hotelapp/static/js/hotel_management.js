/**
 * Script for performing dynamic/AJAX operations for CRUD actions 
 * on hotels. Hotels are fetched from here and can be added, 
 * updated or deleted.
 */
document.addEventListener('DOMContentLoaded', () => {

    // Retrieve the dynamic elements
    const cityInput = document.getElementById("city");
    const hotelList = document.getElementById("hotel-list");
    const hotelForm = document.getElementById("hotel-form");

    // Retrieve the CSRF token from the front-end. This is 
    // basically to make AJAX work with Django.
    const csrfToken = document.getElementById("csrf-token").value;

    /**
     * Retrieves a list of hotels from the backend b
     * ased on a given city, and displays it in the DOM
     */
    const handleCityChange = async () => {
        const cityName = cityInput.value;
        if (cityName.length > 2) {
            try {
                const response = await fetch(`/api/hotels/${cityName}/`);
                const data = await response.json();
    
                // Clear current list
                hotelList.innerHTML = "";
    
                // Load in hotel data
                if (data.hotels) {
                    data.hotels.forEach(hotel => {
                        const listItem = document.createElement("li");
                        listItem.id = `hotel-${hotel.id}`;
                        listItem.classList.add('bg-orange-300', 'text-xl',
                             'border', 'border-black', 'p-4', 'flex', 
                             'justify-between', 'items-center')
                        
                        // Structure the widget
                        listItem.innerHTML = `
                            <span>${hotel.local_code} - ${hotel.name}</span>
                            <div>
                                <button class="border border-slate-400 px-4 py-2 rounded-xl bg-white 
                                cursor-pointer hover:bg-slate-100" onclick="editHotel('${hotel.name}',
                                 '${hotel.city}', '${hotel.local_code}')">Edit</button>
                                <button class="border border-slate-400 px-4 py-2 rounded-xl bg-white 
                                cursor-pointer hover:bg-slate-100" onclick="deleteHotel(${hotel.id})">Delete</button>
                            </div>
                        `;

                        // Add the hotel to the list of hotels
                        hotelList.appendChild(listItem);
                    });
                } else {
                    hotelList.innerHTML = "<li>No hotels found</li>";
                }
            } catch (error) {
                hotelList.innerHTML = "<li>Error fetching data</li>";
                console.error(error);
            }
        }
    }

    // Make sure to fetch the hotels of the selected city on page load
    handleCityChange();

    // Tie the handler to the 'change' event of the cityinput element
    cityInput.addEventListener("change", handleCityChange);
    
    // Submit Hotel Form for Adding or Updating
    hotelForm.addEventListener("submit", async (event) => {
        event.preventDefault();
    
        // Package hotel data
        const hotelData = {
            name: document.getElementById("hotel-name").value,
            local_code: document.getElementById("hotel-local-code").value,
            city: document.getElementById("hotel-city").value,
        };
    
        try {
            // Make POST request to add/update a hotel with 
            // the inputted data
            const response = await fetch("/api/hotels/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify(hotelData),
            });
    
            // Show an alert to inform the user about 
            // whether it succeeded or not
            if (response.ok) {
                alert("Hotel saved successfully");

                // Make sure to refresh changes by 
                // triggering a 'change' events
                cityInput.dispatchEvent(new Event("change"));

                //Clears the form
                hotelForm.reset();
            } else {
                alert("Error saving hotel");
            }
        } catch (error) {
            console.error(error);
            alert("Error saving hotel");
        }
    });
    
    // Edit Hotel
    window.editHotel = (name, city, local_code) => {
        document.getElementById("hotel-name").value = name;
        document.getElementById("hotel-city").value = city;
        document.getElementById("hotel-local-code").value = local_code;
    };
    
    // Delete Hotel
    window.deleteHotel = async (id) => {
        if (confirm("Are you sure you want to delete this hotel?")) {
            try {
                // DELETE request that uses the passed ID to delete a hotel
                const response = await fetch(`/api/hotels/delete/${id}/`, {
                    method: "DELETE",
                    headers: {
                        "X-CSRFToken": csrfToken
                    }
                });
    
                if (response.ok) {
                    alert("Hotel deleted successfully");
                    // Removes it from the DOM
                    document.getElementById(`hotel-${id}`).remove();
                } else {
                    alert("Error deleting hotel");
                }
            } catch (error) {
                console.error(error);
                alert("Error deleting hotel");
            }
        }
    };

});