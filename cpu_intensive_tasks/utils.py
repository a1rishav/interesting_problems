import random
import redis

def get_random_number(range_start, range_end, round_up_to=0):
    return int(round(random.uniform(range_start, range_end), round_up_to))


def get_pubsub(host='localhost', port=6379):
    return redis.Redis(host=host, port=port)


