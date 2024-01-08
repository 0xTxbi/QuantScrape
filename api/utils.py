import redis
from dotenv import load_dotenv
import os
import json


load_dotenv()


redisStore = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


# cache result
def cache_result(key, value):
    """
    Attempts to store a value in the Redis cache with a given key.

    Parameters:
    key (str): The key to associate with the value.
    value (str): The value to store in the cache.

    Returns:
    str: If the connection to the Redis server fails, returns a JSON string indicating that it couldn't connect to the Redis server.
    str: If any other exception occurs, returns a JSON string with a message indicating that an unexpected error occurred.
    """
    try:
        # set the cache key's expiration time
        redisStore.set(key, value, ex=18000)
        print(value)
        return json.dumps({"success": f"Value '{value}' stored with key '{key}'"})
    except redis.exceptions.ConnectionError:
        print(redis.exceptions.ConnectionError)
        return json.dumps({"error": "Error connecting to the Redis database"})
    except Exception as e:
        return json.dumps({"error": f"An unexpected error occured: {e}"})


# retrieve cached result
def get_cached_result(key):
    """
    Retrieves a value from the Redis cache with a given key.

    Parameters:
    key (str): The key associated with the value.

    Returns:
    str: If the connection to the Redis server fails, returns a JSON string indicating that it couldn't connect to the Redis server.
    str: If the key does not exist in the cache, returns None.
    str: If any other exception occurs, returns a JSON string with a message indicating that an unexpected error occurred.
    """
    try:
        value = redisStore.get(key)
        if value is None:
            return None
        print(f"retrieved: {value}")
        return json.loads(value)
    except redis.exceptions.ConnectionError:
        return json.dumps({"error": "Error connecting to the Redis database"})
    except Exception as e:
        return json.dumps({"error": f"An unexpected error occured: {e}"})


# delete cached_result
def delete_cached_result(key):
    """
    Deletes a value from the Redis cache with a given key.

    Parameters:
    key (str): The key associated with the value to delete.

    Returns:
    bool: True if the key was deleted, False if the key did not exist.
    """
    try:
        result = redisStore.delete(key)
        return result > 0
    except Exception as e:
        print(f"An error occurred while deleting the cached item'{key}': {e}")
        return False
