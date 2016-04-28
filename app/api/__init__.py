from flask import Blueprint
from ..errors import (
    ValidationError,
    bad_request,
    not_found,
)

api = Blueprint('api', __name__)


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


@api.errorhandler(400)
def bad_request_error(e):
    return bad_request('invalid request')


@api.errorhandler(404)
def not_found_error(e):
    return not_found('item not found')


# do this last to avoid circular dependencies
from . import snack
