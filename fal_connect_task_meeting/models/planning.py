# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Planning(models.Model):
    _inherit = 'planning.slot'

    meeting_id = fields.Many2one('calendar.event', string='Meeting')

    def _action_create_calendar_event(self):
        for planning in self:
            meeting_name = _("%s on Meeting") % (planning.employee_id.name)
            meeting_values = {
                'name': meeting_name,
                'duration': planning.allocated_hours,
                'description': planning.name,
                'user_id': planning.user_id.id,
                'start': planning.start_datetime,
                'stop': planning.end_datetime,
                'allday': False,
                'privacy': 'confidential',
                'event_tz': planning.user_id.tz,
                'activity_ids': [(5, 0, 0)],
            }
        meetings = self.env['calendar.event'].with_context(
            no_mail_to_attendees=True, active_model=self._name).create(meeting_values)
        self.meeting_id = meetings.id

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Planning, self).create(vals_list)
        res._action_create_calendar_event()

        return res

    def unlink(self):
        for rec in self:
            if rec.meeting_id:
                rec.meeting_id.write({'active': False})

        return super(Planning, self).unlink()
