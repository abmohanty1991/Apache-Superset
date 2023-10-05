# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""The main config file for Superset

All configuration in this file can be overridden by providing a superset_config
in your PYTHONPATH as there is a ``from superset_config import *``
at the end of this file.
"""
# pylint: disable=too-many-lines
import imp  # pylint: disable=deprecated-module
import importlib.util
import json
import logging
import os
import re
import sys
# from collections import OrderedDict
# from datetime import timedelta
# from typing import (
#     Any,
#     Callable,
#     Dict,
#     List,
#     Literal,
#     Optional,
#     Type,
#     TYPE_CHECKING,
#     Union,
# )

# import pkg_resources
# from cachelib.base import BaseCache
# from celery.schedules import crontab
# from dateutil import tz
# from flask_appbuilder.security.manager import AUTH_DB
# from pandas._libs.parsers import STR_NA_VALUES  # pylint: disable=no-name-in-module

# from superset.advanced_data_type.plugins.internet_address import internet_address
# from superset.advanced_data_type.plugins.internet_port import internet_port
# from superset.advanced_data_type.types import AdvancedDataType
# from superset.constants import CHANGE_ME_SECRET_KEY
# from superset.jinja_context import BaseTemplateProcessor
# from superset.stats_logger import DummyStatsLogger
# from superset.superset_typing import CacheConfig
# from superset.utils.core import is_test, parse_boolean_string
# from superset.utils.encrypt import SQLAlchemyUtilsAdapter
# from superset.utils.log import DBEventLogger
# from superset.utils.logging_configurator import DefaultLoggingConfigurator
from flask import request
# from werkzeug.wrappers import Request


class RemoteUserMiddleware(object):
    def __init__(self,app):
        self.app=app
    
    def __call__(self, environ, request):
        from flask import render_template
        referer = request.headers.get("Referer")
        if referer:
            print("**************referer is there****************")
        else:
            # Render a error template
            return render_template('unauth_user.html')