summaries = dict()

summaries["demo-auto-dealership"] = (
    ("1. Turn Aged Used Inventory (>45 Days) & Clear CITs", "Review the 25 pre-owned units over 45 days on lot in Monday's desk huddle to re-price to market, and clear the 21 unfunded Contracts in Transit.", "Aged units bleed ~$55/day in floorplan interest and wholesale depreciation, while unfunded CITs tie up working capital.", "Expected Result: +$485,000 Freed Cash & Avoided Wholesale Loss"),
    ("2. Work Declined MPI Repairs & BDC Stalled Leads", "Have Service BDC follow up on 31 declined Multi-Point Inspection (MPI) brake/30K recommendations and work the 340 stalled internet leads.", "Service labor runs at 67.5% gross margin and closing 15% of stalled BDC leads adds 51 extra retail units with zero extra ad spend.", "Expected Result: +$245,000 Incremental Front & Fixed-Ops Gross"),
    ("3. Mine High-Equity Service Drive Customers", "Assign VIP Sales Managers to greet high-equity customers in the service lane with an appraisal & Pre-Paid Maintenance upgrade offer.", "Sales + Service Loyal buyers generate 2.5x higher 3-year gross profit ($17,658 vs. $13,049) and trade in 18 months sooner.", "Expected Result: +$880,000 Multi-Year Gross Profit Lift")
)

summaries["demo-dental-wellness"] = (
    ("1. Schedule 290 Unscheduled High-Value Treatment Plans", "Have Treatment Coordinators call every patient with an unscheduled crown, bridge, or implant plan over $1,500 to offer flexible payment options.", "Restorative and implant care carry 90%+ net realization and fill high-production doctor chair blocks immediately.", "Expected Result: +$493,000 Scheduled Production (15% Close Rate)"),
    ("2. Reactivate Overdue 6-Month Hygiene & Perio Patients", "Launch automated SMS/email recall reminders plus front-desk outreach for patients overdue past 180 days across all 4 clinic locations.", "Keeping hygiene chairs full protects recurring baseline cash flow and uncovers early restorative needs before emergencies occur.", "Expected Result: +$310,000 Recovered Annual Collections"),
    ("3. Clear 45+ Day Insurance Claims & Wellness Renewals", "Work the 24 aging insurance claims with missing EOBs weekly and auto-renew the 94 expiring In-House Wellness Plan memberships.", "In-House Wellness members generate 2.4x higher 3-year patient collections with zero third-party insurance write-offs.", "Expected Result: +$185,000 Accelerated Cash & Plan Retention")
)

summaries["demo-freight-logistics"] = (
    ("1. Bill Uncollected Detention, Layover & Liftgate Fees", "Audit the 23 unbilled accessorial alerts weekly with shipper sign-off timestamps before closing freight bills in accounting.", "Unbilled detention and liftgate charges leak directly out of net margin on otherwise profitable dedicated and final-mile runs.", "Expected Result: +$135,000 Pure Net Margin Recovered"),
    ("2. Convert Stalled Freight & Fleet Rental RFQs (275 Bids)", "Have Account Managers follow up within 48 hours on all 275 freight and commercial box-truck rental quotes open past 10 days.", "Closing 15% of stalled RFQs adds 41 recurring contracts and higher box-truck fleet utilization without adding tractors.", "Expected Result: +$377,200 Incremental Annual Revenue"),
    ("3. Re-Price Low-Margin Deadhead Lanes & Win Back Shippers", "Re-quote or backhaul-match the 20 lanes running below 12% margin and run 90-day outreach on lapsed $22K+ shippers.", "Dedicated contract shippers generate 2.5x higher 3-year spend than spot freight while stabilizing weekly driver miles.", "Expected Result: +$420,000 Protected Fleet Margin")
)

summaries["demo-legal-partners"] = (
    ("1. Replenish Depleted Trust Retainers & Bill Aging WIP", "Trigger automated evergreen retainer top-up notices for the 21 low-trust matters and finalize all unbilled WIP older than 45 days.", "Unbilled WIP loses 15%–25% of its collectible value every 30 days it sits uninvoiced, while evergreen retainers prevent AR write-offs.", "Expected Result: +$340,000 Accelerated Cash & Avoided Write-Downs"),
    ("2. Convert 185 Unsigned Qualified Consultations", "Have Managing Partners and Intake Coordinators follow up within 5 days on all qualified consultations awaiting signed engagement letters.", "Converting just 15% of stalled consultations adds 28 retained matters (~$6,500 avg fee) with zero additional marketing spend.", "Expected Result: +$182,000 New Retainer Collections"),
    ("3. Collect 60+ Day Past-Due Invoices & Shift to Retainers", "Have the Billing Admin desk execute structured payment-plan calls on the 64 overdue invoices and transition hourly clients to evergreen retainers.", "Evergreen retainer matters achieve 2.3x higher 3-year realization than standard hourly billing across all practice groups.", "Expected Result: +$265,000 Recovered Past-Due Receivables")
)

