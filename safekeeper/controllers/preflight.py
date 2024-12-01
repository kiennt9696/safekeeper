from flask import make_response


def options_handler():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.status_code = 204
    return response


def authorize_preflight():
    return options_handler()


def permission_preflight():
    return options_handler()
