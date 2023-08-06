import os
from aiohttp import web
from aiohttp_rest_api.loader import (
    load_and_connect_all_endpoints_from_folder,
    get_openapi_documentation,
)
from aiohttp_rest_api.redoc import setup_redoc

import logging

logging.basicConfig(level=logging.DEBUG)

app = web.Application()
load_and_connect_all_endpoints_from_folder(
    path="{0}/{1}".format(os.path.dirname(os.path.realpath(__file__)), "endpoints"),
    app=app,
    version_prefix="v1",
)

setup_redoc(app, openapi_info=get_openapi_documentation())

web.run_app(app)
