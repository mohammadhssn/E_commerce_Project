from apps.melipayamak import Api


def send_otp_code(phone_number, code):
    username = '09192311248'
    password = 'F7O1M'
    api = Api(username, password)
    sms = api.sms()
    to = phone_number
    _from = '50004001311248'
    text = f'کد تایید شما : {code}'
    response = sms.send(to, _from, text)
    print('*' * 90)
    print(response)

# from kavenegar import *
#
#
# def send_otp_code(phone_number, code):
#     api = KavenegarAPI('6E39745035626359304A6275577A787A755041782F39553545493470444263417A57584F5348716D44556B3D')
#     params = {'sender': '', 'receptor': '09379621925', 'message': '.وب سرویس پیام کوتاه کاوه نگار'}
#     response = api.sms_send(params)
#     print('*' * 90)
#     print(response)
