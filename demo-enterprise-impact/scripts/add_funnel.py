import json, sqlite3

conn = sqlite3.connect("demo-enterprise-impact/enterprise_impact.db")
cur = conn.cursor()

rows = cur.execute("SELECT touchpoint_type, COUNT(*) FROM digital_engagement GROUP BY 1").fetchall()
counts = {r: r for r in rows}
abandoned = counts.get("Donation Page Abandoned", 1500)
reports = counts.get("Impact Report Downloaded", 1950)
webinars = counts.get("Webinar Attended", 1500)
clicks = counts.get("Email Click", 3300)
opens = counts.get("Email Open", 6750)

p = "demo-enterprise-impact/data.js"
raw = open(p, encoding="utf-8").read().replace("window.DASH_DATA=", "").rstrip(";")
data = json.loads(raw)
data["funnel"] = [
    ["Email Opens", opens],
    ["Email Clicks", clicks],
    ["Impact Reports & Webinars", reports + webinars],
    ["Abandoned Checkout", abandoned],
    ["Recovered Opportunity (15%)", round(abandoned * 0.15)]
]
open(p, "w", encoding="utf-8").write("window.DASH_DATA=" + json.dumps(data) + ";")
print("FUNNEL DATA EXPORTED!", data["funnel"])
