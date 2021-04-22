from django.core.mail import send_mail


def send_activation_email(user):
    message = f"""Thank you for registering. Activate your account using the link:
    http://127.0.0.1:8000/api/v1/account/activate/{user.activation_code}/"""
    send_mail(
        'Активация аккаунта',
        message,
        'vika.sokolova728@gmail.com',
        [user.email, ]
    )
