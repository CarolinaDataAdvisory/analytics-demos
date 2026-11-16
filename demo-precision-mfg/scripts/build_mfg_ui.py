import re

js = open("demo-enterprise-impact/app.js", encoding="utf-8").read()
for o, n in (
    ("1.18", "1.10"), ("2.5", "2.8"), ("* 0.05", "* 0.09"), ("* 15", "* 85"),
    ("3-Year Net Revenue", "3-Year Plant Shipments"), ("UP 22% YoY Recurring Growth", "~$26.4M/Yr Job-Shop Run-Rate"),
    ("Active Donors (2026)", "Active OEM Accounts (2026)"), ("Net Donors", "Net OEMs"),
    ("H1 2027 Run-Rate Projection", "H1 2027 Backlog & Shipment Forecast"),
    ("Grants, Audits & Failed Gifts", "Margin Variances, Scrap & Renewals"), ("gifts/ea", "work orders"),
    ("donors @ $15", "OEMs @ $85"), ("5% Full + 10% Half", "18% Reactivation"),
    ("165", "21500"), ("gifts =", "POs ="),
    ("Grant Risk", "Margin Variance"), ("Flagged Exp", "Scrap / Rework"), ("Failed Recur", "Blanket Renewal"),
    ("r.at(0) + ' (' + Number(r.at(2)).toLocaleString() + ' served | ' + r.at(3) + '/100)'", "r.at(0) + ' (' + fmt(r.at(2)) + ' shipped)'"),
    ("'$' + Number(r.at(4)).toFixed(2) + '/ person'", "Number(r.at(4)).toFixed(1) + '% GM'"),
    ("Digital Engagement Funnel & Checkout Recovery Opportunity", "Engineering RFQ-to-PO Funnel & Stalled Bid Recovery"),
    ("Checkout Recovery Play: ' + abCount.toLocaleString() + ' supporters abandoned the donation page. Triggering an automated 24-hr reminder email recovers ~15%", "RFQ Recovery Play: ' + abCount.toLocaleString() + ' engineering RFQs sit stalled past 14 days. DFM estimator follow-up closes ~15%"),
    ("Executive Director Call + Site Tour", "VP Mfg Plant Tour + DFM Cost-Down Review"),
    ("Handwritten Board Impact Letter", "Lead Estimator Blanket-PO Tier Rebate"),
    ("VIP Gala & Volunteer Preview Invite", "OEM Sales Dir Quick-Turn Prototype Slot"),
    ("Tier 1 - Top 50 Major Lapsed ($3,000+ LTV)", "Tier 1 - Top 15 Major OEMs ($250K+ 3-Yr)"),
    ("Personal phone call from Executive Director + private program site tour.", "VP Manufacturing call + engineering DFM cost-reduction review."),
    ("Tier 2 - Next 150 Mid-Level Lapsed ($1,500-$2,999)", "Tier 2 - Next 15 Mid-Tier Accounts ($120K-$249K)"),
    ("Handwritten impact note signed by a Board Member with 2026 outcome snapshot.", "Lead Estimator outreach + 3% volume rebate on Annual Blanket PO."),
    ("Tier 3 - Remaining Lapsed ($1,000-$1,499)", "Tier 3 - Remaining Lapsed OEMs ($65K-$119K)"),
    ("VIP invitation to upcoming Gala & hands-on volunteer preview day.", "OEM Sales Director check-in + 5-day quick-turn CNC prototype slot.")
):
    js = js.replace(o, n)

js = re.sub(r"Quick Win:[^'\"]+", "Quick Win: Converting 20 Spot-PO buyers onto Annual Blanket PO + VMI stocking agreements adds ~$1.6M in predictable machine utilization.", js)
js = re.sub(r"via calls, handwritten board notes.*?reactivation\.", "via VP Mfg DFM reviews, Blanket-PO rebates & quick-turn slots at ' + wbPct + '% reactivation.", js)
js = re.sub(r"\bdonors\b", "OEM accounts", js, flags=re.IGNORECASE)
js = re.sub(r"\bdonor\b", "OEM account", js, flags=re.IGNORECASE)
js = re.sub(r"\bvolunteers?\b", "Blanket PO accounts", js, flags=re.IGNORECASE)
if "const wbPct" not in js:
    js = js.replace("const wbRoi =", "const wbPct = Math.round((yrRev / annualPool) * 100);\nconst wbRoi =")
open("demo-precision-mfg/app.js", "w", encoding="utf-8").write(js)

h = open("demo-enterprise-impact/dashboard.html", encoding="utf-8").read()
for o, n in (
    ("Piedmont Community Impact Alliance", "Rowan Precision Manufacturing &amp; Fab"),
    ("Simulated Sample Organization", "Simulated $26M CNC &amp; Metal Fab Job Shop"),
    ("Executive Fundraising, Retention &amp; Program Intelligence", "Quoted-vs-Actual Margin, Scrap Variance &amp; OEM Retention Intelligence"),
    ("1,225 Duplicates Removed • 7,403 Typos Standardized", "390 Duplicate BOM/Part Records Merged • 2,840 JobBOSS/QB Entries Cleaned"),
    ("36-Month Net Revenue + 6-Month Shaded Forecast (Baseline vs. Churn Outreach)", "36-Month Plant Shipments + 6-Month Shaded Forecast"),
    ("The Volunteer Multiplier (Avg Lifetime Value)", "The Blanket PO + VMI Multiplier (3-Yr Spend)"),
    ("Donor ID", "OEM ID"), ("Supporter Name", "OEM Customer"), ("Tier", "Primary Work Center"),
    ("Lifetime Giving", "3-Yr Shipments"), ("Last Gift", "Last Ship Date"), ("Days Lapsed", "Days Inactive"),
    ("Program Cost Efficiency ($ Cost per Beneficiary)", "Work Center Gross Margin % &amp; Volume"),
    ("Campaign Profitability &amp; Budget Variance", "Account Engineer Shipments &amp; Gross Margin"),
    ("Campaign", "Account Engineer"), ("Channel", "Active OEMs"), ("Budget", "3-Yr Shipped"), ("Net Raised", "Gross Margin ($)"), ("ROI %", "Gross Margin %"),
    ("Grant Risk", "Margin Variance"), ("Flagged Exp", "Scrap / Rework"), ("Failed Recur", "Blanket Renewal"), ("#7c3aed", "#4f46e5")
):
    h = h.replace(o, n)

