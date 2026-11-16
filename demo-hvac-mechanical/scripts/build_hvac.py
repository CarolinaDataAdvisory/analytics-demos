import json
import os
import random
import sqlite3

random.seed(108)
os.makedirs("demo-hvac-mechanical", exist_ok=True)
db_path = "demo-hvac-mechanical/hvac_mechanical.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE customers (
    cust_id TEXT PRIMARY KEY,
    cust_name TEXT,
    plan_status TEXT,
    neighborhood TEXT,
    lead_tech TEXT
);
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    cust_id TEXT,
    job_date TEXT,
    service_line TEXT,
    revenue REAL,
    gross_margin REAL,
    alert_flag TEXT
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

firsts = ("James", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley")
lasts = ("Miller", "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White", "Lopez", "Lee", "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Perez", "Hall", "Young", "Allen", "Sanchez", "Wright", "King")
towns = ("Concord", "Kannapolis", "Harrisburg", "Salisbury", "Mooresville", "Huntersville", "University City", "Mint Hill", "Matthews", "China Grove")
techs = ("Jake Miller (Sr HVAC)", "Carlos Mendez (Lead Install)", "Brandon Cole (Master Plumber)", "Devin Carter (HVAC Tech)", "Austin Brooks (Service Tech)")

customers = list()
for i in range(1, 1851):
    cid = f"CUST-{2000 + i}"
    cname = f"{random.choice(firsts)} {random.choice(lasts)}"
    if i > 700:
        cname = f"{cname} ({random.choice(towns)})"
    pstatus = "Comfort Club Member" if random.random() < 0.36 else "On-Demand Only"
    town = random.choice(towns)
    tech = random.choice(techs)
    customers.append((cid, cname, pstatus, town, tech))

cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)

services = (
    ("HVAC System Replacement", 0.445, 7800, 14500),
    ("Tankless & Water Heater Install", 0.412, 2400, 5200),
    ("Ductwork & IAQ Upgrades", 0.388, 1600, 4400),
    ("Plumbing Repipe & Sewer", 0.365, 1800, 6200),
    ("Diagnostic & Repair Call", 0.295, 220, 890)
)

jobs = list()
jid_num = 30000
lapsed_ids = set(next(iter(c)) for idx, c in enumerate(customers) if idx < 190)

