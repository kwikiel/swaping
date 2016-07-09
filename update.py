# connect to db
# get keys list
# for each key perform update

from app import Keys, db
from swaper import Yolo, BitapiException

import time
import logging

#logging.basicConfig(level=logging.DEBUG)

k = Keys.query.all()

for i in k:
    try:
        y = Yolo(key=i.public_key, secret=i.private_key)
        print y.cancel_all()
        print y.make_best()
    except BitapiException as e:
        print(e.args[0])
        if e.args[0]['errorMsg'] == 'Invalid API key':
            print "Key to be removed :_: "
            Keys.query.filter_by(private_key=i.private_key).delete()
            db.session.commit()
    except Exception as e:
        logging.exception('General Exception')
        # print e
