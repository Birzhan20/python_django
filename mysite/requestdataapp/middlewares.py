from django.http import HttpRequest, HttpResponseForbidden
import time


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
        self.last_request = {}
        self.THROTTLE_TIME = 0.1  #sec
        self.THROTTLE_MESSAGE = "Слишком много запросов, попробуйте позднее."

    def __call__(self, request: HttpRequest):
        ip_address = self.get_client_ip(request)
        current_time = time.time()

        if ip_address in self.last_request:
            last_request_time = self.last_request[ip_address]
            if current_time - last_request_time < self.THROTTLE_TIME:
                return HttpResponseForbidden(self.THROTTLE_MESSAGE)

        self.last_request[ip_address] = current_time

        self.request_count += 1
        print("request count: ", self.request_count)
        response = self.get_response(request)
        print("response count: ", self.response_count)
        self.response_count += 1
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print("got", self.exception_count, "exeptions so far")


    def get_client_ip(self, request): #IP from request META
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
