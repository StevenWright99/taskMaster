import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Necessary requirements
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #Set up db connection and name
db = SQLAlchemy(app) #Initialize db with our Flask app

class Todo(db.Model): # Creating columns.
    # ID will be the task number
    id = db.Column(db.Integer, primary_key=True)
    # Content will hold the text of task
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    #Everytime we create a new task, we are going to return the task
    # and the id of the task that was just created
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] #Linked to html form name
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        # Looks at all database content in order they ere created and return all of them
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):\
    #Will attempt to get task by ID, if not, 404
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error updating your task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True) #Errors will pop up on webpage so we can see