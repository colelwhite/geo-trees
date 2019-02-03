#~~~~~~~~~~~~~~~~~~~~~~~~~~~~‧͙⁺˚*･༓☾　　☽༓･*˚⁺‧͙~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Name: models.py                                                              #
#                                                                              #
# Defines the data models (Postgres tables) to be used in the application.     #
# Nicole White February 2019                                                   #
#                                                                              #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~‧͙⁺˚*･༓☾　　☽༓･*˚⁺‧͙~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from application import app                  # The Flask application

from sqlalchemy import create_engine         # Manage PostgreSQL session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from geoalchemy2 import Geometry            # Process geom columns

# Connect to the database called chapter11 using SQLAlchemy functions
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

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

class CityBound(Base):
    __tablename__ = 'city_bound'
    id = Column(Integer, primary_key=True)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))

class Ward(Base):
    __tablename__ = 'ward'
    ward_num = Column(Integer, primary_key=True, autoincrement=False)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))

class NeighbourhoodGroup(Base):
    __tablename__ = 'neighbourhood_group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))

class Street(Base):
    __tablename__ = 'street'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326))

class WaterCourse(Base):
    __tablename__ = 'water_course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326))
