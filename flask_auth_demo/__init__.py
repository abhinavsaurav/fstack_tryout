from flask import Flask, request, abort



app=Flask(__name__)
print("app running")

@app.route('/headers')
def headers():
    print("Hi Felicia!")
    print()
    if 'Authorization' not in request.headers:
        abort(401)
    
    auth_token=request.headers['Authorization'].split(' ')
    
    if len(auth_token) != 2:
        abort(401)
    elif auth_token[0].lower() != 'bearer':
        abort(401)
    
    return f"Bye Felicia! {auth_token[1]}"

    
    