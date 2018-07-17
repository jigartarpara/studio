# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, cint, cstr
from frappe.model.naming import make_autoname
from frappe.model.mapper import get_mapped_doc
from frappe import _
import frappe.defaults
from six.moves import urllib
import json

def autoname(doc, method):
	fy = frappe.db.get_value("Global Defaults",None, "current_fiscal_year")
	fy_list = fy.split("-")
	fy_abbr = str(fy_list[0][-2:]) + str(fy_list[1][-2:])
	doc_abbr = frappe.db.get_value("Company", doc.company, "abbr")
	if not doc.is_return:
		doc.name = make_autoname(doc_abbr+"/" + fy_abbr +'/.##')
	else:
		doc.name = make_autoname(doc_abbr+"/SR/" + fy_abbr +'/.##')

def on_submit(doc, method):
	sms_sender = frappe.db.get_value("Company",doc.company,"sms_sender")
	phone = frappe.db.get_value("Address",doc.customer_address,"phone")
	demonstration = frappe.db.get_value("Company",doc.company,"demonstration_link")
	terms_and_conditions = frappe.db.get_value("Company",doc.company,"terms_and_conditions_link")

	if doc.customer and doc.name and doc.grand_total and demonstration and terms_and_conditions:
		invoice_sms = "Hello {0}, Thank you for dealing with us ! Your invoice {1} has been generated with the amount of {2}. You have paid {3} and {4} is the due amount. You will get the delivery on {5}. Look at our demonstration: {6}. Please follow the link for the TNC: {7}".format(cstr(doc.customer), cstr(doc.name), cstr(doc.grand_total), cstr(doc.paid_amount), cstr(flt(doc.outstanding_amount)), cstr(doc.posting_date), cstr(demonstration), cstr(terms_and_conditions))
		# invoice_sms = 'Hello Nishith, Thank you for dealing with us ! Your invoice OFAP/1819/279 has been generated with the amount of 17700.0. You have paid 0.0 and 17700.0 is the due amount. You will get the delivery on 2018-07-09. Look at our demonstration: www.thestudioom.in, https://www.facebook.com/thestudio.om. Please follow the link for the TNC: https://docs.google.com/file/d/1Vxwr65eoQMyGCvFBM_yBJFWh29s5DtFN/edit?usp=docslist_api&filetype=msword'
		frappe.msgprint(cstr(invoice_sms))
		resp =  sendSMSRequest(doc, method, 'UVVzJrmMces-lnseHXCi9BZ2qs5IbUksVOnZjuRNc6', str(phone), sms_sender, invoice_sms)
		resp = json.loads(resp)
		
		if resp['status'] == 'success':
			frappe.msgprint("Invoice message has been sent to customer successfully.")
		else:
			frappe.msgprint("There might be some error to send confirmation message. Please try again.")

def sendSMSRequest(doc, method,apikey, numbers, sender, message):
	data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
		'message' : message, 'sender': sender})
	data = data.encode('utf-8')
	request = urllib.request.Request("https://api.textlocal.in/send/?")
	f = urllib.request.urlopen(request, data)
	fr = f.read()
	return(fr)

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