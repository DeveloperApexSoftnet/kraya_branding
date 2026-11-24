// Kraya branding: browser-side fallback.
// The server already rebrands app data (see boot.py and api.py). This script
// catches any ERPNext logo or name that the desk still draws from its own
// built-in assets, such as the dock/sidebar app icon, and swaps it for Kraya.
// It only changes what is displayed; it never reads or writes documents.
(function () {
	const cfg = Object.assign(
		{
			title: "Kraya",
			logo: "/assets/kraya_branding/images/kraya-mark.svg",
			replace_logos: ["/assets/erpnext/images/erpnext-logo.svg"],
			replace_titles: ["ERPNext"],
			hide_apps: [],
		},
		(window.frappe && frappe.boot && frappe.boot.kraya_branding) || {}
	);

	const SKIP = "input, textarea, [contenteditable], .ql-editor, .CodeMirror, pre, code, .ace_editor";
	const isOldLogo = (src) => !!src && cfg.replace_logos.some((l) => src.indexOf(l) !== -1);
	const hideLogo = (app) => `/assets/${app}/`;

	function swapImages(root) {
		root.querySelectorAll("img").forEach((img) => {
			const src = img.getAttribute("src") || "";
			if (isOldLogo(src)) {
				img.setAttribute("src", cfg.logo);
				img.setAttribute("alt", cfg.title);
				const tile = img.parentElement;
				if (tile) tile.classList.add("kraya-branded-tile");
			}
			if (cfg.hide_apps.some((app) => src.indexOf(hideLogo(app)) !== -1)) {
				const item = img.closest("a, [data-app], .app-item, .desktop-icon, .dropdown-item");
				if (item) item.classList.add("kraya-hidden-app");
			}
		});
	}

	function swapAttributes(root) {
		cfg.replace_titles.forEach((t) => {
			["title", "aria-label", "data-original-title", "data-title"].forEach((attr) => {
				root.querySelectorAll(`[${attr}="${t}"]`).forEach((el) => el.setAttribute(attr, cfg.title));
			});
		});
	}

	function swapText(root) {
		const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
			acceptNode(node) {
				const v = (node.nodeValue || "").trim();
				if (!v || !cfg.replace_titles.includes(v)) return NodeFilter.FILTER_SKIP;
				const parent = node.parentElement;
				if (!parent || parent.closest(SKIP)) return NodeFilter.FILTER_SKIP;
				return NodeFilter.FILTER_ACCEPT;
			},
		});
		const nodes = [];
		while (walker.nextNode()) nodes.push(walker.currentNode);
		nodes.forEach((n) => {
			n.nodeValue = n.nodeValue.replace(n.nodeValue.trim(), cfg.title);
		});
	}

	function apply() {
		if (!document.body) return;
		swapImages(document.body);
		swapAttributes(document.body);
		swapText(document.body);
	}

	let queued = false;
	function schedule() {
		if (queued) return;
		queued = true;
		requestAnimationFrame(() => {
			queued = false;
			apply();
		});
	}

	function start() {
		apply();
		new MutationObserver(schedule).observe(document.body, {
			childList: true,
			subtree: true,
			attributes: true,
			attributeFilter: ["src"],
		});
	}

	if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
	else start();
})();
