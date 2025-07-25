from jose import jwt, JWTError
import requests

from config import Config

user_pool_id = Config.get("USER_POOL_ID")
cognito_region = Config.get("COGNITO_REGION")
client_id = Config.get("CLIENT_ID")
cognito_issuer = f'https://cognito-idp.{cognito_region}.amazonaws.com/{user_pool_id}'
jwks_url = f'{cognito_issuer}/.well-known/jwks.json'


def validar_token_cognito(token: str):
    try:
        headers = jwt.get_unverified_header(token)
        kid = headers['kid']

        jwks = requests.get(jwks_url).json()
        key = next((k for k in jwks['keys'] if k['kid'] == kid), None)

        if key is None:
            raise Exception('Chave pública não encontrada.')

        payload = jwt.decode(
            token,
            key,
            algorithms=['RS256'],
            audience=client_id,
            issuer=cognito_issuer
        )

        return payload

    except JWTError as e:
        raise Exception(f'Token inválido: {str(e)}')
