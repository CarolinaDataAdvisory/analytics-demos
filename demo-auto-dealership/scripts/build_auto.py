import json
import os
import random
import sqlite3

random.seed(505)
os.makedirs("demo-auto-dealership", exist_ok=True)
db_path = "demo-auto-dealership/auto_dealership.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE customers (
    cust_id TEXT PRIMARY KEY,
    cust_name TEXT,
    loyalty_tier TEXT,
    rooftop TEXT,
    advisor TEXT
);
CREATE TABLE deals (
    tx_id TEXT PRIMARY KEY,
    cust_id TEXT,
    tx_date TEXT,
    dept TEXT,
    gross_rev REAL,
    gross_profit REAL
);
CREATE TABLE alerts (
    prio INTEGER,
    alert_type TEXT,
    ref_id TEXT,
    entity_name TEXT,
    owner TEXT,
    dollar_impact REAL,
    due_date TEXT
);
""")

firsts = ("Marcus", "Lauren", "Brandon", "Ashley", "Tyler", "Megan", "Jordan", "Brittany", "Cameron", "Kayla", "Austin", "amber", "Trevor", "Courtney", "Garrett", "Danielle", "Logan", "brianna", "Chase", "Kelsey")
lasts = ("Hendricks", "Earnhardt", "Gordon", "Johnson", "Byron", "Bowman", "Larson", "Elliott", "Hamlin", "Truex", "Logano", "Blaney", "Busch", "Harvick", "Chastain", "Wallace", "Reddick", "Bell", "Gibbs", "Penske")
rooftops = ("Concord Chevrolet Buick GMC", "Charlotte Honda & Acura", "Salisbury Ford Lincoln", "Lake Norman Toyota & Lexus")
advisors = ("M. Vance (Fixed Ops Dir)", "R. Sterling (Used Car Mgr)", "J. Carter (F&I Director)", "S. Jenkins (BDC Manager)", "T. Brooks (Master Service Adv)")

customers = list()
for i in range(1, 2101):
    cid = f"DMS-{5000 + i}"
    cname = f"{random.choice(firsts).title()} {random.choice(lasts)} (#{100+i})"
    ltier = "Sales + Service Loyal" if random.random() < 0.39 else "Sales Only / One-Time"
    rtop = random.choice(rooftops)
    adv = random.choice(advisors)
    customers.append((cid, cname, ltier, rtop, adv))

cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)

depts = (
    ("F&I Products & Warranties", 0.815, 1650, 3400),
    ("Service Labor & Mechanical", 0.675, 420, 1850),
    ("Parts & Collision Wholesale", 0.345, 380, 1600),
    ("Pre-Owned Vehicle Retail", 0.088, 24500, 38500),
    ("New Vehicle Retail", 0.062, 36000, 56000)
)

deals = list()
tx_num = 100000
lapsed_ids = set(next(iter(c)) for idx, c in enumerate(customers) if idx < 220)

for m_idx in range(36):
    yr = 2024 + (m_idx // 12)
    mo = (m_idx % 12) + 1
    season = 1.24 if mo in (3, 5, 6, 7, 8, 11, 12) else 0.90
    growth = 1.0 + (yr - 2024) * 0.085
    n_tx = int(420 * season * growth)
    for _ in range(n_tx):
        tx_num += 1
        c = random.choice(customers)
        cid, cname, ltier, rtop, adv = c
        if cid in lapsed_ids and yr == 2026 and mo >= 7:
            continue
        day = random.randint(1, 28)
        tdate = f"{yr}-{mo:02d}-{day:02d}"
        dept, gm_rate, lo_v, hi_v = random.choices(depts, weights=(18, 36, 16, 16, 14)).pop(0)
        mult = 1.32 if ltier == "Sales + Service Loyal" else 1.0
        rev = round(random.uniform(lo_v, hi_v) * mult, 2)
        gp = round(rev * (gm_rate + random.uniform(-0.012, 0.015)), 2)
        deals.append((f"TX-{tx_num}", cid, tdate, dept, rev, gp))

cur.executemany("INSERT INTO deals VALUES (?,?,?,?,?,?)", deals)

alert_rows = list()
for i in range(1, 26):
    cid, cname, ltier, rtop, adv = customers[i * 5]
    amt = round(random.uniform(28000, 46500), 2)
    alert_rows.append((1, "Aged Lot >45d", f"STK-{400+i}", f"Pre-Owned Unit #{400+i} — {rtop}", "Used Car Director", amt, f"2026-11-{1 + (i % 14):02d}"))

for i in range(1, 32):
    cid, cname, ltier, rtop, adv = customers[i * 7]
    amt = round(random.uniform(850, 3200), 2)
    alert_rows.append((2, "Declined MPI", f"RO-{7000+i}", f"{cname} — Declined Brake/30K Service", "Service BDC Desk", amt, f"2026-11-{1 + (i % 14):02d}"))

for i in range(1, 22):
    cid, cname, ltier, rtop, adv = customers[i * 9]
    amt = round(random.uniform(18500, 42000), 2)
    alert_rows.append((3, "Unfunded CIT", f"CIT-{900+i}", f"{cname} — Lender Stipulations Open (7d+)", "F&I / Controller", amt, f"2026-11-{1 + (i % 14):02d}"))

cur.executemany("INSERT INTO alerts VALUES (?,?,?,?,?,?,?)", alert_rows)
conn.commit()

rev_series = tuple(tuple(r) for r in cur.execute("SELECT substr(tx_date,1,7), COUNT(*), ROUND(SUM(gross_rev),2), ROUND(SUM(gross_profit),2) FROM deals GROUP BY 1 ORDER BY 1").fetchall())
loy_mult = tuple(tuple(r) for r in cur.execute("WITH s AS (SELECT cust_id, COUNT(*) t_cnt, SUM(gross_rev) tot_rev, SUM(gross_profit) tot_gp FROM deals GROUP BY 1) SELECT c.loyalty_tier, COUNT(*), ROUND(AVG(s.t_cnt),1), ROUND(AVG(s.tot_gp),2), ROUND(AVG(s.tot_rev),2) FROM customers c JOIN s ON c.cust_id=s.cust_id GROUP BY 1 ORDER BY 4 DESC").fetchall())
dept_perf = tuple(tuple(r) for r in cur.execute("SELECT dept, COUNT(*), ROUND(SUM(gross_rev),2), ROUND(SUM(gross_profit),2), ROUND(SUM(gross_profit)/SUM(gross_rev)*100,1) gm_pct FROM deals GROUP BY 1 ORDER BY gm_pct DESC").fetchall())
roof_perf = tuple(tuple(r) for r in cur.execute("SELECT c.rooftop, COUNT(DISTINCT c.cust_id), ROUND(SUM(d.gross_rev),2), ROUND(SUM(d.gross_profit),2), ROUND(SUM(d.gross_profit)/SUM(d.gross_rev)*100,1) gm_pct FROM customers c JOIN deals d ON c.cust_id=d.cust_id GROUP BY 1 ORDER BY 3 DESC").fetchall())

churn_all = tuple(tuple(r) for r in cur.execute("SELECT c.cust_id, c.cust_name, c.rooftop, c.loyalty_tier, ROUND(SUM(d.gross_profit),2) ltv, MAX(d.tx_date) last_tx, CAST(julianday('2026-12-31') - julianday(MAX(d.tx_date)) AS INTEGER) days_lapsed FROM deals d JOIN customers c ON d.cust_id=c.cust_id GROUP BY 1,2,3,4 HAVING ltv >= 2800 AND days_lapsed >= 150 ORDER BY ltv DESC").fetchall())
churn_top = tuple(r for idx, r in enumerate(churn_all) if idx < 15)
churn_pool = round(sum(float(r.pop(4)) for r in (list(x) for x in churn_all)), 2)

tot_custs = next(iter(cur.execute("SELECT COUNT(DISTINCT cust_id) FROM deals").fetchone()))
c_2025 = next(iter(cur.execute("SELECT COUNT(DISTINCT cust_id) FROM deals WHERE substr(tx_date,1,4)='2025'").fetchone()))
c_2026 = next(iter(cur.execute("SELECT COUNT(DISTINCT cust_id) FROM deals WHERE substr(tx_date,1,4)='2026'").fetchone()))

funnel = (
    ("Internet Leads", 3420),
    ("BDC Contacted", 2580),
    ("Showroom Appts", 1390),
    ("Stalled Leads", 340),
    ("15% Units Won", 51)
)

all_alerts = tuple(tuple(x for idx, x in enumerate(r) if idx > 0) for r in cur.execute("SELECT prio, alert_type, ref_id, entity_name, owner, dollar_impact, due_date FROM alerts ORDER BY prio ASC, dollar_impact DESC").fetchall())

payload = json.dumps(dict(
    rev=rev_series,
    vol=loy_mult,
    prog=dept_perf,
    camp=roof_perf,
    churn=churn_top,
    churnCount=len(churn_all),
    churnPoolLtv=churn_pool,
    alerts=all_alerts,
    donorStats=dict(totalUnique=tot_custs, active2025=c_2025, active2026=c_2026, netChange=c_2026 - c_2025, pctChange=round((c_2026 - c_2025) / c_2025 * 100, 1)),
    funnel=funnel
))

with open("demo-auto-dealership/data.js", "w", encoding="utf-8") as f:
    f.write("window.DASH_DATA=" + payload + ";")

print("DEALERSHIP DATA READY! Customers:", tot_custs, "| Equity & Service Watchlist:", len(churn_all))
