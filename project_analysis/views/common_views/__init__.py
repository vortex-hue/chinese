# -*- coding: utf-8 -*-
from flask import Blueprint
from constants import UrlPrefix

bp = Blueprint('common', __name__, url_prefix=UrlPrefix.COMMON_PREFIX)
