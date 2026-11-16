import json
import os
import random
import sqlite3

random.seed(212)
os.makedirs("demo-legal-partners", exist_ok=True)
db_path = "demo-legal-partners/legal_partners.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE matters (
    matter_id TEXT PRIMARY KEY,
    client_label TEXT,
    billing_model TEXT,
    practice_area TEXT,
    lead_attorney TEXT
);
CREATE TABLE billing (
    inv_id TEXT PRIMARY KEY,
    matter_id TEXT,
    bill_date TEXT,
    practice_area TEXT,
    collected_rev REAL,
    realized_margin REAL
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

prefixes = ("Mecklenburg", "Cabarrus", "Rowan", "Piedmont", "Queen City", "Carolina", "Concord", "Salisbury", "Uptown", "Ballantyne", "SouthPark", "Catawba", "Metrolina", "Iredell", "Stanly", "Union")
types = ("Holdings LLC", "Properties Group", "Logistics Corp", "Medical Associates", "Construction Inc.", "Family Trust", "Estate Matter", "Ventures LP", "Manufacturing Co.", "Commercial Partners")
practices = (
    ("Business Litigation", 0.895, 4200, 14500),
    ("Estate & Trust Planning", 0.942, 2500, 7800),
    ("Commercial Real Estate", 0.918, 3200, 11200),
    ("Family Law & Domestic", 0.864, 2800, 9500),
    ("Workers Comp & Employment", 0.840, 2200, 7400)
)
attorneys = ("E. Vance (Managing Partner)", "R. Sterling (Litigation)", "M. Chen (Corporate/RE)", "S. Holloway (Family Law)", "D. Brooks (Estates/Trusts)")

matters = list()
for i in range(1, 641):
    mid = f"MAT-{4000 + i}"
    clabel = f"{random.choice(prefixes)} {random.choice(types)} #{i}" if i > 160 else f"{prefixes[i % len(prefixes)]} {types[i % len(types)]}"
    bmodel = "Evergreen Retainer" if random.random() < 0.38 else "Standard Hourly"
    parea = random.choice(practices).pop(0) if False else next(iter(random.choice(practices)))
    atty = random.choice(attorneys)
    matters.append((mid, clabel, bmodel, parea, atty))

cur.executemany("INSERT INTO matters VALUES (?,?,?,?,?)", matters)

bills = list()
bid_num = 50000
lapsed_ids = set(next(iter(m)) for idx, m in enumerate(matters) if idx < 72)

for m_idx in range(36):
    yr = 2024 + (m_idx // 12)
    mo = (m_idx % 12) + 1
    season = 1.16 if mo in (3, 4, 9, 10, 11, 12) else 0.92
    growth = 1.0 + (yr - 2024) * 0.085
    n_bills = int(175 * season * growth)
    for _ in range(n_bills):
        bid_num += 1
        m = random.choice(matters)
        mid, clabel, bmodel, parea, atty = m
        if mid in lapsed_ids and yr == 2026 and mo >= 8:
            continue
        day = random.randint(1, 28)
        bdate = f"{yr}-{mo:02d}-{day:02d}"
        _, real_rate, lo_v, hi_v = random.choice(practices)
        mult = 1.65 if bmodel == "Evergreen Retainer" else 1.0
        rev = round(random.uniform(lo_v, hi_v) * mult, 2)
        gm = round(rev * (real_rate + random.uniform(-0.02, 0.025)), 2)
        bills.append((f"INV-{bid_num}", mid, bdate, parea, rev, gm))

cur.executemany("INSERT INTO billing VALUES (?,?,?,?,?,?)", bills)

alert_rows = list()
for i in range(1, 22):
    mid, clabel, bmodel, parea, atty = matters[i * 4]
    amt = round(random.uniform(5000, 18500), 2)
    alert_rows.append((1, "Retainer Low", f"RET-{700+i}", f"{clabel} — Trust Below Min", atty, amt, f"2026-11-{1 + (i % 14):02d}"))

for i in range(1, 25):
    mid, clabel, bmodel, parea, atty = matters[i * 6]
    amt = round(random.uniform(3200, 14200), 2)
    alert_rows.append((2, "Unbilled WIP", f"WIP-{300+i}", f"{clabel} — Unbilled Time (45d+)", atty, amt, f"2026-11-{1 + (i % 14):02d}"))

for i in range(1, 65):
    mid, clabel, bmodel, parea, atty = matters[i * 8]
    amt = round(random.uniform(2400, 16800), 2)
    alert_rows.append((3, "Overdue 60d+", f"AR-{8000+i}", f"{clabel} — Past Due Invoice", "Billing Admin Desk", amt, f"2026-10-{1 + (i % 28):02d}"))

cur.executemany("INSERT INTO alerts VALUES (?,?,?,?,?,?,?)", alert_rows)
conn.commit()

rev_series = tuple(tuple(r) for r in cur.execute("SELECT substr(bill_date,1,7), COUNT(*), ROUND(SUM(collected_rev),2), ROUND(SUM(realized_margin),2) FROM billing GROUP BY 1 ORDER BY 1").fetchall())
ret_mult = tuple(tuple(r) for r in cur.execute("WITH s AS (SELECT matter_id, COUNT(*) b_cnt, SUM(collected_rev) tot_rev, SUM(realized_margin) tot_gm FROM billing GROUP BY 1) SELECT m.billing_model, COUNT(*), ROUND(AVG(s.b_cnt),1), ROUND(AVG(s.tot_rev),2), ROUND(AVG(s.tot_gm),2) FROM matters m JOIN s ON m.matter_id=s.matter_id GROUP BY 1 ORDER BY 4 DESC").fetchall())
prac_perf = tuple(tuple(r) for r in cur.execute("SELECT practice_area, COUNT(*), ROUND(SUM(collected_rev),2), ROUND(SUM(realized_margin),2), ROUND(SUM(realized_margin)/SUM(collected_rev)*100,1) real_pct FROM billing GROUP BY 1 ORDER BY real_pct DESC").fetchall())
atty_perf = tuple(tuple(r) for r in cur.execute("SELECT m.lead_attorney, COUNT(DISTINCT m.matter_id), ROUND(SUM(b.collected_rev),2), ROUND(SUM(b.realized_margin),2), ROUND(SUM(b.realized_margin)/SUM(b.collected_rev)*100,1) real_pct FROM matters m JOIN billing b ON m.matter_id=b.matter_id GROUP BY 1 ORDER BY 3 DESC").fetchall())

churn_all = tuple(tuple(r) for r in cur.execute("SELECT m.matter_id, m.client_label, m.practice_area, m.lead_attorney, ROUND(SUM(b.collected_rev),2) ltv, MAX(b.bill_date) last_bill, CAST(julianday('2026-12-31') - julianday(MAX(b.bill_date)) AS INTEGER) days_lapsed FROM billing b JOIN matters m ON b.matter_id=m.matter_id GROUP BY 1,2,3,4 HAVING ltv >= 12000 AND days_lapsed >= 110 ORDER BY ltv DESC").fetchall())
churn_top = tuple(r for idx, r in enumerate(churn_all) if idx < 15)
churn_pool = round(sum(float(r.pop(4)) for r in (list(x) for x in churn_all)), 2)

tot_mats = next(iter(cur.execute("SELECT COUNT(DISTINCT matter_id) FROM billing").fetchone()))
m_2025 = next(iter(cur.execute("SELECT COUNT(DISTINCT matter_id) FROM billing WHERE substr(bill_date,1,4)='2025'").fetchone()))
m_2026 = next(iter(cur.execute("SELECT COUNT(DISTINCT matter_id) FROM billing WHERE substr(bill_date,1,4)='2026'").fetchone()))

funnel = (
    ("Qualified Consultations", 920),
    ("Conflict Check Cleared", 780),
    ("Engagement Letter Sent", 540),
    ("Unsigned Retainers (>10d)", 185),
    ("15% Retainer Recovery", 28)
)

all_alerts = tuple(tuple(x for idx, x in enumerate(r) if idx > 0) for r in cur.execute("SELECT prio, alert_type, ref_id, entity_name, owner, dollar_impact, due_date FROM alerts ORDER BY prio ASC, dollar_impact DESC").fetchall())

payload = json.dumps(dict(
    rev=rev_series,
    vol=ret_mult,
    prog=prac_perf,
    camp=atty_perf,
    churn=churn_top,
    churnCount=len(churn_all),
    churnPoolLtv=churn_pool,
    alerts=all_alerts,
    donorStats=dict(totalUnique=tot_mats, active2025=m_2025, active2026=m_2026, netChange=m_2026 - m_2025, pctChange=round((m_2026 - m_2025) / m_2025 * 100, 1)),
    funnel=funnel
))

with open("demo-legal-partners/data.js", "w", encoding="utf-8") as f:
    f.write("window.DASH_DATA=" + payload + ";")

print("LEGAL DATA READY! Matters:", tot_mats, "| Lapsed Pool:", len(churn_all))
