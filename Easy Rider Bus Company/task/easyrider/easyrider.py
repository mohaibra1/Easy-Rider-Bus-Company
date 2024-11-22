import json

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

def is_valid_time(value):
    if not isinstance(value, str):
        return False
    try:
        hours, minutes = map(int, value.split(":"))
        return 0 <= hours < 24 and 0 <= minutes < 60
    except ValueError:
        return False

def is_valid_stop_type(value):
    return value == "" or (isinstance(value, str) and len(value) == 1)

# Validation logic
for record in data:
    if not is_valid_int(record.get("bus_id", None)):
        errors["bus_id"] += 1
    if not is_valid_int(record.get("stop_id", None)):
        errors["stop_id"] += 1
    if not is_valid_str(record.get("stop_name", None)):
        errors["stop_name"] += 1
    if not is_valid_int(record.get("next_stop", None)):
        errors["next_stop"] += 1
    if not is_valid_stop_type(record.get("stop_type", None)):
        errors["stop_type"] += 1
    if not is_valid_time(record.get("a_time", None)):
        errors["a_time"] += 1

# Output results
total_errors = sum(errors.values())
print(f"Type and field validation: {total_errors} errors")
for field, count in errors.items():
    print(f"{field}: {count}")
