app_name = "kraya_branding"
app_title = "Kraya Branding"
app_publisher = "Kraya"
app_description = "Kraya branding for the ERPNext / Frappe desk"
app_email = "admin@example.com"
app_license = "mit"

# Default application logo (used where Navbar Settings has no logo set).
# The last installed app wins, so this app should be installed after ERPNext.
app_logo_url = "/assets/kraya_branding/images/kraya-logo.png"

# Desk assets: small CSS polish + browser-side fallback that swaps any
# remaining ERPNext logo/name for Kraya.
app_include_css = "/assets/kraya_branding/css/kraya_branding.css"
app_include_js = "/assets/kraya_branding/js/kraya_branding.js"

# Login page and website favicon / splash fallbacks.
website_context = {
	"favicon": "/assets/kraya_branding/images/kraya-favicon.png",
	"splash_image": "/assets/kraya_branding/images/kraya-logo.png",
}

# Rebrand app data sent to the desk at login.
extend_bootinfo = "kraya_branding.boot.boot_session"

# Rebrand the apps screen list.
override_whitelisted_methods = {
	"frappe.apps.get_apps": "kraya_branding.api.get_apps",
}

# This app does not add its own tile to the apps screen: it re-labels the
# ERPNext tile as Kraya instead (see branding.py).
