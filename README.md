### README.md

# Growatt API

A Python wrapper for the Growatt API, allowing you to interact with Growatt's services.

## Installation

```bash
pip install growatt-api
```

## Usage

### Initialization and Login

First, create an instance of the `Growatt` class and log in using your Growatt credentials.

```python
from growatt import Growatt

api = Growatt()
api.login("your_email@example.com", "your_password")
```

### Fetching Plant List Title

Retrieve the list of plant titles.

```python
plant_list = api.getPlantListTitle()
print(plant_list)
```

### Fetching Plant Topic

Get detailed information about a specific plant.

```python
plant_id = "your_plant_id"
plant_topic = api.getPlantTopic(plant_id)
print(plant_topic)
```

## Quick Demo

Here's a quick demo showing how to use the Growatt API wrapper.

```python
from growatt import Growatt
from pprint import pprint

# Initialize and login
api = Growatt()
api.login("user@example.com", "pass123")

# Get the plant ID from the plant list
plant_list = api.getPlantListTitle()
plant_id = plant_list[0]["id"]
print(f"Plant ID: {plant_id}")

# Get devices by plant list
mixSn = api.getDevicesByPlantList(1, plantId)["obj"]["datas"][0]["alias"]
pprint(mixSn)

# Get MIX status data
mix_status_data = api.getMIXStatusData(plant_id, mixSn)
pprint(mix_status_data)
```

### License

This project is licensed under the MIT License. See the LICENSE file for more details.