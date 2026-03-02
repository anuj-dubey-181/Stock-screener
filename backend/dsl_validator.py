from dsl_schema import (
    ALLOWED_FIELDS,
    ALLOWED_OPERATORS,
    ALLOWED_LOGIC,
    MAX_CONDITIONS
)

from errors import DSLValidationError


def validate_dsl(dsl: dict):

    if "conditions" not in dsl:
        raise DSLValidationError("Missing conditions")

    conditions = dsl["conditions"]

    if not isinstance(conditions, list):
        raise DSLValidationError("Conditions must be a list")

    if len(conditions) == 0:
        raise DSLValidationError("Conditions cannot be empty")

    if len(conditions) > MAX_CONDITIONS:
        raise DSLValidationError("Too many conditions")

    for condition in conditions:

        validate_condition(condition)

    logic = dsl.get("logic", "AND")

    if logic not in ALLOWED_LOGIC:
        raise DSLValidationError("Invalid logic operator")

    return True


def validate_condition(condition):

    field = condition.get("field")
    operator = condition.get("operator")
    value = condition.get("value")

    if field not in ALLOWED_FIELDS:
        raise DSLValidationError(f"Invalid field: {field}")

    if operator not in ALLOWED_OPERATORS:
        raise DSLValidationError(f"Invalid operator: {operator}")

    expected_type = ALLOWED_FIELDS[field]

    if not isinstance(value, (int, float)):
        raise DSLValidationError(
            f"Invalid value type for {field}"
        )