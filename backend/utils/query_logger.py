import json
from datetime import datetime



def log_query(prompt, dsl, sql, values, results):

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "dsl": dsl,
        "sql": sql,
        "values": values,
        "result_count": len(results),
        "results": results
    }

    with open("logs/query_logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

