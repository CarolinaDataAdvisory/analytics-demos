js = open("demo-enterprise-impact/app.js", encoding="utf-8").read()
for o, n in (
    ("1.18", "1.09"), ("2.5", "2.8"), ("* 0.05", "* 0.09"), ("* 15", "* 35"),
    ("3-Year Net Revenue", "3-Year Dealership Revenue"), ("UP 22% YoY Recurring Growth", "~$68.4M/Yr 4-Rooftop Run-Rate"),
    ("Active Donors (2026)", "Active DMS Customers (2026)"), ("Net Donors", "Net Customers"),
    ("H1 2027 Run-Rate Projection", "H1 2027 Sales & Fixed-Ops Forecast"),
    ("Grants, Audits & Failed Gifts", "Aged Lot, Declined MPI & CIT"), ("gifts/ea", "ROs & deals"),
    ("donors @ $15", "customers @ $35"), ("5% Full + 10% Half", "18% Reactivation"),
    ("165", "3700"), ("gifts =", "units ="),
    ("Grant Risk", "Aged Lot >45d"), ("Flagged Exp", "Declined MPI"), ("Failed Recur", "Unfunded CIT"),
    ("r.at(0) + ' (' + Number(r.at(2)).toLocaleString() + ' served | ' + r.at(3) + '/100)'", "r.at(0) + ' (' + fmt(r.at(2)) + ' rev)'"),
    ("'$' + Number(r.at(4)).toFixed(2) + '/ person'", "Number(r.at(4)).toFixed(1) + '% GM'"),
    ("Digital Engagement Funnel & Checkout Recovery Opportunity", "BDC Lead-to-Showroom Funnel & Stalled Lead Recovery"),
    ("Checkout Recovery Play: ' + abCount.toLocaleString() + ' supporters abandoned the donation page. Triggering an automated 24-hr reminder email recovers ~15%", "BDC Recovery Play: ' + abCount.toLocaleString() + ' showroom & internet leads sit unworked past 7 days. VIP Manager follow-up closes ~15%")
):
    js = js.replace(o, n)
open("demo-auto-dealership/app.js", "w", encoding="utf-8").write(js)

h = open("demo-enterprise-impact/dashboard.html", encoding="utf-8").read()
for o, n in (
    ("Piedmont Community Impact Alliance", "Piedmont Motors &amp; Auto Group"),
    ("Simulated Sample Organization", "Simulated 4-Rooftop Group • $68M Revenue"),
    ("Executive Fundraising, Retention &amp; Program Intelligence", "Fixed-Ops Absorption, Used Lot Turn &amp; Service-to-Sales Intelligence"),
    ("1,225 Duplicates Removed • 7,403 Typos Standardized", "1,480 Duplicate DMS Profiles Merged • 6,850 CDK/VinSolutions Records Cleaned"),
    ("36-Month Net Revenue + 6-Month Shaded Forecast (Baseline vs. Churn Outreach)", "36-Month Dealership Revenue + 6-Month Shaded Forecast"),
    ("The Volunteer Multiplier (Avg Lifetime Value)", "The Service-Loyal Buyer Multiplier (3-Yr Gross Profit)"),
    ("High-Dollar Donor Churn Watchlist (LTV $1,000+ &amp; 120+ Days Lapsed)", "Service-to-Sales Equity &amp; Lapsed Service Watchlist ($2,800+ Gross &amp; 150+ Days)"),
    ("Donor ID", "DMS ID"), ("Supporter Name", "Customer Name"), ("Tier", "Primary Rooftop"),
    ("Lifetime Giving", "3-Yr Gross Profit"), ("Last Gift", "Last Visit/Deal"), ("Days Lapsed", "Days Inactive"),
    ("Program Cost Efficiency ($ Cost per Beneficiary)", "Department Gross Margin % &amp; Volume"),
    ("Campaign Profitability &amp; Budget Variance", "Rooftop Revenue &amp; Gross Profit Contribution"),
    ("Campaign", "Dealership Rooftop"), ("Channel", "Active Customers"), ("Budget", "3-Yr Gross Rev"), ("Net Raised", "Gross Profit ($)"), ("ROI %", "Gross Margin %"),
    ("Grant Risk", "Aged Lot >45d"), ("Flagged Exp", "Declined MPI"), ("Failed Recur", "Unfunded CIT"), ("#7c3aed", "#dc2626")
):
    h = h.replace(o, n)
open("demo-auto-dealership/dashboard.html", "w", encoding="utf-8").write(h)
print("DEALERSHIP DASHBOARD READY!")
