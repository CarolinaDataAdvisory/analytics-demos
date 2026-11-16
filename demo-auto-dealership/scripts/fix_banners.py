import re

banners = dict()

banners["demo-auto-dealership"] = (
    "DEALERSHIP GROWTH BENCHMARKS &amp; SERVICE-TO-SALES EQUITY WATCHLIST",
    "Service-to-Sales Loyalty Play",
    "2.5x Higher 3-Yr Gross Profit",
    "Enrolling buyers into Pre-Paid Maintenance at F&amp;I delivery locks in service retention and pulls forward trade-in cycles by 18 months.",
    "Aged Lot &amp; Declined MPI Leakage",
    "$730K+ Annual Profit Opportunity",
    "Re-pricing 25 pre-owned units over 45 days on lot and following up on 31 declined MPI brake/30K repairs recovers high-margin Fixed-Ops &amp; front-end gross.",
    "Service-to-Sales &amp; Lapsed Service Watchlist ($2,800+ Gross &amp; 150+ Days)",
    "via VIP Sales Mgr calls, equity appraisals &amp; service passes"
)

banners["demo-dental-wellness"] = (
    "CLINIC GROWTH BENCHMARKS &amp; OVERDUE 6-MONTH RECALL WATCHLIST",
    "In-House Wellness Plan Play",
    "2.4x Higher 3-Yr Patient LTV",
    "Enrolling uninsured and PPO patients into the In-House Wellness Plan at hygiene checkout locks in 2 annual cleanings and higher restorative acceptance.",
    "Unscheduled Treatment &amp; Claim Leakage",
    "$678K+ Annual Collection Opportunity",
    "Scheduling 290 unscheduled crown/implant plans and working 24 aging 45+ day insurance claims recovers high-margin production immediately.",
    "Overdue 6-Month Patient Recall Watchlist ($2,200+ Spend &amp; 180+ Days)",
    "via Hygienist recall calls, benefit reminders &amp; SMS booking links"
)

banners["demo-freight-logistics"] = (
    "FLEET MARGIN BENCHMARKS &amp; LAPSED SHIPPER WATCHLIST",
    "Spot-to-Dedicated Contract Play",
    "2.5x Higher 3-Yr Account Spend",
    "Converting repeat spot shippers onto Dedicated Portal Contracts locks in weekly tractor utilization and stabilizes corridor lane margins.",
    "Unbilled Detention &amp; Deadhead Leakage",
    "$555K+ Annual Margin Opportunity",
    "Billing 23 uncollected detention/liftgate fees and re-pricing 20 low-margin deadhead lanes drops pure profit straight to the bottom line.",
    "High-Volume Lapsed Shipper Watchlist ($22K+ Spend &amp; 110+ Days)",
    "via VP Fleet Ops lane audits, rate locks &amp; portal invites"
)

banners["demo-legal-partners"] = (
    "PRACTICE REALIZATION BENCHMARKS &amp; LAPSED CLIENT WATCHLIST",
    "Evergreen Retainer Conversion Play",
    "2.3x Higher 3-Yr Realized Fees",
    "Transitioning hourly business and family-law matters onto auto-replenishing Evergreen Retainers eliminates write-downs and accelerates cash flow.",
    "Unbilled WIP &amp; Aging AR Leakage",
    "$605K+ Annual Collection Opportunity",
    "Finalizing 24 aging WIP files (45d+) and collecting 64 past-due invoices (60d+) prevents fee write-offs across all 5 practice groups.",
    "High-Value Lapsed Client Watchlist ($12K+ Fees &amp; 110+ Days)",
    "via Managing Partner calls, annual audits &amp; retainer reviews"
)