for m_idx in range(36):
    yr = 2024 + (m_idx // 12)
    mo = (m_idx % 12) + 1
    season = 1.32 if mo in (6, 7, 8) else (1.16 if mo in (1, 2, 12) else 0.86)
    growth = 1.0 + (yr - 2024) * 0.095
    n_jobs = int(520 * season * growth)
    for _ in range(n_jobs):
        jid_num += 1
        c = random.choice(customers)
        cid, cname, pstatus, town, tech = c
        if cid in lapsed_ids and yr == 2026 and mo >= 7:
            continue
        day = random.randint(1, 28)
        jdate = f"{yr}-{mo:02d}-{day:02d}"
        sline, base_gm, lo_v, hi_v = random.choices(services, weights=(16, 14, 12, 13, 45)).pop(0)
        mult = 1.35 if pstatus == "Comfort Club Member" else 1.0
        rev = round(random.uniform(lo_v, hi_v) * mult, 2)
        gm = round(rev * (base_gm + random.uniform(-0.025, 0.03)), 2)
        flag = "Callback Risk" if (yr == 2026 and mo >= 10 and random.random() < 0.015) else "OK"
        jobs.append((f"JOB-{jid_num}", cid, jdate, sline, rev, gm, flag))

cur.executemany("INSERT INTO jobs VALUES (?,?,?,?,?,?,?)", jobs)

alert_rows = list()
# 1. Unsold High-Ticket Replacement Quotes (>7 Days)
for i in range(1, 26):
    cid, cname, pstatus, town, tech = customers[i * 7]
    amt = round(random.uniform(6800, 15900), 2)
    alert_rows.append((1, "Unsold Estimate", f"EST-{900+i}", f"{cname} — Full System Quote", tech, amt, f"2026-11-{1 + (i % 14):02d}"))

# 2. Tech Callback / Repeat Warranty Visits
for i in range(1, 19):
    cid, cname, pstatus, town, tech = customers[i * 11]
    amt = round(random.uniform(450, 1850), 2)
    alert_rows.append((2, "Tech Callback", f"CB-{300+i}", f"{cname} — Repeat Diagnostic (<30d)", tech, amt, f"2026-11-{1 + (i % 14):02d}"))

# 3. Expiring Comfort Club Maintenance Plans
for i in range(1, 115):
    cid, cname, pstatus, town, tech = customers[i * 14]
    amt = round(random.uniform(289, 589), 2)
    alert_rows.append((3, "Plan Renewal", f"PLN-{5000+i}", f"{cname} — Annual HVAC + Plumbing Plan", "CSR Renewal Desk", amt, f"2026-12-{1 + (i % 28):02d}"))

cur.executemany("INSERT INTO alerts VALUES (?,?,?,?,?,?,?)", alert_rows)
conn.commit()

rev_series = tuple(tuple(r) for r in cur.execute("SELECT substr(job_date,1,7), COUNT(*), ROUND(SUM(revenue),2), ROUND(SUM(gross_margin),2) FROM jobs GROUP BY 1 ORDER BY 1").fetchall())
plan_mult = tuple(tuple(r) for r in cur.execute("WITH s AS (SELECT cust_id, COUNT(*) j_cnt, SUM(revenue) tot_rev, SUM(gross_margin) tot_gm FROM jobs GROUP BY 1) SELECT c.plan_status, COUNT(*), ROUND(AVG(s.j_cnt),1), ROUND(AVG(s.tot_rev),2), ROUND(AVG(s.tot_gm),2) FROM customers c JOIN s ON c.cust_id=s.cust_id GROUP BY 1 ORDER BY 4 DESC").fetchall())
svc_perf = tuple(tuple(r) for r in cur.execute("SELECT service_line, COUNT(*), ROUND(SUM(revenue),2), ROUND(SUM(gross_margin),2), ROUND(SUM(gross_margin)/SUM(revenue)*100,1) gm_pct FROM jobs GROUP BY 1 ORDER BY gm_pct DESC").fetchall())
town_perf = tuple(tuple(r) for r in cur.execute("SELECT c.neighborhood, COUNT(DISTINCT c.cust_id), ROUND(SUM(j.revenue),2), ROUND(SUM(j.gross_margin),2), ROUND(SUM(j.gross_margin)/SUM(j.revenue)*100,1) gm FROM customers c JOIN jobs j ON c.cust_id=j.cust_id GROUP BY 1 ORDER BY 3 DESC").fetchall())

churn_all = tuple(tuple(r) for r in cur.execute("SELECT c.cust_id, c.cust_name, c.plan_status, c.neighborhood, ROUND(SUM(j.revenue),2) ltv, MAX(j.job_date) last_job, CAST(julianday('2026-12-31') - julianday(MAX(j.job_date)) AS INTEGER) days_lapsed FROM jobs j JOIN customers c ON j.cust_id=c.cust_id GROUP BY 1,2,3,4 HAVING ltv >= 3500 AND days_lapsed >= 150 ORDER BY ltv DESC").fetchall())
churn_top = tuple(r for idx, r in enumerate(churn_all) if idx < 15)
churn_pool = round(sum(float(r.pop(4)) for r in (list(x) for x in churn_all)), 2)

tot_custs = next(iter(cur.execute("SELECT COUNT(DISTINCT cust_id) FROM jobs").fetchone()))
c_2025 = next(iter(cur.execute("SELECT COUNT(DISTINCT cust_id) FROM jobs WHERE substr(job_date,1,4)='2025'").fetchone()))
c_2026 = next(iter(cur.execute("SELECT COUNT(DISTINCT cust_id) FROM jobs WHERE substr(job_date,1,4)='2026'").fetchone()))

funnel = (
    ("In-Home Estimates", 1420),
    ("Good-Better-Best Sent", 1180),
    ("Financing Reviewed", 740),
    ("Stalled Quotes (>7 Days)", 310),
    ("15% Quote Recovery", 47)
)

all_alerts = tuple(tuple(x for idx, x in enumerate(r) if idx > 0) for r in cur.execute("SELECT prio, alert_type, ref_id, entity_name, owner, dollar_impact, due_date FROM alerts ORDER BY prio ASC, dollar_impact DESC").fetchall())

payload = json.dumps(dict(
    rev=rev_series,
    vol=plan_mult,
    prog=svc_perf,
    camp=town_perf,
    churn=churn_top,
    churnCount=len(churn_all),
    churnPoolLtv=churn_pool,
    alerts=all_alerts,
    donorStats=dict(totalUnique=tot_custs, active2025=c_2025, active2026=c_2026, netChange=c_2026 - c_2025, pctChange=round((c_2026 - c_2025) / c_2025 * 100, 1)),
    funnel=funnel
))

with open("demo-hvac-mechanical/data.js", "w", encoding="utf-8") as f:
    f.write("window.DASH_DATA=" + payload + ";")

print("HVAC & PLUMBING DATA READY! Customers:", tot_custs, "| Lapsed Pool:", len(churn_all))
