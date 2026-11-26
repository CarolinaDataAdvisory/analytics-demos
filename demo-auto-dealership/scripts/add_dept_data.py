import json

p = "demo-auto-dealership/data.js"
raw = open(p, encoding="utf-8").read().strip()
payload = json.loads(raw.replace("window.DASH_DATA=", "").rstrip(";"))

# Service Advisors: Name, Rooftop, Closed ROs, Customer-Pay Gross ($), Warranty Gross ($), Hours/RO, Effective Labor Rate ($)
payload["serviceAdvisors"] = (
    ("T. Brooks (Master Adv)", "Charlotte Honda & Acura", 1420, 612400, 248600, 2.6, 168),
    ("M. Vance (Sr Advisor)", "Concord Chevrolet Buick GMC", 1310, 548200, 219400, 2.4, 162),
    ("K. Mercer (Service Adv)", "Lake Norman Toyota & Lexus", 1185, 489500, 198200, 2.3, 159),
    ("D. Kowalski (Express/Main)", "Salisbury Ford Lincoln", 1040, 384800, 164200, 1.9, 148),
    ("R. Morales (Service Adv)", "Concord Chevrolet Buick GMC", 960, 345600, 151800, 1.8, 145)
)

# Parts Channels: Channel Name, Rooftop, Orders/ROs, Gross Sales ($), Gross Profit ($), Margin %, Obsolescence/Aged ($)
payload["partsChannels"] = (
    ("Service Repair Order (Internal/CP)", "All 4 Rooftops", 18450, 4820000, 1879800, 39.0, 42000),
    ("Wholesale Collision & Body Shops", "Charlotte & Concord Hubs", 9640, 3640000, 1055600, 29.0, 68500),
    ("Retail Counter & Accessories", "All 4 Rooftops", 4120, 1290000, 477300, 37.0, 31000),
    ("Warranty & Recall Parts", "All 4 Rooftops", 5280, 1680000, 537600, 32.0, 18500)
)

open(p, "w", encoding="utf-8").write("window.DASH_DATA=" + json.dumps(payload) + ";")
print("ADDED SERVICE ADVISOR & PARTS DATA!")