h = re.sub(r"<h3>Strategic Insights, Nonprofit Benchmarks.*?</h3>", "<h3>PLANT MARGIN BENCHMARKS &amp; LAPSED OEM WATCHLIST</h3>", h, flags=re.IGNORECASE)
h = re.sub(r'<h4>Volunteer-to-Donor Conversion Play</h4>\s*<div class="bstat">.*?</div>\s*<p[^>]*>.*?</p>', '<h4>Spot-to-Blanket PO Conversion Play</h4>\n      <div class="bstat">2.6x Higher 3-Yr Account Spend</div>\n      <p style="margin:0;color:#cbd5e1;">Transitioning repeat spot buyers onto Annual Blanket POs + VMI stocking stabilizes CNC spindle hours and raw material buying.</p>', h, flags=re.DOTALL)
h = re.sub(r'<h4>Payment Failure Leakage Benchmark</h4>\s*<div class="bstat">.*?</div>\s*<p[^>]*>.*?</p>', '<h4>Quote-vs-Actual Variance &amp; Scrap Leakage</h4>\n      <div class="bstat">$688K+ Annual Profit Opportunity</div>\n      <p style="margin:0;color:#cbd5e1;">Re-quoting 21 jobs running +14% over estimated shop hours and closing 15% of 215 stalled engineering RFQs protects plant EBITDA.</p>', h, flags=re.DOTALL)
h = re.sub(r"<h3>High-Dollar Donor Churn Watchlist.*?</h3>", "<h3>High-Value Lapsed OEM Watchlist ($65K+ Spend &amp; 105+ Days Inactive)</h3>", h, flags=re.IGNORECASE)

lt, gt = chr(60), chr(62)
marker = f'{lt}div class="card" style="margin-top:24px;border-color:#10b981;"{gt}'
if marker in h:
    head = h.split(marker).pop(0)
    items = (
        ("1. Re-Price Over-Budget Repeat Jobs &amp; Curb Scrap", "Audit the 21 work orders exceeding quoted shop hours by 14%+ and review the 18 CNC tolerance rework alerts before the next production release.", "Silent labor overruns and raw material spikes erode 8–12 margin points on repeat OEM parts if estimators don't adjust routing standards.", "Expected Result: +$315,000 Protected Annual Gross Margin", "#f59e0b"),
        ("2. Convert 215 Stalled Engineering RFQs (14d+)", "Have Cost Estimators and Sales Engineers follow up on all 215 open CAD/DFM quotes with value-engineering cost-down options.", "Closing 15% of stalled RFQs adds 32 production orders (~$21,500 avg lot) and fills open Q1/Q2 5-axis CNC capacity.", "Expected Result: +$688,000 Incremental Plant Shipments", "#10b981"),
        ("3. Lock In Annual Blanket PO &amp; Steel/Alum Resets", "Execute the 37 Blanket Renewal steel/aluminum index resets and pitch Annual Blanket POs to top lapsed $65K+ OEM accounts.", "Blanket PO + VMI accounts generate 2.6x higher 3-year revenue while eliminating emergency spot-buy material premiums.", "Expected Result: +$540,000 Recurring Backlog Secured", "#f43f5e")
    )
    cards_html = ""
    for title, what, why, res, c in items:
        cards_html += f'{lt}div class="ibox" style="border-color:{c};"{gt}{lt}h4{gt}{title}{lt}/h4{gt}{lt}p style="margin:0 0 8px;color:#cbd5e1;"{gt}{lt}strong{gt}What to Do:{lt}/strong{gt} {what}{lt}/p{gt}{lt}p style="margin:0 0 8px;color:#cbd5e1;"{gt}{lt}strong{gt}Why:{lt}/strong{gt} {why}{lt}/p{gt}{lt}div class="bstat" style="font-size:15px;color:#10b981;"{gt}{res}{lt}/div{gt}{lt}/div{gt}\n'
    h = f'{head}{marker}\n  {lt}h3{gt}Executive Summary: Top 3 Action Items, Execution Plan &amp; Expected ROI{lt}/h3{gt}\n  {lt}div class="grid3" style="margin-bottom:0;"{gt}\n{cards_html}  {lt}/div{gt}\n{lt}/div{gt}\n{lt}script src="app.js?v=1"{gt}{lt}/script{gt}\n{lt}/body{gt}\n{lt}/html{gt}'

open("demo-precision-mfg/dashboard.html", "w", encoding="utf-8").write(h)
print("MANUFACTURING DASHBOARD READY!")
