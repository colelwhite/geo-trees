#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Name: __init__.py                                                            #
#                                                                              #
# Makes the application folder an importable Python module and sets up the     #
# database connection                                                          #
# Nicole White February 2019                                                   #
#                                                                              #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import flask
app = flask.Flask(__name__)

conn_string = 'postgresql://user:password@ip:port/db'
app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = False

import application.views
