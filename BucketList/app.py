import os
from flask import (Flask, render_template, url_for,
                   redirect, request, session)

from activity import Activity
from bucketlist import BucketList
from user import User
from flask_sqlalchemy import SQLAlchemy

users = {}

# get current app directory
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# define SQLAlchemy URL, a configuration parameter
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# The db object instantiated from the class SQLAlchemy represents the database and
# provides access to all the functionality of Flask-SQLAlchemy.
db = SQLAlchemy(app)


current_bucketlist = None


class Accounts(db.Model):
    # __tablename__ class variable defines the name of the table in the database
    __tablename__ = 'accounts'
    # first column is named 'userName'
    # possible second parameters:
    # primary_key If set to True , the column is the table’s primary key
    # unique If set to True , do not allow duplicate values for this column
    # index If set to True , create an index for this column, so that queries are more efficient
    # nullable If set to True , allow empty values for this column. If set to False , the column will not allow null values
    # default Define a default value for the column
    userName = db.Column(db.String(255), primary_key=True, nullable=False)
    # second column is named 'password'
    pwd = db.Column(db.String(255), nullable=False)
    # define defines the reverse direction of the relationship, by adding a role attribute to the User model
    # This attribute can be used on any instance of User instead of the role_id foreign key to access the Role model as an object.
    mail = db.Column(db.String(255), nullable=False)
    # give them a readable string representation that can be used for debugging and testing purposes
    activity = db.relationship('BuckList', backref='accounts.userName')
    def __repr__(self):
        return '<Account %r>' % self.userName

class BuckList(db.Model):
    __tablename__ = 'bucketList'
    title = db.Column(db.String(511), primary_key=True)
    descript = db.Column(db.String(1023), unique=True, index=True)
    account = db.Column(db.String(255), db.ForeignKey('accounts.userName'))

    def __repr__(self):
        return '<Bucket list: %r>' % self.title


@app.route('/', methods=['GET', 'POST'])	
@app.route('/login', methods=['POST', 'GET'])
def login():
    ''' logs in a registered user '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = None

        if username in users.keys():
            user = users[username]
            if password == user.password:
                session['user'] = {'username':user.username, 'email':user.email}

                return render_template('addlists.html', bucketlists=user.bucketlists)
            else:
                return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    ''' registers a new user if the signup form is posted '''
    if request.method == 'POST':
        details = request.form
        username = details['username']
        email = details['email']
        password = details['password']
        confirm_password = details['confirm_password']

        if password == confirm_password:
            user = User(username, email, password)
            users[username] = user

            session['user'] = {'username': username, 'email': email}

            # locates all the subclasses of db.Model and creates corresponding tables in the database for them
            # brute-force solution to avoid updating existing database tables to a different schema
            #db.drop_all()
            #db.create_all()
            # insert rows
            new_account = Accounts(userName=username, pwd=password, mail=email)
            # commit changes:
            db.session.add_all([new_account])
            db.session.commit()
            print(Accounts.query.all())
            return redirect(url_for('add_bucketlist', user=session['user']['username']))

        else:
            return redirect(url_for('signup'))
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    ''' logs out user and redirects to login page '''
    session.clear()

    return redirect(url_for('login'))

@app.route('/add_bucketlist', methods=['POST', 'GET'])
def add_bucketlist():
    ''' creates a new bucketlist and adds it to user's bucketlists property '''
    if request.method == 'POST':
        name = request.form['title']
        description = request.form['description']
        user = None
        username = session['user']['username']

        if username in users.keys():
            user = users[username]
            user.bucketlists[name] = BucketList(name, description)

            # insert rows
            new_bucketList = BuckList(title=name, descript=description, account=username)
            # since now admin_role.id will be none because the changes are not committed
            # commit changes:
            db.session.add_all([new_bucketList])
            db.session.commit()
            print(Accounts.query.all())

        return render_template('addlists.html', bucketlists=user.bucketlists)
    else:
        username = session['user']['username']
        return render_template('addlists.html', username=username)

