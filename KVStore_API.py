import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import gen
import motor.motor_tornado
from pymongo import MongoClient
import pprint


#class to implement motor usage for mongodb interface
class DbAccess:

    def __init__(self):
    #self.client=MongoClient("mongodb://localhost:27017")
        self.client=motor.motor_tornado.MotorClient("mongodb://localhost:27017")
        self.db=self.client["storedb"] 
        self.store_collection=self.db['store']

    @gen.coroutine  
    def get_value(self,key):
        collection=self.db.self.store_collection
        document=yield collection.find_one()
        return document[key]

    def get(self,key):
        self.get_value(key)
        return 'ok'

    @gen.coroutine 
    def set_field(self,key,value):
        collection=self.db.self.store_collection
        field={key:value}
        document=yield collection.find_one()
        if not(document):
            collection.insert(field)
        else:
            collection.update(document,{'$set':field})

    def set(self,key,value):
        self.set_field(key,value)
        return 'ok'


class WebSocket(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True        

    def open(self):
        self.write_message("Hello")

    def on_message(self, message):

        db_access_obj=DbAccess()

        if message.startswith('get'):
            key=message.split('\\')[1]
            self.write_message(db_access_obj.get(key))

        elif message.startswith('set'):
            key=message.split('\\')[1]
            value=''.join(message.split('\\')[2:])
            self.write_message(db_access_obj.set(key,value))

        else:
            self.write_message('invalid message')

    def on_close(self): 
       self.write_message("Closed")


application = tornado.web.Application([
    (r"/connect", WebSocket)
])
 
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()