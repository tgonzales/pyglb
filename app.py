import os
import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.httpserver
from tornado.options import define, options, parse_command_line
import pymongo
from memcache import Client

from main_parse import main

define("port", default=8001, help="run on the given port", type=int)
define("ip", default='127.0.0.1', help="run on the given port")
define("mongo_host", default='127.0.0.1', help="run on the given port")
define("memcached_host", default='127.0.0.1', help="run on the given port")

base_dir = os.path.dirname(os.path.abspath(__file__))

class Hello(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello PyGlb')

class Users(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello Users')

class Noticias(tornado.web.RequestHandler):
    def get(self):
        wrapper = main(limit=int(self.get_query_argument('limit', '1')))
        self.write(wrapper)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/hello/", Hello),
            (r"/api/users/", Users),
            (r"/api/noticias/", Noticias),

        ]
        settings = dict(
            cookie_secret="32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            debug=True,
            login_url="/api/auth/login",
            logout_url="/api/auth/logout",
            server_ip = "{}".format(options.ip),
            server_port = "{}".format(options.port),
        )

        settings['db'] = pymongo.MongoClient('mongodb://{}:27017/'.format(options.mongo_host))
        settings['mc'] = Client(['{}:11211'.format(options.memcached_host)], debug=0)
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port, address='0.0.0.0')
    print('server {0} started ...{1}'.format('Checkin BackEnd', options.port))
    tornado.ioloop.IOLoop.instance().start()
