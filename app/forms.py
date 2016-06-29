from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class MyForm(Form):
    name = StringField('Name', description='Name',
                       validators=[DataRequired(message="You're not listening, are you?")])


class WanderingForm(Form):
    person_number = IntegerField('Persons', description='Number of persons',
                                 validators=[NumberRange(min=1, max=4, message="Insert the number of persons: 1-4")])
    budget_available = IntegerField('Budget Available', description='Budget available ($)',
                                    validators=[NumberRange(min=100,
                                                            max=1000000,
                                                            message="Insert the budget for this trip 100-1000000 $")])