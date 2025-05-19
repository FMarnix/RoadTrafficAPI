# RoadTrafficAPI
Simple API using Django REST Framework to control data.

## Traffic API

### Table of Contents
1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)
3. [Running the API](#running-the-api)
4. [Populating the Database](#populating-the-database)
5. [Using the API](#using-the-api)

## Prerequisites
- Make library installed
- Docker installed

## Getting Started
To use this repository, you will need to have the Make library installed on your system. This will allow you to easily run the Docker and Django commands.

## Running the API
To run the API, follow these steps:
1. Build the Docker image: `make build`
2. Start the Docker container: `make up`
3. Run the migrations: `make migrations`
4. Migrate the database: `make migrate`
5. Populate the database: `make populate`

## Code Formatting
Run `python3 -m black .` to format the code in the app.

## Populating the Database
The `populate` command will populate the database with data from two files in the `data` directory. The origin files are located in this GitHub [repository](https://github.com/Ubiwhere/Traffic-Speed/).

## Using the API

### Road Segments
#### Retrieve All Road Segments
**GET** `/api/road_segments/`
- **Query Parameters:**
  - `intensity` (optional): Possible values: `elevada`, `média`, `baixa`.
- **Response:** Returns a list of road segment objects containing:
  - `id`, `name`, `created_at`, `total_readings`, `traffic_speeds`.

#### Create a New Road Segment
**POST** `/api/road_segments/`
- **Request Body:** JSON object containing `name`.
- **Response:** Returns the newly created road segment object.

### Traffic Speeds
#### Retrieve All Traffic Speeds
**GET** `/api/traffic_speeds/`
- **Query Parameters:**
  - `intensity` (optional): Possible values: `elevada`, `média`, `baixa`.
- **Response:** Returns a list of traffic speed objects containing:
  - `id`, `road_segment`, `start_longitude`, `start_latitude`, `end_longitude`, `end_latitude`, `length`, `speed`, `timestamp`, `intensity`.

#### Create a New Traffic Speed
**POST** `/api/traffic_speeds/`
- **Request Body:** JSON object containing:
  - `road_segment`, `start_longitude`, `start_latitude`, `end_longitude`, `end_latitude`, `length`, `speed`.
- **Response:** Returns the newly created traffic speed object.

### Bulk Observations
#### Create Multiple Observations
**POST** `/api/observations/bulk/?api_key=<API_KEY>`
- **Authentication:** Requires a valid API key in the request header (`Authorization: API_KEY`).
- **Request Body:** JSON array of objects containing:
  - `car__license_plate`, `sensor__uuid`, `road_segment`, `timestamp`.
- **Response:** Returns a success message indicating observations were created.

### Car Observations
#### Retrieve Observations for a Specific Car
**GET** `/api/observations/{license_plate}/`
- **Path Parameter:** `license_plate` (required).
- **Response:** Returns a list of observation objects containing:
  - `road_segment`, `car`, `sensor`, `timestamp`.

### Other Endpoints
- **Admin:** `admin/` - Regular admin endpoint for the Django app.
- **Swagger:** `swagger/` - API documentation and testing UI.
