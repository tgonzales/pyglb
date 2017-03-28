import os
import json
import uuid
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options, parse_command_line
import pymongo
from libs import memcache

from base import BaseHandler

MONGO_HOST = os.environ.get('MONGO_PORT_27017_TCP_ADDR', '127.0.0.1')
MEMCACHE_HOST = os.environ.get('MEMCACHED_PORT_11211_TCP_ADDR', '127.0.0.1')

define("port", default=8001, help="run on the given port", type=int)
define("ip", default='127.0.0.1', help="run on the given port")
define("database", default='checkin', help="run on the database")
define("mongo_host", default=MONGO_HOST, help="run on the given port")
define("memcached_host", default=MEMCACHE_HOST, help="run on the given port")

base_dir = os.path.dirname(os.path.abspath(__file__))

class Hello(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello PyGlb')


class Noticias(tornado.web.RequestHandler):
    def get(self):
        wrapper = main(limit=int(self.get_query_argument('limit', '1')))
        self.write(wrapper)


class HelloAuthHandler(BaseHandler):
    def get(self):
        '''
        curl -X GET \
        -H "X-Version: 1" \
        -H "Authorization: Bearer 85e5d2c1c422422ebab29dab9a39ae1c" \
        http://localhost:8001/hello
        '''
        user = self.is_authenticated().result()
        if user:
            self.write({"msg": "Autenticado", "user": user})
        else:
            self.write("Vc nao esta autenticado")


class UsersHandler(BaseHandler):
    def get(self):
        '''
        curl -X GET \
        -d "email=teste@teste.com&password=1234" \
        http://localhost:8001/api/users/
        '''
        email = self.get_body_argument("email")
        password = self.get_body_argument("password")

        if email and password:
            db = self.settings['db'].pyglb
            user = db.users.find_one({"email":email, "password":password}, 
                                        {"_id": 0, "password": 0})
            msg = "Usuario nao encontrado"
            if user:
                mc = self.settings['mc']
                get_token = uuid.uuid4().hex
                mc.set(get_token, user["email"], time=1*60*60*24)
                msg = {
                        "msg": "Usuario autenticado com sucesso",
                        "user": user,
                        "token": get_token
            }
            self.write(msg)
        else:
            self.set_status(404)
            self.write({"error": "E necessario especificar email e password"})


    def post(self):
        '''
        curl -X POST -v \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d '{"email":"teste@teste.com","password":"1234"}' \
        http://localhost:8001/api/users/
        '''
        data = json.loads(self.request.body.decode('utf-8'))
        email = data.get("email")
        password = data.get("password")
        msg = {"error": "E necessario especificar email e password"}

        if email and password:
            db = self.settings['db'].pyglb
            db.users.insert(data)
            msg = {"response": "Usuario criado com sucesso"}
        
        self.write(msg)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HelloHandler),
            (r"/hello", HelloAuthHandler),
            (r"/api/users/", UsersHandler),
            (r"/api/noticias/", Noticias),
        ]
        settings = dict(
            cookie_secret="32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            debug=True,
        )

        settings['db'] = pymongo.MongoClient('mongodb://{}:27017/'.format(options.mongo_host))
        settings['mc'] = memcache.Client(['{}:11211'.format(options.memcached_host)], debug=0)
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port, address='0.0.0.0')
    print('server {0} started ...{1}'.format('PyGlb BackEnd', options.port))
    tornado.ioloop.IOLoop.instance().start()
