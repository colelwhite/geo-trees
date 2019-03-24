#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Name: forms.py                                                               #
#                                                                              #
# Defines the forms used in the application.                                   #
# Nicole White February 2019                                                   #
#                                                                              #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


from flask_wtf import FlaskForm
from wtforms import widgets, SelectField, SelectMultipleField



class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class TreeForm(FlaskForm):
    description  = "Use the form below to filter results:"
    select_genus = SelectField('Select a genus',choices=[], default=("", "---"))
    select_health = SelectField('Select health status', choices = [], default=("", "---"))
    select_oh = SelectField('Overhead utilities', choices = [], default=("", "---"))
