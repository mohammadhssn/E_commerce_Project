from django.shortcuts import redirect, reverse


class CheckAccessTpPageWithSessionMixins:
    """
        Check access to page or Not,
    """

    def dispatch(self, request, *args, **kwargs):
        user_password_session = request.session.get('user_forgetting_password')
        user_session = request.session.get('user_registration_info')

        if user_session is None and request.path == reverse(
                'account:verify'):
            return redirect('catalogue:home')

        if (request.path == reverse('account:reset_password') or request.path == reverse(
                'account:reset_password_done')) and user_password_session is None:
            return redirect('catalogue:home')

        return super().dispatch(request, *args, **kwargs)
