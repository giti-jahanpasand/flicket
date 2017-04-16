#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import bcrypt
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired

from application.flicket.models.flicket_user import FlicketUser


def login_user_exist(form, field):
    """
    Ensure the username exists.
    :param form:
    :param field:
    :return True False:
    """
    result = FlicketUser.query.filter_by(username=form.username.data)
    if result.count() == 0:
        field.errors.append('Invalid username.')
        return False
    result = result.first()
    if bcrypt.hashpw(form.password.data.encode('utf-8'), result.password) != result.password:
        field.errors.append('Invalid password.')
        return False

    return True


class LogInForm(FlaskForm):
    """ Log in form. """
    username = StringField('username', validators=[DataRequired(), login_user_exist])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
