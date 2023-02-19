from rest_framework.exceptions import ValidationError


class BaseError(ValidationError):
    pass
