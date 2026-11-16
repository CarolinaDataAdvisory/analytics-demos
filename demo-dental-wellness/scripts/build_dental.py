import json
import os
import random
import sqlite3

random.seed(404)
os.makedirs("demo-dental-wellness", exist_ok=True)
db_path = "demo-dental-wellness/dental_wellness.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE patients (
    patient_id TEXT PRIMARY KEY,
    patient_label TEXT,
    plan_type TEXT,
    clinic_loc TEXT,
    provider TEXT
);
CREATE TABLE visits (
    visit_id TEXT PRIMARY KEY,
    patient_id TEXT,
    visit_date TEXT,
    procedure_cat TEXT,
    collected_amt REAL,
    net_realized REAL
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

firsts = ("Hannah", "William", "Olivia", "Benjamin", "Sophia", "Lucas", "Emma", "Henry", "Ava", "Alexander", "Mia", "Sebastian", "Charlotte", "Jack", "Amelia", "Owen", "Harper", "Daniel", "Evelyn", "Matthew")
lasts = ("Brooks", "Reynolds", "Foster", "Simmons", "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes", "Myers", "Ford", "Hamilton", "Graham", "Sullivan", "Wallace", "Woods", "Cole", "West", "Jordan")
clinics = ("Concord Parkway Clinic", "Salisbury Main Clinic", "Huntersville Lake Clinic", "SouthPark Charlotte Clinic")
providers = ("Dr. K. Patel (Clinical Dir)", "Dr. M. Vance (Implants/Restorative)", "Dr. L. Chen (Ortho & Aesthetics)", "S. Miller, RDH (Lead Hygiene)", "T. Brooks, RDH (Perio Care)")

patients = list()
for i in range(1, 1951):
    pid = f"PT-{8000 + i}"
    plabel = f"{random.choice(firsts)} {random.choice(lasts)} (#{1000+i})"
    ptype = "In-House Wellness Plan" if random.random() < 0.37 else "Standard Insurance / FFS"
    cloc = random.choice(clinics)
    prov = random.choice(providers)
    patients.append((pid, plabel, ptype, cloc, prov))

cur.executemany("INSERT INTO patients VALUES (?,?,?,?,?)", patients)

procs = (
    ("Implants & Full-Arch Restorative", 0.945, 3400, 8800),
    ("Clear Aligners & Aesthetic Care", 0.930, 2600, 5400),
    ("Crowns, Bridges & Endodontics", 0.895, 1100, 2800),
    ("Periodontal Therapy & Maintenance", 0.880, 420, 1150),
    ("Preventive Hygiene & Diagnostics", 0.860, 210, 480)
)

visits = list()
vid_num = 90000
lapsed_ids = set(next(iter(p)) for idx, p in enumerate(patients) if idx < 210)

for m_idx in range(36):
    yr = 2024 + (m_idx // 12)
    mo = (m_idx % 12) + 1
    season = 1.24 if mo in (3, 6, 7, 8, 11, 12) else 0.91
    growth = 1.0 + (yr - 2024) * 0.088
    n_visits = int(680 * season * growth)
    for _ in range(n_visits):
        vid_num += 1
        p = random.choice(patients)
        pid, plabel, ptype, cloc, prov = p
        if pid in lapsed_ids and yr == 2026 and mo >= 6:
            continue
        day = random.randint(1, 28)
        vdate = f"{yr}-{mo:02d}-{day:02d}"
        pcat, coll_rate, lo_v, hi_v = random.choices(procs, weights=(11, 12, 18, 19, 40)).pop(0)
        mult = 1.38 if ptype == "In-House Wellness Plan" else 1.0
        rev = round(random.uniform(lo_v, hi_v) * mult, 2)
        net = round(rev * (coll_rate + random.uniform(-0.02, 0.025)), 2)
        visits.append((f"VST-{vid_num}", pid, vdate, pcat, rev, net))

cur.executemany("INSERT INTO visits VALUES (?,?,?,?,?,?)", visits)

alert_rows = list()
for i in range(1, 29):
    pid, plabel, ptype, cloc, prov = patients[i * 5]
    amt = round(random.uniform(1850, 6900), 2)
    alert_rows.append((1, "Unscheduled Tx", f"TX-{400+i}", f"{plabel} — Crown/Implant Plan ({cloc})", "Treatment Coordinator", amt, f"2026-11-{1 + (i % 14):02d}"))

for i in range(1, 25):
    pid, plabel, ptype, cloc, prov = patients[i * 8]
    amt = round(random.uniform(650, 3400), 2)
    alert_rows.append((2, "Aging Claim 45d+", f"CLM-{700+i}", f"{plabel} — Pending Ins EOB ({cloc})", "Insurance Billing Desk", amt, f"2026-10-{1 + (i % 28):02d}"))

for i in range(1, 95):
    pid, plabel, ptype, cloc, prov = patients[i * 12]
    amt = round(random.uniform(349, 599), 2)
    alert_rows.append((3, "Plan Renewal", f"MEM-{3000+i}", f"{plabel} — Annual Wellness Renewal", "Front Desk Recall", amt, f"2026-12-{1 + (i % 28):02d}"))

cur.executemany("INSERT INTO alerts VALUES (?,?,?,?,?,?,?)", alert_rows)
conn.commit()

rev_series = tuple(tuple(r) for r in cur.execute("SELECT substr(visit_date,1,7), COUNT(*), ROUND(SUM(collected_amt),2), ROUND(SUM(net_realized),2) FROM visits GROUP BY 1 ORDER BY 1").fetchall())
plan_mult = tuple(tuple(r) for r in cur.execute("WITH s AS (SELECT patient_id, COUNT(*) v_cnt, SUM(collected_amt) tot_rev, SUM(net_realized) tot_net FROM visits GROUP BY 1) SELECT p.plan_type, COUNT(*), ROUND(AVG(s.v_cnt),1), ROUND(AVG(s.tot_rev),2), ROUND(AVG(s.tot_net),2) FROM patients p JOIN s ON p.patient_id=s.patient_id GROUP BY 1 ORDER BY 4 DESC").fetchall())
proc_perf = tuple(tuple(r) for r in cur.execute("SELECT procedure_cat, COUNT(*), ROUND(SUM(collected_amt),2), ROUND(SUM(net_realized),2), ROUND(SUM(net_realized)/SUM(collected_amt)*100,1) coll_pct FROM visits GROUP BY 1 ORDER BY coll_pct DESC").fetchall())
loc_perf = tuple(tuple(r) for r in cur.execute("SELECT p.clinic_loc, COUNT(DISTINCT p.patient_id), ROUND(SUM(v.collected_amt),2), ROUND(SUM(v.net_realized),2), ROUND(SUM(v.net_realized)/SUM(v.collected_amt)*100,1) coll_pct FROM patients p JOIN visits v ON p.patient_id=v.patient_id GROUP BY 1 ORDER BY 3 DESC").fetchall())

churn_all = tuple(tuple(r) for r in cur.execute("SELECT p.patient_id, p.patient_label, p.clinic_loc, p.plan_type, ROUND(SUM(v.collected_amt),2) ltv, MAX(v.visit_date) last_visit, CAST(julianday('2026-12-31') - julianday(MAX(v.visit_date)) AS INTEGER) days_lapsed FROM visits v JOIN patients p ON v.patient_id=p.patient_id GROUP BY 1,2,3,4 HAVING ltv >= 2200 AND days_lapsed >= 180 ORDER BY ltv DESC").fetchall())
churn_top = tuple(r for idx, r in enumerate(churn_all) if idx < 15)
churn_pool = round(sum(float(r.pop(4)) for r in (list(x) for x in churn_all)), 2)

tot_pts = next(iter(cur.execute("SELECT COUNT(DISTINCT patient_id) FROM visits").fetchone()))
p_2025 = next(iter(cur.execute("SELECT COUNT(DISTINCT patient_id) FROM visits WHERE substr(visit_date,1,4)='2025'").fetchone()))
p_2026 = next(iter(cur.execute("SELECT COUNT(DISTINCT patient_id) FROM visits WHERE substr(visit_date,1,4)='2026'").fetchone()))

funnel = (
    ("Exams Diagnosed", 1840),
    ("Plans Presented", 1410),
    ("Insurance Verified", 980),
    ("Unscheduled Plans", 290),
    ("15% Scheduled", 44)
)

all_alerts = tuple(tuple(x for idx, x in enumerate(r) if idx > 0) for r in cur.execute("SELECT prio, alert_type, ref_id, entity_name, owner, dollar_impact, due_date FROM alerts ORDER BY prio ASC, dollar_impact DESC").fetchall())

payload = json.dumps(dict(
    rev=rev_series,
    vol=plan_mult,
    prog=proc_perf,
    camp=loc_perf,
    churn=churn_top,
    churnCount=len(churn_all),
    churnPoolLtv=churn_pool,
    alerts=all_alerts,
    donorStats=dict(totalUnique=tot_pts, active2025=p_2025, active2026=p_2026, netChange=p_2026 - p_2025, pctChange=round((p_2026 - p_2025) / p_2025 * 100, 1)),
    funnel=funnel
))

with open("demo-dental-wellness/data.js", "w", encoding="utf-8") as f:
    f.write("window.DASH_DATA=" + payload + ";")

print("DENTAL & WELLNESS DATA READY! Patients:", tot_pts, "| Overdue Recall Pool:", len(churn_all))
