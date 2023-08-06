# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool, PoolMeta
from decimal import Decimal


__all__ = ['StatementImport']
__metaclass__ = PoolMeta


class StatementImport(metaclass=PoolMeta):
    __name__ = 'account.statement.import'

    def do_import_(self, action):
        """ try to find invoices for account statement lines
        """
        pool = Pool()
        Statement = pool.get('account.statement')
        StatementLine = pool.get('account.statement.line')
        Invoice = pool.get('account.invoice')

        (action, data) = super(StatementImport, self).do_import_(action)

        if 'res_id' in data:
            for i in data['res_id']:
                stm = Statement(i)
                for k in stm.origins:
                    if isinstance(k.party, type(None)) or \
                        isinstance(k.amount, type(None)):
                        continue
                    if k.amount == Decimal('0.0'):
                        continue

                    # find candidates of unpaied invoices
                    inv_lst = Invoice.search([
                            ('party', '=', k.party),
                            ('state', '=', 'posted'),
                            ('total_amount', '=', k.amount),
                        ])
                    # check if invoice number appears in purpose of statement lines
                    for inv1 in inv_lst:
                        if (inv1.number.lower() in k.description.lower()):
                            # match!
                            stm_lines = list(stm.lines)
                            stm_lines.append(StatementLine(invoice = inv1, origin = k))
                            stm.lines = stm_lines
                            # fill fields of statement line from origin
                            stm.lines[len(stm.lines) - 1].on_change_origin()
                            stm.on_change_lines()
                            stm.save()
                            break
        return (action, data)

# end StatementImport
