from flask import Flask, render_template, flash, session, request, redirect
from mysqlconnection import MySQLConnector
from datetime import datetime

# # # a GET request to /users - calls the index method to display all the users. 
# # This will need a template.

app = Flask(__name__)
app.secret_key = 'aconevn23n!r13ndabcnqib2p33'
mysql = MySQLConnector(app, 'friendsdb')

# Home/Users page
@app.route('/')
def index():
    query = 'SELECT * FROM users;'
    users = mysql.query_db(query)

    return render_template('index.html', users=users)

# Add a new user page
@app.route('/add')
def add():
    return render_template('add.html')

# Process new user
@app.route('/create', methods=['POST'])
def create():
    return redirect('/')

# Edit a current user page
@app.route('/edit')
def edit():
    return render_template('edit.html')

# Show a current user page
@app.route('/user')
def user():
    return render_template('user.html')

app.run(debug=True)

# # # GET request to /users/new - calls the new method to display a form allowing
# #  users to create a new user. This will need a template.

# # # GET request /users/<id>/edit - calls the edit method to display a form 
# # allowing users to edit an existing user with the given id. This will need a 
# template.

# # # GET /users/<id> - calls the show method to display the info for a particular
# #  user with given id. This will need a template.

# # # POST to /users/create - calls the create method to insert a new user record
# # into our database. This POST should be sent from the form on the page 
# /users/new. Have this redirect to /users/<id> once created.

# # # GET /users/<id>/destroy - calls the destroy method to remove a particular 
# # user with the given id. Have this redirect back to /users once deleted.

# # # POST /users/<id> - calls the update method to process the submitted form
# #  sent from /users/<id>/edit. Have this redirect to /users/<id> once updated.

# # # Notice that for every form submission we use a POST method, while we're
# #  rendering our templates from get routes.