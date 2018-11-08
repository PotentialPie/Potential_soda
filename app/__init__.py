# encoding=utf8
import datetime

import logging
from flask_sqlalchemy import SQLAlchemy

digiccyDB = SQLAlchemy()


from app.visualization.soda_visualization_service import SodaVisualizationService

sodaVisualizationService = SodaVisualizationService()



def init_beas_when_app_start(app):
    config_mysql_username = app.config["CONFIG_MYSQL_USERNAME"]
    config_mysql_password =  app.config["CONFIG_MYSQL_PASSWORD"]
    config_mysql_ipport =  '127.0.0.1:1235'
    config_mysql_database =  app.config["CONFIG_MYSQL_DATABASE"]
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"+config_mysql_username+\
        ":"+config_mysql_password+"@"+config_mysql_ipport+"/" +config_mysql_database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@127.0.0.1:3306/digiccy_db_test'

    logging.info("mysql init SQLALCHEMY_DATABASE_URI: " + app.config['SQLALCHEMY_DATABASE_URI'])
    # 配置flask配置对象中键：SQLALCHEMY_COMMIT_TEARDOWN,设置为True,应用会自动在每次请求结束后提交数据库中变动
    app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    digiccyDB.app = app
    digiccyDB.init_app(app)
    digiccyDB.create_all()
