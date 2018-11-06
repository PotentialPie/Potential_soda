# encoding=utf8
import json
import six

import flask
from flask import request
from flask_restplus import Resource, fields, Namespace, reqparse
from flask_restplus.reqparse import Argument, ParseResult
from werkzeug.exceptions import HTTPException
from werkzeug import exceptions
from enum import Enum


class SodaEnvEnum(Enum):
    # 开发环境
    DEVELOP = "develop"
    # 生产环境
    PRODUCTION = "production"


# 服务统一返回接口格式
class SDCommonJsonRet():
    def __init__(self, code, success, msg, data):
        self.code = code
        self.msg = msg
        self.data = data
        self.success = success

    def toJsonStr(self):
        return json.dumps(self.__dict__)

    def toJson(self):
        return self.__dict__


class SDCodeMsg():
    class CM():
        def __init__(self, code, msg):
            self.code = code
            self.msg = msg

    SUCCESS = CM(200, "success")
    FLOW_RECORD_NOT_FOUND = CM(101, "没有查询到相关的人流量记录")
    PARAMS_ERROR = CM(102, "请检查相关参数")

class SDResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        # todo
        super(SDResource, self).__init__(api, args, kwargs)


class SDArgument(Argument):
    def handle_validation_error(self, error, bundle_errors):
        error_str = six.text_type(error)
        error_msg = ' '.join([six.text_type(self.help), error_str]) if self.help else error_str
        errors = {self.name: error_msg}

        if bundle_errors:
            return ValueError(error), errors
        xdAbort(400, None, code=400,
                success=False,
                msg=errors,
                data="")


def xdAbort(codes=500, message=None, **kwargs):
    try:
        flask.abort(codes)
    except HTTPException as e:
        if message:
            kwargs['message'] = str(message)
        if kwargs:
            e.data = kwargs
        raise


class SDRequestParser(reqparse.RequestParser):
    def __init__(self, argument_class=SDArgument, result_class=ParseResult,
                 trim=False, bundle_errors=False):
        self.args = []
        self.argument_class = argument_class
        self.result_class = result_class
        self.trim = trim
        self.bundle_errors = bundle_errors

    def parse_args(self, req=None, strict=False):
        if req is None:
            req = request

        result = self.result_class()

        req.unparsed_arguments = dict(self.argument_class('').source(req)) if strict else {}
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                result[arg.dest or arg.name] = value
        if errors:
            xdAbort(400, None,
                    code=400,
                    success=False,
                    msg=errors,
                    data="")

        if strict and req.unparsed_arguments:
            arguments = ', '.join(req.unparsed_arguments.keys())
            msg = 'Unknown arguments: {0}'.format(arguments)
            raise exceptions.BadRequest(msg)

        return result
