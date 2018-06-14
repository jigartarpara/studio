// cur_frm.fields_dict['items'].grid.get_field('event_detail').get_query = function(doc) {
	// return {
		 // filters: { 'item_group': 'Event' }
	// }
// }

cur_frm.fields_dict['items'].grid.get_field('vendor').get_query = function(doc) {
	return {
		 filters: { 'employment_type': 'Vendor' }
	}
}

// cur_frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc) {
	// return {
		 // filters: { 'item_group': 'Event' }
	// }
// }

frappe.ui.form.on("Sales Order", "before_submit", function(frm, cdt, cdn) {
	// var docstatus = [0,1,2]
	//console.log(this);
	//console.log(this.cur_frm.fields_dict.items.grid);
	// if(!cur_frm.doc.__islocal)
	//if(frm.doc.docstatus == 1)
	//{
		//alert("hi");
		this.cur_frm.fields_dict.items.grid.toggle_reqd("item_code", true);
		this.cur_frm.fields_dict.items.grid.toggle_reqd("item_name", true);
		this.cur_frm.fields_dict.items.grid.toggle_reqd("description", true);
		this.cur_frm.fields_dict.items.grid.toggle_reqd("uom", true);
		this.cur_frm.fields_dict.items.grid.toggle_reqd("conversion_factor", true);
		/*cur_frm.frm.fields_dict.items.grid.toggle_reqd("item_code");
		cur_frm.get_field("items").grid.toggle_reqd("item_code", true);
		cur_frm.get_field("items").grid.toggle_reqd("item_name", true);
		cur_frm.get_field("items").grid.toggle_reqd("description", true);
		cur_frm.get_field("items").grid.toggle_reqd("uom", true);
		cur_frm.get_field("items").grid.toggle_reqd("conversion_factor", true);*/
	//}
});

cur_frm.cscript.rate = function(doc, cdt, cdn) {
	count_total_revenue(doc,cdt,cdn);
}

cur_frm.cscript.discount_amount = function(doc, cdt, cdn) {
	count_total_revenue(doc,cdt,cdn);
}

cur_frm.cscript.total_taxes_and_charges = function(doc, cdt, cdn) {
	count_total_revenue(doc,cdt,cdn);
}

cur_frm.cscript.price = function(doc, cdt, cdn) {
	count_total_price(doc,cdt,cdn);
	count_total_revenue(doc,cdt,cdn);
}

// Copy Event Details From Previous Row while Clicking on add new row
frappe.ui.form.on("Sales Order Item", "items_add", function(frm,cdt,cdn) {

	var d = frappe.get_doc(cdt, cdn);
	var row = frappe.get_doc(cdt, cdn);
	$.each(frm.doc.items, function(i, d) {
		row.event_detail = d.event_detail;
		row.delivery_date = d.delivery_date;
		row.event_vanue = d.event_vanue;
		row.from_time = d.from_time;
		row.to_time = d.to_time;
		row.vendor = d.vendor;
		row.staff = d.staff;
		row.hall = d.hall;
	});

	count_total_price(frm.doc,cdt,cdn);
	count_total_revenue(frm.doc,cdt,cdn);
});

frappe.ui.form.on("Sales Order Item", "items_remove", function(frm,cdt,cdn) {
	count_total_price(frm.doc,cdt,cdn);
	count_total_revenue(frm.doc,cdt,cdn);
});

var count_total_price = function(doc,cdt,cdn){
	var child_table = cur_frm.doc.items || [];
	var total_price = 0
	for(var i = 0; i < child_table.length; i++)
	{
		if (parseFloat(child_table[i].price) > 0)
		{
			total_price = parseFloat(total_price) + parseFloat(child_table[i].price)
		}
	}
	cur_frm.set_value("total_price", total_price);
}

var count_total_revenue = function(doc,cdt,cdn){
	var total_amount = parseFloat(doc.total) > 0 ? parseFloat(doc.total) : 0
	var discount = parseFloat(doc.discount_amount) > 0 ? parseFloat(doc.discount_amount) : 0
	var taxes_and_charges = parseFloat(doc.total_taxes_and_charges) > 0 ? parseFloat(doc.total_taxes_and_charges) : 0
	var amount_paid_to_vendor = parseFloat(doc.total_price) > 0 ? parseFloat(doc.total_price) : 0
	var total_revenue = parseFloat(total_amount) - parseFloat(discount) - parseFloat(taxes_and_charges) - parseFloat(amount_paid_to_vendor)

	cur_frm.set_value("revenue", total_revenue);
}
