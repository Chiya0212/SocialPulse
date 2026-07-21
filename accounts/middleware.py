class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.theme = request.user.theme
        else:
            request.theme = request.session.get('theme', 'dark')
        return self.get_response(request)
