# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


class JiraProjectCategory(models.Model):

    _name = 'jira.category'
    _description = 'Jira Project Category'

    def receive_all(self):
        for pc in self.env['res.company'].search([],limit=1).get('projectCategory').json():
            self.process_response(pc)

    def process_response(self, response):
        category_dict = dict(
            jira_id=response['id'],
            description=False,
            name=response['name']
        )
        if 'description' in response:
            category_dict['description'] = response['description']
        category = self.search([('jira_id', '=', category_dict['jira_id'])])
        if not category:
            category = self.create(category_dict)
        else:
            category.write(category_dict)
        return category

    def key_operation(self, id):
        category = self.search([('jira_id', '=', id)])
        if not category:
            category = self.process_response(
                self.env['res.company'].search([],limit=1).get('projectCategory/' + str(id)).json()
            )
        return category

    name = fields.Char(required=1)
    jira_id = fields.Char(required=1)
    description = fields.Char()
