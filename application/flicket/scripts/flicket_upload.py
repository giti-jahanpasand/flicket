#! usr/bin/python3
# -*- coding: utf8 -*-

import os

from flask import flash
from werkzeug.utils import secure_filename

from application import app, db
from application.flicket.models.flicket_models import FlicketUploads
from application.flicket.scripts.flicket_functions import random_string
from config import BaseConfiguration


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['allowed_extensions']


def upload_documents(files):
    """
    Function to upload files to the static temp folder.
    The file is given a random unique file name.
    :param files:
    :return:
    """
    new_files = []

    if len(files) == 0:
        return None

    if files[0].filename != '':

        for f in files:

            target_file = False
            if f and allowed_file(f.filename):

                target_file = secure_filename(f.filename)
                target_file = os.path.join(app.config['ticket_upload_folder'], target_file)
                print(target_file)
                f.save(target_file)

            # rename file
            if os.path.isfile(target_file):

                while True:
                    new_name_size = BaseConfiguration.db_field_size['ticket']['upload_filename'] - len(
                        os.path.splitext(target_file)[1])
                    new_name = random_string(new_name_size) + os.path.splitext(target_file)[1]
                    new_name = os.path.join(app.config['ticket_upload_folder'], new_name)
                    # make sure new name doesn't already exist
                    if not os.path.isfile(new_name):
                        break

                # rename uploaded file to unique name
                os.rename(target_file, new_name)
                new_files.append((new_name, f.filename))

            else:

                # There has been a problem uploading some documents.
                return False

    return new_files


def add_upload_to_db(new_files, object, post_type=False):
    topic = None
    post = None

    if post_type == 'Ticket':
        topic = object
    if post_type == 'Post':
        post = object

    if post_type == False:
        flash('There was a problem uploading images.')

    # add documents to database.
    # todo: need to find a way to improve this. seems repetitive.
    if len(new_files) > 0:
        # if post_type == 'Ticket':
        #     for f in new_files:
        #         new_image = FlicketUploads(topic=topic, filename=os.path.basename(f[0]), original_filename=f[1])
        #         db.session.add(new_image)
        # if post_type == 'Post':
        #     for f in new_files:
        #         new_image = FlicketUploads(post=post, filename=os.path.basename(f[0]), original_filename=f[1])
        #         db.session.add(new_image)
        for f in new_files:
            new_image = FlicketUploads(topic=topic, post=post, filename=os.path.basename(f[0]), original_filename=f[1])
            db.session.add(new_image)
