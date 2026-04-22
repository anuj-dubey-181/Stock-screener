# import sqlite3

# # db_path = "data/stock_screener.db"


# class SQLCompiler:

#     def __init__(self, db_path = "screener.db"):

#         self.db_path = db_path
#         self.params = []
#         self.field_table_map = self._load_schema()

#     def _load_schema(self):
#         """
#         Load database schema dynamically
#         Maps column -> table
#         """

#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()

#         field_map = {}

#         cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

#         tables = [row[0] for row in cursor.fetchall()]

#         for table in tables:

#             cursor.execute(f"PRAGMA table_info({table})")

#             for col in cursor.fetchall():

#                 column_name = col[1]

#                 field_map[column_name] = table

#         conn.close()

#         return field_map

#     def _compile_conditions(self, conditions, logic):

#         clauses = []

#         for cond in conditions:

#             field = cond["field"]
#             operator = cond["operator"]
#             value = cond["value"]

#             if field not in self.field_table_map:
#                 raise ValueError(f"Field '{field}' not found in database")

#             table = self.field_table_map[field]

#             clauses.append(f"{table}.{field} {operator} ?")

#             self.params.append(value)

#         return f" {logic} ".join(clauses)

#     def compile(self, dsl):

#         entity = dsl.get("entity", "symbol")

#         logic = dsl.get("logic", "AND")

#         conditions = dsl.get("conditions", [])

#         where_clause = self._compile_conditions(conditions, logic)

#         base_query = """
#         SELECT symbols.symbol
#         FROM symbols
#         """

#         tables_needed = set()

#         for cond in conditions:

#             table = self.field_table_map[cond["field"]]

#             if table != "symbols":

#                 tables_needed.add(table)

#         joins = ""

#         for table in tables_needed:

#             joins += f"""
#             LEFT JOIN {table}
#             ON symbols.id = {table}.company_id
#             """

#         sql = base_query + joins

#         if where_clause:

#             sql += f" WHERE {where_clause}"

#         # Time Filter
#         time_filter = dsl.get("time_filter")

#         if time_filter:

#             if time_filter["type"] == "last_n_quarters":

#                 sql += """
#                 AND historical_metrics.quarter IN (
#                     SELECT quarter
#                     FROM historical_metrics
#                     ORDER BY quarter DESC
#                     LIMIT ?
#                 )
#                 """

#                 self.params.append(time_filter["value"])

#         # Limit
#         limit = dsl.get("limit", 20)

#         sql += " LIMIT ?"

#         self.params.append(limit)

#         return sql, self.params
    
    
from dsl_schema import ALLOWED_FIELDS,ALLOWED_TIME_FILTERS


def compile_dsl(dsl:dict):

    base_query = """
    SELECT DISTINCT s.symbol,s.company_name
    FROM symbol s
    """

    joins =set ()
    where_clauses = []
    values = []

    for cond in dsl["conditions"]:

        field = cond["field"]
        operator = cond["operator"]
        value = cond["value"]

        column = ALLOWED_FIELDS[field]

        table = column.split(".")[0]

        if table == "fundamentals":
            joins.add(
                "JOIN fundamentals f ON s.id = f.id"
            )
            column = column.replace("fundamentals", "f")

        if table == "historical_metrics":
            joins.add(
                "JOIN historical_metrics h ON s.id = h.id"
            )
            column = column.replace("historical_metrics", "h")

        where_clauses.append(f"{column} {operator} ?")

        values.append(value)

    where_sql = f" {dsl['logic']} ".join(where_clauses)

    sql = base_query + " ".join(joins)

    if where_sql:
        sql += " WHERE " + where_sql

    
     
    if "time_filter" in dsl:

        tf = dsl["time_filter"]

        if tf["type"] == "last_n_quarters":

            months = tf["value"] * 3

            joins.add("JOIN historical_metrics h ON s.id = h.company_id")

            sql += f"""
            AND h.date >= date('now', '-{months} months')
            """

    if "limit" in dsl:
        sql += f" LIMIT {dsl['limit']}"

    return sql.strip(), values