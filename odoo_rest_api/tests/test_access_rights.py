# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import requests
import json
from odoo.addons.odoo_rest_api.tests.common import TestSaleCommonBase
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tests import HttpCase, tagged
_logger = logging.getLogger(__name__)


class TestAccessRights(TestSaleCommonBase):

    def test_order_mrp(self):
        _logger.info('============start==============')
        base_url = "http://192.168.88.60:8015"
        
