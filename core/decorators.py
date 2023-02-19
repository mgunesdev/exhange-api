from core.helper.response_helper import get_not_authenticated_response


def check_auth(func):
    def wrap(self, request, *args, **kwargs):
        if not bool(request.user and request.user.is_authenticated):
            return get_not_authenticated_response()

        return func(self, request, *args, **kwargs)

    return wrap
