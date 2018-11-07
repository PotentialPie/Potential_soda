import json

# 通用基础服务service
import datetime
import requests


from app import digiccyDB
from app.common.soda_common import SDCodeMsg
#from app.common import xianda_utilimport random
from app.common.soda_common import SDResource, SDCommonJsonRet, SDCodeMsg



class SodaVisualizationService():
    def __init__(self):
        pass

    def query24hourFlowBySiteAndData(self, site, data, year):
        """
        根据site 、data、year 查询某站点某天24小时的流量记录
        :param site: 站点名称
        :param data: 日期
        :param year: 年份
        :return: 当日当前站点人流量记录
        """
        if year == 2016 or year == '2016':
            return Subway16StaByHourModel.query.filter_by(SITE=site, DATA=data).first()
        if year == 2018 or year == '2018':
            return Subway18StaByHourModel.query.filter_by(SITE=site, DATA=data).first()
        return None

    def querySiteTotalRecordsBySiteNumAndDate(self, site_num, date):
        """
        根据线路，日期，来查询当前线路当日所有站点的总人流量
        :param site_num:
        :param date:
        :return: 当日当前线路所有站点的总人流量
        """
        # 如果日期为空，则返回空值
        if date is None or date == '':
            return None

        # 根据site_num查询得所有站点
        site_list = self.querySiteByNum(site_num)
        if site_list is None or len(site_list) == 0:
            return None

        # 用于保存站点人流量数据
        site_totalNum_dict = {}

        year = ''
        if date.startswith('2016'):
            year = '2016'
        if date.startswith('2018'):
            year = '2018'

        if year == '':
            return None

        # 查询站点的人流量记录，并放入site_totalNum_dict
        for site_record in site_list:
            site_name = site_record['SITE_NAME']
            site_flow_record = self.query24hourFlowBySiteAndData(site_name, date,year)
            if site_flow_record is not None:
                site_totalNum_dict[site_flow_record.SITE] = site_flow_record.TOTALRECORDS

        return site_totalNum_dict

    def querySiteByNum(self, site_num):
        """
        根据地铁线号查询所有站点
        :param site_num: 地铁线路名称
        :return: 查询地铁线路的所有站点名称
        """
        filters = {}
        if site_num is not None and site_num != '':
            filters['SITE_NUM'] = site_num
        siteModels = digiccyDB.session.query(SiteModel).filter_by(**filters).all()
        return [ele.as_dict() for ele in siteModels]



'''
class SodaRailwayModel180101(digiccyDB.Model):
    __tablename__ = "soda_s180101_tb"
    __table_args__ = {"useexisting": True}
    CARD_ID = digiccyDB.Column(digiccyDB.VARCHAR(255), primary_key=False, nullable=True)
    DATE = digiccyDB.Column(digiccyDB.VARCHAR(255), primary_key=False, nullable=True)
    TIME = digiccyDB.Column(digiccyDB.VARCHAR(255), primary_key=False, nullable=True)
    LINE = digiccyDB.Column(digiccyDB.VARCHAR(255), primary_key=False, nullable=True)
    AMOUNT = digiccyDB.Column(digiccyDB.Float, primary_key=False, nullable=True)
    IS_DISCOUNT = digiccyDB.Column(digiccyDB.INTEGER, primary_key=False, nullable=True)
    WEEK = digiccyDB.Column(digiccyDB.VARCHAR(255), primary_key=False, nullable=True)
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
'''

class Subway16StaByHourModel(digiccyDB.Model):
    __tablename__ = "subway16_sta_by_hour_tb"
    __table_args__ = {"useexisting": True}
    SITE = digiccyDB.Column(digiccyDB.VARCHAR(255), primary_key=True, nullable=True)
    DATA = digiccyDB.Column(digiccyDB.DATE, primary_key=True, nullable=True)
    TOTALRECORDS = digiccyDB.Column(digiccyDB.INTEGER, primary_key=False, nullable=True)
    TIME0 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME1 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME2 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME3 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME4 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME5 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME6 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME7 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME8 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME9 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME10 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME11 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME12 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME13 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME14 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME15 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME16 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME17 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME18 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME19 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME20 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME21 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME22 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME23 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Subway18StaByHourModel(digiccyDB.Model):
    __tablename__ = "subway18_sta_by_hour_tb"
    #__table_args__ = {"useexisting": True}
    SITE = digiccyDB.Column(digiccyDB.VARCHAR(255), primary_key=True, nullable=True)
    DATA = digiccyDB.Column(digiccyDB.DATE, primary_key=True, nullable=True)
    TOTALRECORDS = digiccyDB.Column(digiccyDB.INTEGER, primary_key=False, nullable=True)
    TIME0 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME1 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME2 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME3 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME4 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME5 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME6 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME7 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME8 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME9 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME10 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME11 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME12 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME13 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME14 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME15 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME16 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME17 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME18 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME19 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME20 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME21 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME22 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)
    TIME23 = digiccyDB.Column(digiccyDB.Float, default=0, primary_key=False, nullable=True)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class SiteModel(digiccyDB.Model):
    __tablename__ = "site_tb"
    #__table_args__ = {"useexisting": True}
    SITE_ID = digiccyDB.Column(digiccyDB.INTEGER, primary_key=True, nullable=False)
    SITE_NAME = digiccyDB.Column(digiccyDB.VARCHAR(255), primary_key=False, nullable=False)
    SITE_NUM = digiccyDB.Column(digiccyDB.VARCHAR(255), primary_key=False, nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
