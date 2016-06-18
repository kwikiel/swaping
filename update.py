# connect to db
# get keys list
# for each key perform update

from app import Keys
from swaper import Yolo

import time
import logging

logging.basicConfig(level=logging.DEBUG)

k = Keys.query.all()

for i in k:
    try:
        y = Yolo(key=i.public_key, secret=i.private_key)
        print y.cancel_all()
        print y.make_best()
    except Exception as e:
        logging.exception('wyjebalo sie xD')
