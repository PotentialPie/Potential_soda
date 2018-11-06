# encoding=utf8
from app.soda_app import app, config_env

import logging
from logging.handlers import WatchedFileHandler

import gevent.monkey

if __name__ == "__main__":
    gevent.monkey.patch_all()

    acclog = logging.getLogger('gunicorn.access')
    acclog.addHandler(WatchedFileHandler('/logs/pyservice_log/soda_pyservice_access.log'))
    acclog.propagate = False
    errlog = logging.getLogger('gunicorn.error')
    errlog.addHandler(WatchedFileHandler('/logs/pyservice_log/soda_pyservice_error.log'))
    errlog.propagate = False

    print("环境 " + config_env.env)
    print(app.config)
    app.run()
