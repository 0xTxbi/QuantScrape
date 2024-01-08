import redis
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
import pytz

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
        # get current time
        current_time = datetime.now(pytz.timezone("US/Eastern"))

        # calculate the time until the next 7am
        if current_time >= 7:
            # if it's past 7am today, wait till tomorrow
            delta = timedelta(days=1) - (current_time - current_time.replace(hour=7))
        else:
            # otherwise, wait until today
            delta = current_time.replace(hour=7) - current_time

        # Convert the timedelta to seconds
        key_expiration_time = int(delta.total_seconds())

        # set the cache key's expiration time
        redisStore.set(key, value, ex=key_expiration_time)
        return json.dumps({"success": f"Value '{value}' stored with key '{key}'"})
    except redis.exceptions.ConnectionError:
        print(redis.exceptions.ConnectionError)
        return json.dumps({"error": "Error connecting to the Redis database"})
    except Exception as e:
        return json.dumps({"error": f"An unexpected error occured: {e}"})


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
        return json.loads(value)
    except redis.exceptions.ConnectionError:
        return json.dumps({"error": "Error connecting to the Redis database"})
    except Exception as e:
        return json.dumps({"error": f"An unexpected error occured: {e}"})
