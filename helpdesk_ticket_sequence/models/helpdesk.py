# -*- coding: utf-8 -*-
"""
# License LGPL-3.0 or later (https://opensource.org/licenses/LGPL-3.0).
#
#This software and associated files (the "Software") may only be used (executed,
#modified, executed after modifications) if you have purchased a valid license
#from the authors, typically via Odoo Apps, or if you have received a written
#agreement from the authors of the Software (see the COPYRIGHT section below).
#
#You may develop Odoo modules that use the Software as a library (typically
#by depending on it, importing it and using its resources), but without copying
#any source code or material from the Software. You may distribute those
#modules under the license of your choice, provided that this license is
#compatible with the terms of the Odoo Proprietary License (For example:
#LGPL, MIT, or proprietary licenses similar to this one).
#
#It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#or modified copies of the Software.
#
#The above copyright notice and this permission notice must be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#DEALINGS IN THE SOFTWARE.
#
#########COPYRIGHT#####
# © 2017 Bernard K Too<bernard.too@optima.co.ke>
"""
from odoo import models, fields, api


class HelpdeskTeam(models.Model):
    """ @Inherit - To add more field to the helpdesk.team model.
        @field: issue_sqn_id - many2one selection field linked to ir.sequence.
        @field: tag_issue - Boolean field to control email subject tagging.
    """
    _inherit = "helpdesk.team"

    issue_sqn_id = fields.Many2one(
        'ir.sequence',
        'Ticket Numbering',
        default=lambda self: self.env.user.company_id.issue_sqn_id,
        help="Select number sequence to use for tickets for the team")
    tag_issue = fields.Boolean(
        'Tag Ticket Subject/Heading',
        default=lambda self: self.env.user.company_id.tag_issue,
        help="Enable it tag new tickets subject with a ticket number..\
                e.g '#16-00003 - Data Migration problem'")


class RefNumber(models.Model):
    """ @Inherit - To add more field to the helpdesk.team model.
        @field: issue_sqn - Character field to store ticket number.
        @method override: create - overrides the create method to \
                assign a number to a new ticket.
    """
    _inherit = "helpdesk.ticket"

    issue_sqn = fields.Char(
        'Ticket Number',
        readonly=True,
        help="a unique ref number assigned to to the ticket to identify")

    @api.one
    def do_nothing(self):
        """Simply do nothing for lack of better way."""  # fixme: There must be a better way
        pass

    @api.model
    def create(self, vals):
        team = None
        ref_no = ""
        team_id = vals.get('team_id', False)
        company = self.env.user.company_id or self.env.ref('base.main_company')
        if team_id:
            team = self.env['helpdesk.team'].browse([team_id])
        if team and team.issue_sqn_id:
            ref_no = team.issue_sqn_id.next_by_id()
        elif company.issue_sqn_id:
            ref_no = company.issue_sqn_id.next_by_id()

        vals.update(dict(issue_sqn=ref_no))

        if team and team.tag_issue:
            vals.update(dict(name=ref_no + ": " + vals.get('name', '')))
        elif company.tag_issue and not team:
            vals.update(dict(name=ref_no + ": " + vals.get('name', '')))
        return super(RefNumber, self).create(vals)
