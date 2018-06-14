# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from datetime import datetime, timedelta
from frappe.utils import flt, cint, cstr
from frappe.model.naming import make_autoname
from frappe import _
import frappe.defaults
from six.moves import urllib 
import json
from frappe.core.doctype.sms_settings.sms_settings import send_sms

def validate(doc, method):
	if doc.is_outdoor == 1:
		for i in doc.items:
			if not i.event_detail:
				frappe.throw("Event detail is mandatory in row " + cstr(i.idx) + ".")
		
		QuotationSMS(doc, method)
		VendorSMS(doc, method)
		if doc.docstatus == 1:
			OrderConfirmationSMS(doc, method)
	else:
		for i in doc.items:
			if not i.item_code:
				frappe.throw("Item code is mandatory in row " + cstr(i.idx) + ".")
	
	# receiver_list = ['9898744127']
	# message = 'Hello From Jeet traders'
	# send_sms(receiver_list, message)
	
def VendorSMS(doc, method):
	equipments = ''
	for i in doc.items:
		if frappe.db.get_value("Item",i.item_code,"item_group") == 'Equipment':
			if len(equipments) == 0:
				equipments += cstr(i.item_code)
			else:
				equipments += ", " + cstr(i.item_code)
	for i in doc.items:
		if i.vendor_sms == 0:
			customer_care = frappe.db.get_value("Company",doc.company,"customer_care_number")
			sms_sender = frappe.db.get_value("Company",doc.company,"sms_sender")
			phone = frappe.db.get_value("Employee",i.vendor,"cell_number")

			if i.vendor and i.item_code and doc.order_name and i.event_detail and i.event_vanue and i.delivery_date and equipments and doc.customer and sms_sender and customer_care and phone:	
				Vendor_SMS ='Hello {0}, You are assigned as {1} for {2} {3} at {4} dated on {5}. You have to keep {6} with you. Please Contact {7} by reaching their. Contact on {8} if you have any query.'.format(str(frappe.db.get_value("Employee",i.vendor,"employee_name")), str(frappe.db.get_value("Item",i.item_code,"quality_of_services")), str(doc.order_name), str(i.event_detail), str(i.event_vanue), str(i.delivery_date),str(equipments).replace("|","-"), str(doc.customer), str(customer_care))
				
				resp =  sendSMSRequest(doc, method, 'UVVzJrmMces-lnseHXCi9BZ2qs5IbUksVOnZjuRNc6', str(phone), sms_sender, Vendor_SMS)

				resp = json.loads(resp)	
				
				if resp['status'] == 'success':
					i.vendor_sms = 1
					frappe.db.set_value("Sales Order Item",{"idx":i.idx,"parent":doc.name},"vendor_sms",1)
					# so_item_name = frappe.db.get_value("Sales Order Item",{"idx":i.idx,"parent":doc.name},"name")
					# update_so_item = frappe.db.sql("""UPDATE `tabSales Order Item` SET vendor_sms = 1 WHERE name=%s""" , (so_item_name), as_dict = 1)
					frappe.db.commit()
					frappe.msgprint("Vendor message has been sent successfully for row." + cstr(i.idx) + ".")
				else:
					frappe.msgprint("There might be some error to send vendor message in row "+ cstr(i.idx) +". Please try again.")
			# else:
			# 	frappe.msgprint("The Vendor_SMSndor SMS can be sent only if the required details like vendor, quality of service, couple name, event detail, venue, equipments, customer care, vendor contact and sms sender has been entered in row "+ cstr(i.idx) +".")
	
def OrderConfirmationSMS(doc, method):
	if doc.order_sms == 0:
		sms_sender = frappe.db.get_value("Company",doc.company,"sms_sender")
		phone = frappe.db.get_value("Address",doc.customer_address,"phone")
		terms_and_conditions = frappe.db.get_value("Company",doc.company,"terms_and_conditions_link")
		
		if doc.order_name and doc.event and doc.wedding_date and doc.grand_total and sms_sender and phone and terms_and_conditions:	
			Order_SMS_To_Customer ='Hello {0}, Greetings from {1} ! Thank you for being our valued customers. We have confirmed to give the services for {2} {3} dated on {4}. Your estimated cost is {5} for your services. Terms and conditions: {6}'.format(str(doc.customer), str(doc.company), str(doc.order_name), str(doc.event), str(doc.wedding_date), str(doc.grand_total), str(terms_and_conditions))
			
			resp =  sendSMSRequest(doc, method, 'UVVzJrmMces-lnseHXCi9BZ2qs5IbUksVOnZjuRNc6', str(phone), sms_sender, Order_SMS_To_Customer)
			resp = json.loads(resp)	
			
			if resp['status'] == 'success':
				doc.order_sms = 1
				frappe.db.set_value("Sales Order",doc.name,"order_sms",1)
				frappe.db.commit()
				frappe.msgprint("Order Confirmation message has been sent to customer successfully.")
			else:
				frappe.msgprint("There might be some error to send confirmation message. Please try again.")
		else:
			frappe.msgprint("The Order Confirmation SMS can be sent only if the required details like couple name, event, event date, customer phone, terms and conditions and sms sender has been entered.")
	
def QuotationSMS(doc, method):
	if doc.quotation_sms == 0:
		sms_sender = frappe.db.get_value("Company",doc.company,"sms_sender")
		payment_terms = frappe.db.get_value("Company",doc.company,"ai_payment_terms")
		phone = frappe.db.get_value("Address",doc.customer_address,"phone")
		demonstration = frappe.db.get_value("Company",doc.company,"demonstration_link")
		
		services = ''
		for item in doc.items:
			if item.idx == 1:
				services += cstr(item.item_code)
			else:
				services += ", " + cstr(item.item_code)

		if services and doc.order_name and doc.event and doc.wedding_date and doc.grand_total and payment_terms and sms_sender and phone and demonstration:	

			Quotation_SMS_To_Customer ='Hello {0}, Greetings from {1}! We got the request to provide {2} for {3} {4} dated on {5}. You can check our demonstration on followed link: {6}. You have to pay {7} for your services. Payment Terms: {8}'.format(str(doc.customer), str(doc.company), str(services).replace("|","-"), str(doc.order_name), str(doc.event), str(doc.wedding_date), str(demonstration), str(doc.grand_total), str(payment_terms))

			resp =  sendSMSRequest(doc, method, 'UVVzJrmMces-lnseHXCi9BZ2qs5IbUksVOnZjuRNc6', str(phone), sms_sender, Quotation_SMS_To_Customer)
			resp = json.loads(resp)	
			
			if resp['status'] == 'success':
				doc.quotation_sms = 1
				frappe.db.set_value("Sales Order",doc.name,"quotation_sms",1)
				frappe.db.commit()
				frappe.msgprint("Quotation message has been sent to customer successfully.")
			else:
				frappe.msgprint("There might be some error to send quotation message. Please try again.")
		else:
			frappe.msgprint("The Quotation SMS can be sent only if the required details like couple name, resources, event, event date, sms sender, contact, demonstration link and payment terms has been entered.")
	
def sendSMSRequest(doc, method,apikey, numbers, sender, message):
	data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
		'message' : message, 'sender': sender})
	data = data.encode('utf-8')
	request = urllib.request.Request("https://api.textlocal.in/send/?")
	f = urllib.request.urlopen(request, data)
	fr = f.read()
	return(fr)