from redis import StrictRedis

def create_user(redis: StrictRedis, nickname, first_name=None, last_name=None):
    user_data = {}
    if first_name:
        user_data['first_name'] = first_name
    if last_name:
        user_data['last_name'] = last_name
    redis.hmset(f"users:{nickname}", user_data)
