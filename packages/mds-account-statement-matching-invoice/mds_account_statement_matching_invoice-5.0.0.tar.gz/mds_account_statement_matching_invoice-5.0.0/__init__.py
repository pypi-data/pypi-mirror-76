# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .statement import StatementImport

def register():
    Pool.register(
        StatementImport,
        module='account_statement_matching_invoice', type_='wizard')
