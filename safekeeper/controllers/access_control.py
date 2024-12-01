from common_utils.exception import ERROR_403
from common_utils.token import get_current_user
from flask import request, current_app, jsonify, abort

from safekeeper.services import rbac_service


def get_access_token(body=None):
    current_user = get_current_user(
        request.authorization.token, current_app.config.get("PUBLIC_KEY")
    )
    scopes = body.get("scopes", "")
    access_token = rbac_service.grant_access(current_user, scopes)
    if not access_token:
        return abort(403, ERROR_403)
    return (
        jsonify(
            {
                "access_token": access_token,
                "expires_in": current_app.config.get("TOKEN_EXPIRATION_TIME"),
                "scopes": scopes,
                "token_type": "Bearer",
            }
        ),
        200,
    )


def get_permission():
    current_user = get_current_user(
        request.authorization.token, current_app.config.get("PUBLIC_KEY")
    )
    role, scopes = rbac_service.get_permissions(current_user)
    return jsonify({"role": role, "scopes": scopes})
