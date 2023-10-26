# -*- coding: utf-8 -*-
from flask import render_template
from .cms_base import CmsTableViewBase, CmsFormViewBase
from models.cms_user import CmsUserModel
from constants import PermissionType


class CmsUserView(CmsTableViewBase):
    MCLS = CmsUserModel
    title = '管理员列表'
    add_url_rules = [['/cms_user/', 'cms_user']]
    template = 'cms/site_config/admin_list.html'
    permission_map = [PermissionType.ACCESS, PermissionType.ADD, PermissionType.EDIT, PermissionType.DELETE]


class CmsUserCenterView(CmsFormViewBase):
    show_menu = False
    MCLS = CmsUserModel
    title = '管理员-个人中心'
    add_url_rules = [['/user_center/<string:data_uuid>/', 'user_center']]
    template = 'cms/site_config/admin_center.html'
    permission_map = [PermissionType.ACCESS, PermissionType.EDIT]

    def view_get(self, data_uuid):
        user_data = self.MCLS.find_one({'uuid': data_uuid})
        if not user_data:
            return self.xtjson.json_params_error()
        self.context['title'] = self.title
        self.context['user_data'] = user_data
        return render_template(self.template, **self.context)
