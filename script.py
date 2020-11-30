import jsonschema
import json
import os

from jsonschema import validate


def get_schema(user_schema):
    """This function loads the given schema available"""
    with open(f'./task_folder/schema/{user_schema}', 'r') as file:
        schema = json.load(file)
    return schema


def validate_json(json_data, schema):
    # Describe what kind of json you expect.
    execute_api_schema = get_schema(schema)
    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        err = " ".join(str(err).split("\n", 4)[:3])
        return False, err
    message = "Given JSON data is Valid"
    return True, message


json_list = os.listdir('./task_folder/event')
schema_list = os.listdir('./task_folder/schema')
log_data = []
with open('log.txt', 'w') as log:
    for json_file in json_list:
        with open(f'./task_folder/event/{json_file}', 'r') as input_file:
            # Convert json to python object.
            jsonData = json.load(input_file)
            try:

                log_data.append(f'\nChosen file: {json_file}')
                log_data.append(f"Schema chosen: {jsonData['event']}.schema")
                if f"{jsonData['event']}.schema" in schema_list:

                    # validate it
                    is_valid, msg = validate_json(jsonData['data'], f"{jsonData['event']}.schema")
                    log_data.append(f'Status: {is_valid}\n{msg} {jsonData["event"]}.schema')
                else:
                    log_data.append(f"{jsonData['event']}.schema: Schema not founded")
            except KeyError:
                log_data.append('Key "event" not founded')
            except TypeError:
                log_data.append('Value of key "event" not be null')
    log.write("\n".join(log_data))
