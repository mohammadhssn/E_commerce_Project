from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from apps.account.models import OtpCode
from apps.melipayamak import Api


def send_otp_code(phone_number, code):
    """
        Send code to user for registering
        use in: app account - views.py
    """
    username = '09192311248'
    password = 'F7O1M'
    api = Api(username, password)
    sms = api.sms()
    to = phone_number
    _from = '50004001311248'
    text = f' :کد تایید شما {code}\n مدت زمان انقظا ۵ دقیقه.'
    response = sms.send(to, _from, text)
    print('*' * 90)
    print(response)


def get_instance_otpcode_from_session(instance_session=None):
    """
        get obj from OtpCode model
        use in: app account - views.py
    """
    try:
        code_instance = get_object_or_404(OtpCode, phone_number=instance_session.get('phone_number'))
    except OtpCode.MultipleObjectsReturned:
        query = OtpCode.objects.filter(phone_number=instance_session.get('phone_number'))
        code_instance = query.last()
        query.exclude(code=code_instance.code).delete()

    return code_instance


def delete_session_key(request=None, key=None):
    """
        delete session key
        use in: app account - views.py
    """
    try:
        del request.session[key]
        request.session.modified = True
    except Exception:
        pass


def send_email_complete_payment(user=None):
    """
        if order create successfully send email
    """
    if user.email:
        subject = _('Order successfully registered.')
        message = _('Visit your career panel to view and follow up.')
        from_email = 'mohammadhssnalizadeh78@gmail.com'
        to = [user.email]
        send_mail(subject, message, from_email, to)
    return None
