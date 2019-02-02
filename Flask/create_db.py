#~~~~~~~~~~~~~~~~~~~~~~~~~~~‧͙⁺˚*･༓☾　　☽༓･*˚⁺‧͙~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Name: create_db.py
#
# Create new PostgreSQL DB with the PostGIS extension. Create models to hold
# the data, based on the schema design in PostgreSQL DB Documentation.xlsx.
#  Next, add spatial (shp) and tabular (csv) data using pop_db.py
# Nicole White January 2019
#
#~~~~~~~~~~~~~~~~~~~~~‧͙⁺˚*･༓☾　　☽༓･*˚⁺‧͙~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

# Define the DB
engine = create_engine('postgresql://postgres:password@localhost:5432/guelph_tree',
               echo=True)

# If the DB needs to be dropped and re-created (otherwise leave commented
# out):
drop_database(engine.url)

# Only run the script if the database doesn't exist
if not database_exists(engine.url):
    create_database(engine.url)

    # Add PostGIS
    conn = engine.connect()
    conn.execute("commit")
    try:
        conn.execute("CREATE EXTENSION postgis")
    except Exception as e:
        print(e)
        print("extension postgis already exists")
    conn.close()

    # Construct data models using sqlalchemy's declarative_base function
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

    # Make the DB tables from the models created above. If the tables already
    # exist, drop them and recreate them.
    # These tables can be created all in one go with the following command:
    Base.metadata.create_all(engine)
    #
    # try:
    #     OHUtil.__table__.create(engine)
    # except:
    #     OHUtil.__table__.drop(engine)
    #     OHUtil.__table__.create(engine)
    #
    # try:
    #     Owner.__table__.create(engine)
    # except:
    #     Owner.__table__.drop(engine)
    #     Owner.__table__.create(engine)
    #
    # try:
    #     HeightClass.__table__.create(engine)
    # except:
    #     HeightClass.__table__.drop(engine)
    #     HeightClass.__table__.create(engine)
    #
    # try:
    #     Health.__table__.create(engine)
    # except:
    #     Health.__table__.drop(engine)
    #     Health.__table__.create(engine)
    #
    # try:
    #     Division.__table__.create(engine)
    # except:
    #     Division.__table__.drop(engine)
    #     Division.__table__.create(engine)
    #
    # try:
    #     Family.__table__.create(engine)
    # except:
    #     Family.__table__.drop(engine)
    #     Family.__table__.create(engine)
    #
    # try:
    #     Species.__table__.create(engine)
    # except:
    #     Species.__table__.drop(engine)
    #     Species.__table__.create(engine)
    #
    # try:
    #     Genus.__table__.create(engine)
    # except:
    #     Genus.__table__.drop(engine)
    #     Genus.__table__.create(engine)
    #
    # try:
    #     Common.__table__.create(engine)
    # except:
    #     Common.__table__.drop(engine)
    #     Common.__table__.create(engine)
    #
    # try:
    #     TreeTab.__table__.create(engine)
    # except:
    #     TreeTab.__table__.drop(engine)
    #     TreeTab.__table__.create(engine)
    #
    # try:
    #     Tree.__table__.create(engine)
    # except:
    #     Tree.__table__.drop(engine)
    #     Tree.__table__.create(engine)
