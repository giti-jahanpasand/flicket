#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime
import random
import string

from flask import flash

from application import db, app
from application.flicket.models.flicket_models import FlicketPost
from application.flicket.models.flicket_user import FlicketUser


def random_string(characters=5):
    chars = string.ascii_lowercase + string.digits
    output_string = ''.join(random.choice(chars) for _ in range(characters))

    return output_string


def announcer_post(ticket_id, user, contents):
    announcer = FlicketUser.query.filter_by(username=app.config['ANNOUNCER']['username']).first()
    if not announcer:
        flash('There is no user allocated to close tickets.')
        return False
    else:
        # add post to say who closed ticket.
        new_reply = FlicketPost(
            ticket_id=ticket_id,
            user=announcer,
            date_added=datetime.datetime.now(),
            content='{}: {}.'.format(contents, user.username)
        )
        db.session.add(new_reply)
        db.session.commit()
        return True


def is_ticket_closed(status):
    # check to see if topic is closed. ticket can't be edited once it's closed.
    if status == 'Closed':
        flash('Users can not edit closed tickets.')
        return True


def block_quoter(foo):
    """
    Indents input with '> '. Used for quoting text in posts.
    :param foo:
    :return:
    """

    foo = foo.strip()
    split_string = foo.split('\n')
    new_string = ''
    if len(split_string) > 0:
        for i in split_string:
            temp_string = '> ' + i
            new_string += temp_string
        return new_string
    else:
        return '> ' + foo
