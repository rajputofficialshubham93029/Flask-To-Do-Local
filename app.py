import datetime
from flask import Flask , render_template , request
from pymongo import MongoClient
import urllib
import os
from bson.objectid import ObjectId

app = Flask(__name__)
mongo_uri = "mongodb+srv://rajputsrshubham930:" + urllib.parse.quote("Shubham123@") + "@todolistappication.tn0o23o.mongodb.net/test"
client = MongoClient(mongo_uri)
app.db = client.usernameandpassword
username=''

@app.route("/"  , methods=['GET' , 'POST'])
def login():
    global username
    print(request.method)
    print(request)
    if request.method=='GET':
        return render_template('login.html' , message='' , link='/' , loginorlogout='Login')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username=='' or password=='':
            return render_template('login.html' , message = 'Please Enter Username/Password' , link='/' , loginorlogout='Login')

        
        for x in app.db.password.find({}):
            print(x['username'] , x['password'])
            if x['username']==username and x['password']==password:
                todos = getAllTodoByUsername()
               
                return render_template('home.html' , username = username , todos = todos  , link='/' , loginorlogout='Logout')
        return render_template('login.html' , message='Invalid Username/Password' , link='/' , loginorlogout='Login')

@app.route("/add-todo" ,  methods=['POST'])
def add_to_do():
    print(username)
    title = request.form.get('title')
    description = request.form.get('description')
    print('title: '+title+' decsription: '+description)
    message = ''
    if(title=='' or description==''):
        message = 'Please Enter Valid Title And Description'
    else:
          
            app.db.todos.insert_one({
                'username':username , "title":title , "description":description

            })

    todos = getAllTodoByUsername()
    return render_template('home.html' , username=username , todos=todos , message=message , link='/' , loginorlogout='Logout')




def getAllTodoByUsername():
    todos = app.db.todos.find({})
    temp = []
    for x in todos:
        if x['username']==username:
            temp.append(x)
    return temp

@app.route("/delete")
def delete_to_do():
    id = request.args.get('id')
    result = app.db.todos.delete_one({'_id': ObjectId(id)})
    todos = getAllTodoByUsername()
    return render_template('home.html' , username=username , todos=todos , message='' , link='/' , loginorlogout='Logout')


@app.route("/update" ,methods=['GET' , 'POST'])
def update_to_do():
    if request.method=='GET':
        id = request.args.get('id')
        print('id for updation: '+id)
        todos = getAllTodoByUsername()
        temp = []
        for x in todos:
            if str(x['_id'])==id:
                temp.append(x)
        print('We Are Going To Update This Entry ' , temp) 
        return render_template('update.html' ,  todo=temp , username = username , link='/' , loginorlogout='Logout')
    else:
        description = request.form.get('description')
        title = request.form.get('title')
        id = request.form.get('id')
        message = ''
        if description=='' or title=='':
            message = 'Please Enter Valid Title And Description'
            return render_template('update.html' ,  todo=[{'title':title , 'description':description , '_id':id}] , message = message , username = username , link='/' , loginorlogout='Logout')
        else:
           
            print('title: '+title+' description: '+description+' id'+id)
            result = app.db.todos.update_one({'_id': ObjectId(id)} ,{"$set":{"title":title ,"description":description}})
            todos = getAllTodoByUsername()  
            print('After Submitting form username: '+username , todos )
            return render_template('home.html' ,  todos=todos , username = username , link='/' , loginorlogout='Logout')     
 

@app.route("/register"  , methods=['GET' , 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html' , link='/' , loginorlogout='Login')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username=='' or password=='':
            return render_template('register.html' , link='/' , loginorlogout='Login' , message='Please Enter Username/Password')
        else:
            print('USername to register' , username , password)
            app.db.password.insert_one({
                'username':username , "password"
:password
            })
            return render_template('login.html' , link='/' , loginorlogout='Login' , message='User Added Successfully')