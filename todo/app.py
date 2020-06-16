# Need to import jsonify for returning the json data
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys 

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost:5432/todoapp'

db= SQLAlchemy(app)

# For migrating, instance created of migrate
migrate= Migrate(app,db)

class TodoList(db.Model):
    __tablename__="todolists"
    id=db.Column(db.Integer,primary_key= True)
    name= db.Column(db.String(), nullable=False)
    # Bakcref means the name of the thing so while specifying it would be todos.list basically a name i guess
    todos = db.relationship('Todo',backref='list', lazy=True)
    

#Forgot about inheriting remember -----
class Todo(db.Model):
    __tablename__ = "todos"
    id=db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    # New column added
    completed = db.Column(db.Boolean, nullable=False, default=False)
    # the todolists is the table name and id the column referencing it
    # Also, foreign key constraint are by default not null but we like to be explicit here
    list_id=db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)
    
    def __repr__(self):
        return f'< ID:{self.id}, Description: {self.description} >'


#Don't forget this line too to make the database
# DOn't need this while using migrations
# db.create_all()


# Remember >>> methods <<<<<< 
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error=False
    body={}
    try:
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
        
        body['description']=todo.description

    except :
        error=True
        db.session.rollback()
        print(sys.exc_info())
        # Returning the data as a JSON value. ALso need to import jsonify from flask
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)
    
@app.route('/todos/<todo_id>/check-completed', methods=['POST'])
def check_completed(todo_id):
    try:
        completed= request.get_json()['completed']
        print('completed',completed)
        
        #  Watch we are taking reference for the line here of the class that;s why
        todo= Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>/delete-button', methods=['DELETE'])
def delete_todos(todo_id):
    try:
        print(todo_id)
        todo=Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except :
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return jsonify({'success':True})

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    # Adding lists as exrea and modifying todos
    return render_template('index.html',
                        lists=TodoList.query.all() ,
                        active_list=TodoList.query.get(list_id),
                        todos=Todo.query.filter_by(list_id=list_id).order_by(Todo.id)
                        .all())
                           
@app.route('/')
def index():
    return redirect(url_for('get_list_todos',list_id=1))

    