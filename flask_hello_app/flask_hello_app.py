from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask("__main__")
#settign the configuration variable for connecting to the database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost:5432/example'
#Removing the deprecated warning 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__="persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    
    def __repr__(self):
        return f'<ID: {self.id}, Name:{self.name}>'

class Todos(db.Model):
    __tablename__="todos"
    id=  db.Column(db.Integer, primary_key=True)
    description =db.Column(db.String(),nullable=False)
    
    def __repr__(self):
         return f'<ID: {self.id}, description:{self.description}>'

db.create_all()

@app.route('/')
def index():
    jres=Person.query.join(Todos,Person.id==Todos.id).all();
    print(jres)
    return 'Hello'+ jres[0].description +'!'

if __name__ == "__main__":
    app.run()