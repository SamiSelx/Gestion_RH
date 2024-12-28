from django.http import HttpResponseForbidden

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")
            if getattr(request.user, 'role', None) != role:
                return HttpResponseForbidden(f"Access denied. Role '{role}' required.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
