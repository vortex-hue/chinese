# -*- coding: utf-8 -*-
import datetime
from flask import views, render_template, request, session, redirect, url_for
from common_utils import xtjson
from common_utils.utils_funcs import graph_captcha, checkcap, get_ip
from models.cms_user import CmsUserModel
from constants import CMS_USER_SESSION_KEY, EventType, SITE_CONFIG_CACHE
from ..view_func import current_admin_data_dict, add_admin_log, get_ip
from common_utils.lqredis import SiteRedis


class CmsLoginOut(views.MethodView):
    add_url_rules = [['/login_out/', 'cms_login_out']]

    def get(self):
        session.pop(CMS_USER_SESSION_KEY)
        add_admin_log(EventType.OUTLOG, '退出登录')
        return redirect(url_for('admin.cms_login'))


class CmsLogin(views.MethodView):
    add_url_rules = [['/admin/login/', 'cms_login']]

    def login_limit(self):
        ip = get_ip()
        if not ip:
            return
        key = 'ADMIN_LOGIN_LIMIT_NUM_%s' % ip
        _crr_num = SiteRedis.get(key)
        if not _crr_num:
            return
        if int(_crr_num.decode()) >= 10:
            return True
        if not _crr_num:
            SiteRedis.set(key, 1, expire=600)
        else:
            SiteRedis.incrby(key, 1)
            SiteRedis.expire(key, 600)
        return

    def get(self):
        print("Login Page")
        has_session = current_admin_data_dict()
        print("HasSession:", has_session)
        # if True:
        if current_admin_data_dict() != {}:
            return redirect(url_for('admin.cms_index'))

        context = {
            'title': 'CMS-管理员登录',
            'img_cap': graph_captcha(),
            'cms_captcha': False,
        }
        if hasattr(SITE_CONFIG_CACHE, 'cms_captcha') and getattr(SITE_CONFIG_CACHE, 'cms_captcha'):
            context['cms_captcha'] = True
        return render_template('cms/login.html', **context)

    def post(self):
        action = request.form.get('action')
        if action == 'pwdLogin':
            login_account = request.form.get('login_account')
            password = request.form.get('password')
            graph_captcha = request.form.get('graph_captcha')
            if not login_account.strip() or not password.strip():
                return xtjson.json_params_error('登录失败!')
            if self.login_limit():
                return xtjson.json_params_error('尝试次数过多！请稍后再试...')
            user_cls = CmsUserModel.find_one({'login_account': login_account.strip()})
            if not user_cls:
                return xtjson.json_params_error('该用户不存在!')
            if not CmsUserModel.check_password(user_cls.get('password'), password.strip()):
                return xtjson.json_params_error('登录失败!')
            if not graph_captcha.strip():
                return xtjson.json_params_error('请输入验证码!')
            if not checkcap(graph_captcha.strip()):
                return xtjson.json_params_error('验证码输入错误！')
            if not user_cls.get('statu'):
                return xtjson.json_params_error('该账户已被锁定!')
            _ccu = CmsUserModel.find_one({'login_account': login_account.strip()})
            upda_dict = {
                '_last_login_time': _ccu.get('_current_login'),
                '_last_login_ip': get_ip(),
                '_current_login': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            CmsUserModel.update_one({'login_account': login_account.strip()},{'$set': upda_dict})
            session[CMS_USER_SESSION_KEY] = user_cls.get('uuid')
            session.permanent = True
            add_admin_log(EventType.LOGIN_SUCCESS, '登录成功!')
            print('ip:', get_ip(), '登录成功！')
            return xtjson.json_result()
        return xtjson.json_params_error('操作失败!')

