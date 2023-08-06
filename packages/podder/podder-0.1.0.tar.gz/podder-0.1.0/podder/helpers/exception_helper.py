from podder.exceptions import *


def client_exception_handler(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (AuthorizationException, PodderApiException) as e:
            print(f'{type(e).__name__}: {e}')

    return wrap
