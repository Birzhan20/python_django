from django.http import HttpRequest
from django_ratelimit.decorators import ratelimit


def set_useragent_on_request_middleware(get_response):

    def middleware(request: HttpRequest):
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        return response
    return middleware


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exception_count = 0

    @ratelimit(key='ip', rate='1/s')
    def __call__(self, request: HttpRequest):
        self.request_count += 1
        print("request count: ", self.request_count)
        response = self.get_response(request)
        print("response count: ", self.response_count)
        self.response_count += 1
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print("got", self.exception_count, "exeptions so far")
