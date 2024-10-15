from fastapi import HTTPException, status

default_fields = {
    'status_code': status.HTTP_401_UNAUTHORIZED,
    'headers': {'WWW-Authenticate': 'Bearer'},
}

credentials_exception = HTTPException(
    **default_fields, detail='Could not validate credentials'
)

expired_token_exception = HTTPException(
    **default_fields, detail='Token has expired'
)

not_found_exception = HTTPException(**default_fields, detail='User not found')

invalid_credentials = HTTPException(
    **default_fields,
    detail='Invalid username or password',
)
