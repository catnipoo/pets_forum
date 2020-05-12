from django.conf import settings
from django.contrib.auth.backends import ModelBackend
import re
from apps.users.models import User

from pets_forum.settings import logger


def get_user_by_account(account):
    try:
        if re.match('^1[345789]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)

    except User.DoesNotExist:
        logger.error('用户对象不存在')
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 区分是前台在调用登录，还是后台在调用登录
        # if 'meiduo_amin/' in request.path:
        #     # 后台
        #     pass
        # else:
        #     # 前台
        #     pass

        if request is None:
            # 后台：jwt调用时未传递request对象
            try:
                # 查询指定用户名，并且是管理员
                user = User.objects.get(username=username, is_staff=True)
            except:
                return None
            else:
                # 判断密码是否正确
                if user.check_password(password):
                    return user
                else:
                    return None
        else:
            # 前台：调用时传递request对象
            # 3. 实现多账号 校验用户名和 手机号
            user = get_user_by_account(username)

            # 校验密码是否正确
            if user and user.check_password(password):
                return user
            else:
                return None


def generate_verify_email_url(user):
    # http://www.meiduo.site:8000/emails/verification/?token=eyJhbGciOiJIUzUxMiIsImlhdCI6MTU2NjE5ODk4MywiZXhwIjoxNTY2MjAyNTgzfQ.eyJ1c2VyX2lkIjo2LCJlbWFpbCI6ImxpdWNoZW5nZmVuZzY2NjZAMTYzLmNvbSJ9.okIKKAHjeskFild3EZeK3034N2r0vMb_tvUaVA7h4qPdfxmsDG4JvzXsTLl2_98Ln6rpWN4EmAdrdthZeG2DdQ
    host_url = settings.EMAIL_ACTIVE_URL
    data_dict = {
        'user_id': user.id,
        'email': user.email
    }
    from utils.secret import SecretOauth
    dumps_params = SecretOauth().dumps(data_dict)
    verify_url = host_url + "?token=" + dumps_params

    return verify_url
