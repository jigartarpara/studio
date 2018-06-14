# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, cint, cstr
from frappe.model.naming import make_autoname
from frappe.model.mapper import get_mapped_doc
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

@frappe.whitelist()		
def make_post_production(source_name, target_doc=None, ignore_permissions=False):
	
	def postprocess(source, target):
		pass

	def set_missing_values(source, target):
		pass

	def update_item(source, target, source_parent):
		pass

	doclist = get_mapped_doc("Sales Invoice", source_name, {
		"Sales Invoice": {
			"doctype": "Post Production",
			"field_map": {
				"name": "invoice_number",
				"event":"function",
				"order_name":"client_name",
				"status":"payment_status"
			},
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Invoice Item": {
			"doctype": "Deliverable Detail",
			"field_map": {
				"item_code": "requirement_of_client",
				"deliverable_type":"deliverable_type"
			},
			"condition":lambda doc: doc.deliverable_type == "Album" or doc.deliverable_type == "Video"
		}
	}, target_doc, postprocess, ignore_permissions=ignore_permissions)

	return doclist