from flask import Flask, render_template
app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',data=[{
        'description':"todo1"
    },{
        'description':'todo2'
    },{
        'description':'todos3'
    }])