# Kraya Branding

A small Frappe app that replaces ERPNext branding on the desk with **Kraya**:

| Where | Before | After |
|---|---|---|
| Apps screen (`/desk`) | "ERPNext" tile with the blue E | "Kraya" tile with the Kraya mark |
| Dock / sidebar app icon | Blue "E" | Kraya "k" mark |
| Any other ERPNext logo or "ERPNext" label drawn by the desk | ERPNext | Kraya |
| Default application logo, favicon, splash image | Frappe / ERPNext | Kraya (used when the settings fields are empty) |
| Other app tiles (Frappe HR, India Compliance, Insights) | Shown | Shown, or hidden if you list them in `HIDE_APPS` |

It changes **only what is displayed**. It adds no DocTypes, writes nothing to the
database and never edits documents, so uninstalling it restores the standard look.

Works with Frappe / ERPNext **version 16**.

---

## What is inside

```
kraya_branding/
├── pyproject.toml                 package definition
├── README.md                      this guide
├── license.txt                    MIT
└── kraya_branding/
    ├── __init__.py                version (1.0.0)
    ├── hooks.py                   wires everything into Frappe
    ├── branding.py                ← the only file you normally edit
    ├── api.py                     rebrands the apps screen list
    ├── boot.py                    rebrands app data sent at login
    ├── modules.txt / patches.txt  required by Frappe
    ├── config/ templates/         required by Frappe (empty)
    └── public/
        ├── css/kraya_branding.css
        ├── js/kraya_branding.js   browser-side fallback logo/name swap
        └── images/
            ├── kraya-logo.png     full "kraya" wordmark (transparent)
            ├── kraya-mark.svg     square "k" mark for icons and tiles
            ├── kraya-mark.png     same mark as PNG
            └── kraya-favicon.png  64×64 browser tab icon
```

### How it works

1. **`api.py`** overrides `frappe.apps.get_apps` (the list behind the apps screen):
   the ERPNext entry gets the Kraya title and mark, and apps in `HIDE_APPS` are dropped.
2. **`boot.py`** (`extend_bootinfo`) applies the same changes to the app data the
   desk receives at login, which feeds the dock and sidebar.
3. **`kraya_branding.js`** is a safety net in the browser: any `erpnext-logo.svg`
   image or exact "ERPNext" label that is still drawn gets swapped for Kraya.
   It skips input fields and editors, so typed text is never changed.
4. **`hooks.py`** also sets `app_logo_url`, `favicon` and `splash_image`
   defaults, so new sites look right even before the settings are filled in.

---

## Step 1 – Put the app on GitHub

1. Sign in to GitHub and create a **new repository** named `kraya_branding`.
   Private is fine; Frappe Cloud can read private repos through its GitHub app.
2. On your computer, unzip `kraya_branding.zip` and push it:

   ```bash
   cd kraya_branding
   git init
   git add .
   git commit -m "Kraya branding app v1.0.0"
   git branch -M version-16
   git remote add origin https://github.com/<your-account>/kraya_branding.git
   git push -u origin version-16
   ```

   Using a branch named `version-16` matches the Frappe and ERPNext branch names,
   which keeps Frappe Cloud's version checks happy. `main` also works.

Without git installed, you can create the repository on GitHub and use
**Add file → Upload files** to upload the unzipped folder contents, keeping the
folder structure, then create the `version-16` branch from the branch dropdown.

---

## Step 2 – Add the app on Frappe Cloud

> Custom apps need a **private bench group** (Frappe Cloud calls it a "Bench Group"
> or "Bench"). Sites on a shared/public bench cannot install custom apps. If your
> site `apex-khb-demo.nvi.frappe.cloud` is on a shared bench, first create a private
> bench group on version 16 with ERPNext, Frappe HR, India Compliance and Insights,
> then move the site to it (Site → Actions → Move to another bench / Change bench group).

1. Open the Frappe Cloud dashboard → **Benches** (Bench Groups) → your bench group.
2. Go to the **Apps** tab → **Add App**.
3. Choose **GitHub**. If asked, install / authorise the **Frappe Cloud GitHub app**
   for your account and give it access to the `kraya_branding` repository.
4. Pick the repository `kraya_branding` and branch `version-16`, then **Add**.
   Frappe Cloud validates the app (it reads `pyproject.toml` and `hooks.py`).
5. Click **Deploy** (or **Update available → Deploy**) on the bench group and wait
   for the build to finish. This usually takes a few minutes.

## Step 3 – Install it on the site

1. Dashboard → **Sites** → `apex-khb-demo` → **Apps** tab.
2. Click **Install App** → choose **Kraya Branding** → confirm.
3. When the job finishes, open the site and **log out and back in**
   (the app list is sent at login). Then do a hard refresh (Ctrl+Shift+R).

## Step 4 – Check the result

- `/desk` apps screen: the first tile reads **Kraya** with the k mark.
- Open Kraya: the dock / sidebar app icon is the k mark instead of the blue E.
- Browser tab: title "Kraya" (System Settings) and the Kraya icon.
- Hover tooltips and menus that said "ERPNext" now say "Kraya".

---

## Customising

Everything is in **`kraya_branding/branding.py`**:

```python
BRAND = {
    "title": "Kraya",                               # name on tile/tooltips
    "logo": f"{ASSET}/kraya-mark.svg",              # tile + dock icon
    "wordmark": f"{ASSET}/kraya-logo.png",          # default app logo
    "favicon": f"{ASSET}/kraya-favicon.png",
}

REBRAND_APPS = {"erpnext"}     # tiles that become "Kraya"
HIDE_APPS = set()              # e.g. {"insights", "india_compliance", "hrms"}
```

- **Hide tiles:** add app names to `HIDE_APPS`. Hidden apps still work by URL,
  and their permissions are unchanged: this only declutters the apps screen.
  App names: `erpnext`, `hrms`, `india_compliance`, `insights`.
- **New logo files:** replace the files in `public/images/` with the same names,
  or add new ones and point `BRAND` at them.

After any change: commit, push, then **Deploy** the bench group again on
Frappe Cloud. Users see the change after logging in again.

---

## Self-hosted bench (instead of Frappe Cloud)

```bash
cd ~/frappe-bench
bench get-app https://github.com/<your-account>/kraya_branding.git --branch version-16
bench --site <your-site> install-app kraya_branding
bench build --app kraya_branding
bench --site <your-site> clear-cache
bench restart        # production setups only
```

---

## Removing it

- **Frappe Cloud:** Site → Apps → Kraya Branding → **Uninstall**. Optionally remove
  it from the bench group's Apps tab and deploy.
- **Self-hosted:** `bench --site <your-site> uninstall-app kraya_branding`

The desk goes back to the standard ERPNext tiles and icon at the next login.
The logo fields set in Navbar Settings, Website Settings, System Settings and
Company are separate and stay as they are.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Tile still says ERPNext | Log out and back in, then hard refresh: app data is cached per session. |
| Images are broken (404) | The bench was not rebuilt. Redeploy on Frappe Cloud, or run `bench build --app kraya_branding`. |
| Frappe Cloud rejects the app | Check the branch name, and that `pyproject.toml` and `kraya_branding/hooks.py` are at the paths shown above. |
| "Install App" does not list Kraya Branding | The bench group was not deployed after adding the app, or the site is on a different bench group. |
| Navbar shows the old logo | Navbar Settings → Application Logo overrides `app_logo_url`; set it to the Kraya logo or clear it. |