summaries["demo-hvac-mechanical"] = (
    ("1. Close Stalled Replacement Estimates (310 Quotes)", "Have Comfort Advisors call every homeowner with an open HVAC or water-heater replacement quote older than 7 days to offer 0% financing.", "Replacement installs carry 41%–45% gross margin; timely financing follow-up wins 15% of stalled bids before competitors re-quote.", "Expected Result: +$418,300 Revenue (47 Installs Closed)"),
    ("2. Renew Expiring Comfort Club Maintenance Plans", "Work the 114 Plan Renewal alerts via CSR outbound calls and SMS booking links 30 days prior to expiration.", "Comfort Club members generate ~2x higher 3-year spend and call Carolina Climate first when aging AC units fail in July.", "Expected Result: +$145,000 Protected Recurring & Pull-Through"),
    ("3. Coach High-Callback Techs & Re-Engage Lapsed Homes", "Review the 18 repeat warranty callbacks in Monday's dispatch huddle and send $50 tune-up vouchers to lapsed $3,500+ homeowners.", "Eliminating unbilled callback truck rolls recovers peak-season dispatch capacity worth $450/hr in lost billable time.", "Expected Result: +$110,000+ Recovered Margin & Win-Backs")
)

summaries["demo-electrical-supply"] = (
    ("1. Recover Stalled Commercial Bids (460 Quotes)", "Have Inside Sales & Estimators send a 48-hour price-lock follow-up on all 460 commercial quotes open past 21 days.", "Contractors often delay submittals over minor spec questions; proactive follow-up beats competing supply houses before re-bidding.", "Expected Result: +$1.69M Revenue (~15% / 69 Jobs Won)"),
    ("2. Execute 90-Day Lapsed Contractor Win-Back", "Assign Branch Managers & Outside Reps to conduct job-site visits for Top 15 lapsed accounts ($350K+) and offer a 2% lighting/PLC rebate.", "Retaining an established $50K+ contractor costs ~90% less than acquiring a new commercial account from scratch.", "Expected Result: +$650K–$950K Recovered Annual Spend"),
    ("3. Clear Backorders, Change Orders & Overdue AR", "Review the 78 prioritized Operational Alerts weekly—billing unbilled spec changes before closeout and offering approved switchgear substitutes.", "Unbilled change orders and Net-30 overages silently erode 1.5+ points of net EBITDA across commercial switchgear jobs.", "Expected Result: +$620K+ Protected Margin & Faster Cash")
)

colors = ("#f59e0b", "#10b981", "#f43f5e")
lt = chr(60)
gt = chr(62)

for folder, items in summaries.items():
    path = f"{folder}/dashboard.html"
    h = open(path, encoding="utf-8").read()
    marker = f'{lt}div class="card" style="margin-top:24px;border-color:#10b981;"{gt}'
    if marker in h:
        head = h.split(marker).pop(0)
        cards_html = ""
        for idx, (title, what, why, res) in enumerate(items):
            c = colors.__getitem__(idx)
            cards_html += f'{lt}div class="ibox" style="border-color:{c};"{gt}{lt}h4{gt}{title}{lt}/h4{gt}{lt}p style="margin:0 0 8px;color:#cbd5e1;"{gt}{lt}strong{gt}What to Do:{lt}/strong{gt} {what}{lt}/p{gt}{lt}p style="margin:0 0 8px;color:#cbd5e1;"{gt}{lt}strong{gt}Why:{lt}/strong{gt} {why}{lt}/p{gt}{lt}div class="bstat" style="font-size:15px;color:#10b981;"{gt}{res}{lt}/div{gt}{lt}/div{gt}\n'
        new_block = f'{marker}\n  {lt}h3{gt}Executive Summary: Top 3 Action Items, Execution Plan &amp; Expected ROI{lt}/h3{gt}\n  {lt}div class="grid3" style="margin-bottom:0;"{gt}\n{cards_html}  {lt}/div{gt}\n{lt}/div{gt}\n{lt}script src="app.js?v=4"{gt}{lt}/script{gt}\n{lt}/body{gt}\n{lt}/html{gt}'
        open(path, "w", encoding="utf-8").write(head + new_block)
        print("UPDATED TOP-3 SUMMARY:", folder)
