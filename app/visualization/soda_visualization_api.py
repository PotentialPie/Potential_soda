#encoding=utf8
import json

from flask_restplus import reqparse
from flask_restplus import Namespace

from app import sodaVisualizationService
from app.common.soda_common import SDResource, SDCodeMsg, SDCommonJsonRet, SDRequestParser
import requests
import math

base_ns = Namespace("base_api", description="base_api doc and test")



@base_ns.route("/query_flow")
class GetFlowInterface(SDResource):
    @base_ns.doc("query_flow",
                 params={"site": "站点名称",
                         "date": "日期",
                         "year": "年份"},
                 description=u"根据站点名称，日期，年份来获取24小时的人流量数据。\n"
                             u"年份参数必须为2016或者2018"
                             u"返回200：成功\n"
                             u"返回101：没有查询到相关人流量记录\n"
                             u"返回102：参数错误，检查参数")
    def get(self):
        parser_ = SDRequestParser()
        parser_.add_argument("site", type=str, required=True)
        parser_.add_argument("date", type=str, required=True)
        parser_.add_argument("year", type=str, required=True)

        params = parser_.parse_args()
        site = params['site']
        date = params['date']
        year = params['year']

        # 判断年份参数是否合法
        if year is None or (year != '2016' and year != '2018'):
            ret = SDCommonJsonRet(code=SDCodeMsg.PARAMS_ERROR.code,
                                  success=False,
                                  msg=SDCodeMsg.PARAMS_ERROR.msg,
                                  data=SDCodeMsg.PARAMS_ERROR.msg)
            return ret.toJson()

        # 查询当日当前站点人流量数据
        flow_data = sodaVisualizationService.query24hourFlowBySiteAndData(site,date,year)

        # 判断人流量数据是否为空，为空则返回错误
        if flow_data is None or flow_data == '':
            ret = SDCommonJsonRet(code=SDCodeMsg.FLOW_RECORD_NOT_FOUND.code,
                                  success=False,
                                  msg=SDCodeMsg.FLOW_RECORD_NOT_FOUND.msg,
                                  data=SDCodeMsg.FLOW_RECORD_NOT_FOUND.msg)
        else:
            # 不为空，则返回数据
            ret = SDCommonJsonRet(code=SDCodeMsg.SUCCESS.code,
                                  success=True,
                                  msg=SDCodeMsg.SUCCESS.msg,
                                  data=flow_data.as_dict())
        return ret.toJson()
