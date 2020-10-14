import jwt
from django.conf import settings

def authenticate_credentials(token):
    track = False
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY)
        jwt.decode

        # try:
        #     key = JWTSession.objects.get(jwt=token)
        # except:
        #     key = None

        if payload:
            print(payload)
            return True
        else:
            return False
    except Exception as ex:
        return False


def decode_jwt(token):
    payload = jwt.decode(token, settings.JWT_SECRET_KEY)
    return payload
