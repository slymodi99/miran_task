import jwt
from django.conf import settings

def encode_token(payload):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
