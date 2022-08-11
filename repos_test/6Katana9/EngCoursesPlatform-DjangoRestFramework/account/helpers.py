from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_activation_email(email, activation_code):
    activation_url = f'http://127.0.0.1:8000/account/activate/{activation_code}/'
    context = f'''
              Спасибо за регистрацию на нашем сайте.
              Пожайлуста, активируйте свой аккаунт.
              Кликнув на эту ссылку: {activation_url}  
            '''
    msg_html = render_to_string('email.html', {"small_text_detail":context})
    plain_message = strip_tags(msg_html)
    
    send_mail(
        'Здравствуйте, активируйте Свой аккаунт',
        plain_message,
        'tlbkvs@gmail.com',
        [email, ],
        html_message=msg_html,
    )