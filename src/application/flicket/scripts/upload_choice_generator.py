#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import url_for

from application.flicket.models.flicket_models import FlicketTicket, FlicketPost


def generate_choices(item, id=id):
    """
    Generates a list of file uploads associated with a given ticket or post.

    :param item: A string indicating the type of object ('Ticket' or 'Post').
    :param id: The ID of the object (ticket or post).
    :return: A list of tuples containing upload ID and a clickable HTML link to the file.
    """

    query = None  # Initialize query variable

    if item == 'Ticket':
        query = FlicketTicket.query.filter_by(id=id).first()
    elif item == 'Post':
        query = FlicketPost.query.filter_by(id=id).first()

    if query:
        # Define the multi-select box for document uploads
        upload = []
        for u in query.uploads:  # Iterate through the uploads associated with the ticket/post
            upload.append((u.id, u.filename, u.original_filename))

        uploads = []

        for x in upload:
            # Generate a URL for the uploaded file
            uri = url_for('flicket_bp.view_ticket_uploads', filename=x[1])
            uri_label = '<a href="' + uri + '">' + x[2] + '</a>'
            uploads.append((x[0], uri_label))

        return uploads  # Return the list of file uploads
