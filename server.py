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
    query = 'SELECT * FROM users;'
    users = mysql.query_db(query)

    return render_template('add.html', users=users)


# Process new user
@app.route('/create', methods=['POST'])
def create():
    # Gather form information 
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    # print first_name, last_name, email

    query = 'INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, now(), now());' 
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }   
    mysql.query_db(query,data)
    return redirect('/')

# Edit a current user page
@app.route('/<users_id>/edit')
def edit(users_id):
    # Query to show which user to edit
    query = 'SELECT * FROM users WHERE id = :users_id;'
    data = {
        'users_id': users_id
    }
    user = mysql.query_db(query, data)
    print user
    return render_template('edit.html', user=user)

# View/Process changes to current user
@app.route('/<users_id>', methods=['POST', 'GET'])
def modify(users_id):
    # print users_id
    query = 'SELECT * FROM users WHERE id = :users_id;'
    data = {
        'users_id': users_id
    }
    user = mysql.query_db(query, data) 
    created = user[0]['created_at'].strftime('%B %d, %Y')

    if request.form:
        # Simple validation of data received from form
        errors = False
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        if first_name == '':
            flash('First Name field is empty')
            errors = True
        if last_name == '':
            flash('Last Name field is empty')
            errors = True
        if email == '':
            flash('Email field is empty')
            errors = True
        if errors == True:
            return redirect('/'+users_id+'/edit')

        query = 'UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :users_id;'
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'users_id': users_id
        }
        mysql.query_db(query, data)
        return redirect('/'+users_id)
    else:
        return render_template('user.html', user=user, created=created)

@app.route('/<users_id>/destroy')
def delete(users_id):

    query = 'DELETE FROM users WHERE id = :users_id'
    data = {
        'users_id': users_id
    }
    mysql.query_db(query,data)

    return redirect('/')



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