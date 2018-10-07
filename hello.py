# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
from face.entry import facer
import time
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

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
    app.run(host='0.0.0.0', port=8080)
