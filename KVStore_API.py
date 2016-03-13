import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import gen
import motor.motor_tornado
from pymongo import MongoClient
import pprint
import yaml

class DbAccess_Pymongo:

    def __init__(self,db_config):

        config=self.parse_config(db_config)

        self.identity=config["document"]
        self.collection=MongoClient(config["client"])[config['db']][config['collection']]

        self.collection.insert(self.identity)

    def parse_config(self,db_config):

        config_file=open(db_config)
        config=yaml.load(config_file)
        config_file.close()
        return config

    def get(self,key):
        try: 
            document=self.collection.find_one(self.identity)
            return document[key]
        except KeyError as e:
            return "Doesnt exists in store"


    def set(self,key,value):
        field={key:value}
        self.collection.update(self.identity,{'$set':field})
        return 'inserted field '+key


#class to implement motor usage for mongodb interface
class DbAccess:

    def __init__(self,db_config):

        config=self.parse_config(db_config)

        self.identity=config["document"]
        self.collection=motor.motor_tornado.MotorClient(config["client"])[config['db']][config['collection']]

        self.collection.insert(self.identity)

    def parse_config(self,db_config):

        config_file=open(db_config)
        config=yaml.load(config_file)
        config_file.close()
        return config

    @gen.coroutine  
    def get_value(self,key):
        try:
            document=yield self.collection.find_one(self.identity)
            return document[key]
        except KeyError as e:
            return "Doesnt exists in store"

    def get(self,key):
        return(self.get_value(key))
        
    @gen.coroutine 
    def set_field(self,key,value):
        field={key:value}
        self.collection.update(self.identity,{'$set':field})

    def set(self,key,value):
        self.set_field(key,value)
        return 'inserted field '+key


class WebSocket(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True        

    def open(self):
        self.write_message("Hello")

    def on_message(self, message):

        db_access_obj=DbAccess_Pymongo('appcfg.yaml')
        #db_access_obj=DbAccess('appcfg.yaml')

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