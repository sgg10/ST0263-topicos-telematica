from typing import Optional

from fastapi import status
from redis import StrictRedis

from app.exceptions import HTTPAppException

class CRUDUsers:

    def __init__(self, redis_connection: StrictRedis):
        self.redis = redis_connection

    def get_users(self, *args, **kwargs):
        return [user.decode('utf8') for user in self.redis.lrange("users", 0, -1)]

    def get_user(self, nickname: str, *args, **kwargs):
        _key = f"users:{nickname}"
        users = self.get_users()

        if nickname in users:
            first_name = self.redis.hget(_key, "first_name")
            last_name = self.redis.hget(_key, "last_name")
            return {
                "nickname": nickname,
                "first_name": first_name.decode("utf-8") if first_name else None,
                "last_name": last_name.decode("utf-8") if last_name else None
            }
        raise HTTPAppException(message="User not exist", status_code=status.HTTP_404_NOT_FOUND)

    def create_user(self, nickname:str, first_name: Optional[str]=None, last_name: Optional[str]=None, *args, **kwargs):
        users = self.get_users()

        if nickname not in users:
            user_data = {}
            if first_name:
                user_data['first_name'] = first_name
            if last_name:
                user_data['last_name'] = last_name
            self.redis.hmset(f"users:{nickname}", user_data)
            self.redis.rpush(f"users", nickname)

            return {"nickname": nickname, **user_data}

        raise HTTPAppException(message="User already exist", status_code=status.HTTP_400_BAD_REQUEST)


    def update_user(self, nickname: str, first_name: Optional[str] = None, last_name: Optional[str] = None, *args, **kwargs):
        users = self.get_users()

        if nickname in users:
            user_data = {}
            if first_name:
                user_data['first_name'] = first_name
            if last_name:
                user_data['last_name'] = last_name
            self.redis.hmset(f"users:{nickname}", user_data)

            return self.get_user(nickname)

        raise HTTPAppException(message="User not exist", status_code=status.HTTP_404_NOT_FOUND)

    def delete_user(self, nickname: str, *args, **kwargs):
        users = self.get_users()

        if nickname in users:
            self.redis.delete(f"users:{nickname}")
            self.redis.lrem("users", 0, nickname)
            return

        raise HTTPAppException(message="User not exist", status_code=status.HTTP_404_NOT_FOUND)
