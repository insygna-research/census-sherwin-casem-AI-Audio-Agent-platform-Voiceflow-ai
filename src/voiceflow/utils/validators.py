import re
import hmac
import hashlib
from typing import Any
from fastapi import Request


def validate_phone_number(phone: str) -> bool:
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone))


def validate_twilio_signature(request: Request, auth_token: str) -> bool:
    signature = request.headers.get('X-Twilio-Signature', '')
    url = str(request.url)
    
    params = {}
    if request.method == 'POST':
        params = dict(request.form)
    
    data = url + ''.join(f'{k}{v}' for k, v in sorted(params.items()))
    expected_signature = base64.b64encode(
        hmac.new(
            auth_token.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha1
        ).digest()
    ).decode('utf-8')
    
    return hmac.compare_digest(signature, expected_signature)


def validate_api_key(key: str) -> bool:
    return len(key) > 20 and key.startswith('sk-')
