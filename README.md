# Real-Time Weather Dashboard

This is a simple serverless web application that provides real-time weather information based on the given latitude and longitude. The application fetches current weather data and a 5-day forecast from the OpenWeatherMap API and displays it in a user-friendly format.

## Features

- Fetch current weather data including temperature in Celsius and Fahrenheit, weather description, humidity, and wind speed.
- Display a 5-day weather forecast.
- Display the city name based on the given latitude and longitude.

## Architecture

The application uses the following AWS services:

- **AWS Lambda**: Fetches weather data from the OpenWeatherMap API.
- **Amazon API Gateway**: Serves as the HTTP endpoint for the Lambda function.
- **Amazon S3**: Hosts the static website.
- **Amazon CloudFront** (optional): Serves the website over HTTPS for secure access to the Geolocation API.

## Prerequisites

- AWS CLI installed and configured with appropriate permissions.
- SAM CLI installed.
- An S3 bucket to store deployment artifacts.

## Deployment

### Step 1: Update the Lambda Function

Update the Lambda function code in `hello_world/app.py` as needed.

### Step 2: Build and Package the Application

```bash
sam build
sam package --output-template-file packaged.yaml --s3-bucket your-s3-bucket-name
```

### Step 3: Deploy the Application

```bash
sam deploy --template-file packaged.yaml --stack-name weather-dashboard-stack --capabilities CAPABILITY_IAM
```

### Step 4: Upload the Static Website to S3 Update the website/index.html file with your API Gateway URL.
```bash
aws s3 cp website/ s3://your-unique-bucket-name/ --recursive