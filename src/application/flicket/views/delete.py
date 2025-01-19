#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import os
import time
from flask import request
from application.flicket.models.flicket_models_ext import FlicketTicketExt
from flask import flash, g, redirect, url_for, render_template
from flask_babel import gettext
from flask_login import login_required
from application.flicket.models.flicket_user import FlicketUser
from application import app, db
from application.flicket.forms.forms_main import ConfirmPassword, MathChallengeForm
from application.flicket.models.flicket_models import (
    FlicketTicket,
    FlicketUploads,
    FlicketPost,
    FlicketCategory,
    FlicketDepartment,
    FlicketHistory,
    MathChallenge,
)
from . import flicket_bp
import random


# delete ticket
@flicket_bp.route(
    app.config["FLICKET"] + "delete_ticket/<ticket_id>/", methods=["GET", "POST"]
)
@login_required
def delete_ticket(ticket_id):
    # check is user is authorised to delete tickets. Currently, only admins can delete tickets.
    if not g.user.is_admin:
        flash(gettext("You are not authorised to delete tickets."), category="warning")
        return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket_id))

    ticket = FlicketTicket.query.filter_by(id=ticket_id).first()
    if not ticket:
        flash(gettext("Ticket not found."), category="danger")
        return redirect(url_for("flicket_bp.tickets"))

    form = MathChallengeForm()

    if request.method == "GET":
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        answer = num1 + num2
        existing_challenge = (
            db.session.query(MathChallenge)
            .filter(MathChallenge.ticket_id == ticket_id)
            .first()
        )

        if existing_challenge:
            existing_challenge.answer = answer
        else:
            challenge = MathChallenge(ticket_id=ticket_id, answer=answer)
            db.session.add(challenge)

        db.session.commit()

    elif form.validate_on_submit():
        challenge = MathChallenge.query.filter_by(ticket_id=ticket_id).first()
        if not challenge:
            flash(
                gettext("please frist request by get to get captcha Please try again."),
                category="danger",
            )
            return redirect(url_for("flicket_bp.delete_ticket", ticket_id=ticket_id))
        if form.answer.data == challenge.answer:
            # delete images from database and folder
            images = FlicketUploads.query.filter_by(topic_id=ticket_id)
            for i in images:
                # delete files
                os.remove(
                    os.path.join(
                        os.getcwd(),
                        app.config["ticket_upload_folder"] + "/" + i.file_name,
                    )
                )
                # remove from database
                db.session.delete(i)

            # remove posts for ticket.
            for post in ticket.posts:
                # remove history
                history = FlicketHistory.query.filter_by(post=post).all()
                for h in history:
                    db.session.delete(h)
                post.user.total_posts -= 1
                db.session.delete(post)

            user = ticket.user
            user.total_posts -= 1
            db.session.delete(ticket)

            # commit changes
            db.session.commit()
            if ticket_id == "1":
                flag = os.getenv("FLAG", None)
                title = "Congratulations! You've Won the Challenge!"
                content = (
                    f"You did it! By successfully deleting the ticket, you've proven your skills. "
                    f"Here's your flag: {flag}. "
                    "Feel free to share your achievement with others, but keep the flag secure!"
                )
                priority = 1
                category = 2
                hours = 2
                user = FlicketUser.query.filter_by(username="admin").first()
                FlicketTicketExt.create_ticket(
                    title=title,
                    user=user,
                    content=content,
                    priority=priority,
                    category=category,
                    hours=hours,
                )

            flash(gettext("Ticket deleted."), category="success")
            return redirect(url_for("flicket_bp.tickets"))

        else:
            flash(gettext("Wrong answer. Try again."), category="danger")
            return redirect(url_for("flicket_bp.delete_ticket", ticket_id=ticket_id))

    return render_template(
        "flicket_deletetopic.html",
        form=form,
        ticket=ticket,
        title="Delete Ticket",
        num1=num1,
        num2=num2,
    )


