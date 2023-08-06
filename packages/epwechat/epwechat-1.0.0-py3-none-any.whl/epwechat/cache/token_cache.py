import redis


class RedisInstance:
    def __init__(self, host: str, port: int, decode_responses=True):
        self.host = host
        self.port = port
        self.decode_responses = decode_responses

    def get_instance(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=self.decode_responses)
        return redis.Redis(connection_pool=pool)
