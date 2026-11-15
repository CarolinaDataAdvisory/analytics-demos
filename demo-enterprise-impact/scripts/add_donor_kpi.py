import json, sqlite3

conn = sqlite3.connect("demo-enterprise-impact/enterprise_impact.db")
cur = conn.cursor()

tot_donors = next(iter(cur.execute("SELECT COUNT(DISTINCT constituent_id) FROM donations WHERE amount > 0").fetchone()))
d_2025 = next(iter(cur.execute("SELECT COUNT(DISTINCT constituent_id) FROM donations WHERE amount > 0 AND substr(donation_date, 1, 4) = '2025'").fetchone()))
d_2026 = next(iter(cur.execute("SELECT COUNT(DISTINCT constituent_id) FROM donations WHERE amount > 0 AND substr(donation_date, 1, 4) = '2026'").fetchone()))
net_change = d_2026 - d_2025
pct_change = round((net_change / d_2025) * 100, 1) if d_2025 else 0

p = "demo-enterprise-impact/data.js"
raw = open(p, encoding="utf-8").read().replace("window.DASH_DATA=", "").rstrip(";")
data = json.loads(raw)
data["donorStats"] = {"totalUnique": tot_donors, "active2025": d_2025, "active2026": d_2026, "netChange": net_change, "pctChange": pct_change}
open(p, "w", encoding="utf-8").write("window.DASH_DATA=" + json.dumps(data) + ";")
print(f"DONOR KPI READY! Total Unique: {tot_donors:,} | 2026 Active: {d_2026:,} ({net_change:+,} vs 2025)")
