# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, cint, cstr
from frappe.model.naming import make_autoname
from frappe import _
import frappe.defaults

def autoname(doc, method):
	fy = frappe.db.get_value("Global Defaults",None, "current_fiscal_year")
	fy_list = fy.split("-")
	fy_abbr = str(fy_list[0][-2:]) + str(fy_list[1][-2:])
	doc_abbr = frappe.db.get_value("Company", doc.company, "abbr")
	if not doc.is_return:
		doc.name = make_autoname(doc_abbr+"/" + fy_abbr +'/.##')
	else:
		doc.name = make_autoname(doc_abbr+"/SR/" + fy_abbr +'/.##')