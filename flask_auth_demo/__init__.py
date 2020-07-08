from flask import Flask, request, abort
from functools import wraps

def get_token_auth_header():
    print("Hi Felicia!")
    print()
    if 'Authorization' not in request.headers:
        abort(401)

    auth_token=request.headers['Authorization'].split(' ')

    if len(auth_token) != 2:
        abort(401)
    elif auth_token[0].lower() != 'bearer':
        abort(401)
    
    return auth_token[1]

# creating decorator for getting the authorization token 
# it makes thing more convinent now we don't have to pass any more value 
# we just need to add the @requires_auth header and use the param jwt to get the received value
def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # calling the auth header
        jwt=get_token_auth_header()
        # passing the received value or headers as a parameter
        return f(jwt,*args, **kwargs)
    return wrapper

app=Flask(__name__)
print("app running")

@app.route('/headers')
@requires_auth
def headers(jwt):
    # the parameter can now be accessed above and then we can use it to print the values
    print(jwt)
    return f"Bye Felicia! {jwt}"

    
    