# bucket-list-app

[![Build Status](https://travis-ci.org/mkiterian/bucket-list-app.svg?branch=master)](https://travis-ci.org/mkiterian/bucket-list-app)

[![Coverage Status](https://coveralls.io/repos/github/mkiterian/bucket-list-app/badge.svg?branch=master)](https://coveralls.io/github/mkiterian/bucket-list-app?branch=master)

**Installation**

- Clone the repo to your local file system

- Install python 3 if not available

- Use the requirements file to install the dependencies. (pip could be
  used as such: pip install -r requirements.txt --no-index --find-links
  file:///local)

- With these setup, the app can be from the terminal by running python
  app.py from the file directory which starts the flask server

- The app can then be accessed from a web browser e.g to access the signup page use the url http://127.0.0.1:5000/signup

  **Usage**
  Users can sign up by inputting a username, email, password and confirmation password (all fields are required)
  Once signed up the user is redirected to the manage bucketlists page where they can create a bucket list by giving it a name and description
  A link is created for each bucketlist page
  A bucketlist can be deleted by clicking on a delete button next to it
  By clicking the link to a bucketlist, the user is redirected to a page where they can add activities for that particular bucketlist
  The user can add activities by clicking on the add activity button and entering a name and description
  To logout the user clicks on the logout button on the top right of the page