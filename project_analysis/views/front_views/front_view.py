# -*- coding: utf-8 -*-
from flask import render_template, views, request
from . import bp
from ..view_func import front_risk_control
from common_utils import xtjson
from common_utils.utils_funcs import get_ip

@bp.before_request
def site_before_request():
    statu, res = front_risk_control()
    if not statu:
        return res


