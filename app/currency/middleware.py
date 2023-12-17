from time import time
from .models import RequestResponseLog


class RequestResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print('BEFORE IN MIDDLEWARE')
        start = time()
        response = self.get_response(request)
        end = time()
        duration = int((end - start) * 1000)
        # print(f'AFTER IN MIDDLEWARE {duration} ms')
        RequestResponseLog.objects.create(
            path=request.path,
            request_method=request.method,
            time=duration
        )
        return response
