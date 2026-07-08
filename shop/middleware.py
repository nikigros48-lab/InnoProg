class DiscountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.discount = True
        else:
            request.discount = False

        response = self.get_response(request)
        return response
