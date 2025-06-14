from fastapi import Depends, HTTPException, Header
from jose import jwt
import requests

import core.config as configs

def get_jwk():
    jwks_url = f"{configs.COGNITO_ISSUER}/.well-known/jwks.json"
    return requests.get(jwks_url).json()

def verify_token(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    jwks = get_jwk()
    headers = jwt.get_unverified_header(token)
    kid = headers["kid"]
    key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

    if not key:
        raise HTTPException(status_code=403, detail="Public key not found")

    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=configs.APP_CLIENT_ID,
            issuer=configs.COGNITO_ISSUER
        )
        return payload  # contains user info
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")