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

### Fetching Plants

Retrieve the first plant and get the id.

```python
plant_list = api.get_plants()[0]["id"]
print(plant_list)
```

### Fetching Specific Plant

Get detailed information about a specific plant.

```python
plant_id = "plant_id"
plant_topic = api.get_plant(plant_id)
print(plant_topic)
```

## Quick Demo

Here's a quick demo showing how to use the Growatt API wrapper.

```python
from growatt import Growatt

api = Growatt()

api.login("user@example.com", "pass123")

plantId = api.get_plants()[0]["id"]
print(f"Plant ID: {plantId}")

plant = api.get_plant(plantId)
print(plant)

mixSn = api.get_mix_ids(plantId)[0][1]
print(mixSn)

mixTotal = api.get_mix_total(plantId, mixSn)
print(mixTotal)

mixStatus = api.get_mix_status(plantId, mixSn)
pprint(mixStatus)
```

### License

This project is licensed under the MIT License. See the LICENSE file for more details.