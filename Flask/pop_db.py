#------------------------------------------------------------------------------
# Name: pop_db.py
#
#  create_db.py should be run first.
#  Add spatial (shp) and tabular (csv) data.
# Nicole White January 2019
#
#------------------------------------------------------------------------------

import csv # for csv import
import os

# The pyshapefile module is used to read shapefiles and
# the pygeoif module is used to convert between geometry types
import shapefile
import pygeoif

# The database connections and session management are managed with
# SQLAlchemy functions
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

# The Geometry columns of the data tables are added to the ORM using the
# Geometry data type
from geoalchemy2 import Geometry

# The built-in Tkinter GUI module allows for file dialogs
from tkinter import filedialog
from tkinter import Tk

# Connect to the database called chapter11 using SQLAlchemy functions
conn_string = 'postgresql://postgres:word@localhost:5432/guelph_tree'
engine = create_engine(conn_string, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()



# Speces: tree species LUT

class OHUtil(Base):
    __tablename__ = 'oh_util'

    id = Column(Integer, primary_key=True, autoincrement=False)
    description = Column(String)

class HtClass(Base):
    __tablename__ = 'ht_class'

    id = Column(Integer, primary_key=True, autoincrement=False)

    description = Column(String)

class Owner(Base):
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True, autoincrement=False)
    description = Column(String)

class Health(Base):
    __tablename__ = 'health'

    id = Column(Integer, primary_key=True, autoincrement=False)
    description = Column(String)

class Division(Base):
    __tablename__ = 'division'
    id = Column(Integer, primary_key=True, autoincrement=False)
    description = Column(String)

class Family(Base):
    __tablename__ = 'family'
    id = Column(Integer, primary_key=True, autoincrement=False)
    description = Column(String)

    division = Column(Integer, ForeignKey('division.id'))
    division_ref = relationship("Division", backref='family')

class Genus(Base):
    __tablename__ = 'genus'
    id = Column(Integer, primary_key=True, autoincrement=False)
    description = Column(String)
    family = Column(Integer, ForeignKey('family.id'))
    family_ref = relationship("Family", backref='genus')

class CommonName(Base):
    __tablename__ = 'common_name'
    id = Column(Integer, primary_key=True, autoincrement=False)
    description = Column(String)

class Species(Base):
    __tablename__ = 'species'
    id = Column(Integer, primary_key=True, autoincrement=False)
    description = Column(String)

class TreeTab(Base):
    __tablename__ = 'tree_tab'
    common_name = Column(Integer, ForeignKey('common_name.id'), primary_key=True, autoincrement=False)
    common_name_ref = relationship("CommonName", backref='tree_tab')

    genus = Column(Integer, ForeignKey('genus.id'))
    genus_ref = relationship("Genus", backref='tree_tab')

    species = Column(Integer, ForeignKey('species.id'))
    species_ref = relationship("Species", backref='tree_tab')

# Tree: Point spatial layer of tree locations, attributes including FKs
class Tree(Base):
    __tablename__ = 'tree'

    tree_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(Integer, ForeignKey('tree_tab.common_name'))
    name_ref = relationship("TreeTab", backref='tree')

    health = Column(Integer, ForeignKey('health.id'))
    health_ref = relationship("Health", backref='tree')

    owner = Column(Integer, ForeignKey('owner.id'))
    owner_ref = relationship("Owner", backref='tree')

    ht_class = Column(Integer, ForeignKey('ht_class.id'))
    ht_class_ref = relationship("HtClass", backref='tree')

    dbh = Column(Integer)

    address = Column(String)

    oh_util = Column(Integer, ForeignKey('oh_util.id'))
    oh_ref = relationship("OHUtil", backref='tree')

    comments = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))

# Initiate the Tkinter module and withdraw the console it generates
root = Tk()
root.withdraw()

treefile = "D:\\Winter2019\\Elective\\Project\\data2\\db_geometries\\tree_sample_2000.shp"

