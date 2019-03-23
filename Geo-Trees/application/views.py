#~~~~~~~~~~~~~~~~~~~~~~~~~~~~‧͙⁺˚*･༓☾　　☽༓･*˚⁺‧͙~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Name: views.py                                                               #
#                                                                              #
# Defines the URLs used in the application.                                    #
# Nicole White February 2019                                                   #
#                                                                              #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~‧͙⁺˚*･༓☾　　☽༓･*˚⁺‧͙~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from application import app
from flask import render_template,jsonify, redirect, url_for, request, Markup
from .forms import *
from .models import *
import geoalchemy2,shapely
from geoalchemy2.shape import to_shape
from sqlalchemy import and_

from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

# URL arguments for the tree resource
tree_args = {'ward': fields.Int(required=False),
             'genus': fields.String(required=False),
             'health': fields.String(required=False),
             'owner': fields.String(required=False),
             'common_nane': fields.String(required=False),
             'ht_class': fields.Int(required=False),
             'family': fields.String(required=False),
             'division': fields.String(required=False),
             'oh_util': fields.String(required=False)}

# @app.route("/hey")
# @use_args(hello_args)
# def index(args):
#     return "Hello " + args["name"]

# Redirect to the geo-trees url
@app.route('/', methods=["GET"])
def home():
    return redirect(url_for('GeoTrees'))

# Redirect from the home url to the API's defined base url
# @app.route('/', methods=['GET'])
# def get_api():
# 	return redirect('/tree_inv/api/v0.1')

# The base url for the API
@app.route('/tree_inv/api/v0.1', methods=['GET'])
def get_endpoints():
	data= [{'name':"Tree", "endpoint":"/tree"},]
	return jsonify({"endpoints":data})

# Get all trees
@app.route('/tree_inv/api/v0.1/tree', methods=['GET'])
@use_kwargs(tree_args) # Inject the url arguments if there are any

def get_trees(**kwargs):
    results = (
    session.query(Tree)
    .join(Owner, Tree.owner == Owner.id)
    .join(HtClass, Tree.ht_class == HtClass.id)
    .join(Health, Tree.health == Health.id)
    .join(OHUtil, Tree.oh_util == OHUtil.id)
    .join(TreeTab, Tree.name == TreeTab.common_name)
    .join(CommonName, TreeTab.common_name == CommonName.id)
    .join(Genus, TreeTab.genus == Genus.id)
    .join(Family, Genus.family == Family.id)
    .join(Division, Family.division == Division.id)
    )

    # If ward has been specified, get only trees whose geometry falls within
    # that ward
    if 'ward' in kwargs.keys():
        ward = session.query(Ward).get(kwargs['ward'])
        results = results.filter(Tree.geom.ST_Intersects(ward.geom))

    if 'genus' in kwargs.keys():
        print('genus yes')
        results = results.filter(Genus.description == kwargs['genus'])

    if 'health' in kwargs.keys():
        results = results.filter(Health.description == kwargs['health'])

    if 'owner' in kwargs.keys():
        results = results.filter(Owner.description == kwargs['owner'])

    if 'common_name' in kwargs.keys():
        results = results.filter(CommonName.description == kwargs['common_name'])

    if 'ht_class' in kwargs.keys():
        results = results.filter(HtClass.id == kwargs['ht_class'])

    if 'family' in kwargs.keys():
        results = results.filter(Family.description == kwargs['family'])

    if 'division' in kwargs.keys():
        results = results.filter(Division.description == kwargs['division'])

    if 'oh_util' in kwargs.keys():
        results = results.filter(OHUtil.description == kwargs['oh_util'])

   # Combine the results of any filtering above
    results = results.all()

    # If results are returned from filtering, serve them in JSON form
    if results != None:
        data = [{"type": "Feature",
        "properties":{"name":item.name,
                      "id":item.tree_id,
                      },
        "geometry":{"type":"Point",
        "coordinates":[item.longitude, item.latitude]},
        } for item in results]
        return jsonify({"type": "FeatureCollection","features":data})


    # If no url arguments have been supplied, return the entire collection
    else:
        print('none')
        print(kwargs)
        results = session.query(Tree).all()

        data = [{"type": "Feature",
        "properties":{"name":results.name, "id":results.tree_id},
        "geometry":{"type":"Point",
        "coordinates":[results.longitude, results.latitude]},
        }  for tree in results]
        return jsonify({"type": "FeatureCollection","features":data})

