import json
import re
from collections import defaultdict

# Input JSON data
data = json.loads(input())

# Error counters
errors = {
    "bus_id": 0,
    "stop_id": 0,
    "stop_name": 0,
    "next_stop": 0,
    "stop_type": 0,
    "a_time": 0,
}

# Validation functions
def is_valid_int(value):
    return isinstance(value, int)

def is_valid_str(value):
    return isinstance(value, str) and value != ""

def is_valid_stop_name(value):
    if not is_valid_str(value):
        return False
    # Validate stop_name format
    return re.match(r"^[A-Z][a-z]+.*\s(Road|Avenue|Boulevard|Street)$", value) is not None

def is_valid_stop_type(value):
    # Valid stop_type: empty or one of 'S', 'O', 'F'
    return value == "" or value in ["S", "O", "F"]

def is_valid_time(value):
    if not isinstance(value, str):
        return False
    # Validate time format: HH:MM in 24-hour format
    return re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", value) is not None

# Validation and line processing
bus_lines = defaultdict(list)  # To group stops by bus_id
for record in data:
    # Type and field validation
    if not is_valid_int(record.get("bus_id", None)):
        errors["bus_id"] += 1
    if not is_valid_int(record.get("stop_id", None)):
        errors["stop_id"] += 1
    if not is_valid_stop_name(record.get("stop_name", None)):
        errors["stop_name"] += 1
    if not is_valid_int(record.get("next_stop", None)):
        errors["next_stop"] += 1
    if not is_valid_stop_type(record.get("stop_type", None)):
        errors["stop_type"] += 1
    if not is_valid_time(record.get("a_time", None)):
        errors["a_time"] += 1

    # Collect valid bus line data
    bus_id = record.get("bus_id")
    if is_valid_int(bus_id):
        bus_lines[bus_id].append(record["stop_id"])

# Output results
total_errors = sum(errors.values())
print(f"Type and field validation: {total_errors} errors")
for field, count in errors.items():
    print(f"{field}: {count}")

# Print bus lines and their stop counts
print("\nLine names and number of stops:")
for bus_id, stops in bus_lines.items():
    print(f"bus_id: {bus_id} stops: {len(stops)}")
