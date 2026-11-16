import re

playbooks = dict()

playbooks["demo-auto-dealership"] = (
    ("Executive Director Call + Site Tour", "VIP Sales Mgr Equity Appraisal + Service Pass"),
    ("Handwritten Board Impact Letter", "Service BDC 30K/60K Maintenance Voucher"),
    ("VIP Gala & Volunteer Preview Invite", "Pre-Paid Maintenance & Trade-In Upgrade Offer"),
    ("Tier 1 - Top 50 Major Lapsed ($3,000+ LTV)", "Tier 1 - Top 50 High-Equity Buyers ($5,500+ Gross)"),
    ("Personal phone call from Executive Director + private program site tour.", "Personal call from VIP Sales Manager + complimentary trade-in appraisal & detail."),
    ("Tier 2 - Next 150 Mid-Level Lapsed ($1,500-$2,999)", "Tier 2 - Next 150 Service-Loyal Buyers ($3,500-$5,499)"),
    ("Handwritten impact note signed by a Board Member with 2026 outcome snapshot.", "Service Director outreach + $75 factory maintenance & alignment credit."),
    ("Tier 3 - Remaining Lapsed ($1,000-$1,499)", "Tier 3 - Remaining Lapsed Buyers ($2,800-$3,499)"),
    ("VIP invitation to upcoming Gala & hands-on loyal accounts preview day.", "Automated BDC text/email with seasonal tire & oil-change package.")
)

playbooks["demo-dental-wellness"] = (
    ("Executive Director Call + Site Tour", "Clinical Director Call + Priority Hygiene Slot"),
    ("Handwritten Board Impact Letter", "Treatment Coordinator Benefit-Expiration Notice"),
    ("VIP Gala & Volunteer Preview Invite", "In-House Wellness Membership Credit ($75)"),
    ("Tier 1 - Top 50 Major Lapsed ($3,000+ LTV)", "Tier 1 - Top 50 High-Value Patients ($4,500+ LTV)"),
    ("Personal phone call from Executive Director + private program site tour.", "Personal check-in from Lead Hygienist + reserved priority morning hygiene slot."),
    ("Tier 2 - Next 150 Mid-Level Lapsed ($1,500-$2,999)", "Tier 2 - Next 150 Overdue Recall Patients ($2,800-$4,499)"),
    ("Handwritten impact note signed by a Board Member with 2026 outcome snapshot.", "Treatment Coordinator call + annual insurance benefit-use reminder."),
    ("Tier 3 - Remaining Lapsed ($1,000-$1,499)", "Tier 3 - Remaining Overdue Patients ($2,200-$2,799)"),
    ("VIP invitation to upcoming Gala & hands-on loyal accounts preview day.", "Automated 2-way SMS recall link + $75 In-House Wellness Plan enrollment credit.")
)

playbooks["demo-freight-logistics"] = (
    ("Executive Director Call + Site Tour", "VP Fleet Ops Rate Lock + Dedicated Capacity Review"),
    ("Handwritten Board Impact Letter", "Account Mgr Backhaul & Box-Truck Discount Offer"),
    ("VIP Gala & Volunteer Preview Invite", "Shipper Portal Onboarding + Fuel Surcharge Cap"),
    ("Tier 1 - Top 50 Major Lapsed ($3,000+ LTV)", "Tier 1 - Top 20 Major Shippers ($85K+ 3-Yr Spend)"),
    ("Personal phone call from Executive Director + private program site tour.", "VP Fleet Operations call + guaranteed I-85/I-77 dedicated tractor capacity."),
    ("Tier 2 - Next 150 Mid-Level Lapsed ($1,500-$2,999)", "Tier 2 - Next 25 Regional Accounts ($40K-$84K)"),
    ("Handwritten impact note signed by a Board Member with 2026 outcome snapshot.", "Account Manager lane audit + 5% discount on commercial box-truck rentals."),
    ("Tier 3 - Remaining Lapsed ($1,000-$1,499)", "Tier 3 - Remaining Lapsed Shippers ($22K-$39K)"),
    ("VIP invitation to upcoming Gala & hands-on loyal accounts preview day.", "Inside Sales check-in + instant online freight & rental quoting portal invite.")
)

