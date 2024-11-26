import json
from re import search
from datetime import datetime


def is_valid_bus_id(j_obj):
    return j_obj is not None and j_obj.get('bus_id') is not None and type(j_obj.get('bus_id')) == int


def is_valid_stop_id(j_obj):
    return j_obj is not None and j_obj.get('stop_id') is not None and type(j_obj['stop_id']) == int


def is_valid_stop_name(j_obj):
    return j_obj is not None and j_obj.get('stop_name') is not None and type(j_obj['stop_name']) == str and \
        len(j_obj['stop_name']) > 0 and search('([A-Z]{1}[a-z]+\\s)(Road|Avenue|Boulevard|Street)$', j_obj['stop_name'].strip()) is not None and \
        search(f'^[A-Z]', j_obj['stop_name']) is not None


def is_valid_next_stop(j_obj):
    return j_obj is not None and j_obj.get('next_stop') is not None and type(j_obj['next_stop']) == int


def is_valid_stop_type(j_obj):
    if j_obj is not None:
        if j_obj.get('stop_type') is None:
            return True
        if j_obj['stop_type'] is not None and type(j_obj['stop_type']) == str:
            return (j_obj['stop_type'] in ('S', 'O', 'F') and len(j_obj['stop_type']) == 1) or len(j_obj['stop_type']) == 0
    return False


def is_valid_atime(j_obj, prev_time, prev_bus_line, prev_a_time_validation, is_first):
    '''
        Validation criteria:
          * prev a_time is less than current a_time of the same bus_id
          * no need to validate more than 1 failed validation for the same bus_id
    '''
    if is_first or prev_bus_line != j_obj['bus_id'] or (prev_bus_line == j_obj['bus_id'] and prev_a_time_validation == False): return True

    # print(j_obj['bus_id'], prev_time < datetime.strptime(j_obj['a_time'], '%H:%M').time(), prev_time, datetime.strptime(j_obj['a_time'], '%H:%M').time())
    return prev_time < datetime.strptime(j_obj['a_time'], '%H:%M').time()


def is_valid_atime_format(j_obj):
    return j_obj is not None and j_obj.get('a_time') is not None and \
        type(j_obj['a_time']) == str and search('^[0-9][0-9]:[0-9][0-9]$', j_obj['a_time']) is not None and \
        int(j_obj['a_time'].split(":")[0]) <= 24 and int(j_obj['a_time'].split(":")[1]) <= 59


def validate_a_time(j_obj, validation_dict, prev_time, prev_bus_id, prev_a_time_validation, is_first):
    valid_time = False
    if is_valid_atime_format(j_obj) is True:
        valid_time = is_valid_atime(j_obj, prev_time, prev_bus_id, prev_a_time_validation, is_first)
        validation_dict['a_time'] += 0 if valid_time else 1
    return valid_time

def validate_non_time_based_json(j_obj, validation_dict):
    validation_dict['bus_id'] += 0 if is_valid_bus_id(j_obj) else 1
    validation_dict['stop_id'] += 0 if is_valid_stop_id(j_obj) else 1
    validation_dict['stop_name'] += 0 if is_valid_stop_name(j_obj) else 1
    validation_dict['next_stop'] += 0 if is_valid_next_stop(j_obj) else 1
    validation_dict['stop_type'] += 0 if is_valid_stop_type(j_obj) else 1


def populate_bus_lines(j_obj, bus_lines_dict):
    if j_obj['bus_id']:
        bus_id = str(j_obj['bus_id'])
        if bus_lines_dict.get(bus_id) is not None:
            bus_lines_dict[bus_id] += 1
        else:
            bus_lines_dict[bus_id] = 1


def add_start_finish_to_dict(my_dict, bus_id_str, stop_type):
    if my_dict.get(bus_id_str) is None:
        my_dict[bus_id_str] = list(stop_type)
    elif my_dict[bus_id_str] and stop_type not in my_dict[bus_id_str]:
        my_dict[bus_id_str].append(stop_type)


