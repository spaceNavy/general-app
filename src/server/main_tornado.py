# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : main_tornado.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
from pprint import pprint

import tornado
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from api_tornado.api_dashboard import *
from api_tornado.api_base import *

define("port", default=9996, help="run on the given port", type=int)
define("host", default="0.0.0.0", help="run on the given port", type=str)


class Application(tornado.web.Application):

    def __init__(self):

        self.handlers = [
            (r"/",                                                   ApiHome),
            (r"/api/general/login/",                    ApiLogin),
            (r"/api/general/db-init/",                 ApiDBInit),
            (r"/api/general/file-transform/",     ApiFileTransform),
            (r"/api/dashboard/user/",                ApiUser),
            (r"/api/dashboard/role/",                ApiRole),
            (r"/api/dashboard/company/",     ApiCompany),
        ]

        settings = dict(
            blog_title="Tornado Blog",
            # template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # static_path=os.path.join(os.path.dirname(__file__), "static"),
            # xsrf_cookies=True,
            debug=True,
        )

        tornado.web.Application.__init__(self, self.handlers, **settings)


# 入口函数
def main():
    app = Application()
    print("start with http://{host}:{port}".format(host=options.host, port=options.port))
    apis = [h[0] for h in app.handlers]
    print("api list:")
    pprint(apis)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, options.host)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    print("main_tornado start")
    main()
