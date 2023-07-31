import requests
from datetime import datetime, timedelta, timezone
api_key = '1b6e515768131b3f2e08f97c66fc26f9'

#latitude = input('Enter lat: ')
#longitude = input('Enter longitude: ')

url = 'https://api.weather.gov/points/39.7456,-97.0892'

response = requests.get(url)
#print(response)
#print(response.json())

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the forecast URL from the response JSON
    data = response.json()
    forecast_url = data['properties']['forecast']

    # Send a GET request to the forecast URL
    forecast_response = requests.get(forecast_url)

    # Check if the forecast request was successful
    if forecast_response.status_code == 200:
        # Extract the forecast data from the response JSON
        forecast_data = forecast_response.json()

        # Access the forecast periods
        periods = forecast_data['properties']['periods']

        # Initialize variables for the closest period
        closest_period = None
        min_time_diff = timedelta.max
        # Input time as the current time
        input_time = datetime.now(timezone.utc)
        print(input_time)
# Iterate through each forecast period
        for period in periods:
            # Parse the start time of the period
            start_time = datetime.fromisoformat(period['startTime'])

            # Calculate the time difference
            input_time = datetime.now(timezone.utc)
            time_diff = abs(start_time - input_time)

            # Check if the current period has a smaller time difference
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_period = period

        # Display the closest forecast period
        if closest_period is not None:
            print('Closest Period:')
            print('Start time:', closest_period['startTime'])
            print('End time:', closest_period['endTime'])
            print('Temperature:', closest_period['temperature'], closest_period['temperatureUnit'])
            print('Short forecast:', closest_period['shortForecast'])
            print('Detailed forecast:', closest_period['detailedForecast'])
        else:
            print('No forecast period found.')

    else:
        print('Failed to retrieve the forecast. Error:', forecast_response.status_code)
else:
    print('Failed to retrieve the API data. Error:', response.status_code)