# -*- coding: utf-8 -*-
from flask import Blueprint
from constants import UrlPrefix

bp = Blueprint('api', __name__, url_prefix=UrlPrefix.API_PREFIX)
