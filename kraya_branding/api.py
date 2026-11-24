import frappe
from frappe.apps import get_apps as core_get_apps

from kraya_branding.branding import rebrand_app_list


@frappe.whitelist()
def get_apps():
	"""Replacement for frappe.apps.get_apps (see override_whitelisted_methods in hooks.py).

	Returns the standard app list with the ERPNext entry shown as Kraya and any
	apps listed in HIDE_APPS removed.
	"""
	return rebrand_app_list(core_get_apps())
