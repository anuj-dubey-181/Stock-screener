from dsl_schema import ALLOWED_FIELDS, ALLOWED_OPERATORS, ALLOWED_LOGIC,ALLOWED_TIME_FILTERS

class DSLValidationError():
    pass

def validate_dsl(dsl: dict):

    if not isinstance(dsl, dict):
        raise ValueError("DSL must be a dictionary")

    # ----------------------------
    # Handle filters vs conditions
    # ----------------------------

    conditions = dsl.get("conditions") or dsl.get("filters")

    if not conditions:
        raise ValueError("DSL must contain conditions or filters")

    if not isinstance(conditions, list):
        raise ValueError("conditions must be a list")

    # ----------------------------
    # Validate logic
    # ----------------------------

    logic = dsl.get("logic", "AND")

    if logic not in ALLOWED_LOGIC:
        raise ValueError(f"Invalid logic operator: {logic}")

    # ----------------------------
    # Validate each condition
    # ----------------------------

    for cond in conditions:

        if "field" not in cond:
            raise ValueError("Condition missing field")

        if "operator" not in cond:
            raise ValueError("Condition missing operator")

        if "value" not in cond:
            raise ValueError("Condition missing value")

        field = cond["field"]
        operator = cond["operator"]
        value = cond["value"]

        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Invalid field: {field}. Allowed fields: {list(ALLOWED_FIELDS.keys())}"
            )

        if operator not in ALLOWED_OPERATORS:
            raise ValueError(
                f"Invalid operator: {operator}"
            )

        if not isinstance(value, (int, float)):
            raise ValueError(
                f"Value must be numeric for field {field}"
            )

    # ----------------------------
    # Validate time filter
    # ----------------------------


        
    if "time_filter" in dsl:

        tf = dsl["time_filter"]

        # Check structure
        if not isinstance(tf, dict):
            raise DSLValidationError("time_filter must be an object")

        # Check type
        if tf.get("type") not in ALLOWED_TIME_FILTERS:
            raise DSLValidationError(
                f"Invalid time filter type: {tf.get('type')}"
            )

        # Check value exists
        if "value" not in tf:
            raise DSLValidationError("time_filter must have 'value'")

        # Check type of value
        if not isinstance(tf["value"], int) or tf["value"] <= 0:
            raise DSLValidationError(
                "time_filter value must be a positive integer"
            )

    # ----------------------------
    # Validate limit
    # ----------------------------

    if "limit" in dsl:

        if not isinstance(dsl["limit"], int):
            raise ValueError("limit must be integer")

    return True
