import logging
from time import sleep
from random import randint
from typing import Optional
import multiprocessing as mp
from threading import Thread

from jinja2 import Template

from app.redis import connect
from app.cruds.users import CRUDUsers

str_template = """
<html>
    <h1>Hi, I'm {{first_name}} {{last_name}} | @{{nickname}}</h1>
</html>
"""

logging.basicConfig(level=logging.DEBUG, format="%(thread)s - %(threadName)s: %(message)s")

class HTMLGeneratorSuscriber(Thread):
    def __init__(self, name: Optional[str] = None, daemon: Optional[bool]=False):
        Thread.__init__(self, name=name, daemon=daemon)
        self.redis = connect()
        self.chanel = "users-readme"
        self.subscription = self.redis.pubsub()
        self.subscription.subscribe(self.chanel)

    def run(self):
        last_message = None
        for message in self.subscription.listen():
            actual_message = last_message or message
            logging.debug(f"MESSAGE ====== {message} | {type(message)}")
            if type(actual_message["data"]) == bytes:
                try:
                    nickname = actual_message["data"].decode("utf-8")
                    seconds = randint(30, 60)
                    logging.info(f"{nickname}: {seconds}s")
                    sleep(seconds)
                    template: Template = Template(str_template)

                    user_data = CRUDUsers(self.redis).get_user(nickname)
                    readme = template.render(user_data)

                    self.redis.hset(f"users:{nickname}", mapping={"readme": readme})
                    last_message=None
                except Exception as e:
                    last_message = message
                    logging.error(f"{e}")