def process_xfer_stop(j_obj, xfer_dict):
    if xfer_dict.get(j_obj['stop_name']) is None:
        xfer_dict[j_obj['stop_name']] = []
        xfer_dict[j_obj['stop_name']].append(j_obj['bus_id'])
    else:
        if j_obj['bus_id'] not in xfer_dict[j_obj['stop_name']]:
            xfer_dict[j_obj['stop_name']].append(j_obj['bus_id'])


def populate_stop_types(j_obj, stop_types_dict, bus_start_finish_dict, xfer_dict):
    if j_obj['stop_type'].strip() == 'S' and j_obj['stop_name'] not in stop_types_dict['Start']:
        stop_types_dict['Start'].append(j_obj['stop_name'])
        add_start_finish_to_dict(bus_start_finish_dict, str(j_obj['bus_id']), 'S')
    elif j_obj['stop_type'].strip() == 'F' and j_obj['stop_name'] not in stop_types_dict['Finish']:
        stop_types_dict['Finish'].append(j_obj['stop_name'])
        add_start_finish_to_dict(bus_start_finish_dict, str(j_obj['bus_id']), 'F')

    process_xfer_stop(j_obj, xfer_dict)


def print_validation_results(validation_dict):
    print(f'Type and field validation: {sum(validation_dict.values())} errors')
    for k, v in validation_dict.items():
        print(k, ':', v)


def print_line_and_number_of_stops(bus_lines_dict):
    print('\nLine names and number of stops:')
    for k, v in bus_lines_dict.items():
        print(f'bus_id: {k} stops: {v}')


def print_xfer_type(xfer_dict):
    return [k[0] for k in list(filter(lambda x: len(x[1]) > 1, xfer_dict.items()))]


def print_stop_type(bus_lines_dict, stop_finish_dict, xfer_dict):
    for k, v in stop_finish_dict.items():
        if 'F' not in v and 'S' not in v:
            print(f'There is no start or end stop for the line: {k}')
            return

    print()
    xfers = print_xfer_type(xfer_dict)
    if len(bus_lines_dict['Start']) > 0: print(f"Start stops: {len(bus_lines_dict['Start'])} {sorted(bus_lines_dict['Start'])}")
    if len(xfers) > 0: print(f'Transfer stops: {len(xfers)} {sorted(xfers)}')
    if len(bus_lines_dict['Finish']) > 0: print(f"Finish stops: {len(bus_lines_dict['Finish'])} {sorted(bus_lines_dict['Finish'])}")


def main():
    json_input = input()
    json_data = json.loads(json_input)

    bus_start_finish_dict = {}   # key => bus id, value ['S', 'F', '', 'O']
    bus_lines_dict = {}     # key => bus id, value []
    xfer_dict = {} # key => stop name, value => [bus_id]
    stop_types_dict = {key: [] for key in ['Start', 'Finish', 'Transfer']}
    validation_dict = {key: 0 for key in ['bus_id', 'stop_id', 'stop_name', 'next_stop', 'stop_type', 'a_time']}

    is_first = True
    prev_bus_line = ""
    prev_time = datetime.strptime("00:00", "%H:%M").time()
    prev_a_time_validation = True
    for j in json_data:
        validate_non_time_based_json(j, validation_dict)
        prev_a_time_validation = validate_a_time(j, validation_dict, prev_time, prev_bus_line, prev_a_time_validation, is_first)

        populate_bus_lines(j, bus_lines_dict)
        populate_stop_types(j, stop_types_dict, bus_start_finish_dict, xfer_dict)
        is_first = False
        prev_time = datetime.strptime(j['a_time'], "%H:%M").time()
        prev_bus_line = j['bus_id']

    print_validation_results(validation_dict)
    print_line_and_number_of_stops(bus_lines_dict)
    print_stop_type(stop_types_dict, bus_start_finish_dict, xfer_dict)


if __name__ == '__main__':
    main()