@app.route('/delete_bucketlist/<name>', methods=['GET'])
def delete_bucketlist(name):
    ''' delete bucketlist given a name '''
    username = session['user']['username']

    user = None

    if username in users.keys():
        user = users[username]
        if name in user.bucketlists.keys():
            del user.bucketlists[name]

    return render_template('addlists.html', bucketlists=user.bucketlists)

@app.route('/back_to_bucketlists', methods=['GET'])
def back_to_bucketlists():
    user = None
    username = session['user']['username']

    if username in users.keys():
        user = users[username]

        return render_template('addlists.html', bucketlists=user.bucketlists)

@app.route('/update_bucket', methods=['POST', 'GET'])
def update_bucket():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        user = None
        username = session['user']['username']

        if username in users.keys():
            user = users[username]
            user.bucketlists[name] = BucketList(name, description)

        return render_template('addlists.html', bucketlists=user.bucketlists)

    else:
        return render_template('update_bucketlist.html')

@app.route('/update_bucketlist/<name>/<description>', methods=['POST', 'GET'])
def update_bucketlist(name, description):
    username = session['user']['username']

    user = None

    if username in users.keys():
        user = users[username]
        if name in user.bucketlists.keys():
            del user.bucketlists[name]

    return redirect(url_for('update_bucket', name=name, description=description))

@app.route('/update_activity/<name>/<title>/<description>', methods=['POST', 'GET'])
def update_activity(name, title, description):
    username = session['user']['username']

    user = None

    if username in users.keys():
        user = users[username]
        if name in user.bucketlists.keys():
            for i in range(len(user.bucketlists[name].activities)):
                if user.bucketlists[name].activities[i].title == title:
                    user.bucketlists[name].activities.pop(i)
                    break

    return redirect(url_for('updt_act', name=name, title=title, description=description))

@app.route('/updt_act', methods=['POST', 'GET'])
def updt_act():    
    user = None
    username = session['user']['username']

    if username in users.keys():
        user = users[username]

    current_bucketlist = request.args.get('name')

    if request.method == 'POST':
        current_bucketlist = request.form['name']

        title = request.form['title']
        description = request.form['description']

        activity = Activity(title, description)

        if current_bucketlist in user.bucketlists.keys():
            user.bucketlists[current_bucketlist].add_activity(activity)

        activities = user.bucketlists[current_bucketlist].activities

        return render_template('bucketlist.html',
                               bucketlist=current_bucketlist,
                               activities=activities)
    else:
        return render_template('update_activity.html', name=current_bucketlist)

@app.route('/add_activity', methods=['POST', 'GET'])
def add_activity_to_bucketlist():
    ''' Add activity to named bucketlist '''
    user = None
    username = session['user']['username']

    if username in users.keys():
        user = users[username]

    current_bucketlist = request.args.get('name')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']


        activity = Activity(title, description)

        if current_bucketlist in user.bucketlists.keys():
            user.bucketlists[current_bucketlist].add_activity(activity)

        activities = user.bucketlists[current_bucketlist].activities

        return render_template('bucketlist.html',
                               name=current_bucketlist,
                               activities=activities)
    else:
        return render_template('bucketlist.html', name=current_bucketlist,
                               activities=user.bucketlists[current_bucketlist].activities)

@app.route('/delete_activity/<name>/<title>', methods=['GET'])
def delete_activity(name, title):
    ''' delete an activity given a name '''
    username = session['user']['username']

    user = None

    if username in users.keys():
        user = users[username]

    for i in range(len(user.bucketlists[name].activities)):
        if user.bucketlists[name].activities[i].title == title:
            user.bucketlists[name].activities.pop(i)

            return redirect(url_for('add_activity_to_bucketlist',
                                    name=user.bucketlists[name].name,
                                    activities=user.bucketlists[name].activities))

#if __name__ == '__main__':
app.secret_key = 'xcxcyuxcyuxcyuxcyxuee'

app.run(debug=True)# host='127.0.0.1')
