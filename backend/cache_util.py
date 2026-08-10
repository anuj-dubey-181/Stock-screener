import hashlib
import json

from redis_client import redis_client


# Cache duration in seconds
CACHE_TTL = 300


def generate_cache_key(query: str) -> str:

    normalized_query = query.strip().lower()

    query_hash = hashlib.sha256(
        normalized_query.encode("utf-8")
    ).hexdigest()

    return f"screener:result:{query_hash}"


def get_cached_result(query: str):

    key = generate_cache_key(query)

    try:

        cached = redis_client.get(key)

        if cached is None:
            return None

        return json.loads(cached)

    except Exception:

        return None


def cache_result(
    query: str,
    result: dict
):

    key = generate_cache_key(query)

    try:

        redis_client.setex(
            key,
            CACHE_TTL,
            json.dumps(result, default=str)
        )
    
    except Exception:

        pass

def delete_cached_result(query: str):

    key = generate_cache_key(query)

    redis_client.delete(key)