'''
Created on Jul 2, 2012

@author: Roxly Rivero
'''

from osv import osv, fields, orm
import netsvc
import pooler
import psycopg2
import time
from tools.translate import _
import datetime

from tools.misc import logged

class entry_alteration(osv.osv):
	_name = 'entry.alteration'
	_description = 'Entry Alteration for account_move_lines'
	_columns = {
	    'name':fields.date('Alteration Date'),
	    'entry_ids': fields.many2many('account.move.line', 'entry_move_line_ids', 'entry_id', 'move_id', 'Entries to Alter'),
	    'journal_id':fields.many2one('account.journal', 'Journal'),
	    'account_id':fields.many2one('account.account','Account'),
	    'log_ids':fields.one2many('entry.alteration.log','alter_id','Alteration Logs', readonly=True),
		}
	def apply_alteration(self, cr, uid, ids, context=None):
		move_line_pool=self.pool.get('account.move.line')
		alter_log=self.pool.get('entry.alteration.log')
		for inv in self.browse(cr, uid, ids, context=None):
			inv_id = inv.id
			if inv.account_id:
				account_id = inv.account_id.id
				for entry_id in inv.entry_ids:
					entry_uid = entry_id.id
					account_orig=entry_id.account_id.id
					entry_name = entry_id.name
					entry_name = "'"+entry_name+"'"
					query=("""update account_move_line set account_id=%s where id=%s"""% (entry_uid, account_id))
					cr.execute(query)
					query=("""insert into entry_alteration_log(account_from, account_to, entry_id, name, alter_id) values(%s,%s,%s,%s,%s)"""% (account_orig, account_id,entry_uid,entry_name, inv_id))
					cr.execute(query)
				continue
			if inv.journal_id:
				continue
#	    
#	    for inv in self.browse(cr, uid, ids,context=None):
#			inv_id = inv.id
#			if inv.account_id:
#				account_id=inv.account_id.id
##					account_orig=entry_id.account_id.id
	#                move_line_pool.update(cr, uid,{'account_id':account_id})
	 #           continue
	           
	  #      if inv.journal_id:
	   #     	journal_id=inv.journal_id.id
	    #    	for entry_id in inv.entry_ids:
	     #   		journal_orig=entry_id.journal_id.id
	      #          entry_id=entry_id.id
	       #         move_line_pool.update(cr, uid,{'journal_id':journal_id})
	        #    continue
entry_alteration()

class entry_alteration_log(osv.osv):
    _name = 'entry.alteration.log'
    _description = 'Entry Alteration Log'
    _columns = {
		'name':fields.char('Entry Name', size=200),
		'entry_id':fields.integer('Entry ID'),
        'account_from':fields.many2one('account.account', 'From Account', readonly=True),
        'account_to':fields.many2one('account.account', 'To Account', readonly=True),
        'journal_from':fields.many2one('account.journal', 'From Journal', readonly=True),
        'journal_to':fields.many2one('account.journal','To Journal',readonly=True),
        'alter_date':fields.datetime('Alter Date', readonly=True),
        'alter_id':fields.many2one('entry.alteration', 'Alteration', ondelete='cascade',select=True),
        }
entry_alteration_log()

