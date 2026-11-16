import re

configs = (
    ("demo-auto-dealership", "buyers", "Enrolling 15% of Sales-Only buyers into Pre-Paid Maintenance adds ~$880K in cumulative 3-yr Fixed-Ops & trade-in gross."),
    ("demo-dental-wellness", "patients", "Enrolling 15% of Standard Insurance patients into the In-House Wellness Plan adds ~$720K in recurring collections."),
    ("demo-freight-logistics", "accounts", "Converting 20% of Spot Shippers onto Dedicated Portal Contracts adds ~$1.4M in recurring freight margin."),
    ("demo-legal-partners", "matters", "Transitioning 20% of Standard Hourly clients onto Evergreen Retainers adds ~$680K in realized fees."),
    ("demo-hvac-mechanical", "homeowners", "Converting 15% of On-Demand callers into Comfort Club members adds ~$640K in recurring multi-year revenue."),
    ("demo-electrical-supply", "accounts", "Converting 25 Counter-Only contractors to Portal ordering adds ~$1.8M in incremental pull-through revenue.")
)

for folder, unit, qw in configs:
    js_path = f"{folder}/app.js"
    html_path = f"{folder}/dashboard.html"
    try:
        js = open(js_path, encoding="utf-8").read()
        js = re.sub(r"Quick Win:[^'\"]+", f"Quick Win: {qw}", js)
        js = re.sub(r"\bdonors\b", unit, js, flags=re.IGNORECASE)
        js = re.sub(r"\bdonor\b", unit.rstrip("s"), js, flags=re.IGNORECASE)
        js = re.sub(r"\bvolunteers?\b", "loyal accounts", js, flags=re.IGNORECASE)
        open(js_path, "w", encoding="utf-8").write(js)

        html = open(html_path, encoding="utf-8").read()
        html = re.sub(r'src="app\.js[^"]*"', 'src="app.js?v=3"', html)
        open(html_path, "w", encoding="utf-8").write(html)
        print("UPDATED & CACHE-BUSTED:", folder)
    except Exception as e:
        print("Skipped:", folder, e)
