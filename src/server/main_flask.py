# coding: utf-8
"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : main_flask.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
import json
import jwt

from flask import Flask
from flask import request
from flask import session
from flask import g as g_user
from werkzeug.contrib.fixers import ProxyFix
from configure.parameter import AppSetting
from configure.status import APIStatus


from api_flask.api_dashboard import blueprint as blueprint_dashboard

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['SECRET_KEY'] = AppSetting.SECRET_KEY
app.config['RESTPLUS_VALIDATE'] = True
# the toolbar is only enabled in debug mode
app.debug = True

token_external = [
    "/api/dashboard/admin-space/login/",
    "/api/dashboard/admin-space/init-db/",
    "/api/dashboard/",
    "/api/dashboard/swagger.json"
]


@app.after_request
def cross_domain(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type, Authorization'
    return environ


@app.before_request
def before_request():
    req_path = request.path
    session.permanent = True
    app.permanent_session_lifetime = 3600
    if req_path.startswith("/api/dashboard/") and (req_path not in token_external):
        res = AppSetting.general_result()
        if AppSetting.AUTH_KEY not in request.headers:
            res["result"] = "fail"
            res["err_code"] = APIStatus.TOKEN_BROKEN
            res["message"] = "no token"
            return json.dumps(res)
        token = request.headers[AppSetting.AUTH_KEY]
        try:
            user_payload = jwt.decode(token, AppSetting.TOKEN_SECRET, algorithm='HS256')
        except Exception as err:
            res["result"] = "fail"
            res["err_code"] = APIStatus.TOKEN_BROKEN
            res["message"] = str(err)
            return json.dumps(res)
        # print(session)
        # if user_payload["uid"] not in session:
        #     res["result"] = "fail"
        #     res["err_code"] = APIStatus.NOT_YET_LOGIN
        #     res["message"] = "this user is not login: {}".format(user_payload["username"])
        #     return json.dumps(res)
        # if token != session[user_payload["uid"]]["token"]:
        #     res["result"] = "fail"
        #     res["err_code"] = APIStatus.TOKEN_EXPIRED
        #     res["message"] = "login expired, other client is using this user"
        #     return json.dumps(res)
        del res
        # g_user.user = session[user_payload["uid"]]
        g_user.user = user_payload


app.register_blueprint(blueprint_dashboard, url_prefix="/api/dashboard")


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=9998)
