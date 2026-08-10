from dsl_schema import (
    VALID_FIELDS,
    FIELD_TABLES
)


# ============================================================
# SQL Compiler
# ============================================================

def compile_dsl(dsl: dict):
    """
    Convert DSL into parameterized PostgreSQL SQL.
    Returns:
        sql (str)
        params (dict)
    """

    # --------------------------------------------------------
    # Base Query
    # --------------------------------------------------------

    select_clause = """
    SELECT DISTINCT
    s.id,
    s.symbol,
    s.company_name,
    s.sector,
    s.industry,
    s.exchange
    """

    from_clause = """
    FROM symbol s
    """

    joins = set()

    where_clauses = []

    params = {}

    param_index = 0

    # ========================================================
    # Conditions
    # ========================================================

    for condition in dsl["conditions"]:

        field = condition["field"]

        operator = condition["operator"].lower()

        value = condition["value"]

        table = FIELD_TABLES[field]

        column = VALID_FIELDS[field]

        # ----------------------------------------------------
        # Replace aliases
        # ----------------------------------------------------

        if table == "symbol":

            column = column.replace(
                "symbol.",
                "s."
            )

        elif table == "fundamentals":

            joins.add("""
            JOIN fundamentals f
            ON s.id = f.company_id
            """)

            column = column.replace(
                "fundamentals.",
                "f."
            )

        elif table == "historical_metrics":

            joins.add("""
            JOIN historical_metrics h
            ON s.id = h.company_id
            """)

            column = column.replace(
                "historical_metrics.",
                "h."
            )

        # ====================================================
        # Normal Operators
        # ====================================================

        if operator in {

            "=",
            "!=",
            ">",
            "<",
            ">=",
            "<="

        }:

            key = f"p{param_index}"

            param_index += 1

            where_clauses.append(

                f"{column} {operator} :{key}"

            )

            params[key] = value

        # ====================================================
        # BETWEEN
        # ====================================================

        elif operator == "between":

            k1 = f"p{param_index}"

            param_index += 1

            k2 = f"p{param_index}"

            param_index += 1

            where_clauses.append(

                f"{column} BETWEEN :{k1} AND :{k2}"

            )

            params[k1] = value[0]

            params[k2] = value[1]

        # ====================================================
        # IN
        # ====================================================

        elif operator == "in":

            placeholders = []

            for item in value:

                key = f"p{param_index}"

                param_index += 1

                placeholders.append(f":{key}")

                params[key] = item

            where_clauses.append(

                f"{column} IN ({','.join(placeholders)})"

            )

        # ====================================================
        # LIKE
        # ====================================================

        elif operator == "like":

            key = f"p{param_index}"

            param_index += 1

            where_clauses.append(

                f"{column} ILIKE :{key}"

            )

            params[key] = f"%{value}%"

    # ========================================================
    # Time Filter
    # ========================================================

    if "time_filter" in dsl:

        tf = dsl["time_filter"]

        joins.add("""
        JOIN historical_metrics h
        ON s.id = h.company_id
        """)

        tf_type = tf["type"]

        if tf_type == "latest":

            where_clauses.append("""

            h.date = (

                SELECT MAX(date)

                FROM historical_metrics

            )

            """)

        elif tf_type == "last_n_quarters":

            months = tf["value"] * 3

            where_clauses.append(

                f"""

                h.date >=

                CURRENT_DATE - INTERVAL '{months} months

                """

            )

        elif tf_type == "last_n_years":

            years = tf["value"]

            where_clauses.append(

                f"""

                h.date >=

                CURRENT_DATE - INTERVAL '{years} years'

                """

            )

    # ========================================================
    # Build SQL
    # ========================================================

    sql = select_clause

    sql += from_clause

    if joins:

        sql += "\n"

        sql += "\n".join(sorted(joins))

    if where_clauses:

        sql += "\nWHERE\n"
        logic=dsl.get('logic','AND').upper()
        sql += f"\n {logic} ".join(

            where_clauses

        )

    limit = dsl.get(

        "limit",

        20

    )

    sql += f"\nLIMIT {limit}"

    return sql.strip(), params