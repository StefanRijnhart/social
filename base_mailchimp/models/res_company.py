# -*- coding: utf-8 -*-
# Copyright 2016 Opener B.V. <https://opener.amsterdam>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Some snippets were inspired by https://github.com/mailchimp/APIv3-examples
# Copyright (c) 2015, The Rocket Science Group, LLC

import requests
from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class Company(models.Model):
    _inherit = 'res.company'
    mailchimp_key = fields.Char(
        'Mailchimp API V3.0 Key', groups="base.group_system", password=True)

    @api.multi
    def mailchimp_test(self):
        """ Try to connect to Mailching with the given key """
        self.ensure_one()
        parts = (self.mailchimp_key or '').strip().split('-')
        if len(parts) != 2:
            raise UserError(_(
                "Please enter a key that contains a single dash and a server "
                "name (something like qwertyu98hggdsazxx-am4)"))
        apikey, server = parts
        url = "https://%s.api.mailchimp.com/3.0/" % server
        try:
            response = requests.get(url, auth=('apikey', apikey))
            response.raise_for_status()
        except (requests.ConnectionError, requests.HTTPError) as e:
            raise UserError(_(
                "Could not connect to Mailchimp:\n"), e)
        contents = response.json()
        raise UserError(_(
            "Connection looks good from here. Working with the following "
            "account:\n%s (%s)") % (contents['username'],
                                    contents['account_name']))
