import frappe

def validate(doc, method):
	if (not doc.task_sync) and doc.project:
		so = frappe.get_value("Project", doc.project, "sales_order")
		if so:
			so_doc = frappe.get_doc("Sales Order", so)
			for item in so_doc.items:
				if item.item_code == doc.subject:
					doc.description = item.description
					doc.append("studio_details",{
						"requirement_of_client": item.item_code,
					})
					doc.task_sync = True
					doc.save()