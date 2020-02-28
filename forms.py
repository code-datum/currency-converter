from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ExchangeForm(FlaskForm):
    currency_val = FloatField('Currency value', validators=[DataRequired()])
    select_currency = SelectField(u'Select currency', choices=[('CAD', 'CAD'), ('USD', 'USD')])
    select_converted = SelectField(u'Select currency', choices=[('CAD', 'CAD'), ('USD', 'USD')])
    submit = SubmitField('Convert')