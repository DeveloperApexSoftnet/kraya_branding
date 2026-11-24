"""Central Kraya branding settings.

Edit the values in this file to change what the app does, then commit and
redeploy. Nothing here touches the database: all changes happen when pages and
app lists are sent to the browser, so uninstalling the app restores the
standard look.
"""

ASSET = "/assets/kraya_branding/images"

BRAND = {
	"title": "Kraya",
	# Square mark: used for the app tile and the sidebar / dock app icon.
	"logo": f"{ASSET}/kraya-mark.svg",
	# Full "kraya" wordmark: used as the default application logo.
	"wordmark": f"{ASSET}/kraya-logo.png",
	"favicon": f"{ASSET}/kraya-favicon.png",
}

# Apps whose tile, icon and name become Kraya.
REBRAND_APPS = {"erpnext"}

# Apps to hide from the apps screen (their pages keep working by URL).
# Example: {"insights", "india_compliance"}
HIDE_APPS = set()

# Logo files that are swapped for the Kraya mark wherever they appear.
REPLACE_LOGOS = [
	"/assets/erpnext/images/erpnext-logo.svg",
	"/assets/erpnext/images/erpnext-logo.png",
]

REPLACE_TITLES = ["ERPNext"]


def rebrand_app(app):
	"""Return a copy of one apps-screen entry with Kraya branding applied."""
	if not isinstance(app, dict):
		return app
	app = dict(app)
	name = app.get("name") or app.get("app_name")
	if name in REBRAND_APPS:
		for key in ("logo", "app_logo_url", "icon"):
			if app.get(key):
				app[key] = BRAND["logo"]
		for key in ("title", "app_title", "label"):
			if app.get(key):
				app[key] = BRAND["title"]
	return app


def rebrand_app_list(apps):
	"""Rebrand and filter a list of apps-screen entries."""
	if not isinstance(apps, list):
		return apps
	out = []
	for app in apps:
		name = app.get("name") or app.get("app_name") if isinstance(app, dict) else None
		if name in HIDE_APPS:
			continue
		out.append(rebrand_app(app))
	return out


def client_config():
	"""Settings passed to the browser script through frappe.boot."""
	return {
		**BRAND,
		"replace_logos": REPLACE_LOGOS,
		"replace_titles": REPLACE_TITLES,
		"hide_apps": sorted(HIDE_APPS),
	}
