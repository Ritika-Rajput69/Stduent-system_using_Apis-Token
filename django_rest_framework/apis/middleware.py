from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                elapsed_time = timezone.now() - last_activity
                if elapsed_time.total_seconds() > settings.SESSION_TIMEOUT:
                    logout(request)
                    return redirect(settings.LOGIN_URL)

            request.session['last_activity'] = timezone.now()

        response = self.get_response(request)
        return response
