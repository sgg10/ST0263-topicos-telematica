from redis import StrictRedis

def connect(host: str = "0.0.0.0", password: str = "abc123", port: int = 6379, db: int = 0):
    try:
        return StrictRedis(host=host, password=password, port=port, db=db)
    except:
        raise Exception("Error while connecting to redis")