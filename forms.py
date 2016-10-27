from flask_wtf import Form
from wtforms import SubmitField, SelectField


class ChooseModel(Form):
    model = SelectField('models', choices=[('ruscorpora', 'Russian National Corpus'), ('bnc', 'British')])
    #model = SelectField('', choices=())