import json
import os
import random
import sqlite3

random.seed(42)
os.makedirs("demo-electrical-supply", exist_ok=True)
db_path = "demo-electrical-supply/electrical_supply.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE contractors (
    contractor_id TEXT PRIMARY KEY,
    company_name TEXT,
    segment TEXT,
    channel_type TEXT,
    account_rep TEXT,
    credit_limit REAL
);
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    contractor_id TEXT,
    order_date TEXT,
    category TEXT,
    revenue REAL,
    gross_margin REAL,
    invoice_status TEXT
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

prefixes = ("Piedmont", "Rowan", "Cabarrus", "Carolina", "Salisbury", "Concord", "Metrolina", "Yadkin", "Blue Ridge", "Tar Heel", "Triad", "Queen City", "Catawba", "Iredell", "Stanly", "Union")
suffixes = ("Electric Co.", "Power Systems", "Industrial Controls", "Mechanical & Electric", "Commercial Wiring", "Solar & Grid", "Automation Group", "Electrical Contractors", "Lighting & Supply", "Energy Solutions")
segments = ("Commercial Contractor", "Industrial Plant", "Municipal & Utility", "Solar & EV Installer")
reps = ("Marcus Vance", "Sarah Jenkins", "Devon Brooks", "Elena Rostova", "Tyler Morgan")

contractors = list()
for i in range(1, 421):
    cid = f"ACCT-{1000 + i}"
    cname = f"{random.choice(prefixes)} {random.choice(suffixes)} #{i}" if i > 160 else f"{prefixes[i % len(prefixes)]} {suffixes[i % len(suffixes)]}"
    seg = next(iter(random.choices(segments, weights=(45, 25, 15, 15))))
    ch = "Counter + Portal" if random.random() < 0.34 else "Counter Only"
    rep = random.choice(reps)
    clim = random.choice((25000, 50000, 100000, 250000))
    contractors.append((cid, cname, seg, ch, rep, clim))

cur.executemany("INSERT INTO contractors VALUES (?,?,?,?,?,?)", contractors)

categories = (
    ("Switchgear & Panels", 0.285),
    ("Industrial Automation & PLCs", 0.312),
    ("Commercial LED Lighting", 0.264),
    ("Transformers & Distribution", 0.248),
    ("Copper Wire & Conduit", 0.162)
)

orders = list()
oid_num = 10000
lapsed_ids = set(next(iter(c)) for idx, c in enumerate(contractors) if idx < 48)

