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

from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

# URL arguments for the tree resource
tree_args = {"ward": fields.Int(required=False),
             "genus": fields.String(required=False)}

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

    # If ward has been specified, get only trees whose geometry falls within
    # that ward
    if 'ward' in kwargs.keys():
        ward = session.query(Ward).get(kwargs['ward'])
        filtr = Tree.geom.ST_Intersects(ward.geom)
        print(filtr)
        trees = session.query(Tree).filter(filtr).all()

    if 'genus' in kwargs.keys():
        print('genus yes')

        genus = (
        session.query(Genus)
        .filter(Genus.description == kwargs['genus'])
        )

        f = Genus.description == kwargs['genus']

        trees = (
        session.query(Tree)
        .join(TreeTab, Tree.name == TreeTab.common_name)
        .join(Genus, TreeTab.genus == Genus.id)
        .filter(f).all()
        )

    if trees != None:
    	data = [{"type": "Feature",
    	"properties":{"name":tree.name, "id":tree.tree_id},
    	"geometry":{"type":"Point",
    	"coordinates":[tree.longitude, tree.latitude]},
    	}  for tree in trees]
    	return jsonify({"type": "FeatureCollection","features":data})

    # If no url arguments have been supplied, return the entire collection
    else:
        print('none')
        print(kwargs)
        trees = session.query(Tree).all()

        data = [{"type": "Feature",
        "properties":{"name":tree.name, "id":tree.tree_id},
        "geometry":{"type":"Point",
        "coordinates":[tree.longitude, tree.latitude]},
        }  for tree in trees]
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

# Fix me - not returning correct lat and long
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


@app.route('/geo-trees', methods=["GET","POST"])
def GeoTrees():
    # form = TreeForm(request.form)

    return render_template('index.html')


# @app.route('/geo-trees', methods=["GET","POST"])
# def GeoTrees():
#     form = TreeForm(request.form)
#
#     trees = session.query(Tree).all()
#     genuses = session.query(Genus).all()
#     tt = session.query(TreeTab).all()
#     common_name = session.query(CommonName).all()
#
#     form.selections.choices = [(genus.id, genus.description) for genus in genuses]
#     form.popup = "Select a Tree"
#     form.latitude = 43.541115
#     form.longitude = -80.247028
#
#     if request.method == "POST":
#
#         genus_id = form.selections.data
#
#
#        # Query all trees of the selected genus
#         q = (session.query(Genus,TreeTab,CommonName,Tree)
#         .filter(Genus.id == TreeTab.genus)
#         .filter(TreeTab.common_name == Tree.name)
#         .filter(CommonName.id == TreeTab.common_name)
#         .filter(Genus.id == genus_id)
#         .all())
#
#         tree_pts = []
#         tree_popup = []
#
#         # Loop through the results and get the lat and long of each tree
#         for j, result in enumerate(q):
#             common_name = result[2]
#             tree = result[3]
#             print(common_name.description)
#             print(tree.latitude, tree.longitude)
#
#             tree_pts.append(tree)
#
#             if tree != None:
#                 # form.longitude = round(tree.longitude,4)
#                 # form.latitude = round(tree.latitude,4)
#
#                 ward = session.query(Ward).filter(Ward.geom.ST_Contains(tree.geom)).first()
#                 if ward != None:
#                     tree_popup.append('{0} located at {2}, {3}, in Ward {1}.'.format(common_name.description, ward.ward_num, tree.longitude, tree.latitude))
#                 else:
#                     tree_popup.append('{0} located at {1}, {2}'.format(common_name.description, tree.longitude, tree.latitude))
#
#
#         return render_template('index.html',form=form, tree_pts=tree_pts, tree_popup=tree_popup)
#     return render_template('index.html',form=form)
