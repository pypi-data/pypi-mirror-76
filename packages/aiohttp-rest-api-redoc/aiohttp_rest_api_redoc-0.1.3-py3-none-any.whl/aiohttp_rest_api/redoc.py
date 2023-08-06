import yaml
from collections import defaultdict
from typing_extensions import Final
import ujson as json
from os.path import abspath, dirname, join

from aiohttp.web import Application
from aiohttp import web

from aiohttp_rest_api.responses import (
    respond_with_json,
    respond_with_html,
    respond_with_yaml,
)


STATIC_PATH: Final = abspath(join(dirname(__file__), "redoc_ui"))


def build_doc_from_func_doc(handler, method):
    """

    :param handler:
    :param method:
    :return:
    """
    end_point_doc = handler.__doc__.splitlines()

    # Find openapi start point in doc
    end_point_openapi_start = 0
    for i, doc_line in enumerate(end_point_doc):
        if "---" in doc_line:
            end_point_openapi_start = i + 1
            break

    # Build JSON YAML Obj
    try:
        end_point_openapi_doc = yaml.safe_load(
            "\n".join(end_point_doc[end_point_openapi_start:])
        )
    except yaml.YAMLError:
        end_point_openapi_doc = {
            "description": "⚠ openapi document could not be loaded " "from docstring ⚠",
            "tags": ["Invalid openapi"],
        }

    # Add to general openapi doc
    return {method.lower(): end_point_openapi_doc}


def generate_doc_template(
    api_base_url: str = "",
    description: str = "openapi API definition",
    api_version: str = "v1",
    title: str = "openapi API",
    schemes: list = ("http", "https"),
) -> dict:
    return {
        "openapi": "3.0",
        "info": {
            "title": title,
            "description": description.strip(),
            "version": api_version,
        },
        "paths": defaultdict(dict),
    }


async def _openapi_home(request):
    """
    Return the index.html main file
    """
    return respond_with_html(request.app["openapi_TEMPLATE_CONTENT"])


async def _openapi_def(request):
    """
    Returns the openapi JSON Definition
    """
    return respond_with_yaml(request.app["openapi_DEF_CONTENT"])


async def _openapi_def_json(request):
    """
    Returns the openapi JSON Definition
    """
    return respond_with_json(request.app["openapi_DEF_CONTENT"])


def setup_redoc(
    app: Application,
    redoc_url: str = "/doc",
    # api_base_url: str = "/lol",
    description: str = "OpenAPI definition",
    api_version: str = "1.0.0",
    title: str = "Redoc API",
    contact: str = "",
    openapi_info: dict = None,
):
    _redoc_url = "/{}".format(redoc_url) if not redoc_url.startswith("/") else redoc_url
    _base_redoc_url = _redoc_url.rstrip("/")
    _openapi_def_url = "{}/openapi.yaml".format(_base_redoc_url)
    _openapi_def_url_json = "{}/openapi.json".format(_base_redoc_url)
    openapi_info = openapi_info

    # Add API routes
    # app.router.add_route('GET', _openapi_url, _openapi_home)
    # app.router.add_route('GET', "{}/".format(_base_openapi_url), _openapi_home)
    # app.router.add_route('GET', _openapi_def_url, _openapi_def)
    app.router.add_route("GET", _redoc_url, _openapi_home)
    app.router.add_route("GET", "{}/".format(_base_redoc_url), _openapi_home)
    app.router.add_route("GET", _openapi_def_url, _openapi_def)
    app.router.add_route("GET", _openapi_def_url_json, _openapi_def_json)

    # Set statics
    statics_path = "{}/openapi_static".format(_base_redoc_url)
    app.router.add_static(statics_path, STATIC_PATH)

    # --------------------------------------------------------------------------
    # Build templates
    # --------------------------------------------------------------------------
    app["openapi_DEF_CONTENT"] = openapi_info
    with open(join(STATIC_PATH, "index.html"), "r") as f:
        app["openapi_TEMPLATE_CONTENT"] = (
            f.read()
            .replace("##openapi_CONFIG##", _openapi_def_url)
            .replace("##STATIC_PATH##", "{}".format(statics_path))
        )


__all__ = "setup_redoc"

