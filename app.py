import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import os

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server
# Layout of the app
app.layout = html.Div([
    html.H1("Weather Dashboard"),
    
    # Input for city name
    dcc.Input(id='city-input', type='text', placeholder='Enter city name', debounce=True),
    
    # Dropdown to select temperature unit
    dcc.Dropdown(
        id='unit-dropdown',
        options=[{'label': 'Celsius', 'value': 'metric'}, {'label': 'Fahrenheit', 'value': 'imperial'}],
        value='metric',  # Default is Celsius
        style={'width': '40%'}
    ),
    
    # Graph for displaying temperature over time
    dcc.Graph(id='temperature-graph'),
    
    # Text output for weather description
    html.Div(id='weather-description'),
])

# API key for OpenWeatherMap (replace with your own API key)
API_KEY = "81c5bcdcc612d7e091edf3107ec20359"

# Callback to update weather data based on city input and selected unit
@app.callback(
    [Output('temperature-graph', 'figure'),
     Output('weather-description', 'children')],
    [Input('city-input', 'value'),
     Input('unit-dropdown', 'value')]
)
def update_weather(city, unit):
    if city is None or city == '':
        return px.line(), "Enter a city name to get weather data."
    
    # Format the city input to include the country code for Peru (PE)
    city_name = f"{city},PE"  # Add ',PE' for Peru
    
    # Request weather data from OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units={unit}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # Print the response from the API for debugging
    print(data)  # Add this line to print the response
    
    if data['cod'] != 200:
        return px.line(), f"Error: {data.get('message', 'City not found. Please try again.')}"
    
    # Extract relevant data
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    
    # Create temperature graph
    fig = px.bar(x=[city], y=[temperature], labels={'x': 'City', 'y': 'Temperature'}, title=f"Current Temperature in {city}")
    
    # Return the figure and description
    return fig, f"Weather Description: {description.capitalize()}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 80))  
    app.run_server(debug=True, host='0.0.0.0', port=port)
