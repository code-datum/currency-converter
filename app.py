# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, url_for, flash, redirect
import pytest
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from datetime import date
from forms import ExchangeForm
from model import Exchange
import os

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')


# db = SQLAlchemy(app)


# ----------------------------------------------------------------------------#
# procedures
# ----------------------------------------------------------------------------#



# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/', methods=['GET', 'POST'])
def exchange():
    currency_val = None
    currency_title = None
    converted_val = None
    converted_title = None
    today = None
    form = ExchangeForm()
    if form.validate_on_submit():
        '''TODO 
        if everything is validated then give the data to Exchange methods
        1. send to api
        2. returned result to prepare and give to view
        '''
        flash(f'Currency converted', 'success')
        currency_val = form.currency_val.data
        currency_code = form.select_currency.data
        converted_code = form.select_converted.data
        # calculate data from input

        exchange = Exchange()
        currency_title = exchange.get_currency_title(currency_code)
        converted_title = exchange.get_currency_title(converted_code)
        converted_val, error = exchange.convert(currency_val, from_currency=currency_code, to_currency=converted_code)
        if error:
            flash(f'{error["msg"]}', 'error')
        today = date.today()
    else:
        flash(f'Please fill the all fields', 'error')

    from_currency = {'value': currency_val, 'title': currency_title}
    to_currency = {'value': converted_val, 'title': converted_title}
    return render_template('pages/exchange.html', form=form, from_currency=from_currency,
                           to_currency=to_currency, today=today)


'''
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('pages/register.html', title='Register', form=form)

'''


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
