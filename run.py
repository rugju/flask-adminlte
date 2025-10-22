# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_minify  import Minify
from   sys import exit
from apps.config import config_dict
from apps import create_app, db
from apps.cryptobot.models import API

import logging
class HTTP_code_Filter(logging.Filter):
    def filter(self, record):  
        return "/static/" not in record.getMessage()

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
DEBUG = True

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    #app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)

    log = logging.getLogger('werkzeug')
    log.addFilter(HTTP_code_Filter())

if __name__ == "__main__":
    app.run(host="192.168.188.38")
    #app.context_processor ( inject_crypt_apis )
