import json
import os
import random
import sqlite3

random.seed(606)
os.makedirs("demo-precision-mfg", exist_ok=True)
db_path = "demo-precision-mfg/precision_mfg.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE customers (
    cust_id TEXT PRIMARY KEY,
    oem_name TEXT,
    contract_model TEXT,
    industry_sector TEXT,
    acct_engineer TEXT
);
CREATE TABLE work_orders (
    wo_id TEXT PRIMARY KEY,
    cust_id TEXT,
    ship_date TEXT,
    work_center TEXT,
    shipped_rev REAL,
    gross_margin REAL
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

prefixes = ("Piedmont", "Rowan", "Cabarrus", "Carolina", "Iredell", "Catawba", "Metrolina", "Triad", "Blue Ridge", "Salisbury", "Concord", "Statesville", "Mooresville", "Yadkin", "Tar Heel", "Queen City")
suffixes = ("Aerospace Systems", "Heavy Equipment", "Automation OEM", "Defense Components", "Industrial Machinery", "Powertrain Mfg", "Fluid Controls", "Medical Devices", "Commercial HVAC Mfg", "Energy Enclosures")
work_centers = (
    ("5-Axis CNC Precision Machining", 0.345, 8500, 24000),
    ("Laser Cutting & Sheet Metal Fab", 0.295, 5200, 16500),
    ("Robotic Welding & Sub-Assembly", 0.278, 6800, 21000),
    ("Powder Coating & Finishing", 0.315, 2400, 7500),
    ("Prototype & Quick-Turn Tooling", 0.380, 3500, 11500)
)
engineers = ("R. Vance (VP Mfg & Estimating)", "M. Kowalski (CNC Plant Mgr)", "D. Chen (Lead Cost Estimator)", "S. Holloway (OEM Sales Dir)", "T. Brooks (Quality & Scrap Lead)")

customers = list()
for i in range(1, 381):
    cid = f"OEM-{7000 + i}"
    oname = f"{random.choice(prefixes)} {random.choice(suffixes)} #{i}" if i > 160 else f"{prefixes[i % len(prefixes)]} {suffixes[i % len(suffixes)]}"
    cmodel = "Annual Blanket PO + VMI" if random.random() < 0.36 else "Spot / One-Off PO"
    sec = next(iter(random.choice(work_centers)))
    eng = random.choice(engineers)
    customers.append((cid, oname, cmodel, sec, eng))

cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)

wos = list()
wo_num = 200000
lapsed_ids = set(next(iter(c)) for idx, c in enumerate(customers) if idx < 42)

