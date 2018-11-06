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

    # 根据user_address 、coin_type查询绑定记录
    def query24hourFlowBySiteAndData(self, site, data, year):
        """
        根据user_address 、coin_type查询用户和公司绑定的coin_type信息
        :param user_address: 用户地址
        :param coin_type: 币种 ETH／BTC／EOS 等
        :return: 用户绑定记录
        """
        if year == 2016 or year == '2016':
            return Subway16StaByHourModel.query.filter_by(SITE=site, DATA=data).first()
        if year == 2018 or year == '2018':
            return Subway18StaByHourModel.query.filter_by(SITE=site, DATA=data).first()
        return None



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