banners["demo-hvac-mechanical"] = (
    "DISPATCH MARGIN BENCHMARKS &amp; LAPSED HOMEOWNER WATCHLIST",
    "On-Demand to Comfort Club Play",
    "2.2x Higher 3-Yr Customer LTV",
    "Training techs &amp; CSRs to offer Comfort Club membership at diagnostic checkout locks in 2 annual tune-ups and priority replacement bids.",
    "Unsold Quote &amp; Callback Leakage",
    "$563K+ Annual Profit Opportunity",
    "Closing 15% of 310 stalled replacement quotes and curbing 18 repeat warranty callbacks recovers peak-season dispatch capacity.",
    "High-LTV Lapsed Homeowner Watchlist ($3,500+ Spend &amp; 150+ Days)",
    "via Comfort Advisor calls, $89 waived dispatch &amp; SMS offers"
)

banners["demo-electrical-supply"] = (
    "DISTRIBUTOR MARGIN BENCHMARKS &amp; LAPSED CONTRACTOR WATCHLIST",
    "Counter-to-Portal Conversion Play",
    "2.4x Higher 3-Yr Account Spend",
    "Onboarding Counter-Only contractors onto mobile job-site ordering + Will-Call staging locks in repeat switchgear and commodity pull-through.",
    "Unbilled Change-Order &amp; Bid Leakage",
    "$1.69M+ Annual Revenue Opportunity",
    "Following up on 460 stalled commercial quotes (>21d) and billing 18 unbilled spec changes protects 1.5+ points of net EBITDA.",
    "High-Value Lapsed Contractor Watchlist ($50K+ Spend &amp; 65+ Days)",
    "via Branch Mgr job-site visits, spec reviews &amp; lighting rebates"
)

for folder, b in banners.items():
    sec_hdr, b1_t, b1_s, b1_p, b3_t, b3_s, b3_p, wl_hdr, wb_via = b
    html_path = f"{folder}/dashboard.html"
    h = open(html_path, encoding="utf-8").read()

    # Replace section header
    h = re.sub(r"<h3>Strategic Insights, Nonprofit Benchmarks.*?</h3>", f"<h3>{sec_hdr}</h3>", h, flags=re.IGNORECASE)
    # Replace Box 1 (Volunteer-to-Donor)
    h = re.sub(r'<h4>Volunteer-to-Donor Conversion Play</h4>\s*<div class="bstat">.*?</div>\s*<p[^>]*>.*?</p>', f'<h4>{b1_t}</h4>\n      <div class="bstat">{b1_s}</div>\n      <p style="margin:0;color:#cbd5e1;">{b1_p}</p>', h, flags=re.DOTALL)
    # Replace Box 3 (Payment Failure / annual pledges)
    h = re.sub(r'<h4>Payment Failure Leakage Benchmark</h4>\s*<div class="bstat">.*?</div>\s*<p[^>]*>.*?</p>', f'<h4>{b3_t}</h4>\n      <div class="bstat">{b3_s}</div>\n      <p style="margin:0;color:#cbd5e1;">{b3_p}</p>', h, flags=re.DOTALL)
    # Replace Watchlist table sub-header
    h = re.sub(r"<h3>High-Dollar Donor Churn Watchlist.*?</h3>", f"<h3>{wl_hdr}</h3>", h, flags=re.IGNORECASE)
    # Cache-bust app.js
    h = re.sub(r'src="app\.js[^"]*"', 'src="app.js?v=6"', h)
    open(html_path, "w", encoding="utf-8").write(h)

    # Fix Box 2 dynamic description in app.js ("handwritten board notes & VIP tours... half-gift")
    js_path = f"{folder}/app.js"
    js = open(js_path, encoding="utf-8").read()
    js = re.sub(
        r"via calls, handwritten board notes.*?reactivation\.",
        f"{wb_via} at ' + wbPct + '% reactivation.",
        js
    )
    # Define wbPct cleanly if not present
    if "const wbPct" not in js:
        js = js.replace("const wbRoi =", "const wbPct = Math.round((yrRev / annualPool) * 100);\nconst wbRoi =")
    open(js_path, "w", encoding="utf-8").write(js)
    print("FIXED BANNERS:", folder)
