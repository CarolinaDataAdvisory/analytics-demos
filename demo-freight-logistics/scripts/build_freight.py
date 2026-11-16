import json
import os
import random
import sqlite3

random.seed(315)
os.makedirs("demo-freight-logistics", exist_ok=True)
db_path = "demo-freight-logistics/freight_logistics.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE shippers (
    shipper_id TEXT PRIMARY KEY,
    account_name TEXT,
    contract_type TEXT,
    division TEXT,
    account_mgr TEXT
);
CREATE TABLE loads (
    load_id TEXT PRIMARY KEY,
    shipper_id TEXT,
    load_date TEXT,
    division TEXT,
    freight_rev REAL,
    net_margin REAL
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

prefixes = ("Piedmont", "Cabarrus", "Rowan", "I-85", "Carolina", "Metrolina", "Queen City", "Salisbury", "Concord", "Catawba", "Triad", "Yadkin", "Blue Ridge", "Tar Heel", "Stanly", "Iredell")
suffixes = ("Distribution", "Manufacturing", "Retail Supply", "Building Materials", "Foodservice", "Industrial Packaging", "Medical Supply", "Logistics Group", "Commercial Warehousing", "Beverage Co.")
divisions = (
    ("Dedicated Regional Freight", 0.245, 1650, 4200),
    ("Commercial Fleet & Box Rentals", 0.340, 1200, 3800),
    ("Final-Mile & White-Glove Delivery", 0.275, 950, 2900),
    ("Commercial Office & Plant Moving", 0.310, 2400, 6800),
    ("Spot & Brokered Backhauls", 0.142, 850, 2200)
)
mgrs = ("D. Kowalski (VP Fleet Ops)", "T. Jenkins (Dedicated Sales)", "R. Morales (Rentals & Leasing)", "K. Vance (Final-Mile Dispatch)", "B. Mercer (Commercial Moving)")

shippers = list()
for i in range(1, 521):
    sid = f"SHP-{6000 + i}"
    aname = f"{random.choice(prefixes)} {random.choice(suffixes)} #{i}" if i > 160 else f"{prefixes[i % len(prefixes)]} {suffixes[i % len(suffixes)]}"
    ctype = "Dedicated Contract + Portal" if random.random() < 0.35 else "Spot / On-Call Shipper"
    div = next(iter(random.choice(divisions)))
    mgr = random.choice(mgrs)
    shippers.append((sid, aname, ctype, div, mgr))

cur.executemany("INSERT INTO shippers VALUES (?,?,?,?,?)", shippers)

loads = list()
lid_num = 70000
lapsed_ids = set(next(iter(s)) for idx, s in enumerate(shippers) if idx < 58)

for m_idx in range(36):
    yr = 2024 + (m_idx // 12)
    mo = (m_idx % 12) + 1
    season = 1.22 if mo in (5, 6, 8, 9, 10, 11) else 0.91
    growth = 1.0 + (yr - 2024) * 0.09
    n_loads = int(560 * season * growth)
    for _ in range(n_loads):
        lid_num += 1
        s = random.choice(shippers)
        sid, aname, ctype, div, mgr = s
        if sid in lapsed_ids and yr == 2026 and mo >= 8:
            continue
        day = random.randint(1, 28)
        ldate = f"{yr}-{mo:02d}-{day:02d}"
        _, margin_rate, lo_v, hi_v = random.choice(divisions)
        mult = 1.75 if ctype == "Dedicated Contract + Portal" else 1.0
        rev = round(random.uniform(lo_v, hi_v) * mult, 2)
        gm = round(rev * (margin_rate + random.uniform(-0.025, 0.03)), 2)
        loads.append((f"LD-{lid_num}", sid, ldate, div, rev, gm))

cur.executemany("INSERT INTO loads VALUES (?,?,?,?,?,?)", loads)

alert_rows = list()
for i in range(1, 24):
    sid, aname, ctype, div, mgr = shippers[i * 4]
    amt = round(random.uniform(1800, 9400), 2)
    alert_rows.append((1, "Unbilled Detention", f"DET-{400+i}", f"{aname} — Layover & Liftgate Fees", mgr, amt, f"2026-11-{1 + (i % 14):02d}"))

for i in range(1, 21):
    sid, aname, ctype, div, mgr = shippers[i * 7]
    amt = round(random.uniform(3500, 14500), 2)
    alert_rows.append((2, "Idle / Low Margin", f"TRK-{200+i}", f"{aname} — High Deadhead Lane (<12% GM)", "Fleet Dispatch Desk", amt, f"2026-11-{1 + (i % 14):02d}"))

for i in range(1, 55):
    sid, aname, ctype, div, mgr = shippers[i * 9]
    amt = round(random.uniform(2200, 18900), 2)
    alert_rows.append((3, "Overdue Freight AR", f"INV-{9000+i}", f"{aname} — Past Due Net-30", "Billing & Collections", amt, f"2026-10-{1 + (i % 28):02d}"))

cur.executemany("INSERT INTO alerts VALUES (?,?,?,?,?,?,?)", alert_rows)
conn.commit()

rev_series = tuple(tuple(r) for r in cur.execute("SELECT substr(load_date,1,7), COUNT(*), ROUND(SUM(freight_rev),2), ROUND(SUM(net_margin),2) FROM loads GROUP BY 1 ORDER BY 1").fetchall())
cont_mult = tuple(tuple(r) for r in cur.execute("WITH s AS (SELECT shipper_id, COUNT(*) l_cnt, SUM(freight_rev) tot_rev, SUM(net_margin) tot_gm FROM loads GROUP BY 1) SELECT c.contract_type, COUNT(*), ROUND(AVG(s.l_cnt),1), ROUND(AVG(s.tot_rev),2), ROUND(AVG(s.tot_gm),2) FROM shippers c JOIN s ON c.shipper_id=s.shipper_id GROUP BY 1 ORDER BY 4 DESC").fetchall())
div_perf = tuple(tuple(r) for r in cur.execute("SELECT division, COUNT(*), ROUND(SUM(freight_rev),2), ROUND(SUM(net_margin),2), ROUND(SUM(net_margin)/SUM(freight_rev)*100,1) gm_pct FROM loads GROUP BY 1 ORDER BY gm_pct DESC").fetchall())
mgr_perf = tuple(tuple(r) for r in cur.execute("SELECT c.account_mgr, COUNT(DISTINCT c.shipper_id), ROUND(SUM(l.freight_rev),2), ROUND(SUM(l.net_margin),2), ROUND(SUM(l.net_margin)/SUM(l.freight_rev)*100,1) gm_pct FROM shippers c JOIN loads l ON c.shipper_id=l.shipper_id GROUP BY 1 ORDER BY 3 DESC").fetchall())

churn_all = tuple(tuple(r) for r in cur.execute("SELECT c.shipper_id, c.account_name, c.division, c.account_mgr, ROUND(SUM(l.freight_rev),2) ltv, MAX(l.load_date) last_load, CAST(julianday('2026-12-31') - julianday(MAX(l.load_date)) AS INTEGER) days_lapsed FROM loads l JOIN shippers c ON l.shipper_id=c.shipper_id GROUP BY 1,2,3,4 HAVING ltv >= 22000 AND days_lapsed >= 110 ORDER BY ltv DESC").fetchall())
churn_top = tuple(r for idx, r in enumerate(churn_all) if idx < 15)
churn_pool = round(sum(float(r.pop(4)) for r in (list(x) for x in churn_all)), 2)

tot_shps = next(iter(cur.execute("SELECT COUNT(DISTINCT shipper_id) FROM loads").fetchone()))
s_2025 = next(iter(cur.execute("SELECT COUNT(DISTINCT shipper_id) FROM loads WHERE substr(load_date,1,4)='2025'").fetchone()))
s_2026 = next(iter(cur.execute("SELECT COUNT(DISTINCT shipper_id) FROM loads WHERE substr(load_date,1,4)='2026'").fetchone()))

funnel = (
    ("Freight & Rental RFQs", 1640),
    ("Lane & Fleet Priced", 1310),
    ("Rate Quotes Issued", 940),
    ("Stalled RFQs (>10 Days)", 275),
    ("15% Quote Recovery", 41)
)

all_alerts = tuple(tuple(x for idx, x in enumerate(r) if idx > 0) for r in cur.execute("SELECT prio, alert_type, ref_id, entity_name, owner, dollar_impact, due_date FROM alerts ORDER BY prio ASC, dollar_impact DESC").fetchall())

payload = json.dumps(dict(
    rev=rev_series,
    vol=cont_mult,
    prog=div_perf,
    camp=mgr_perf,
    churn=churn_top,
    churnCount=len(churn_all),
    churnPoolLtv=churn_pool,
    alerts=all_alerts,
    donorStats=dict(totalUnique=tot_shps, active2025=s_2025, active2026=s_2026, netChange=s_2026 - s_2025, pctChange=round((s_2026 - s_2025) / s_2025 * 100, 1)),
    funnel=funnel
))

with open("demo-freight-logistics/data.js", "w", encoding="utf-8") as f:
    f.write("window.DASH_DATA=" + payload + ";")

print("FREIGHT DATA READY! Shippers:", tot_shps, "| Lapsed Pool:", len(churn_all))
