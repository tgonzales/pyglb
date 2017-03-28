import tornado.web
import tornado.gen

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.set_header('Access-Control-Max-Age', 10000000)
        self.set_header('Access-Control-Allow-Headers', 'X-HTTP-Method-Override, Content-Type ')
        self.set_header('Content-type', 'application/json')
        self.set_header("Cache-control", "no-cache")

    def options(self):
        self.set_status(204)
        self.finish()

    @tornado.gen.coroutine
    def get_current_token(self):
        auth_header = self.request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            mc = self.settings['mc']
            auth_found = mc.get(token)
        
            print('token, auth_found, auth_header', token, auth_found, auth_header)
            if auth_found:
                return token, auth_found
            else:
                return (False,False)
        else:
            return (False, False)


    @tornado.gen.coroutine
    def is_authenticated(self):
        token, user = yield self.get_current_token()
        print('self.get_current_token()', self.get_current_token().result())
        print('self.get_current_token', token, user)
        #token = False
        if token:
            msg = 'Bearer {}'.format(token)
            self.set_status(200)
            self.set_header('Authorization', msg)
            return user
        else:
            self.set_status(401)
            self.set_header('Authorization', "Restricted")
            return False
