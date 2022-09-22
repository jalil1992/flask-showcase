import secrets

"""Default application settings"""


class DefaultConfig:
    """Default configuration"""

    API_VERSION = "1.0"
    API_TITLE = "CALC Analysis"

    OPENAPI_VERSION = "3.0.2"

    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

    API_SPEC_OPTIONS = {"info": {"description": "This is a state-less microservice that serves all needs of CALC calculation. Check diagrams [here](https://miro.com/app/board/uXjVO2F_aI4=/)."}}

    JSON_SORT_KEYS = True

    SECRET_KEY = secrets.token_urlsafe(16)
    WTF_CSRF_SECRET_KEY = secrets.token_urlsafe(16)
    WTF_CSRF_CHECK_DEFAULT = False
