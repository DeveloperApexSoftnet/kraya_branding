from kraya_branding.branding import client_config, rebrand_app, rebrand_app_list


def boot_session(bootinfo):
	"""Rebrand app data sent to the desk when a user logs in (extend_bootinfo hook)."""
	# Apps screen data (name of the key differs between Frappe v15/v16 releases).
	apps_data = bootinfo.get("apps_data")
	if isinstance(apps_data, dict) and isinstance(apps_data.get("apps"), list):
		apps_data["apps"] = rebrand_app_list(apps_data["apps"])

	# Dock / sidebar app entries (Frappe v16 new navigation).
	app_data = bootinfo.get("app_data")
	if isinstance(app_data, list):
		bootinfo["app_data"] = [rebrand_app(app) for app in app_data]

	# Settings for the browser-side fallback in kraya_branding.js.
	bootinfo["kraya_branding"] = client_config()
