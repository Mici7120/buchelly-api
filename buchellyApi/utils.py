from datetime import timedelta
from django.utils import timezone
import hashlib
import os

def generate_token(user_id):
    token = hashlib.sha256(os.urandom(64)).hexdigest()
    expiration_date = timezone.now() + timedelta(hours=1)
    return token, expiration_date