import frappe

@frappe.whitelist()
def validate(doc, method):
	pass
	# if (not doc.task_sync) and doc.project:
	# 	so = frappe.get_value("Project", doc.project, "sales_order")
	# 	if so:
	# 		so_doc = frappe.get_doc("Sales Order", so)
	# 		for item in so_doc.items:
	# 			if item.item_code == doc.subject:
	# 				doc.description = item.description
	# 				doc.append("studio_details",{
	# 					"requirement_of_client": item.item_code,
	# 					"deliverable_type": "Album"
	# 				})
	# 				doc.task_sync = True
	# 				doc.save()

def on_update(doc, method):
	if not doc.event :
		event = frappe.get_doc({
			"doctype": "Event",
			"subject": doc.subject + doc.project ,
			"event_category": "Event",
			"event_type": "Public",
			"starts_on": doc.exp_start_date,
			"ends_on": doc.exp_end_date,
			"status": "Open",
			"description": str(doc.studio_description) + "\n" + str(doc.description)
		})
		event.flags.ignore_mandatory = True
		event.flags.ignore_permissions = True
		event.insert()
		doc.event = event.name
		doc.save(ignore_permissions=True)
	else:
		event = frappe.get_doc("Event", doc.event)
		# event.starts_on = doc.exp_start_date
		# event.ends_on = doc.exp_end_date
		event.description = str(doc.studio_description) + "\n" + str(doc.description)
		event.save(ignore_permissions=True)