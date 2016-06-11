# connect to db
# get keys list
# for each key perform update

from app import Keys
from swaper import Yolo

k = Keys.query.all()

for i in k:
    y = Yolo(key=i.public_key, secret=i.private_key)
    print y.cancel_all()
    print y.make_best()

