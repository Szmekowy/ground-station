import json
from validation_rules import RULES

def validate_single_value(value, rules):
    if "types" in rules and not isinstance(value, rules["types"]):
        return False

    if "min" in rules and value < rules["min"]:
        return False

    if "max" in rules and value > rules["max"]:
        return False

    return True

def process_data_recursive(data, rules_dict):
    processed_data = {}
    is_valid = True

    for key, value in data.items():
        if key not in rules_dict:
            processed_data[key] = value
            continue

        rule = rules_dict[key]

        if isinstance(value, dict) and isinstance(rule, dict) and not ("types" in rule or "min" in rule):
            nested_data, nested_valid = process_data_recursive(value, rule)
            processed_data[key] = nested_data
            if not nested_valid:
                is_valid = False

        else:
            if validate_single_value(value, rule):
                processed_data[key] = value
            else:
                processed_data[key] = None
                is_valid = False

    return processed_data, is_valid

def data_read_validate(input_filepath):
    try:
        with open(input_filepath, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Błąd odczytu pliku: {e}")
        return None
    processed_data, data_is_valid = process_data_recursive(data, RULES)
    processed_data["is_valid"] = data_is_valid

    return processed_data
if __name__ == "__main__":
    print(data_read_validate("E:\\GIT\\Simle-gs\\ground-station\\tests\\raw_dara_sample\\raw_data1.json"))
