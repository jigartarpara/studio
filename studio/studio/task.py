import frappe

@frappe.whitelist()
def validate(doc, method):
	print("Helloooooooooooooooo")
	if (not doc.task_sync) and doc.project:
		print("1")
		so = frappe.get_value("Project", doc.project, "sales_order")
		if so:
			print("2")
			so_doc = frappe.get_doc("Sales Order", so)
			for item in so_doc.items:
				print("3")
				if item.item_code == doc.subject:
					doc.description = item.description
					doc.append("studio_details",{
						"requirement_of_client": item.item_code,
						"deliverable_type": "Album"
					})
					doc.task_sync = True
					doc.save()
					print("4")