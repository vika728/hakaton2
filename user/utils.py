from django.core.mail import send_mail


def send_activation_email(email, activation_code):
    activation_url = f"http://localhost:8000/v1/api/account/activate/{activation_code}"
    message = f"""

        Спасибо что зарегестрировались,
        пожалуйста активируйте свой аккаунт!
        Activation link: {activation_url}

"""
    send_mail(
        'activate your account',
        message,
        'test@test.com',
        [email, ],
        fail_silently=False
    )