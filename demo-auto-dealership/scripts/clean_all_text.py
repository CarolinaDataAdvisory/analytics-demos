# 1. Dealership-specific fixes
p_auto = "demo-auto-dealership/app.js"
s = open(p_auto, encoding="utf-8").read()
s = s.replace(" donors | ", " buyers | ")
s = s.replace(
    "Converting 10% of Donor-Only supporters into volunteers adds ~$550K in cumulative lifetime giving.",
    "Enrolling 15% of Sales-Only buyers into Pre-Paid Maintenance adds ~$880K in cumulative 3-yr Fixed-Ops & trade-in gross."
)
s = s.replace("donors", "buyers")
open(p_auto, "w", encoding="utf-8").write(s)

# 2. Clean sweep across the other 5 commercial demos just in case
fixes = (
    ("demo-dental-wellness", " patients | ", "Enrolling 15% of Standard Insurance patients into the In-House Wellness Plan adds ~$720K in recurring collections."),
    ("demo-freight-logistics", " accounts | ", "Converting 20% of Spot Shippers onto Dedicated Portal Contracts adds ~$1.4M in recurring freight margin."),
    ("demo-legal-partners", " matters | ", "Transitioning 20% of Standard Hourly clients onto Evergreen Retainers adds ~$680K in realized fees."),
    ("demo-hvac-mechanical", " homeowners | ", "Converting 15% of On-Demand callers into Comfort Club members adds ~$640K in recurring multi-year revenue."),
    ("demo-electrical-supply", " accounts | ", "Converting 25 Counter-Only contractors to Portal ordering adds ~$1.8M in incremental pull-through revenue.")
)

for folder, unit_lbl, qw_text in fixes:
    path = f"{folder}/app.js"
    try:
        txt = open(path, encoding="utf-8").read()
        txt = txt.replace(" donors | ", unit_lbl)
        txt = txt.replace("Converting 10% of Donor-Only supporters into volunteers adds ~$550K in cumulative lifetime giving.", qw_text)
        txt = txt.replace("donors", unit_lbl.strip().strip("|").strip())
        open(path, "w", encoding="utf-8").write(txt)
        print("CLEANED:", folder)
    except Exception as e:
        print("Skipped:", folder, e)
