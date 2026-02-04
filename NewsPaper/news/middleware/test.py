class MobileorFullMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        if request.mobile:
            preffix = 'mobile/'
        else:
            preffix = 'full/'
        response.template_name = preffix + response.template_name