class HTMXMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # check if the request is from htmx
        request.htmx = request.headers.get('HX-Request') == "true"
        return self.get_response(request)