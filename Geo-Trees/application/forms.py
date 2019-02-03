#~~~~~~~~~~~~~~~~~~~~~~~~~~~~‧͙⁺˚*･༓☾　　☽༓･*˚⁺‧͙~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Name: forms.py                                                               #
#                                                                              #
# Defines the forms used in the application.                                   #
# Nicole White February 2019                                                   #
#                                                                              #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~‧͙⁺˚*･༓☾　　☽༓･*˚⁺‧͙~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


from flask_wtf import FlaskForm
from wtforms import SelectField

class TreeForm(FlaskForm):
    description  = "Use the dropdown to select a tree."
    selections = SelectField('Select a Tree',choices=[])
