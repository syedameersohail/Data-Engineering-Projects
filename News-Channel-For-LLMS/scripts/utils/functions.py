from datetime import datetime

def validated_data(item, schema):
    validated_dict = {}
    
    # Data versioning fields initialized first
    validated_dict['versioned_at'] = datetime.utcnow().isoformat(" ", "seconds")
    print("Timestamp being inserted:", validated_dict['versioned_at'])
    validated_dict['is_latest'] = True

    # Start validation for other fields
    for key, values in schema.items():
        if key in ['versioned_at', 'is_latest']:
            continue  # Skip these as they are already initialized

        if item.get(key) is None:
            if values['required']:
                if values['default'] is not None:
                    validated_dict[key] = values['default']
                else:
                    raise ValueError(f"Missing required field: {key}")
            else:
                validated_dict[key] = values['default']
        else:
            value = item.get(key)
            # if data type doesn't match, raise a type error
            if not isinstance(value, values['type']):
                raise TypeError(f"Incorrect type for field {key}: Expected {values['type'].__name__}, got {type(value).__name__}")
            validated_dict[key] = value

    return validated_dict
