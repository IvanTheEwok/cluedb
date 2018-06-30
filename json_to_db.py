import json
from app import db

json_data = open('objects_87.json').read()
data = json.loads(json_data)

for i in data:
    #print i["id"]
    #print i["name"].lower()

    item = Rs_items(id=i["id"], name=i["name"].lower())
    db.session.add(item)

db.session.commit()
