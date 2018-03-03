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
from odoo import fields, models


class HelpdeskSettings(models.TransientModel):
    """ @Inherit - Transient configuration model to add fields.
        @field: issue_sqn_id - many2one field linked to ir.sequence.
        @field: tag_issue - Boolean field to control email subject tagging.
    """
    _inherit = 'res.config.settings'

    issue_sqn_id = fields.Many2one(
        'ir.sequence',
        'Default Ticket Numbering Plan',
        required=True,
        help="This is the default numbering plan for tickets in case the\
                support teams do not have one assigned",
        related='company_id.issue_sqn_id')
    tag_issue = fields.Boolean(
        "Tag Ticket Subjects with Ticket Number",
        help="Enable/Disable the tagging of ticket subjects with a number..\
                e.g '16-00001 - Migration of data failed'..",
        related='company_id.tag_issue')
