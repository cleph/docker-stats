# Docker Stats API with FastAPI

This project provides a FastAPI-based REST API that retrieves Docker container statistics and returns them in JSON format. The API converts memory usage, network I/O, and block I/O values to megabytes and calculates CPU usage as a percentage.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Example Output](#example-output)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- Retrieves statistics of running Docker containers.
- Converts memory, network I/O, and block I/O data to megabytes.
- Calculates CPU usage as a percentage.
- Provides statistics in a JSON format suitable for monitoring and logging.

## Installation

### Prerequisites

- **Python 3.7+**
- **Docker** installed and running on your system
- **FastAPI** and **Docker SDK** for Python

### Step 1: Clone the Repository

```git clone https://github.com/cleph/docker-stats-api.git ```\
cd docker-stats-api
Step 2: Install Dependencies
Use pip to install the required packages.

```pip install fastapi docker uvicorn```\
Usage
To start the API server, run:

```uvicorn main:app --reload``` 
\
This will start the FastAPI server on http://127.0.0.1:8000.

API Endpoints
GET /docker-stats
Fetches the current statistics for all running Docker containers.

URL: /docker-stats
Method: GET
Response: JSON array containing stats for each container
Example Output
The API will return data in the following format:

```
{
  "containers": [
    {
      "container_id": "58976e29b201",
      "name": "bakerydemo-redis-1",
      "cpu_percent": 0.09,
      "mem_usage_mb": 13.31,
      "mem_limit_mb": 7756.34,
      "mem_percent": 0.17,
      "net_rx_mb": 0.002,
      "net_tx_mb": 0.001,
      "blk_read_mb": 0.0,
      "blk_write_mb": 0.0,
      "pids": 5
    },
    {
      "container_id": "1ac19a47ac40",
      "name": "bakerydemo-db-1",
      "cpu_percent": 0.05,
      "mem_usage_mb": 33.06,
      "mem_limit_mb": 7756.34,
      "mem_percent": 0.43,
      "net_rx_mb": 0.001,
      "net_tx_mb": 0.0,
      "blk_read_mb": 0.0,
      "blk_write_mb": 0.0,
      "pids": 7
    }
  ]
}
```
