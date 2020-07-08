from flask import Flask, request

def create_app(test_config=None):
    app=Flask(__name__)
    print("app running")
    
    @app.route('/headers')
    def headers():
        print("Hi Felicia!")
        return "Bye Felicia!"
    
    