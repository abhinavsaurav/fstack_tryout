from flask import Flask, request, abort
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'innocent.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Image'

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code  

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    print("Hi Felicia!")
    print()
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.1'
        }, 401)
        
    auth_token=request.headers['Authorization'].split(' ')

    if auth_token[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    elif len(auth_token) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    elif len(auth_token) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)
    

    return auth_token[1]

# Code for verification
def verify_decode_jwt(token):
    # we are fetching public key here using our domain and hitting the endpoint
    # It gives us a set of information for which we have to check if some info is present
    # This information resides in the header of the JWT
    
    # uses the public key
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # Now we are fetching our kid (key ID i guess) from the token 
    # Bascially we are doing a public-private key match i guess 
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    
    # If no kid is found that means its invalid we need it
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.4'
        }, 401)

    # We are now matching the keys here and then storing the values if it matches then we store its corresponding details
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


# creating decorator for getting the authorization token 
# it makes thing more convinent now we don't have to pass any more value 
# we just need to add the @requires_auth header and use the param jwt to get the received value
def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # calling the auth header
        jwt=get_token_auth_header()
        try:
            payload=verify_decode_jwt(jwt)
        except:
            abort(401)
        # passing the received value or headers as a parameter
        return f(payload,*args, **kwargs)
    return wrapper

app=Flask(__name__)
print("app running")

@app.route('/headers')
@requires_auth
def headers(payload):
    # the parameter can now be accessed above and then we can use it to print the values
    try:
        print(payload)
    except :
        abort(401)
    return f"Bye Felicia! {payload}"

    
    