from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings

class SecretOauth(object):
    # 加密
    def dumps(self,data):
        s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
        result = s.dumps(data)
        return result.decode()

    def loads(self,data):
        s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
        result = s.loads(data)
        return result