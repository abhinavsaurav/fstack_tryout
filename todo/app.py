from flask import Flask, render_template
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

@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.all())
                           
    #                        data=[{
    #     'description':"todo1"
    # },{
    #     'description':'todo2'
    # },{
    #     'description':'todos3'
    # }])