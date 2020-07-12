import frappe

def on_update(doc, method):
	# Project on_update
	# project studio_sales_order studio_item
	if doc.sales_order :
		sales_order = frappe.get_doc("Sales Order", doc.sales_order)
		for item in sales_order.items:
			if not task_exist(doc, item):
				task = frappe.get_doc({
					"doctype": "Task",
					"subject": item.item_code,
					"project": doc.name,
					"studio_sales_order": doc.sales_order,
					"studio_item": item.item_code,
					"so_item_id": item.name
				})
				task.flags.ignore_mandatory = True
				task.flags.ignore_permissions = True
				task.insert()
			else:
				task =  frappe.get_doc("Task", task_exist(doc, item))
			
			task.studio_description = item.description
			if not task.exp_end_date:
				task.exp_end_date	 = item.delivery_date
			task.save(ignore_permissions=True)
				

def task_exist(project, item):
	task = frappe.db.get_value("Task", {
			"project": project.name,
			"studio_sales_order": project.sales_order, 
			"studio_item": item.item_code,
			"so_item_id": item.name
		}, "name")
	if task:
		return task
	else:
		return False