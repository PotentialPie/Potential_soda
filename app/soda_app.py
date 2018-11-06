# -*- coding: utf-8 -*-
import logging
from flask import Flask
from flask_restplus import reqparse
from flask_environments import Environments
from flask_restplus import Resource, Api
from app.soda_log import init_log
from app import init_beas_when_app_start
from app.visualization.soda_visualization_api import base_ns
from app.common.soda_common import SDCommonJsonRet, SDResource, SDCodeMsg, SDRequestParser

SERVICE_NAME = "soda_potentialpie_pyservice"
APP_URL_PREFIX = "/v1/api/soda"
app = Flask(SERVICE_NAME)
config_env = Environments(app,default_env="DEVELOPMENT")
config_env.from_object('config')

# 日志
init_log()

#加载配置 生产对应环境（生产／开发）的bean
init_beas_when_app_start(app)



api_plus = Api(app,version="v1.0.0",title=SERVICE_NAME,prefix=APP_URL_PREFIX)


#基础接口
BASE_URL_PREFIX = "/base"
api_plus.add_namespace(base_ns,BASE_URL_PREFIX)




@app.route("/")
def hello():
    return "Hello World!"

#统一404处理
@app.errorhandler(404)
def page_not_not_found(error):
    return SDCommonJsonRet(code=404,
                           success=False,
                           msg="404 Not Found . there is not this api",
                           data="").toJsonStr()

#统一异常处理
@api_plus.errorhandler
def default_error_handler(exception):
    logging.error(exception)
    return SDCommonJsonRet(code=500,
                           success=False,
                           msg=exception.message,
                           data="server exception capture").toJson()

@app.route(APP_URL_PREFIX+"/health_check")
def health_check():
    return SDCommonJsonRet(code=200,
                           success=True,
                           msg="health check is ok",
                           data="").toJsonStr()



@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = basepath + '/static/uploads/' + secure_filename(f.filename)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        t0 = time.time()
        boxes, lands, res_paths = facer.process_image(upload_path)
        ptime = time.time() - t0
        data = {'boxes':boxes.tolist(), 'time':ptime, 'lands':lands.tolist()}
        rpaths = []
        for rpath in res_paths:
            rpaths.append('http://2178zx8749.51mypc.cn' + rpath)
        data['paths'] = rpaths
        return json.dumps(data, ensure_ascii=False)
        return redirect(url_for('upload'))
    return render_template('upload.html')

if __name__ == "__main__":
    print("环境 " + config_env.env)
    print(app.config)
    app.run(debug=True, host='0.0.0.0', port=58480)