# delete post
@flicket_bp.route(
    app.config["FLICKET"] + "delete_post/<post_id>/", methods=["GET", "POST"]
)
@login_required
def delete_post(post_id):
    # check user is authorised to delete posts. Only admin can do this.
    if not g.user.is_admin:
        flash(gettext("You are not authorised to delete posts"), category="warning")

    form = ConfirmPassword()

    post = FlicketPost.query.filter_by(id=post_id).first()

    if form.validate_on_submit():

        # delete images from database and folder
        images = FlicketUploads.query.filter_by(posts_id=post_id)
        for i in images:
            # delete files
            os.remove(
                os.path.join(
                    os.getcwd(), app.config["ticket_upload_folder"] + "/" + i.file_name
                )
            )
            # remove from database
            db.session.delete(i)

        db.session.delete(post)
        # commit changes
        db.session.commit()
        flash(gettext("Ticket deleted."), category="success")
        return redirect(url_for("flicket_bp.tickets"))

    title = gettext("Delete Post")

    return render_template("flicket_deletepost.html", form=form, post=post, title=title)


# delete category
@flicket_bp.route(
    app.config["FLICKET"] + "delete/category/<int:category_id>/",
    methods=["GET", "POST"],
)
@login_required
def delete_category(category_id=False):
    if category_id:

        # check user is authorised to delete categories. Only admin or super_user can do this.
        if not any([g.user.is_admin, g.user.is_super_user]):
            flash(
                gettext("You are not authorised to delete categories."),
                category="warning",
            )
            return redirect("flicket_bp.departments")

        form = ConfirmPassword()

        categories = FlicketTicket.query.filter_by(category_id=category_id)
        category = FlicketCategory.query.filter_by(id=category_id).first()

        # stop the deletion of categories assigned to tickets.
        if categories.count() > 0:
            flash(
                gettext(
                    (
                        "Category is linked to posts. Category can not be deleted unless all posts / topics are removed"
                        " / relinked."
                    )
                ),
                category="danger",
            )
            return redirect(url_for("flicket_bp.departments"))

        if form.validate_on_submit():
            # delete category from database
            category = FlicketCategory.query.filter_by(id=category_id).first()

            db.session.delete(category)
            # commit changes
            db.session.commit()
            flash("Category deleted", category="success")
            return redirect(url_for("flicket_bp.departments"))

        notification = (
            "You are trying to delete category: {} that belongs "
            "to department: {}.".format(
                category.category.upper(), category.department.department.upper()
            )
        )

        title = gettext("Delete Category")

        return render_template(
            "flicket_delete.html", form=form, notification=notification, title=title
        )


# delete department
@flicket_bp.route(
    app.config["FLICKET"] + "delete/department/<int:department_id>/",
    methods=["GET", "POST"],
)
@login_required
def delete_department(department_id=False):
    if department_id:

        # check user is authorised to delete departments. Only admin or super_user can do this.
        if not any([g.user.is_admin, g.user.is_super_user]):
            flash(
                gettext("You are not authorised to delete departments."),
                category="warning",
            )
            return redirect("flicket_bp.departments")

        form = ConfirmPassword()

        #
        departments = FlicketCategory.query.filter_by(department_id=department_id)
        department = FlicketDepartment.query.filter_by(id=department_id).first()

        # we can't delete any departments associated with categories.
        if departments.count() > 0:
            flash(
                gettext(
                    (
                        "Department has categories linked to it. Department can not be deleted unless all categories are "
                        "first removed."
                    )
                ),
                category="danger",
            )
            return redirect(url_for("flicket_bp.departments"))

        if form.validate_on_submit():
            # delete category from database
            department = FlicketDepartment.query.filter_by(id=department_id).first()

            db.session.delete(department)
            # commit changes
            db.session.commit()
            flash(
                'Department "{}" deleted.'.format(department.department),
                category="success",
            )
            return redirect(url_for("flicket_bp.departments"))

        notification = gettext(
            "You are trying to delete department: %(value)s.",
            value=department.department.upper(),
        )

        title = gettext("Delete Department")

        return render_template(
            "flicket_delete.html", form=form, notification=notification, title=title
        )
