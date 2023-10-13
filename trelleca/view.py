from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from bson import ObjectId
from . import db
from datetime import datetime
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        task = request.form.get('task-description')
        titlle = request.form.get('task-titlle')
        if len(task)<1:
            flash("pica curta irmao", category='error')
        else:
            db.tasks.insert_one({
                "titlle": titlle,
                "description": task,
                "date": datetime.utcnow()
            })
    return render_template("home.html")

@views.route('/delete_task/<id>', methods=['GET', 'POST'])
def delete_task(id):
    db.tasks.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo successfully deleted", "success")
    return redirect("/")

'''@views.route("/update_todo/<id>", methods = ['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todos_flask.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        }})
        flash("Todo successfully updated", "success")
        return redirect("/")
    else:
        form = TodoForm()

        todo = db.todos_flask.find_one_or_404({"_id": ObjectId(id)})
        print(todo)
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completd", None)

    return render_template("add_todo.html", form = form)'''