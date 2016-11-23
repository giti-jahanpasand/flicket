#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import redirect, url_for, flash, g
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.models.flicket_models import FlicketTicket, FlicketStatus
from application.flicket.scripts.flicket_functions import announcer_post


# view for self claim a ticket
@flicket_bp.route(app.config['FLICKETHOME'] + 'ticket_claim/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_claim(ticket_id=False):
    if ticket_id:
        # claim ticket
        ticket = FlicketTicket.query.filter_by(id=ticket_id).first()

        # set status to in work
        status = FlicketStatus.query.filter_by(status='In Work').first()
        ticket.assigned = g.user
        ticket.current_status = status
        db.session.commit()

        # add post to say user claimed ticket.
        announcer_post(ticket_id, g.user, 'Ticket assigned to')

        flash('You claimed ticket:{}'.format(ticket.id))
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

    return redirect(url_for('flicket_bp.tickets_main'))
