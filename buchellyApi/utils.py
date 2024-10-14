from datetime import timedelta
from django.utils import timezone
import hashlib
import os
import jwt
import datetime
from django.conf import settings

def generate_token(user_id):
    token = hashlib.sha256(os.urandom(64)).hexdigest()
    expiration_date = timezone.now() + timedelta(hours=1)
    return token, expiration_date

def generate_jwt_token(user_id):
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    token = jwt.encode({
        'user_id': str(user_id),
        'exp': expiration
    }, settings.SECRET_KEY, algorithm='HS256')
    return token