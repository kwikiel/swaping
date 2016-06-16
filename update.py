# connect to db
# get keys list
# for each key perform update

from app import Keys
from swaper import Yolo

import time

k = Keys.query.all()

for x in range(1,9):
    for i in k:
        try:
            y = Yolo(key=i.public_key, secret=i.private_key)
            print y.cancel_all()
            print y.make_best()
        except:
            print "Invalid API KEY"
    time.sleep(59)

