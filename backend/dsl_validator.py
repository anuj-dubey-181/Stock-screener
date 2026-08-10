from dsl_schema import (
    VALID_FIELDS,
    FIELD_TYPES,
    VALID_OPERATORS,
    VALID_LOGIC,
    VALID_TIME_FILTERS
)


# ==========================================================
# Custom Exception
# ==========================================================

class DSLValidationError(Exception):
    """Raised when DSL validation fails."""
    pass


# ==========================================================
# Internal Helpers
# ==========================================================

def _validate_numeric(value, field):

    if not isinstance(value, (int, float)):
        raise DSLValidationError(
            f"'{field}' expects a numeric value."
        )


def _validate_string(value, field):

    if not isinstance(value, str):
        raise DSLValidationError(
            f"'{field}' expects a string value."
        )


# ==========================================================
# Main DSL Validator
# ==========================================================

def validate_dsl(dsl: dict):

    if not isinstance(dsl, dict):
        raise DSLValidationError(
            "DSL must be a dictionary."
        )

    conditions = dsl.get("conditions") or dsl.get("filters")

    if not conditions:
        raise DSLValidationError(
            "DSL must contain 'conditions'."
        )

    if not isinstance(conditions, list):
        raise DSLValidationError(
            "'conditions' must be a list."
        )

    logic = dsl.get("logic", "AND")

    if logic not in VALID_LOGIC:
        raise DSLValidationError(
            f"Invalid logic '{logic}'."
        )

    # =====================================================
    # Validate Conditions
    # =====================================================

    for condition in conditions:

        field = condition.get("field")
        operator = condition.get("operator")
        value = condition.get("value")

        if field is None:
            raise DSLValidationError(
                "Condition missing 'field'."
            )

        if operator is None:
            raise DSLValidationError(
                f"'{field}' missing operator."
            )

        if value is None:
            raise DSLValidationError(
                f"'{field}' missing value."
            )

        if field not in VALID_FIELDS:
            raise DSLValidationError(
                f"Invalid field '{field}'."
            )

        if operator not in VALID_OPERATORS:
            raise DSLValidationError(
                f"Invalid operator '{operator}'."
            )

        field_type = FIELD_TYPES[field]

        # ==============================================
        # Normal Operators
        # ==============================================

        if operator in {
            "=",
            "!=",
            ">",
            "<",
            ">=",
            "<="
        }:

            if field_type == "number":

                _validate_numeric(
                    value,
                    field
                )

            else:

                _validate_string(
                    value,
                    field
                )

        # ==============================================
        # BETWEEN
        # ==============================================

        elif operator == "between":

            if field_type != "number":

                raise DSLValidationError(
                    "'between' only supports numeric fields."
                )

            if not isinstance(value, list):
                raise DSLValidationError(
                    "'between' requires a list."
                )

            if len(value) != 2:
                raise DSLValidationError(
                    "'between' requires exactly two values."
                )

            for v in value:

                _validate_numeric(
                    v,
                    field
                )

        # ==============================================
        # IN
        # ==============================================

        elif operator == "in":

            if not isinstance(value, list):
                raise DSLValidationError(
                    "'in' requires a list."
                )

            if len(value) == 0:
                raise DSLValidationError(
                    "'in' cannot be empty."
                )

            if field_type == "number":

                for v in value:

                    _validate_numeric(
                        v,
                        field
                    )

            else:

                for v in value:

                    _validate_string(
                        v,
                        field
                    )

        # ==============================================
        # LIKE
        # ==============================================

        elif operator == "like":

            if field_type != "string":

                raise DSLValidationError(
                    "'like' only supports string fields."
                )

            _validate_string(
                value,
                field
            )

    # =====================================================
    # Time Filter
    # =====================================================

    if "time_filter" in dsl:

        tf = dsl["time_filter"]

        if not isinstance(tf, dict):

            raise DSLValidationError(
                "time_filter must be an object."
            )

        tf_type = tf.get("type")

        if tf_type not in VALID_TIME_FILTERS:

            raise DSLValidationError(
                f"Invalid time filter '{tf_type}'."
            )

        if tf_type != "latest":

            value = tf.get("value")

            if (
                not isinstance(value, int)
                or value <= 0
            ):

                raise DSLValidationError(
                    "time_filter value must be positive."
                )

    # =====================================================
    # LIMIT
    # =====================================================

    limit = dsl.get("limit", 20)

    if not isinstance(limit, int):

        raise DSLValidationError(
            "limit must be integer."
        )

    if limit <= 0:

        raise DSLValidationError(
            "limit must be greater than zero."
        )

    return True


# ==========================================================
# Alert Validator
# ==========================================================

def validate_alert_request(alert: dict):

    if not isinstance(alert, dict):
        raise DSLValidationError(
            "Alert must be a dictionary."
        )

    required_fields = [
        "symbol",
        "field",
        "operator",
        "target_value"
    ]

    for field in required_fields:

        if field not in alert:
            raise DSLValidationError(
                f"Missing required field '{field}'."
            )

    # --------------------------------
    # Symbol
    # --------------------------------

    if not isinstance(alert["symbol"], str):

        raise DSLValidationError(
            "symbol must be a string."
        )

    if not alert["symbol"].strip():

        raise DSLValidationError(
            "symbol cannot be empty."
        )

    # --------------------------------
    # Field
    # --------------------------------

    if alert["field"] not in VALID_FIELDS:

        raise DSLValidationError(
            f"Invalid alert field '{alert['field']}'."
        )

    # --------------------------------
    # Operator
    # --------------------------------

    allowed_alert_operators = {
        ">",
        "<",
        ">=",
        "<=",
        "=",
        "!="
    }

    if alert["operator"] not in allowed_alert_operators:

        raise DSLValidationError(
            f"Invalid alert operator '{alert['operator']}'."
        )

    # --------------------------------
    # Target value
    # --------------------------------

    if not isinstance(
        alert["target_value"],
        (int, float)
    ):

        raise DSLValidationError(
            "target_value must be numeric."
        )

    return True