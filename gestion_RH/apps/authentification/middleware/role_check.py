from django.http import HttpResponseForbidden
from django.shortcuts import redirect

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define route and role mapping
        protected_routes = {
            '/manager/': 'Manager',
            '/employee/': 'Employee',
            '/hr/': 'RH',
        }

        # Check if the request path matches any protected route
        for path, required_role in protected_routes.items():
            if request.path.startswith(path):
                # Check if the user is authenticated
                if not request.user.is_authenticated:
                    return redirect('/login/')  # Redirect to login if not authenticated
                
                # Check if the user has the required role
                if not hasattr(request.user, 'role') or request.user.role != required_role:
                    return HttpResponseForbidden(f"Access denied. Role '{required_role}' required.")

        # Proceed with the request if no restriction applies
        return self.get_response(request)