# Get specific trees by genus
@app.route('/tree_inv/api/v0.1/genus/<genus>', methods=['GET'])
def get_trees_by_genus(genus):
    results = (
    session.query(Tree, TreeTab, CommonName, Genus, Species, Family, Division,
                  Owner, HtClass, Health, OHUtil)
    .join(Owner, Tree.owner == Owner.id)
    .join(HtClass, Tree.ht_class == HtClass.id)
    .join(Health, Tree.health == Health.id)
    .join(OHUtil, Tree.oh_util == OHUtil.id)
    .join(TreeTab, Tree.name == TreeTab.common_name)
    .join(CommonName, TreeTab.common_name == CommonName.id)
    .join(Genus, TreeTab.genus == Genus.id)
    .join(Family, Genus.family == Family.id)
    .join(Division, Family.division == Division.id)
    .filter(Genus.description == genus)
    .all()
    )

    data = [{"type": "Feature",
             "properties":{"Name":results[0].CommonName.description, "id":results[0].Tree.tree_id,
                           "Genus":results[0].Genus.description,
                           "Species":results[0].Species.description,
                           "Family":results[0].Family.description,
                           "Division":results[0].Division.description,
                           "Owner":results[0].Owner.description,
                           "HeightClass":results[0].HtClass.description,
                           "DBH":results[0].Tree.dbh,
                           "Health":results[0].Health.description,
                           "OverheadUtilities":results[0].OHUtil.description,
                           "Address":results[0].Tree.address,
                           "Comments":results[0].Tree.comments},
             "geometry":{"type":"Point",
                         "coordinates":[results[0].Tree.longitude,
                                        results[0].Tree.latitude]},
             } for item in results]
    return jsonify({"type": "FeatureCollection","features":data})

# Get specific tree by ID number
@app.route('/tree_inv/api/v0.1/tree/<int:tree_id>', methods=['GET'])
def get_tree(tree_id):

    # Join technique from https://stackoverflow.com/questions/20357540/
    # how-do-i-return-results-from-both-tables-in-a-sqlalchemy-join

    results = (
    session.query(Tree, TreeTab, CommonName, Genus, Species, Family, Division,
                  Owner, HtClass, Health, OHUtil)
                  .join(Owner, Tree.owner == Owner.id)
                  .join(HtClass, Tree.ht_class == HtClass.id)
                  .join(Health, Tree.health == Health.id)
                  .join(OHUtil, Tree.oh_util == OHUtil.id)
                  .join(TreeTab, Tree.name == TreeTab.common_name)
                  .join(CommonName, TreeTab.common_name == CommonName.id)
                  .join(Genus, TreeTab.genus == Genus.id)
                  .join(Species, TreeTab.species == Species.id)
                  .join(Family, Genus.family == Family.id)
                  .join(Division, Family.division == Division.id)
                  .filter(Tree.tree_id == tree_id)
                  .first()
              )


    if results.Tree != None:
        data = [{"type": "Feature",
        "properties":{"Name":results.CommonName.description, "id":results.Tree.tree_id,
                      "Genus":results.Genus.description,
                      "Species":results.Species.description,
                      "Family":results.Family.description,
                      "Division":results.Division.description,
                      "Owner":results.Owner.description,
                      "HeightClass":results.HtClass.description,
                      "DBH":results.Tree.dbh,
                      "Health":results.Health.description,
                      "OverheadUtilities":results.OHUtil.description,
                      "Address":results.Tree.address,
                      "Comments":results.Tree.comments},
        "geometry":{"type":"Point",
        "coordinates":[round(results.Tree.longitude,6), round(results.Tree.latitude,6)]},
        }]
    else:
        data = []
    return jsonify({"type": "FeatureCollection","features":data})

# Return all trees within specific ward
@app.route('/tree_inv/api/v0.1/ward/<int:ward_num>')
def ward_intersect(ward_num):
    ward = session.query(Ward).get(ward_num)
    trees = session.query(Tree).filter(Tree.geom.ST_Intersects(ward.geom)).all()
    print(trees)

    if trees != None:
    	data = [{"type": "Feature",
    	"properties":{"name":tree.name, "id":tree.tree_id},
    	"geometry":{"type":"Point",
    	"coordinates":[tree.longitude, tree.latitude]},
    	}  for tree in trees]
    	return jsonify({"type": "FeatureCollection","features":data})
    else:
        data = []
    return jsonify({"type": "FeatureCollection", "features":data})


# @app.route('/tree_inv', methods=["GET","POST"])
# def GeoTrees():
#     form = TreeForm(request.form)
#
#     return render_template('index.html', form=form)


@app.route('/tree_inv', methods=["GET","POST"])
def GeoTrees():
    form = TreeForm(request.form)
    genuses = session.query(Genus).all()
    health_choices = session.query(Health).all()
    oh_choices = session.query(OHUtil).all()
    form.select_genus.choices = [("", "---")] + [(genus.description, genus.description) for genus in genuses]
    form.select_health.choices = [("", "---")] + [(item.description, item.description) for item in health_choices]
    form.select_oh.choices = [("", "---")] + [(item.description, item.description) for item in oh_choices]

    if request.method == "POST":
        genus_id = form.select_genus.data
        health_id = form.select_health.data
        oh_id = form.select_oh.data


        return render_template('index.html',form=form, genus_id=genus_id,
                                health_id=health_id, oh_id=oh_id)

    return render_template('index.html',form=form)
