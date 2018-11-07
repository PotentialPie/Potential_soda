#encoding=utf8
import json

from flask_restplus import reqparse
from flask_restplus import Namespace
from flask import make_response
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
            ret = make_response(ret.toJsonStr())
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret

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
        ret = make_response(ret.toJsonStr())
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret

@base_ns.route("/query_site_by_line_num")
class GetSiteByLineNum(SDResource):
    @base_ns.doc("query_site_by_line_num",
                 params={"site_num": "地铁线路"},
                 description=u"根据地铁线号查询所有站点。\n"
                             u"地铁线路若为空，默认查询所有站点"
                             u"返回200：成功\n"
                             u"返回103：没有查询到相关站点记录\n"
                             u"返回102：参数错误，检查参数")
    def get(self):
        parser_ = SDRequestParser()
        parser_.add_argument("site_num", type=str, required=False)

        params = parser_.parse_args()
        site_num = params['site_num']

        # 查询线路的所有站点列表
        site_list = sodaVisualizationService.querySiteByNum(site_num)

        # 判断站点数据是否为空，为空则返回错误
        if site_list is None or site_list == '' or len(site_list) == 0:
            ret = SDCommonJsonRet(code=SDCodeMsg.SITE_RECORD_NOT_FOUND.code,
                                  success=False,
                                  msg=SDCodeMsg.SITE_RECORD_NOT_FOUND.msg,
                                  data=SDCodeMsg.SITE_RECORD_NOT_FOUND.msg)
        else:
            # 不为空，则返回数据
            ret = SDCommonJsonRet(code=SDCodeMsg.SUCCESS.code,
                                  success=True,
                                  msg=SDCodeMsg.SUCCESS.msg,
                                  data=site_list)
        ret = make_response(ret.toJsonStr())
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret

@base_ns.route("/query_site_flow_records_by_site_num_and_date")
class GetFlowRecordsBySiteNumAndDate(SDResource):
    @base_ns.doc("query_site_flow_records_by_site_num_and_date",
                 params={"site_num": "地铁线路",
                         "date": "日期"},
                 description=u"根据地铁线号和日期查询所有站点的某日总人流量记录。\n"
                             u"地铁线路若为空，默认查询所有站点"
                             u"返回200：成功\n"
                             u"返回104：某有查询到相关线路所有站点的人流总量记录\n"
                             u"返回102：参数错误，检查参数")
    def get(self):
        parser_ = SDRequestParser()
        parser_.add_argument("site_num", type=str, required=False)
        parser_.add_argument("date", type=str, required=True)

        params = parser_.parse_args()
        site_num = params['site_num']
        date = params['date']

        # 判断date是否合法
        if date is None or date == '' or (not str(date).startswith('2016') and not str(date).startswith('2018')):
            ret = SDCommonJsonRet(code=SDCodeMsg.PARAMS_ERROR.code,
                                  success=False,
                                  msg=SDCodeMsg.PARAMS_ERROR.msg,
                                  data=SDCodeMsg.PARAMS_ERROR.msg)
            ret = make_response(ret.toJsonStr())
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret


        # 查询线路的所有站点列表
        site_totalNum_dict = sodaVisualizationService.querySiteTotalRecordsBySiteNumAndDate(site_num, date)

        # 判断站点数据是否为空，为空则返回错误
        if site_totalNum_dict is None or site_totalNum_dict == '' or len(site_totalNum_dict) == 0:
            ret = SDCommonJsonRet(code=SDCodeMsg.SITE_FLOW_RECORD_NOT_FOUND.code,
                                  success=False,
                                  msg=SDCodeMsg.SITE_FLOW_RECORD_NOT_FOUND.msg,
                                  data=SDCodeMsg.SITE_FLOW_RECORD_NOT_FOUND.msg)
        else:
            # 不为空，则返回数据
            ret = SDCommonJsonRet(code=SDCodeMsg.SUCCESS.code,
                                  success=True,
                                  msg=SDCodeMsg.SUCCESS.msg,
                                  data=site_totalNum_dict)
        ret = make_response(ret.toJsonStr())
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret