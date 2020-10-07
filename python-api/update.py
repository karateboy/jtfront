import io
import sys
import json

import urllib.request
from bson import ObjectId

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.__str__()
        else:
            return obj
i = 991  #792  952 problem 990
while i < 1000:
    # mongo_api = "http://localhost:5000/mysql/order/108819?force=1"  # local
    # mongo_api = "http://localhost:5000/mysql/order/108819?force=1"  # local
    mongo_api = "http://localhost:5000/mysql/product/"+str(i)+"?force=1"  # local
    print(mongo_api)
    i+=1

    data = urllib.request.urlopen(mongo_api).read().decode('utf8')
    json_document = json.loads(data)
    json_document = json.dumps(
        json_document, ensure_ascii=False, cls=Encoder, indent=2, sort_keys=True)
    # print(json_document)

