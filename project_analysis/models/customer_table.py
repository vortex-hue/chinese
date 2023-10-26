# -*- coding: utf-8 -*-
from . import dbModel
from constants import ExportStatu


class CustomerTable(dbModel):
    __tablename__ = 'customer_table'
    uuid = dbModel.UUIDField()
    user_account = dbModel.StringField('用户账号', is_index=True)
    user_name = dbModel.StringField('用户姓名', is_index=True)
    vip_level = dbModel.StringField('会员等级', is_index=True)
    pay_level = dbModel.StringField('支付层级', is_index=True)
    upper_id = dbModel.StringField('上级代理ID', is_index=True)
    agency = dbModel.StringField('上级代理', is_index=True)
    superAgentName =  dbModel.StringField('m.user.superAgentName', is_index=True)
    invite_code = dbModel.StringField('邀请码', is_index=True)
    inviter = dbModel.StringField('邀请人', is_index=True)
    user_email = dbModel.StringField('用户邮箱', is_index=True)
    user_tele = dbModel.StringField('用户手机', is_index=True)
    user_QQ = dbModel.StringField('用户QQ', is_index=True)
    login_time = dbModel.DateTimeField('登录时间')
    new_time = dbModel.DateTimeField('新增时间')
    is_deposit = dbModel.StringField('是否存款', is_index=True)
    deposit_count = dbModel.IntegerField('存款次数', is_index=True)
    deposit_money = dbModel.FloatField('存款金额')
    withdrawal_count = dbModel.IntegerField('取款次数', is_index=True)
    withdrawal_money = dbModel.IntegerField('提款金额', is_index=True)
    facebook = dbModel.StringField('facebook')
    zalo = dbModel.StringField('zalo')
    whatsapp = dbModel.StringField('whatsapp')
    telegram = dbModel.StringField('telegram')
    _create_time = dbModel.DateTimeField('时间', nullable=False)

    @classmethod
    def field_search(cls):
        return [
            'user_account',
            'user_name',
            'user_tele',
            'agency',
            'new_time',
            '_create_time',
        ]


class ExportDataModel(dbModel):
    """导出数据"""
    __tablename__ = 'export_data_table'
    uuid = dbModel.UUIDField()
    filename = dbModel.StringField('文件名', nullable=False, is_index=True)
    path = dbModel.StringField('文件路径', nullable=False)
    file_size = dbModel.IntegerField('文件大小(KB)', nullable=False)
    total = dbModel.IntegerField('数据量', nullable=False)
    out_count = dbModel.IntegerField('已导出')
    statu = dbModel.DictField('导出状态', dict_cls=ExportStatu, nullable=False, btn_show=True, is_index=True)
    _create_time = dbModel.DateTimeField('导出时间', nullable=False)
    note = dbModel.StringField('备注')
    @classmethod
    def field_search(cls):
        return ['statu', 'filename', '_create_time', 'note']


