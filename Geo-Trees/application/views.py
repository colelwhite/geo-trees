#~~~~~~~~~~~~~~~~~~~~~~~~~~~~‧͙⁺˚*･༓☾　　☽༓･*˚⁺‧͙~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Name: views.py                                                               #
#                                                                              #
# Defines the URLs used in the application.                                    #
# Nicole White February 2019                                                   #
#                                                                              #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~‧͙⁺˚*･༓☾　　☽༓･*˚⁺‧͙~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from application import app
from flask import render_template,jsonify, redirect, url_for, request
from .forms import *
from .models import *

# Redirect to the geo-trees url
@app.route('/', methods=["GET"])
def home():
    return redirect(url_for('GeoTrees'))

# Deal with queries from the form

@app.route('/geo-trees', methods=["GET","POST"])
def GeoTrees():
    form = TreeForm(request.form)

    trees = session.query(Tree).all()
    form.selections.choices = [(tree.tree_id, tree.name) for tree in trees]
    form.popup = "Select a Tree"
    form.latitude = 43.541115
    form.longitude = -80.247028

    if request.method == "POST":

        tree_id = form.selections.data
        tree = session.query(Tree).get(tree_id)
        form.longitude = round(tree.longitude,4)
        form.latitude = round(tree.latitude,4)

        ward = session.query(Ward).filter(Ward.geom.ST_Contains(tree.geom)).first()
        if ward != None:
            form.popup = "The {0} is located at {2}, {3}, which is in {1} ward.".format(tree.name, ward.ward_num, form.longitude, form.latitude)
        else:
            form.popup = "The ward couldn't be located using point in polygon analysis"


        return render_template('index.html',form=form)
    return render_template('index.html',form=form)
