from django.http import HttpResponseForbidden

class AdminIPRestrictionMiddleware:
    """
    Middleware to restrict access to the admin interface based on IP address.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ips = ['156.0.214.6']
        
    def __call__(self, request):
        # Check if the request is for the admin interface
        if request.path.startswith('/admin/') and request.META.get('REMOTE_ADDR') not in self.allowed_ips:
            return HttpResponseForbidden("You are not allowed to access this page.")
        
        # Process the request
        response = self.get_response(request)
        
        return response