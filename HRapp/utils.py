import pyotp
from twilio.rest import Client
from django.http import JsonResponse
from datetime import datetime, timedelta

def send_otp(request):
    try:
        totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
        otp = totp.now()
        request.session['otp_secret_key'] = totp.secret
        valid_date = datetime.now() + timedelta(minutes=1)
        request.session['otp_valid_date'] = str(valid_date)

        print(f"Your OTP is {otp}")
        return JsonResponse({'status': 'success', 'message': 'OTP sent successfully'})
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return JsonResponse({'status': 'error', 'message': 'Error sending OTP'})

    

