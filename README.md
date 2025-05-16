# RoadTrafficAPI
 Simple API usign Django REST Framework to control data

# Traffic API

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)
3. [Running the API](#running-the-api)
4. [Populating the Database](#populating-the-database)
5. [Using the API](#using-the-api)

## Prerequisites

* Make library installed
* Docker installed

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

You can run the command 'python3 -m black .' to format the code in the app.

## Populating the Database

The `populate` command will use a function to populate the database with data from two files in the `data` directory. This will ensure that the database is populated with the necessary data.
The origin two files are locate on this GitHub [repository](https://github.com/Ubiwhere/Traffic-Speed/)

## Using the API

Once the API is running, you can use it to send requests to the `/api/observations/bulk/?api_key=...` endpoint. This endpoint accepts a JSON payload with the following format:
```json
[
  {
    "road_segment": 1,
    "car__license_plate": "AA16AA",
    "timestamp": "2023-02-20T14:30:00",
    "sensor__uuid": "270e4cc0-d454-4b42-8682-80e87c3d163c"
  }
]
