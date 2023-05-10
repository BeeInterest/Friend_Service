import redis

class Relation:
    user_status = ""
    relations = []

    def __init__(self, user_status, relations):
        self.user = user_status
        self.relations = relations


class RedisDB:
    __redis_connect = redis.StrictRedis(host='localhost', port=6379, charset="utf-8", decode_responses=True)

    @classmethod
    def set_user(cls, username: str):
        cls.__redis_connect.set(username, username)

    @classmethod
    def set_relation(cls, relation: Relation):
        for value in relation.relations:
            cls.__redis_connect.rpush(f"{relation.user_status}", str(value))

    @classmethod
    def get_data(cls, key: str, count: int):
        return cls.__redis_connect.lrange(key, 0, count)

    @classmethod
    def get_keys(cls, who: str):
        return cls.__redis_connect.keys(pattern=f'{who}')

    @classmethod
    def del_relation(cls, userel: str, other_user: str):
        cls.__redis_connect.lrem(f'{userel}', 1, other_user)

    @classmethod
    def del_user(cls, user: str):
        cls.__redis_connect.delete(user)

    @classmethod
    def clear_redis(cls, who: str):
        for key in cls.__redis_connect.scan_iter(f"{who}*"):
            cls.__redis_connect.delete(key)
