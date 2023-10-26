# -*- coding: utf-8 -*-
from . import dbModel
from werkzeug.security import generate_password_hash, check_password_hash


class CmsUserModel(dbModel):
    """CMS-管理员表"""
    __tablename__ = 'cms_user_table'
    uuid = dbModel.UUIDField()
    id = dbModel.IDField()
    username = dbModel.StringField('用户名', nullable=False, is_index=True)
    login_account = dbModel.StringField('登录账户名', nullable=False)
    password = dbModel.PasswordField('密码',nullable=False)
    zalo = dbModel.StringField('zalo')
    email = dbModel.StringField('邮箱')
    statu = dbModel.BooleanField('状态', default=True, nullable=False, true_text='正常', false_text='禁用', is_index=True)
    _create_time = dbModel.DateTimeField('创建时间', nullable=False)
    _current_login = dbModel.DateTimeField('最后登录时间')
    _last_login_time = dbModel.DateTimeField('上次登录时间')
    _last_login_ip = dbModel.StringField(u'上次登录IP')
    intro = dbModel.StringField('介绍')
    note = dbModel.StringField('备注')
    permissions = []

    @classmethod
    def field_sort(cls):
        return ['id', 'telephone', 'login_account', 'email', 'statu', '_create_time', 'note']
    @classmethod
    def field_search(cls):
        return ['statu', 'username', 'login_account', 'note', '_create_time']
    @classmethod
    def add_field_sort(cls):
        return ['username', 'login_account', 'password', 'zalo', 'email', 'note']
    @classmethod
    def edit_field_sort(cls):
        return ['username', 'login_account', 'email', 'zalo', 'note']

    @property
    def is_superadmin(self):
        if self.permissions == ['superadmin']:
            return True
        return

    def has_permission(self, *args):
        if self.is_superadmin:
            return True
        for p in args:
            if p and p in self.permissions:
                return True
        return False

    @classmethod
    def encry_password(cls, raspwd):
        return generate_password_hash(raspwd)

    @classmethod
    def check_password(cls, pwd, rawpwd):
        """
        :param pwd: 密文
        :param rawpwd: 明文
        """
        return check_password_hash(pwd, rawpwd)