playbooks["demo-legal-partners"] = (
    ("Executive Director Call + Site Tour", "Managing Partner Annual Corporate/Estate Audit"),
    ("Handwritten Board Impact Letter", "Lead Attorney Compliance & Contract Review Check-In"),
    ("VIP Gala & Volunteer Preview Invite", "Evergreen Retainer Priority Access Offer"),
    ("Tier 1 - Top 50 Major Lapsed ($3,000+ LTV)", "Tier 1 - Top 20 Major Clients ($35K+ 3-Yr Fees)"),
    ("Personal phone call from Executive Director + private program site tour.", "Personal call from Managing Partner + complimentary annual corporate/estate review."),
    ("Tier 2 - Next 150 Mid-Level Lapsed ($1,500-$2,999)", "Tier 2 - Next 25 Mid-Tier Matters ($18K-$34K)"),
    ("Handwritten impact note signed by a Board Member with 2026 outcome snapshot.", "Lead Attorney check-in + flat-fee contract/lease compliance audit."),
    ("Tier 3 - Remaining Lapsed ($1,000-$1,499)", "Tier 3 - Remaining Lapsed Clients ($12K-$17K)"),
    ("VIP invitation to upcoming Gala & hands-on loyal accounts preview day.", "Client Relations outreach + priority scheduling under an Evergreen Retainer.")
)

playbooks["demo-hvac-mechanical"] = (
    ("Executive Director Call + Site Tour", "Senior Comfort Advisor 21-Point System Audit"),
    ("Handwritten Board Impact Letter", "CSR Outbound Call + $89 Waived Dispatch Credit"),
    ("VIP Gala & Volunteer Preview Invite", "Comfort Club Renewal + $50 Repair Voucher"),
    ("Tier 1 - Top 50 Major Lapsed ($3,000+ LTV)", "Tier 1 - Top 40 High-LTV Homeowners ($8,500+ Spend)"),
    ("Personal phone call from Executive Director + private program site tour.", "Senior Comfort Advisor call + complimentary 21-point HVAC & water heater inspection."),
    ("Tier 2 - Next 150 Mid-Level Lapsed ($1,500-$2,999)", "Tier 2 - Next 75 Lapsed Club Members ($5,000-$8,499)"),
    ("Handwritten impact note signed by a Board Member with 2026 outcome snapshot.", "CSR outbound call + waived $89 diagnostic dispatch fee on next tune-up."),
    ("Tier 3 - Remaining Lapsed ($1,000-$1,499)", "Tier 3 - Remaining Lapsed Homes ($3,500-$4,999)"),
    ("VIP invitation to upcoming Gala & hands-on loyal accounts preview day.", "Automated SMS/email seasonal reminder with $50 plumbing/HVAC repair voucher.")
)

playbooks["demo-electrical-supply"] = (
    ("Executive Director Call + Site Tour", "VP Sales + Branch Mgr Job-Site Spec Visit"),
    ("Handwritten Board Impact Letter", "Custom Switchgear Quote Rebate Offer"),
    ("VIP Gala & Volunteer Preview Invite", "Outside Rep Counter Lunch & Portal Onboarding"),
    ("Tier 1 - Top 50 Major Lapsed ($3,000+ LTV)", "Tier 1 - Top 15 Major Contractors ($250K+ 3-Yr)"),
    ("Personal phone call from Executive Director + private program site tour.", "Branch Manager + VP Sales site visit with priority switchgear allocation."),
    ("Tier 2 - Next 150 Mid-Level Lapsed ($1,500-$2,999)", "Tier 2 - Next 20 Mid-Tier Contractors ($100K-$249K)"),
    ("Handwritten impact note signed by a Board Member with 2026 outcome snapshot.", "2% volume rebate on next commercial lighting or PLC automation package."),
    ("Tier 3 - Remaining Lapsed ($1,000-$1,499)", "Tier 3 - Remaining Lapsed Accounts ($50K-$99K)"),
    ("VIP invitation to upcoming Gala & hands-on loyal accounts preview day.", "Outside Sales rep check-in + mobile Will-Call ordering portal setup.")
)

for folder, swaps in playbooks.items():
    js_path = f"{folder}/app.js"
    html_path = f"{folder}/dashboard.html"
    js = open(js_path, encoding="utf-8").read()
    for o, n in swaps:
        js = js.replace(o, n)
    open(js_path, "w", encoding="utf-8").write(js)

    html = open(html_path, encoding="utf-8").read()
    html = re.sub(r'src="app\.js[^"]*"', 'src="app.js?v=5"', html)
    open(html_path, "w", encoding="utf-8").write(html)
    print("UPDATED PLAYBOOK:", folder)
