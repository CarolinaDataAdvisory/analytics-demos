import json

p = "demo-auto-dealership/data.js"
raw = open(p, encoding="utf-8").read().strip()
payload = json.loads(raw.replace("window.DASH_DATA=", "").rstrip(";"))

# Salespeople: Name, Rooftop, New Units, Used Units, Front Gross ($), Avg Front PVR ($)
payload["salesReps"] = (
    ("D. Maillie (Top Producer)", "Charlotte Honda & Acura", 184, 162, 648400, 1874),
    ("T. Vance (Sr Sales)", "Concord Chevrolet Buick GMC", 152, 138, 498800, 1720),
    ("M. Carter (Internet/BDC)", "Lake Norman Toyota & Lexus", 146, 129, 442750, 1610),
    ("J. Brooks (Floor Sales)", "Salisbury Ford Lincoln", 118, 134, 390600, 1550),
    ("R. Holloway (Pre-Owned)", "Concord Chevrolet Buick GMC", 74, 158, 368880, 1590),
    ("K. Sterling (Sales Rep)", "Charlotte Honda & Acura", 108, 102, 289800, 1380),
    ("A. Mendez (Junior Rep)", "Salisbury Ford Lincoln", 82, 79, 178710, 1110)
)

# Finance Managers: Name, Rooftop, Deals Turned, VSC/Warranty ($), GAP ($), Paint/Tire/Ancillary ($), Total Backend Gross ($), Backend PVR ($)
payload["fiManagers"] = (
    ("M. Ricks (F&I Director)", "Charlotte Honda & Acura", 412, 395520, 189520, 148320, 733360, 1780),
    ("S. Bowles (Sr F&I Mgr)", "Charlotte Honda & Acura", 378, 343980, 166320, 128520, 638820, 1690),
    ("B. McDaniel (Desk / F&I)", "Concord Chevrolet Buick GMC", 356, 309720, 149520, 117480, 576720, 1620),
    ("C. Jenkins (F&I Mgr)", "Lake Norman Toyota & Lexus", 324, 265680, 126360, 93960, 486000, 1500),
    ("L. Kowalski (F&I Mgr)", "Salisbury Ford Lincoln", 285, 208050, 96900, 71250, 376200, 1320)
)

open(p, "w", encoding="utf-8").write("window.DASH_DATA=" + json.dumps(payload) + ";")
print("ADDED SALES & F&I DESK DATA TO CAROLINAS AUTO GROUP!")
