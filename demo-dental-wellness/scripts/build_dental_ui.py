js = open("demo-enterprise-impact/app.js", encoding="utf-8").read()
for o, n in (
    ("1.18", "1.10"), ("2.5", "2.8"), ("* 0.05", "* 0.08"), ("* 15", "* 20"),
    ("3-Year Net Revenue", "3-Year Patient Collections"), ("UP 22% YoY Recurring Growth", "~$11.2M/Yr 4-Clinic Run-Rate"),
    ("Active Donors (2026)", "Active Patients (2026)"), ("Net Donors", "Net Patients"),
    ("H1 2027 Run-Rate Projection", "H1 2027 Collections Forecast"),
    ("Grants, Audits & Failed Gifts", "Unscheduled Tx, Claims & Plans"), ("gifts/ea", "visits"),
    ("donors @ $15", "patients @ $20"), ("5% Full + 10% Half", "16% Reactivation"),
    ("165", "1700"), ("gifts =", "plans ="),
    ("Grant Risk", "Unscheduled Tx"), ("Flagged Exp", "Aging Claim 45d+"), ("Failed Recur", "Plan Renewal"),
    ("r.at(0) + ' (' + Number(r.at(2)).toLocaleString() + ' served | ' + r.at(3) + '/100)'", "r.at(0) + ' (' + fmt(r.at(2)) + ' billed)'"),
    ("'$' + Number(r.at(4)).toFixed(2) + '/ person'", "Number(r.at(4)).toFixed(1) + '% Net'"),
    ("Digital Engagement Funnel & Checkout Recovery Opportunity", "Treatment Acceptance Funnel & Recall Recovery"),
    ("Checkout Recovery Play: ' + abCount.toLocaleString() + ' supporters abandoned the donation page. Triggering an automated 24-hr reminder email recovers ~15%", "Treatment Recovery Play: ' + abCount.toLocaleString() + ' diagnosed treatment plans sit unscheduled past 14 days. Coordinator follow-up schedules ~15%")
):
    js = js.replace(o, n)
open("demo-dental-wellness/app.js", "w", encoding="utf-8").write(js)

h = open("demo-enterprise-impact/dashboard.html", encoding="utf-8").read()
for o, n in (
    ("Piedmont Community Impact Alliance", "Piedmont Dental &amp; Wellness Partners"),
    ("Simulated Sample Organization", "Simulated 4-Location Group • $11M Collections"),
    ("Executive Fundraising, Retention &amp; Program Intelligence", "Patient Recall, Chair Utilization &amp; Net Collection Intelligence"),
    ("1,225 Duplicates Removed • 7,403 Typos Standardized", "790 Duplicate Patient Charts Merged • 4,120 Dentrix/QB Records Cleaned"),
    ("36-Month Net Revenue + 6-Month Shaded Forecast (Baseline vs. Churn Outreach)", "36-Month Patient Collections + 6-Month Shaded Forecast"),
    ("The Volunteer Multiplier (Avg Lifetime Value)", "The Wellness Plan Multiplier (3-Yr Patient LTV)"),
    ("High-Dollar Donor Churn Watchlist (LTV $1,000+ &amp; 120+ Days Lapsed)", "Overdue 6-Month Recall Watchlist ($2,200+ Spend &amp; 180+ Days Overdue)"),
    ("Donor ID", "Patient ID"), ("Supporter Name", "Patient Chart"), ("Tier", "Primary Clinic"),
    ("Lifetime Giving", "3-Yr Collections"), ("Last Gift", "Last Visit"), ("Days Lapsed", "Days Overdue"),
    ("Program Cost Efficiency ($ Cost per Beneficiary)", "Procedure Category Net Collection % &amp; Volume"),
    ("Campaign Profitability &amp; Budget Variance", "Clinic Location Collections &amp; Net Realization"),
    ("Campaign", "Clinic Location"), ("Channel", "Active Patients"), ("Budget", "3-Yr Production"), ("Net Raised", "Collected ($)"), ("ROI %", "Net Coll %"),
    ("Grant Risk", "Unscheduled Tx"), ("Flagged Exp", "Aging Claim 45d+"), ("Failed Recur", "Plan Renewal"), ("#7c3aed", "#059669")
):
    h = h.replace(o, n)
open("demo-dental-wellness/dashboard.html", "w", encoding="utf-8").write(h)
print("DENTAL & WELLNESS DASHBOARD READY!")