for m_idx in range(36):
    yr = 2024 + (m_idx // 12)
    mo = (m_idx % 12) + 1
    season = 1.18 if mo in (3, 4, 5, 9, 10, 11) else 0.92
    growth = 1.0 + (yr - 2024) * 0.092
    n_wos = int(165 * season * growth)
    for _ in range(n_wos):
        wo_num += 1
        c = random.choice(customers)
        cid, oname, cmodel, sec, eng = c
        if cid in lapsed_ids and yr == 2026 and mo >= 8:
            continue
        day = random.randint(1, 28)
        sdate = f"{yr}-{mo:02d}-{day:02d}"
        wc, gm_rate, lo_v, hi_v = random.choice(work_centers)
        mult = 1.72 if cmodel == "Annual Blanket PO + VMI" else 1.0
        rev = round(random.uniform(lo_v, hi_v) * mult, 2)
        gm = round(rev * (gm_rate + random.uniform(-0.025, 0.03)), 2)
        wos.append((f"WO-{wo_num}", cid, sdate, wc, rev, gm))

cur.executemany("INSERT INTO work_orders VALUES (?,?,?,?,?,?)", wos)

alert_rows = list()
for i in range(1, 22):
    cid, oname, cmodel, sec, eng = customers[i * 4]
    amt = round(random.uniform(6800, 24500), 2)
    alert_rows.append((1, "Margin Variance", f"JOB-{400+i}", f"{oname} — Actual Labor +14% vs Quote", "Lead Cost Estimator", amt, f"2026-11-{1 + (i % 14):02d}"))

for i in range(1, 19):
    cid, oname, cmodel, sec, eng = customers[i * 6]
    amt = round(random.uniform(3200, 14800), 2)
    alert_rows.append((2, "Scrap / Rework", f"NCR-{700+i}", f"{oname} — CNC Tolerance Rework Lot", "Quality & Scrap Lead", amt, f"2026-11-{1 + (i % 14):02d}"))

for i in range(1, 38):
    cid, oname, cmodel, sec, eng = customers[i * 8]
    amt = round(random.uniform(14000, 52000), 2)
    alert_rows.append((3, "Blanket Renewal", f"BLK-{900+i}", f"{oname} — Annual Steel/Alum Price Reset", "OEM Sales Director", amt, f"2026-12-{1 + (i % 28):02d}"))

cur.executemany("INSERT INTO alerts VALUES (?,?,?,?,?,?,?)", alert_rows)
conn.commit()

rev_series = tuple(tuple(r) for r in cur.execute("SELECT substr(ship_date,1,7), COUNT(*), ROUND(SUM(shipped_rev),2), ROUND(SUM(gross_margin),2) FROM work_orders GROUP BY 1 ORDER BY 1").fetchall())
po_mult = tuple(tuple(r) for r in cur.execute("WITH s AS (SELECT cust_id, COUNT(*) w_cnt, SUM(shipped_rev) tot_rev, SUM(gross_margin) tot_gm FROM work_orders GROUP BY 1) SELECT c.contract_model, COUNT(*), ROUND(AVG(s.w_cnt),1), ROUND(AVG(s.tot_rev),2), ROUND(AVG(s.tot_gm),2) FROM customers c JOIN s ON c.cust_id=s.cust_id GROUP BY 1 ORDER BY 4 DESC").fetchall())
wc_perf = tuple(tuple(r) for r in cur.execute("SELECT work_center, COUNT(*), ROUND(SUM(shipped_rev),2), ROUND(SUM(gross_margin),2), ROUND(SUM(gross_margin)/SUM(shipped_rev)*100,1) gm_pct FROM work_orders GROUP BY 1 ORDER BY gm_pct DESC").fetchall())
eng_perf = tuple(tuple(r) for r in cur.execute("SELECT c.acct_engineer, COUNT(DISTINCT c.cust_id), ROUND(SUM(w.shipped_rev),2), ROUND(SUM(w.gross_margin),2), ROUND(SUM(w.gross_margin)/SUM(w.shipped_rev)*100,1) gm_pct FROM customers c JOIN work_orders w ON c.cust_id=w.cust_id GROUP BY 1 ORDER BY 3 DESC").fetchall())

churn_all = tuple(tuple(r) for r in cur.execute("SELECT c.cust_id, c.oem_name, c.industry_sector, c.acct_engineer, ROUND(SUM(w.shipped_rev),2) ltv, MAX(w.ship_date) last_ship, CAST(julianday('2026-12-31') - julianday(MAX(w.ship_date)) AS INTEGER) days_lapsed FROM work_orders w JOIN customers c ON w.cust_id=c.cust_id GROUP BY 1,2,3,4 HAVING ltv >= 65000 AND days_lapsed >= 105 ORDER BY ltv DESC").fetchall())
churn_top = tuple(r for idx, r in enumerate(churn_all) if idx < 15)
churn_pool = round(sum(float(r.pop(4)) for r in (list(x) for x in churn_all)), 2)

tot_oems = next(iter(cur.execute("SELECT COUNT(DISTINCT cust_id) FROM work_orders").fetchone()))
o_2025 = next(iter(cur.execute("SELECT COUNT(DISTINCT cust_id) FROM work_orders WHERE substr(ship_date,1,4)='2025'").fetchone()))
o_2026 = next(iter(cur.execute("SELECT COUNT(DISTINCT cust_id) FROM work_orders WHERE substr(ship_date,1,4)='2026'").fetchone()))

funnel = (
    ("OEM RFQs Received", 1180),
    ("CAD / DFM Reviewed", 960),
    ("Formal Quotes Sent", 740),
    ("Stalled RFQs (>14d)", 215),
    ("15% POs Won", 32)
)

all_alerts = tuple(tuple(x for idx, x in enumerate(r) if idx > 0) for r in cur.execute("SELECT prio, alert_type, ref_id, entity_name, owner, dollar_impact, due_date FROM alerts ORDER BY prio ASC, dollar_impact DESC").fetchall())

payload = json.dumps(dict(
    rev=rev_series,
    vol=po_mult,
    prog=wc_perf,
    camp=eng_perf,
    churn=churn_top,
    churnCount=len(churn_all),
    churnPoolLtv=churn_pool,
    alerts=all_alerts,
    donorStats=dict(totalUnique=tot_oems, active2025=o_2025, active2026=o_2026, netChange=o_2026 - o_2025, pctChange=round((o_2026 - o_2025) / o_2025 * 100, 1)),
    funnel=funnel
))

with open("demo-precision-mfg/data.js", "w", encoding="utf-8") as f:
    f.write("window.DASH_DATA=" + payload + ";")

print("MANUFACTURING DATA READY! OEMs:", tot_oems, "| Lapsed Pool:", len(churn_all))