for m_idx in range(36):
    yr = 2024 + (m_idx // 12)
    mo = (m_idx % 12) + 1
    season = 1.18 if mo in (5, 6, 7, 8, 9, 10) else 0.92
    growth = 1.0 + (yr - 2024) * 0.085
    n_orders = int(460 * season * growth)
    for _ in range(n_orders):
        oid_num += 1
        c = random.choice(contractors)
        cid, cname, seg, ch, rep, clim = c
        if cid in lapsed_ids and yr == 2026 and mo >= 9:
            continue
        day = random.randint(1, 28)
        odate = f"{yr}-{mo:02d}-{day:02d}"
        cat, base_gm = random.choice(categories)
        mult = 2.45 if ch == "Counter + Portal" else 1.0
        rev = round(random.uniform(1400, 6800) * mult * (1.2 if seg == "Industrial Plant" else 1.0), 2)
        gm = round(rev * (base_gm + random.uniform(-0.02, 0.025)), 2)
        istatus = "Overdue Net-30" if (yr == 2026 and mo >= 10 and random.random() < 0.04) else "Paid"
        orders.append((f"ORD-{oid_num}", cid, odate, cat, rev, gm, istatus))

cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", orders)

alert_rows = list()
for i in range(1, 13):
    cid, cname, seg, ch, rep, clim = contractors[i * 3]
    amt = round(random.uniform(18500, 74000), 2)
    alert_rows.append((1, "Backorder Risk", f"BO-{400+i}", f"{cname} (Custom Switchgear)", rep, amt, f"2026-12-{10+i:02d}"))

for i in range(1, 19):
    cid, cname, seg, ch, rep, clim = contractors[i * 5]
    amt = round(random.uniform(4200, 22500), 2)
    alert_rows.append((2, "Margin Leak", f"CO-{800+i}", f"{cname} (Unbilled Spec Change)", rep, amt, f"2026-11-{10 + (i % 18):02d}"))

overdue_orders = cur.execute("SELECT o.order_id, c.company_name, c.account_rep, o.revenue, o.order_date FROM orders o JOIN contractors c ON o.contractor_id=c.contractor_id WHERE o.invoice_status='Overdue Net-30' ORDER BY o.revenue DESC LIMIT 120").fetchall()
for oid, cname, rep, rev, odate in overdue_orders:
    alert_rows.append((3, "Overdue Net-30", oid, cname, rep, rev, odate))

cur.executemany("INSERT INTO alerts VALUES (?,?,?,?,?,?,?)", alert_rows)
conn.commit()

rev_series = tuple(tuple(r) for r in cur.execute("SELECT substr(order_date,1,7), COUNT(*), ROUND(SUM(revenue),2), ROUND(SUM(gross_margin),2) FROM orders GROUP BY 1 ORDER BY 1").fetchall())
ch_mult = tuple(tuple(r) for r in cur.execute("WITH s AS (SELECT contractor_id, COUNT(*) ord_cnt, SUM(revenue) tot_rev, SUM(gross_margin) tot_gm FROM orders GROUP BY 1) SELECT c.channel_type, COUNT(*), ROUND(AVG(s.ord_cnt),1), ROUND(AVG(s.tot_rev),2), ROUND(AVG(s.tot_gm),2) FROM contractors c JOIN s ON c.contractor_id=s.contractor_id GROUP BY 1 ORDER BY 4 DESC").fetchall())
cat_perf = tuple(tuple(r) for r in cur.execute("SELECT category, COUNT(*), ROUND(SUM(revenue),2), ROUND(SUM(gross_margin),2), ROUND(SUM(gross_margin)/SUM(revenue)*100,1) gm_pct FROM orders GROUP BY 1 ORDER BY gm_pct DESC").fetchall())
seg_perf = tuple(tuple(r) for r in cur.execute("SELECT c.segment, COUNT(DISTINCT c.contractor_id), ROUND(SUM(o.revenue),2), ROUND(SUM(o.gross_margin),2), ROUND(SUM(o.gross_margin)/SUM(o.revenue)*100,1) roi FROM contractors c JOIN orders o ON c.contractor_id=o.contractor_id GROUP BY 1 ORDER BY 3 DESC").fetchall())

churn_all = tuple(tuple(r) for r in cur.execute("SELECT c.contractor_id, c.company_name, c.segment, c.account_rep, ROUND(SUM(o.revenue),2) ltv, MAX(o.order_date) last_ord, CAST(julianday('2026-12-31') - julianday(MAX(o.order_date)) AS INTEGER) days_lapsed FROM orders o JOIN contractors c ON o.contractor_id=c.contractor_id GROUP BY 1,2,3,4 HAVING ltv >= 50000 AND days_lapsed >= 65 ORDER BY ltv DESC").fetchall())
churn_top = tuple(r for idx, r in enumerate(churn_all) if idx < 15)
churn_pool = round(sum(float(r.pop(4)) for r in (list(x) for x in churn_all)), 2)

tot_accts = next(iter(cur.execute("SELECT COUNT(DISTINCT contractor_id) FROM orders").fetchone()))
a_2025 = next(iter(cur.execute("SELECT COUNT(DISTINCT contractor_id) FROM orders WHERE substr(order_date,1,4)='2025'").fetchone()))
a_2026 = next(iter(cur.execute("SELECT COUNT(DISTINCT contractor_id) FROM orders WHERE substr(order_date,1,4)='2026'").fetchone()))

funnel = (
    ("Commercial Quotes Issued", 2840),
    ("Spec Review Completed", 1920),
    ("Submittal Approved", 1290),
    ("Stalled Bids (>21 Days)", 460),
    ("15% Bid Recovery Target", 69)
)

all_alerts = tuple(tuple(x for idx, x in enumerate(r) if idx > 0) for r in cur.execute("SELECT prio, alert_type, ref_id, entity_name, owner, dollar_impact, due_date FROM alerts ORDER BY prio ASC, dollar_impact DESC").fetchall())

payload = json.dumps(dict(
    rev=rev_series,
    vol=ch_mult,
    prog=cat_perf,
    camp=seg_perf,
    churn=churn_top,
    churnCount=len(churn_all),
    churnPoolLtv=churn_pool,
    alerts=all_alerts,
    donorStats=dict(totalUnique=tot_accts, active2025=a_2025, active2026=a_2026, netChange=a_2026 - a_2025, pctChange=round((a_2026 - a_2025) / a_2025 * 100, 1)),
    funnel=funnel
))

with open("demo-electrical-supply/data.js", "w", encoding="utf-8") as f:
    f.write("window.DASH_DATA=" + payload + ";")

print("ELECTRICAL DATA FIXED! Accounts:", tot_accts, "| Lapsed Pool:", len(churn_all))
