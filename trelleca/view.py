from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from bson import ObjectId
from . import users
from datetime import datetime

views = Blueprint('views', __name__)

tasks = []

@views.route('/')
@login_required
def home():
    
    user = users.find_one({"_id": current_user.id}) 
    tasks = []
    for task in user["tasks"]: #Aqui convertemos os dados para que sejam exibidos
        task["_id"] = str(task["_id"])
        task["tittle"] = task["titlle"]
        task["date"] = task["date"].strftime("%b %d %Y %H:%M:%S")
        task["completed"] = task["completed"]
        tasks.append(task)
    return render_template('home.html', tasks = tasks)

@views.route('/add-tasks', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        description = request.form.get('task-description')
        titlle = request.form.get('task-titlle')
        if len(description)<1 or len(titlle)<1:
            flash("Empty quote", category='error')
        else:
            task = {
                "_id": ObjectId(),
                "titlle": titlle,
                "description": description,
                "date": datetime.utcnow(),
                "completed": False}
            
            users.update_one({"_id":current_user.id}, {"$push": {"tasks": task}})
            flash("Task added!", category='success')
            return redirect(url_for('views.home'))
    
    return render_template('add-task.html')
            
    

@views.route('/edit-task/<id>', methods=['GET', 'POST'])
def edit_task(id):
    if request.method == "POST":
        description = request.form.get('task-description')
        if len(description)<1:
            flash("Empty quote", category='error')
        else:    
            users.update_one({"_id":current_user.id, "tasks._id":ObjectId(id)}, {"$set": {"tasks.$.description": description}})
            return redirect('/') 
    return render_template('add-task.html')


@views.route('/delete-task/<id>', methods=['GET', 'POST'])
def delete_task(id):
    users.update_one({"_id":current_user.id}, {"$pull": {"tasks":{"_id": ObjectId(id)}}})
    flash("Task deleted successfully", category="success")
    return redirect("/")

@views.route('/update-task/<id>', methods=['GET', 'POST'])
def update_task(id):
    users.update_one({"_id":current_user.id, "tasks._id":ObjectId(id)}, {"$set": {"tasks.$.completed": True}})
    return redirect('/')

