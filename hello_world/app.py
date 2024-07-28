import os
import json
import requests
import boto3

ssm = boto3.client('ssm')

def get_api_key():
    response = ssm.get_parameter(Name='WeatherApiKey', WithDecryption=True)
    return response['Parameter']['Value']

WEATHER_API_URL = os.environ['WEATHER_API_URL']
WEATHER_API_KEY = get_api_key()

def lambda_handler(event, context):
    try:
        lat = event['queryStringParameters']['lat']
        lon = event['queryStringParameters']['lon']
        url = f"{WEATHER_API_URL}?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            current_weather = {
                'temp_celsius': weather_data['current']['temp'],
                'temp_fahrenheit': weather_data['current']['temp'] * 9/5 + 32,
                'description': weather_data['current']['weather'][0]['description'],
                'humidity': weather_data['current']['humidity'],
                'wind_speed': weather_data['current']['wind_speed'],
                'city_name': weather_data['timezone']
            }
            forecast = weather_data['daily'][:5]  # Get 5-day forecast
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'current_weather': current_weather, 'forecast': forecast})
            }
        else:
            return {
                'statusCode': response.status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Unable to fetch weather data'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }