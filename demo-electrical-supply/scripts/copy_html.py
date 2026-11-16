h = open("demo-enterprise-impact/dashboard.html", encoding="utf-8").read()

swaps = (
    ("Piedmont Community Impact Alliance", "Piedmont Power &amp; Electrical Supply"),
    ("Simulated Sample Organization", "Simulated $40M Regional Distributor"),
    ("Executive Fundraising, Retention &amp; Program Intelligence", "Commercial Revenue, Gross Margin &amp; Contractor Retention Intelligence"),
    ("Executive Fundraising, Retention & Program Intelligence", "Commercial Revenue, Gross Margin & Contractor Retention Intelligence"),
    ("1,225 Duplicates Removed • 7,403 Typos Standardized", "840 Duplicate SKUs Merged • 4,190 ERP/CRM Records Standardized"),
    ("36-Month Net Revenue + 6-Month Shaded Forecast (Baseline vs. Churn Outreach)", "36-Month Gross Revenue + 6-Month Shaded Forecast (Baseline vs. Contractor Win-Back)"),
    ("Q4 Spikes", "Peak Construction Months"),
    ("With Donor Outreach (5% Full + 10% Half)", "With Contractor Outreach (14% Reactivation)"),
    ("The Volunteer Multiplier (Avg Lifetime Value)", "The Portal Ordering Multiplier (3-Yr Avg Spend)"),
    ("Strategic Insights, Nonprofit Benchmarks &amp; High-Dollar Churn Watchlist", "Commercial Growth Plays, Margin Benchmarks &amp; Lapsed Contractor Watchlist"),
    ("Strategic Insights, Nonprofit Benchmarks & High-Dollar Churn Watchlist", "Commercial Growth Plays, Margin Benchmarks & Lapsed Contractor Watchlist"),
    ("Volunteer-to-Donor Conversion Play", "Counter-to-Portal Conversion Play"),
    ("3.0x Higher LTV ($1,443 vs $482)", "2.4x Higher Account Spend"),
    ("Invite top 500 Donor-Only supporters to VIP hands-on impact days (insider access) &amp; promote Corporate Volunteer Grants matching hours with cash.", "Onboarding top 100 Counter-Only contractors onto job-site mobile ordering + automated Will-Call staging locks in repeat commodity &amp; switchgear orders."),
    ("Invite top 500 Donor-Only supporters to VIP hands-on impact days (insider access) & promote Corporate Volunteer Grants matching hours with cash.", "Onboarding top 100 Counter-Only contractors onto job-site mobile ordering + automated Will-Call staging locks in repeat commodity & switchgear orders."),
    ("High-Dollar Churn Win-Back ROI", "Lapsed Contractor Win-Back ROI"),
    ("Payment Failure Leakage Benchmark", "Unbilled Change-Order &amp; Credit Leakage"),
    ("20%–30% Annual Sustainer Loss", "$620K+ Annual Margin Protected"),
    ("Automated card-updater SMS/email outreach for the 959 Failed Recurring alerts recovers an estimated $68,000+ in annual pledges.", "Flagging unbilled spec upgrades &amp; Net-30 overages before closeout protects 1.5+ points of net EBITDA across commercial switchgear jobs."),
    ("High-Dollar Donor Churn Watchlist (LTV $1,000+ &amp; 120+ Days Lapsed)", "High-Value Lapsed Contractor Watchlist ($50K+ Spend &amp; 65+ Days Inactive)"),
    ("High-Dollar Donor Churn Watchlist (LTV $1,000+ & 120+ Days Lapsed)", "High-Value Lapsed Contractor Watchlist ($50K+ Spend & 65+ Days Inactive)"),
    ("Donor ID", "Account ID"),
    ("Supporter Name", "Contractor Name"),
    ("Tier", "Segment"),
    ("Lifetime Giving", "3-Yr Revenue"),
    ("Last Gift", "Last Order"),
    ("Days Lapsed", "Days Inactive"),
    ("Program Cost Efficiency ($ Cost per Beneficiary)", "Product Line Gross Margin % &amp; Volume"),
    ("Campaign Profitability &amp; Budget Variance", "Customer Segment Revenue &amp; Gross Margin"),
    ("<th>Campaign</th><th>Channel</th><th>Budget</th><th>Net Raised</th><th>ROI %</th>", "<th>Customer Segment</th><th>Accounts</th><th>3-Yr Revenue</th><th>Gross Margin ($)</th><th>Gross Margin %</th>"),
    ("Live Executive Action Queue (Grants, Audits &amp; Failed Recurring — 979 Total)", "Live Operations &amp; Credit Action Queue (Backorders, Margin Leaks &amp; Overdue AR)"),
    ("Live Executive Action Queue (Grants, Audits & Failed Recurring — 979 Total)", "Live Operations & Credit Action Queue (Backorders, Margin Leaks & Overdue AR)"),
    ("All Alert Types (Prioritized)", "All Operational Alerts (Prioritized)"),
    ("Grant Risk", "Backorder Risk"),
    ("At-Risk Grants (Top Priority)", "Custom Switchgear Backorders"),
    ("Flagged Exp", "Margin Leak"),
    ("Flagged Vendor Expenses", "Unbilled Change Orders"),
    ("Failed Recur", "Overdue Net-30"),
    ("Failed Recurring Gifts", "Overdue Net-30 Invoices"),
    ("Name / Foundation / Vendor", "Account / Job"),
    ("Owner / Contact", "Account Rep")
)

for old, new in swaps:
    h = h.replace(old, new)

h = h.replace("#7c3aed", "#d97706")
open("demo-electrical-supply/dashboard.html", "w", encoding="utf-8").write(h)
print("COPIED & CUSTOMIZED WORKING HTML! Bytes:", len(h))
