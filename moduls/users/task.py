from trello.celery import app
from django.core.mail import send_mail



@app.task(name='user-email-task')

def user_email(data): 
    print('Send mail!')
    send_mail(
                subject='Trello registration',
                message=f'Hi {data["username"]}, thanks for registering!',
                from_email='trelloregister@group.com',
                recipient_list=[data["email"]],
                fail_silently=False
        )