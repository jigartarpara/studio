# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "studio"
app_title = "Studio"
app_publisher = "August Infotech"
app_description = "Managing Studio related Works"
app_icon = "octicon octicon-clock"
app_color = "#D10056"
app_email = "info@augustinfotech.com"
app_license = "GNU General Public Licence"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/studio/css/studio.css"
# app_include_js = "/assets/studio/js/studio.js"

doctype_js = {
	"Sales Order": ["custom_scripts/sales_order.js"],
	"Sales Invoice": ["custom_scripts/sales_invoice.js"]
}

doc_events = {
	"Sales Invoice": {
		"autoname": "studio.studio.sales_invoice.autoname",
		"on_submit": "studio.studio.sales_invoice.on_submit"
	},
	"Sales Order": {
		"validate": "studio.studio.sales_order.validate"
	}
}

# include js, css files in header of web template
# web_include_css = "/assets/studio/css/studio.css"
# web_include_js = "/assets/studio/js/studio.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}
#page_js = {
    #"pos”" : "public/js/pos_page_js.js",
    #"point-of-sale" : "public/js/pos_page_js.js"
#} # <= this loading is visible only inside POS page
# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "studio.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "studio.install.before_install"
# after_install = "studio.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "studio.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"studio.tasks.all"
# 	],
# 	"daily": [
# 		"studio.tasks.daily"
# 	],
# 	"hourly": [
# 		"studio.tasks.hourly"
# 	],
# 	"weekly": [
# 		"studio.tasks.weekly"
# 	]
# 	"monthly": [
# 		"studio.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "studio.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "studio.event.get_events"
# }
