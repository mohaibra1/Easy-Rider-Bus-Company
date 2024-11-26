import json
import re
from collections import defaultdict


# Validation functions
def is_valid_int(value):
    return isinstance(value, int)

def is_valid_str(value):
    return isinstance(value, str) and value != ""

def is_valid_stop_name(value):
    return is_valid_str(value) and re.match(r"^[A-Z][a-z]+.*\s(Road|Avenue|Boulevard|Street)$", value)

def is_valid_stop_type(value):
    # Valid stop_type: empty or one of 'S', 'O', 'F'
    return value == "" or value in ["S", "O", "F"]

def is_valid_time(value):
    if not isinstance(value, str):
        return False
    # Validate time format: HH:MM in 24-hour format
    return re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", value) is not None

def validate_and_process(data):
    # Error counters
    errors = {
        "bus_id": 0,
        "stop_id": 0,
        "stop_name": 0,
        "next_stop": 0,
        "stop_type": 0,
        "a_time": 0,
    }
    # Validation and line processing
    bus_lines = defaultdict(list)  # To group stops by bus_id
    stop_types = defaultdict(list)  # {bus_id: {"S": [], "F": []}}
    all_stops = defaultdict(set)  # {stop_name: {bus_id}}

    for record in data:
        # Validate fields
        if not is_valid_int(record.get("bus_id")):
            errors["bus_id"] += 1
        if not is_valid_int(record.get("stop_id")):
            errors["stop_id"] += 1
        if not is_valid_stop_name(record.get("stop_name")):
            errors["stop_name"] += 1
        if not is_valid_int(record.get("next_stop")):
            errors["next_stop"] += 1
        if not is_valid_stop_type(record.get("stop_type")):
            errors["stop_type"] += 1
        if not is_valid_time(record.get("a_time")):
            errors["a_time"] += 1

        # Collect valid data
        bus_id = record.get("bus_id")
        stop_name = record.get("stop_name")
        stop_type = record.get("stop_type")
        #
        if is_valid_int(bus_id) and is_valid_stop_name(stop_name):
            bus_lines[bus_id].append(stop_name)
            all_stops[stop_name].add(bus_id)
            if stop_type in ["S", "F"]:
                stop_types[bus_id].append(stop_type)

    # Output errors
    total_errors = sum(errors.values())
    print(f"Type and field validation: {total_errors} errors")
    for field, count in errors.items():
        print(f"{field}: {count}")

    # Check each bus line for a single start and final stop
    print("\nLine names and number of stops:")
    for bus_id, stops in bus_lines.items():
        print(f"bus_id: {bus_id} stops: {len(stops)}")
    for bus_id, stops in bus_lines.items():
        # Check start and final stop conditions
        start_count = stop_types[bus_id].count("S")
        final_count = stop_types[bus_id].count("F")
        if start_count != 1 or final_count != 1:
            print(f"There is no start or end stop for the line: {bus_id}")
            return

    # Gather start, transfer, and final stops
    start_stops = sorted([stop for stop, buses in all_stops.items() if
                          "S" in [record.get("stop_type") for record in data if record.get("stop_name") == stop]])
    final_stops = sorted([stop for stop, buses in all_stops.items() if
                          "F" in [record.get("stop_type") for record in data if record.get("stop_name") == stop]])
    transfer_stops = sorted([stop for stop, buses in all_stops.items() if len(buses) > 1])

    # Output results
    print("\nStart stops:", len(start_stops), start_stops)
    print("Transfer stops:", len(transfer_stops), transfer_stops)
    print("Finish stops:", len(final_stops), final_stops)

# Example usage
if __name__ == "__main__":
    # Input data
    input_data = json.loads(input())  # JSON string
    validate_and_process(input_data)