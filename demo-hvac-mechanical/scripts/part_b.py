h = open("demo-enterprise-impact/dashboard.html", encoding="utf-8").read()
for o, n in (
    ("Piedmont Community Impact Alliance", "Carolina Climate &amp; Mechanical"),
    ("Simulated Sample Organization", "Simulated $12M HVAC &amp; Plumbing Contractor"),
    ("Executive Fundraising, Retention &amp; Program Intelligence", "Dispatch Revenue, Gross Margin &amp; Comfort Club Intelligence"),
    ("1,225 Duplicates Removed • 7,403 Typos Standardized", "615 Duplicate Addresses Merged • 3,280 ServiceTitan/QB Records Cleaned"),
    ("36-Month Net Revenue + 6-Month Shaded Forecast (Baseline vs. Churn Outreach)", "36-Month Gross Revenue + 6-Month Shaded Forecast"),
    ("The Volunteer Multiplier (Avg Lifetime Value)", "The Comfort Club Multiplier (3-Yr Customer LTV)"),
    ("High-Dollar Donor Churn Watchlist (LTV $1,000+ &amp; 120+ Days Lapsed)", "High-LTV Lapsed Homeowner Watchlist ($3,500+ Spend &amp; 150+ Days Inactive)"),
    ("Donor ID", "Customer ID"), ("Supporter Name", "Homeowner Name"), ("Tier", "Plan Status"),
    ("Lifetime Giving", "3-Yr Spend"), ("Last Gift", "Last Service"), ("Days Lapsed", "Days Inactive"),
    ("Program Cost Efficiency ($ Cost per Beneficiary)", "Service Line Gross Margin % &amp; Volume"),
    ("Campaign Profitability &amp; Budget Variance", "Service Territory Revenue &amp; Gross Margin"),
    ("Campaign", "City / Territory"), ("Channel", "Active Homes"), ("Budget", "3-Yr Revenue"), ("Net Raised", "Gross Margin ($)"), ("ROI %", "Gross Margin %"),
    ("Grant Risk", "Unsold Estimate"), ("Flagged Exp", "Tech Callback"), ("Failed Recur", "Plan Renewal"), ("#7c3aed", "#0284c7")
):
    h = h.replace(o, n)
open("demo-hvac-mechanical/dashboard.html", "w", encoding="utf-8").write(h)
print("PART B DONE! HVAC DASHBOARD READY!")