htfile = "D:\\Winter2019\\Elective\\Project\\data2\\db_tables\\ht_class.csv"
tabfile = "D:\\Winter2019\\Elective\\Project\\data2\\db_tables\\treeta2.csv"
ownerfile = "D:\\Winter2019\\Elective\\Project\\data2\\db_tables\\owner.csv"
healthfile = "D:\\Winter2019\\Elective\\Project\\data2\\db_tables\\health.csv"
ohfile = "D:\\Winter2019\\Elective\\Project\\data2\\db_tables\\oh_util.csv"
genfile = "D:\\Winter2019\\Elective\\Project\\data2\\db_tables\\genus.csv"
famfile = "D:\\Winter2019\\Elective\\Project\\data2\\db_tables\\family.csv"
divfile = "D:\\Winter2019\\Elective\\Project\\data2\\db_tables\\division.csv"
comfile = "D:\\Winter2019\\Elective\\Project\\data2\\db_tables\\common.csv"
spfile = "D:\\Winter2019\\Elective\\Project\\data2\\db_tables\\species.csv"
# # Use file dialog to get the needed files
# root.treefile = filedialog.askopenfilename(initialdir = filedir,
#                                          title = "Select tree shapefile",
#                                          filetypes = (("shapefiles", "*.shp"),
#                                                        ("all files", "*.*")))
#
# root.treetabfile = filedialog.askopenfilename(initialdir = filedir,
#                                          title = "Select treetab LUT",
#                                          filetypes = (("dbf", "*.dbf"),
#                                                        ("all files", "*.*")))
#
# root.commonfile = filedialog.askopenfilename(initialdir = filedir,
#                                          title = "Select common name LUT",
#                                          filetypes = (("dbf", "*.dbf"),
#                                                        ("all files", "*.*")))
#
# root.genusfile = filedialog.askopenfilename(initialdir = filedir,
#                                          title = "Select genus LUT",
#                                          filetypes = (("csv", "*.csv"),
#                                                        ("all files", "*.*")))
#
# root.familyfile = filedialog.askopenfilename(initialdir = filedir,
#                                          title = "Select family LUT",
#                                          filetypes = (("csv", "*.csv"),
#                                                        ("all files", "*.*")))
#
# root.divisionfile = filedialog.askopenfilename(initialdir = filedir,
#                                          title = "Select division LUT",
#                                          filetypes = (("csv", "*.csv"),
#                                                        ("all files", "*.*")))
# root.healthfile = filedialog.askopenfilename(initialdir = filedir,
#                                          title = "Select health LUT",
#                                          filetypes = (("csv", "*.csv"),
#                                                        ("all files", "*.*")))
# root.htclassfile = filedialog.askopenfilename(initialdir = filedir,
#                                          title = "Select height class LUT",
#                                          filetypes = (("csv", "*.csv"),
#                                                        ("all files", "*.*")))
# root.ownerfile = filedialog.askopenfilename(initialdir = filedir,
#                                          title = "Select owner LUT",
#                                          filetypes = (("csv", "*.csv"),
#                                                        ("all files", "*.*")))
#
# root.ohutilfile = filedialog.askopenfilename(initialdir = filedir,
#                                          title = "Select oh util LUT",
#                                          filetypes = (("csv", "*.csv"),
#                                                        ("all files", "*.*")))


# Read the tree shapefile using the Reader class of the pyshp module
tree_shapefile = shapefile.Reader(treefile)
tree_shapes = tree_shapefile.shapes()
tree_records = tree_shapefile.records()


# Read the csvs
with open(spfile, newline='') as csvfile:
    myreader = csv.reader(csvfile)
    sp_records = [row for row in myreader]
    sp_records.pop(0)

with open(comfile, newline='') as csvfile:
    myreader = csv.reader(csvfile)
    com_records = [row for row in myreader]
    com_records.pop(0)

