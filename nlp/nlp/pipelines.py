from pymongo import Connection

MONGO_USER     = "admin"
MONGO_PASSWD   = "admin"
MONGO_HOST     = "localhost"
MONGO_PORT     = 3002
MONGO_DATABASE = "meteor"

class MongoDBPipeline(object):
    def __init__(self):
        self.connection = Connection(host=MONGO_HOST, port=MONGO_PORT)
        self.db=self.connection[MONGO_DATABASE]
   
    def process_item(self, item, spider):
        collection = self.db["lyrics_letsingit"]
        item_to_insert = dict(item)
        collection.insert(item_to_insert)
        return item
