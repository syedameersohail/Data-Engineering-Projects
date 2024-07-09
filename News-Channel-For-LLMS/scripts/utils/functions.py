def validated_data(item, schema):
    validated_data = []
    for key,values in schema.items():
        if item.get(key) is None:
            if values['required']:
                if values['default'] is not None:
                    validated_data.append(values['default'])
                else:
                    raise ValueError(f"Missing required field: {key}")
            else:
                validated_data.append(values['default'])
        else:
            value = item.get(key)
            if not isinstance(value, values['type']):
                raise TypeError(f"Incorrect type for field {key}: Expected {values['type']}, got {type(value)}")
            validated_data.append(value)
    return validated_data
                