with open(divfile, newline='') as csvfile:
    myreader = csv.reader(csvfile)
    div_records = [row for row in myreader]
    div_records.pop(0)

with open(famfile, newline='') as csvfile:
    myreader = csv.reader(csvfile)
    fam_records = [row for row in myreader]
    fam_records.pop(0)

with open(genfile, newline='') as csvfile:
    myreader = csv.reader(csvfile)
    gen_records = [row for row in myreader]
    gen_records.pop(0)

with open(tabfile, newline='') as csvfile:
    myreader = csv.reader(csvfile)
    tab_records = [row for row in myreader]
    tab_records.pop(0)

with open(htfile, newline='') as csvfile:
    myreader = csv.reader(csvfile)
    ht_records = [row for row in myreader]
    ht_records.pop(0)

with open(ownerfile, newline='') as csvfile:
    myreader = csv.reader(csvfile)
    owner_records = [row for row in myreader]
    owner_records.pop(0)

with open(healthfile, newline='') as csvfile:
    myreader = csv.reader(csvfile)
    health_records = [row for row in myreader]
    health_records.pop(0)

with open(ohfile, newline='') as csvfile:
    myreader = csv.reader(csvfile)
    oh_records = [row for row in myreader]
    oh_records.pop(0)

# Populate the DB tables

for count, record in enumerate(sp_records):
    sp = Species()
    sp.id = record[0]
    sp.description = record[1]
    session.add(sp)
session.commit()

for count, record in enumerate(com_records):
    com = CommonName()
    com.id = record[0]
    com.description = record[1]
    session.add(com)
session.commit()

for count, record in enumerate(div_records):
    div = Division()
    div.id = record[0]
    div.description = record[1]
    session.add(div)
session.commit()

for count, record in enumerate(fam_records):
    fam = Family()
    fam.id = record[0]
    fam.description = record[1]
    fam.division = record[2]
    session.add(fam)
session.commit()

for count, record in enumerate(gen_records):
    gen = Genus()
    gen.id = record[0]
    gen.description = record[1]
    gen.family = record[2]
    session.add(gen)
session.commit()

for count, record in enumerate(oh_records):
    oh = OHUtil()
    oh.id = record[0]
    oh.description = record[1]
    session.add(oh)
session.commit()

for count, record in enumerate(health_records):
    hlth = Health()
    hlth.id = record[0]
    hlth.description = record[1]
    session.add(hlth)
session.commit()

for count, record in enumerate(owner_records):
    ownr = Owner()
    ownr.id = record[0]
    ownr.description = record[1]
    session.add(ownr)
session.commit()

for count, record in enumerate(ht_records):
    ht = HtClass()
    ht.id = record[0]
    ht.description = record[1]
    session.add(ht)
session.commit()

for count, record in enumerate(tab_records):
    tab = TreeTab()
    tab.common_name = record[0]
    tab.genus = record[1]
    tab.species = record[2]
    session.add(tab)
session.commit()

# Iterate through tree
for count, record in enumerate(tree_records):
    # Instantiate an tree from the Tree class and populate the fields
    tree = Tree()
    tree.address = record[6]
    print(tree.address)

    # Get the geometry and insert as WKT. Populate other attribute values
    # from the shp's attribute table.
    point = tree_shapes[count].points[0]
    tree.longitude = float(point[0])
    tree.latitude = float(point[1])
    tree.tree_id = record[0]
    tree.name = record[1]
    tree.health = record[2]
    tree.owner = record[3]
    tree.ht_class = record[4]
    tree.dbh = record[5]
    tree.oh_util = record[7]
    tree.comments = record[8]
    tree.geom = 'SRID=4326;POINT({0} {1})'.format(tree.longitude, tree.latitude)
    session.add(tree)

    # There are a large number of records. Commit every 10 records for
    # better efficiency
    if count % 10 == 0:
        session.commit()
session.commit()
#



#
# # Close the session and dispose of the engine connection to the database
session.close()
engine.dispose()
