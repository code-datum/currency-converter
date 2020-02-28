from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired


class ExchangeForm(FlaskForm):
    CURRENCY_CODE = [('CZK', 'CZK'), ('USD', 'USD'), ('PLN', 'PLN'), ('EUR', 'EUR')]
    currency_val = FloatField('Currency value', validators=[DataRequired()])
    select_currency = SelectField(u'Select currency', choices=CURRENCY_CODE)
    select_converted = SelectField(u'Select currency', choices=CURRENCY_CODE)
    submit = SubmitField('Convert')
