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

conn_string = 'postgresql://postgres:postgres@localhost:5433/guelph_tree'
app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
app.config['SECRET_KEY'] = '6xvPzkqdpM9VaiCA0cqN'
app.config['DEBUG'] = True

import application.views
