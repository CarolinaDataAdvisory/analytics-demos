js = open("demo-enterprise-impact/app.js", encoding="utf-8").read()
for o, n in (
    ("1.18", "1.10"), ("2.5", "2.8"), ("* 0.05", "* 0.08"), ("* 15", "* 65"),
    ("3-Year Net Revenue", "3-Year Fleet & Freight Revenue"), ("UP 22% YoY Recurring Growth", "~$18.2M/Yr Corridor Run-Rate"),
    ("Active Donors (2026)", "Active Shippers & Renters (2026)"), ("Net Donors", "Net Accounts"),
    ("H1 2027 Run-Rate Projection", "H1 2027 Fleet & Lane Forecast"),
    ("Grants, Audits & Failed Gifts", "Detention, Deadhead & Aging AR"), ("gifts/ea", "loads/rentals"),
    ("donors @ $15", "shippers @ $65"), ("5% Full + 10% Half", "16% Reactivation"),
    ("165", "9200"), ("gifts =", "contracts ="),
    ("Grant Risk", "Unbilled Detention"), ("Flagged Exp", "Idle / Low Margin"), ("Failed Recur", "Overdue Freight AR"),
    ("/ person", "% Margin"), ("'$' + Number(r.at(4)).toFixed(2) + '% Margin'", "Number(r.at(4)).toFixed(1) + '% Margin'")
):
    js = js.replace(o, n)
open("demo-freight-logistics/app.js", "w", encoding="utf-8").write(js)

h = open("demo-enterprise-impact/dashboard.html", encoding="utf-8").read()
for o, n in (
    ("Piedmont Community Impact Alliance", "Carolina Freight &amp; Fleet Logistics"),
    ("Simulated Sample Organization", "Simulated $18M Carrier, Delivery &amp; Rentals"),
    ("Executive Fundraising, Retention &amp; Program Intelligence", "Lane Margin, Fleet Utilization &amp; Shipper Retention Intelligence"),
    ("1,225 Duplicates Removed • 7,403 Typos Standardized", "530 Duplicate Shipper Profiles Merged • 3,910 TMS/ELD/QB Records Cleaned"),
    ("36-Month Net Revenue + 6-Month Shaded Forecast (Baseline vs. Churn Outreach)", "36-Month Freight &amp; Rental Revenue + 6-Month Forecast"),
    ("The Volunteer Multiplier (Avg Lifetime Value)", "The Dedicated Contract Multiplier (3-Yr Spend)"),
    ("High-Dollar Donor Churn Watchlist (LTV $1,000+ &amp; 120+ Days Lapsed)", "High-Volume Lapsed Shipper Watchlist ($22K+ Spend &amp; 110+ Days Inactive)"),
    ("Donor ID", "Shipper ID"), ("Supporter Name", "Shipper / Renter Account"), ("Tier", "Primary Division"),
    ("Lifetime Giving", "3-Yr Revenue"), ("Last Gift", "Last Load"), ("Days Lapsed", "Days Inactive"),
    ("Program Cost Efficiency ($ Cost per Beneficiary)", "Fleet Division Gross Margin % &amp; Volume"),
    ("Campaign Profitability &amp; Budget Variance", "Account Manager Revenue &amp; Margin"),
    ("Campaign", "Account Manager"), ("Channel", "Active Accounts"), ("Budget", "3-Yr Revenue"), ("Net Raised", "Net Margin ($)"), ("ROI %", "Margin %"),
    ("Grant Risk", "Unbilled Detention"), ("Flagged Exp", "Idle / Low Margin"), ("Failed Recur", "Overdue Freight AR"), ("#7c3aed", "#2563eb")
):
    h = h.replace(o, n)
open("demo-freight-logistics/dashboard.html", "w", encoding="utf-8").write(h)
print("FREIGHT DASHBOARD READY!")
