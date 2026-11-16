js = open("demo-enterprise-impact/app.js", encoding="utf-8").read()
for o, n in (
    ("1.18", "1.09"), ("2.5", "2.8"), ("* 0.05", "* 0.08"), ("* 15", "* 45"),
    ("3-Year Net Revenue", "3-Year Collected Fees"), ("UP 22% YoY Recurring Growth", "~$9.5M/Yr Firm Run-Rate"),
    ("Active Donors (2026)", "Active Matters (2026)"), ("Net Donors", "Net Matters"),
    ("H1 2027 Run-Rate Projection", "H1 2027 Billing Projection"),
    ("Grants, Audits & Failed Gifts", "Low Retainers, WIP & Aging AR"), ("gifts/ea", "invoices"),
    ("donors @ $15", "clients @ $45"), ("5% Full + 10% Half", "16% Reactivation"),
    ("165", "6500"), ("gifts =", "retainers ="),
    ("Grant Risk", "Retainer Low"), ("Flagged Exp", "Unbilled WIP"), ("Failed Recur", "Overdue 60d+"),
    ("/ person", "% Realized"), ("'$' + Number(r.at(4)).toFixed(2) + '% Realized'", "Number(r.at(4)).toFixed(1) + '% Realized'")
):
    js = js.replace(o, n)
open("demo-legal-partners/app.js", "w", encoding="utf-8").write(js)

h = open("demo-enterprise-impact/dashboard.html", encoding="utf-8").read()
for o, n in (
    ("Piedmont Community Impact Alliance", "Piedmont Legal Partners"),
    ("Simulated Sample Organization", "Simulated 16-Attorney Firm • $9.5M Billings"),
    ("Executive Fundraising, Retention &amp; Program Intelligence", "Fee Realization, Evergreen Retainer &amp; WIP/AR Intelligence"),
    ("1,225 Duplicates Removed • 7,403 Typos Standardized", "410 Duplicate Client Records Merged • 2,640 Clio/QB Entries Standardized"),
    ("36-Month Net Revenue + 6-Month Shaded Forecast (Baseline vs. Churn Outreach)", "36-Month Fee Collections + 6-Month Shaded Forecast"),
    ("The Volunteer Multiplier (Avg Lifetime Value)", "The Evergreen Retainer Multiplier (3-Yr Billings)"),
    ("High-Dollar Donor Churn Watchlist (LTV $1,000+ &amp; 120+ Days Lapsed)", "High-Value Lapsed Client Watchlist ($12K+ Billings &amp; 110+ Days Inactive)"),
    ("Donor ID", "Matter ID"), ("Supporter Name", "Client / Matter"), ("Tier", "Practice Area"),
    ("Lifetime Giving", "3-Yr Fees"), ("Last Gift", "Last Invoice"), ("Days Lapsed", "Days Inactive"),
    ("Program Cost Efficiency ($ Cost per Beneficiary)", "Practice Area Fee Realization % &amp; Volume"),
    ("Campaign Profitability &amp; Budget Variance", "Lead Partner Collections &amp; Realization"),
    ("Campaign", "Lead Partner"), ("Channel", "Active Matters"), ("Budget", "3-Yr Billed"), ("Net Raised", "Realized ($)"), ("ROI %", "Realization %"),
    ("Grant Risk", "Retainer Low"), ("Flagged Exp", "Unbilled WIP"), ("Failed Recur", "Overdue 60d+"), ("#7c3aed", "#0d9488")
):
    h = h.replace(o, n)
open("demo-legal-partners/dashboard.html", "w", encoding="utf-8").write(h)
print("LEGAL DASHBOARD READY!")
