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
    return value in ["S", "O", "F", ""]

def is_valid_time(value):
    return isinstance(value, str) and re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", value)

def validate_and_process(data):
    # Error tracking
    errors = {
        "bus_id": 0,
        "stop_id": 0,
        "stop_name": 0,
        "next_stop": 0,
        "stop_type": 0,
        "a_time": 0,
    }

    # Bus line details
    bus_lines = defaultdict(list)  # {bus_id: [stops]}
    stop_types = defaultdict(list)  # {bus_id: {"S": [], "F": []}}
    all_stops = defaultdict(set)  # {stop_name: {bus_id}}

    # Validate each record
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
            continue

        # Collect valid data
        bus_id = record.get("bus_id")
        stop_name = record.get("stop_name")
        stop_type = record.get("stop_type")

        if is_valid_int(bus_id) and is_valid_stop_name(stop_name):
            bus_lines[bus_id].append(record)
            all_stops[stop_name].add(bus_id)
            if stop_type in ["S", "F"]:
                stop_types[bus_id].append(stop_type)

    # Check each bus line for a single start and final stop
    print(f"Type and field validation: {sum(errors.values())} errors")
    for field, count in errors.items():
        print(f"{field}: {count}")

    print("\nLine names and number of stops:")
    for bus_id, stops in bus_lines.items():
        print(f"bus_id: {bus_id} stops: {len(stops)}")
        # Check start and final stop conditions
        start_count = [s for s in stops if s["stop_type"] == "S"]
        final_count = [s for s in stops if s["stop_type"] == "F"]
        if len(start_count) != 1 or len(final_count) != 1:
            print(f"There is no start or end stop for the line: {bus_id}")
            return

    # Gather start, transfer, and final stops
    start_stops = sorted([stop for stop, buses in all_stops.items() if "S" in [record.get("stop_type") for record in data if record.get("stop_name") == stop]])
    final_stops = sorted([stop for stop, buses in all_stops.items() if "F" in [record.get("stop_type") for record in data if record.get("stop_name") == stop]])
    transfer_stops = sorted([stop for stop, buses in all_stops.items() if len(buses) > 1])

    # Identify incorrect "on-demand" stops
    on_demand_stops = sorted([record["stop_name"] for record in data if record["stop_type"] == "O"])
    incorrect_on_demand = sorted(
        [
            stop for stop in on_demand_stops
            if stop in start_stops or stop in final_stops or stop in transfer_stops
        ]
    )
    correct_on_demand = sorted(set(on_demand_stops) - set(incorrect_on_demand))

    # Output results
    print("\nStart stops:", len(start_stops), start_stops)
    print("Transfer stops:", len(transfer_stops), transfer_stops)
    print("Finish stops:", len(final_stops), final_stops)

    print("\nOn demand stops:", len(correct_on_demand), correct_on_demand)

    if incorrect_on_demand:
        print("\nIncorrect on demand stops:", len(incorrect_on_demand), incorrect_on_demand)

# Example usage
if __name__ == "__main__":
    # Input data
    input_data = input()  # JSON string
    data = json.loads(input_data)
    validate_and_process(data)
