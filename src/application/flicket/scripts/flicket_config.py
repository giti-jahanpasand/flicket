#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from application import app
from application.flicket_admin.models.flicket_config import FlicketConfig


def set_flicket_config():
    """
    Updates the flicket application settings based on the values stored in the database.
    :return:
    """
    config = FlicketConfig.query.first()
    try:
        posts_per_page = config.posts_per_page
    except AttributeError:
        raise AttributeError(
            'No FlicketConfig object is in db did you run "flask run-set-up" ?'
        )

    app.config.update(
        posts_per_page=posts_per_page,
        allowed_extensions=config.allowed_extensions.split(", "),
        ticket_upload_folder=config.ticket_upload_folder,
        avatar_upload_folder=config.avatar_upload_folder,
        base_url=config.base_url,
        application_title=config.application_title,
        use_auth_domain=config.use_auth_domain,
        auth_domain=config.auth_domain,
        csv_dump_limit=config.csv_dump_limit,
        change_category=config.change_category,
        change_category_only_admin_or_super_user=config.change_category_only_admin_or_super_user,
    )
