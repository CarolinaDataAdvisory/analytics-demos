js = open("demo-enterprise-impact/app.js", encoding="utf-8").read()

replacements = (
    ("1.18", "1.09"),
    ("2.5", "3.0"),
    ("* 0.05", "* 0.07"),
    ("* 15", "* 120"),
    ("3-Year Net Revenue", "3-Year Gross Revenue"),
    ("UP 22% YoY Recurring Growth", "~$40.4M/Yr Regional Run-Rate"),
    ("Active Donors (2026)", "Active Contractors (2026)"),
    ("Net Donors", "Net Accounts"),
    ("H1 2027 Run-Rate Projection", "H1 2027 Backlog & Run-Rate"),
    ("Grants, Audits & Failed Gifts", "Backorders, Change Orders & AR"),
    ("gifts/ea", "orders"),
    ("Donor-Only supporters into volunteers adds ~$550K in cumulative lifetime giving.", "Counter-Only contractors to Portal ordering adds ~$1.8M in incremental pull-through revenue."),
    ("Executive Director Call + Site Tour", "VP Sales + Branch Mgr Job-Site Visit"),
    ("Handwritten Board Impact Letter", "Custom Switchgear Quote Rebate Offer"),
    ("VIP Gala & Volunteer Preview Invite", "Outside Rep Counter Lunch & Spec Review"),
    ("High-Dollar Churn Win-Back ROI (6-Mo & 12-Mo)", "Contractor Win-Back ROI (6-Mo & 12-Mo)"),
    ("donors @ $15", "accts @ $120"),
    ("5% Full + 10% Half", "14% Reactivation"),
    ("90-Day Lapsed Donor Outreach Playbook", "90-Day Lapsed Contractor Playbook"),
    ("Tier 1 - Top 50 Major Lapsed ($3,000+ LTV)", "Tier 1 - Top 15 Major Accounts ($350K+ 3-Yr)"),
    ("Personal phone call from Executive Director + private program site tour.", "Branch Manager + VP Sales site visit with priority switchgear allocation."),
    ("Tier 2 - Next 150 Mid-Level Lapsed ($1,500-$2,999)", "Tier 2 - Next 20 Mid-Tier Contractors ($150K-$349K)"),
    ("Handwritten impact note signed by a Board Member with 2026 outcome snapshot.", "2% volume rebate on next commercial lighting or PLC package."),
    ("Tier 3 - Remaining Lapsed ($1,000-$1,499)", "Tier 3 - Remaining Lapsed ($50K-$149K)"),
    ("VIP invitation to upcoming Gala & hands-on volunteer preview day.", "Outside Sales rep check-in + mobile Will-Call portal onboarding."),
    ("Digital Engagement Funnel & Checkout Recovery Opportunity", "Commercial Quote-to-Order Funnel & Bid Recovery"),
    ("supporters abandoned the donation page. Triggering an automated 24-hr reminder email recovers ~15%", "commercial quotes sit stalled past 21 days. Automated Estimator follow-up closes ~15%"),
    ("165", "24500"),
    ("Grant Risk", "Backorder Risk"),
    ("Flagged Exp", "Margin Leak"),
    ("Failed Recur", "Overdue Net-30")
)

for old, new in replacements:
    js = js.replace(old, new)

open("demo-electrical-supply/app.js", "w", encoding="utf-8").write(js)
print("CREATED demo-electrical-supply/app.js! Bytes:", len(js))
