// Function to open Google Maps with location services
function openGoogleMaps() {
    // Redirect user to Google Maps API with the location services data
    // You can replace the URL with your desired Google Maps URL
    window.open('https://maps.google.com', '_blank');
}

// Function to open Google Calendar with event calendar
function openGoogleCalendar() {
    // Redirect user to Google Calendar API with the event calendar data
    // You can replace the URL with your desired Google Calendar URL
    window.open('https://calendar.google.com', '_blank');
}

// Function to open Weather API with weather forecast
function openWeatherForecast() {
    // Redirect user to Weather API with the weather forecast data
    // You can replace the URL with your desired Weather API URL
    window.open('https://weather.com', '_blank');
}

// Fetch API data and update placeholders
fetch('/api/organizer')
.then(response => response.json())
.then(data => {
    // Update placeholder text with API data
    document.getElementById('event-calendar-link').textContent += ` ${data.event_calendar}`;  // Remove .join(', ')
    document.getElementById('weather-forecast-link').textContent += ` ${data.weather_forecast}`;
    document.getElementById('location-services-link').textContent += ` ${data.location_services}`;
    
    // Add click event listeners to the links
    document.getElementById('event-calendar-link').addEventListener('click', openGoogleCalendar);
    document.getElementById('weather-forecast-link').addEventListener('click', openWeatherForecast);
    document.getElementById('location-services-link').addEventListener('click', openGoogleMaps);
})
.catch(error => console.error('Error fetching API data:', error));
