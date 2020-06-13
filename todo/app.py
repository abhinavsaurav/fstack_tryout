# Need to import jsonify for returning the json data
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost:5432/todoapp'

db= SQLAlchemy(app)

#Forgot about inheriting remember -----
class Todo(db.Model):
    __tablename__ = "todos"
    id=db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    
    def __repr__(self):
        return f'< ID:{self.id}, Description: {self.description} >'


#Don't forget this line too to make the database
db.create_all()


# Remember >>> methods <<<<<< 
@app.route('/todos/create', methods=['POST'])
def create_todo():
    # Also, the blank 2nd param is the default text passed if there is no data
    ''' description = request.form.get('description','')         '''
    
    # Updated--to JSON--
    # We will receive a json body on ajax req which we set as the body and the param will be description
    # So we are accessing the dictionary
    description=request.get_json()['description']
    
    # Forgot the description = description field
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    
    # We need to import redirect, url_for and request from flask -------------------[IMP]
    # Also we are redirecting to the index function below so that it prints the data. 
    # It optionally takes in a second argument which index function might take like redirect(url_for('index'),data)
    # Also index might be taking a parameter data then like def index(data) 
    # return redirect(url_for('index'))
    
    # Returning the data as a JSON value. ALso need to import jsonify from flask
    return jsonify({
        'description': todo.description
    })
    
@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.all())
                           
    # List of objects 
    # 
    # data=[{
    #     'description':"todo1"
    # },{
    #     'description':'todo2'
    # },{
    #     'description':'todos3'
    # }])
    
    