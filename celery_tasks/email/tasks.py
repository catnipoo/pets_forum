from django.conf import settings
from celery_tasks.main import celery_app

@celery_app.task(bind=True, name="send_verify_email", retry_backoff=3)
def send_verify_email(self, to_email, verify_url):
    from django.core.mail import send_mail
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用灵宠。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)

    # print('路劲为：',html_message)
    print('路径为：',to_email)
    print('来自',settings.EMAIL_FROM)
    try:
        send_mail(
            subject="灵宠",
            message=" ",
            from_email=settings.EMAIL_FROM,
            recipient_list=[to_email],
            html_message=html_message,
        )
    except Exception as e:

        raise self.retry(exe=e, max_retries=3)
