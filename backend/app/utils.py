def _type_name(pyobj):
    if isinstance(pyobj, bool): return "bool"
    if isinstance(pyobj, int): return "int"
    if isinstance(pyobj, float): return "float"
    if isinstance(pyobj, str): return "string"
    if isinstance(pyobj, dict): return "object"
    if isinstance(pyobj, list): return "array"
    return type(pyobj).__name__

def validate_parameters(schema: dict, params: dict):
    """
    Simple schema validation:
    - Ensures all keys in schema are present in params
    - Ensures type match by strings: string, int, float, bool, object, array
    - Ignores additional params (could restrict if desired)
    Returns (True, None) or (False, "error message")
    """
    if not isinstance(schema, dict):
        return False, "parameters_schema must be a JSON object"
    if not isinstance(params, dict):
        return False, "parameters must be a JSON object"

    for key, expected_type in schema.items():
        if key not in params:
            return False, f"Missing parameter '{key}'"
        actual = params[key]
        actual_type = _type_name(actual)
        if expected_type not in {"string","int","float","bool","object","array"}:
            return False, f"Unsupported expected type '{expected_type}' for '{key}'"
        if expected_type != actual_type:
            return False, f"Parameter '{key}' expected {expected_type} but got {actual_type}"
    return True, None
