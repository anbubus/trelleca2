from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from bson import ObjectId
from . import users
from datetime import datetime
views = Blueprint('views', __name__)

tasks = []

@views.route('/')
@login_required
def home():
    
    user = users.find_one({"_id": current_user.id})
    tasks = user["tasks"]
    return render_template('home.html', tasks = tasks)

@views.route('/add-tasks', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        task = request.form.get('task-description')
        titlle = request.form.get('task-titlle')
        if len(task)<1:
            flash("pica curta irmao", category='error')
        else:
            tasks = [{
                "titlle": titlle,
                "description": task,
                "date": datetime.utcnow()}]
            
            users.update_one({"_id":current_user.id}, {"$set": {"tasks": tasks}})
            
    return redirect(url_for('views.home'))

@views.route('/edit_task/<id>', methods=['GET', 'POST'])
def edit_task(id):
    if request.method == 'POST':
        task = request.form.get('task-description')
        titlle = request.form.get('task-titlle')
        if len(task)<1:
            flash("pica curta irmao", category='error')
        else:
            n_tasks = [{
                "titlle": titlle,
                "description": task,
                "date": datetime.utcnow()}]
            
            users.update_one({"_id":current_user.id, "tasks._id":ObjectId(id)}, {"$set": {"tasks": n_tasks}})


@views.route('/delete_task/<id>', methods=['GET', 'POST'])
def delete_task(id):
    users.update_one({"_id":current_user.id, "tasks._id":ObjectId(id)}, {"$pull": {"tasks._id": ObjectId(id)}})
    flash("Task deletada com sucesso", category="success")
    return redirect("/")

