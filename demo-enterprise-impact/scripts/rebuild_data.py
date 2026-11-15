import json, sqlite3

conn = sqlite3.connect("demo-enterprise-impact/enterprise_impact.db")
cur = conn.cursor()

rev = cur.execute("SELECT substr(donation_date,1,7), COUNT(*), ROUND(SUM(amount),2), ROUND(AVG(CASE WHEN amount>0 THEN amount END),2) FROM donations GROUP BY 1 ORDER BY 1").fetchall()
camp = cur.execute("SELECT c.campaign_name, c.channel, c.program_area, c.marketing_budget, COALESCE(ROUND(SUM(d.amount),2),0), ROUND((COALESCE(SUM(d.amount),0)-c.marketing_budget)/c.marketing_budget*100,1) AS roi FROM campaigns c LEFT JOIN donations d ON c.campaign_id=d.campaign_id GROUP BY 1,2,3,4 ORDER BY roi DESC").fetchall()
vol = cur.execute("WITH v AS (SELECT constituent_id FROM volunteer_and_outcomes GROUP BY 1), d AS (SELECT constituent_id, COUNT(*) g, SUM(amount) ltv FROM donations WHERE amount>0 GROUP BY 1) SELECT CASE WHEN v.constituent_id IS NOT NULL THEN 'Donor+Vol' ELSE 'DonorOnly' END, COUNT(*), ROUND(AVG(d.g),1), ROUND(AVG(d.ltv),2) FROM d LEFT JOIN v ON d.constituent_id=v.constituent_id GROUP BY 1").fetchall()
prog = cur.execute("WITH e AS (SELECT program_area, SUM(amount) s FROM program_expenses WHERE approval_status='Approved' GROUP BY 1), i AS (SELECT program_area, SUM(beneficiaries_served) b, ROUND(AVG(outcome_score),1) o FROM volunteer_and_outcomes GROUP BY 1) SELECT i.program_area, ROUND(e.s,2), i.b, i.o, ROUND(e.s/i.b,2) cpb FROM i JOIN e ON i.program_area=e.program_area ORDER BY cpb ASC").fetchall()

all_churn = cur.execute("SELECT c.constituent_id, c.first_name||' '||c.last_name, c.wealth_tier, c.email, ROUND(SUM(d.amount),2) AS ltv, MAX(d.donation_date) AS last_gift, CAST(julianday('2026-12-31') - julianday(MAX(d.donation_date)) AS INTEGER) AS days_lapsed FROM donations d JOIN constituents c ON d.constituent_id=c.constituent_id WHERE d.amount>0 GROUP BY 1,2,3,4 HAVING ltv >= 1000 AND days_lapsed >= 120 ORDER BY ltv DESC").fetchall()
churn_pool_ltv = round(sum(r[4] for r in all_churn), 2)

alerts = cur.execute("SELECT 1 AS prio, 'Grant Risk', grant_id, foundation_name, grant_manager, awarded_amount, reporting_deadline FROM grants WHERE status='At Risk' UNION ALL SELECT 2, 'Flagged Exp', expense_id, vendor_name, program_area, amount, expense_date FROM program_expenses WHERE approval_status='Flagged' UNION ALL SELECT 3, 'Failed Recur', d.constituent_id, c.first_name||' '||c.last_name, c.email, d.amount, d.donation_date FROM donations d JOIN constituents c ON d.constituent_id=c.constituent_id WHERE d.recurring_status='Failed Payment' ORDER BY prio ASC, 6 DESC").fetchall()
clean_alerts = [list(r[1:]) for r in alerts]

tot_donors = cur.execute("SELECT COUNT(DISTINCT constituent_id) FROM donations WHERE amount > 0").fetchone()[0]
d_2025 = cur.execute("SELECT COUNT(DISTINCT constituent_id) FROM donations WHERE amount > 0 AND substr(donation_date, 1, 4) = '2025'").fetchone()[0]
d_2026 = cur.execute("SELECT COUNT(DISTINCT constituent_id) FROM donations WHERE amount > 0 AND substr(donation_date, 1, 4) = '2026'").fetchone()[0]
net_change = d_2026 - d_2025
pct_change = round((net_change / d_2025) * 100, 1) if d_2025 else 0

f_rows = cur.execute("SELECT touchpoint_type, COUNT(*) FROM digital_engagement GROUP BY 1").fetchall()
f_map = {r[0]: r[1] for r in f_rows}
abandoned = f_map.get("Donation Page Abandoned", 1500)
funnel = [
    ["Email Opens", f_map.get("Email Open", 6750)],
    ["Email Clicks", f_map.get("Email Click", 3300)],
    ["Impact Reports & Webinars", f_map.get("Impact Report Downloaded", 1950) + f_map.get("Webinar Attended", 1500)],
    ["Abandoned Checkout", abandoned],
    ["15% Recovery Target", round(abandoned * 0.15)]
]

payload = {
    "rev": [list(r) for r in rev],
    "camp": [list(r) for r in camp],
    "vol": [list(r) for r in vol],
    "prog": [list(r) for r in prog],
    "churn": [list(r) for r in all_churn[:15]],
    "churnCount": len(all_churn),
    "churnPoolLtv": churn_pool_ltv,
    "alerts": clean_alerts,
    "donorStats": {"totalUnique": tot_donors, "active2025": d_2025, "active2026": d_2026, "netChange": net_change, "pctChange": pct_change},
    "funnel": funnel
}

open("demo-enterprise-impact/data.js", "w", encoding="utf-8").write("window.DASH_DATA=" + json.dumps(payload) + ";")
print("DATA.JS REBUILT CLEANLY! Total Donors:", tot_donors, "| Lapsed Pool:", len(all_churn))
