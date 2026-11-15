import csv
import os
import re
import sqlite3
from datetime import datetime

raw_dir = os.path.join("demo-enterprise-impact", "data", "raw")
clean_dir = os.path.join("demo-enterprise-impact", "data", "clean")
os.makedirs(clean_dir, exist_ok=True)
db_path = os.path.join("demo-enterprise-impact", "enterprise_impact.db")

if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

def read_csv(name):
    with open(os.path.join(raw_dir, name), "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def clean_date(val):
    val = (val or "").strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%b %d, %Y"):
        try:
            return datetime.strptime(val, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None

def clean_phone(val):
    digits = re.sub(r"\D", "", val or "")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}" if len(digits) == 10 else ""

# 1. Clean Constituents
raw_const = read_csv("constituents.csv")
cur.execute("""CREATE TABLE constituents (
    constituent_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT,
    email_status TEXT, phone TEXT, city TEXT, state TEXT, zip_code TEXT,
    constituent_type TEXT, acquisition_channel TEXT, signup_date TEXT,
    wealth_tier TEXT, is_opted_out INTEGER)""")

seen_emails = set()
bad_emails = 0
for r in raw_const:
    em = (r["email"] or "").strip().lower()
    if not em or "@" not in em or "." not in em.split("@")[-1]:
        status = "Invalid/Missing"
        bad_emails += 1
    elif em in seen_emails:
        status = "Shared Household"
    else:
        status = "Valid"
        seen_emails.add(em)
    cur.execute("INSERT INTO constituents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        r["constituent_id"], r["first_name"].strip(), r["last_name"].strip(), em,
        status, clean_phone(r["phone"]), r["city"].strip(), r["state"].strip(),
        r["zip_code"][:5], r["constituent_type"], r["acquisition_channel"],
        clean_date(r["signup_date"]), r["wealth_tier"], 1 if r["is_opted_out"] == "True" else 0
    ))

# 2. Load Campaigns
raw_camp = read_csv("campaigns.csv")
cur.execute("""CREATE TABLE campaigns (
    campaign_id TEXT PRIMARY KEY, campaign_name TEXT, channel TEXT, start_date TEXT,
    end_date TEXT, marketing_budget REAL, staff_hours_allocated INTEGER,
    target_goal REAL, program_area TEXT)""")
camp_lookup = {}
for r in raw_camp:
    camp_lookup[r["campaign_name"].lower()] = (r["campaign_id"], r["campaign_name"])
    cur.execute("INSERT INTO campaigns VALUES (?,?,?,?,?,?,?,?,?)", (
        r["campaign_id"], r["campaign_name"], r["channel"], r["start_date"], r["end_date"],
        float(r["marketing_budget"]), int(r["staff_hours_allocated"]),
        float(r["target_goal"]), r["program_area"]
    ))

# 3. Clean & Deduplicate Donations
raw_don = read_csv("donations.csv")
cur.execute("""CREATE TABLE donations (
    donation_id TEXT PRIMARY KEY, constituent_id TEXT, campaign_id TEXT,
    campaign_name TEXT, donation_date TEXT, amount REAL, is_refund INTEGER,
    payment_method TEXT, is_recurring INTEGER, recurring_status TEXT)""")

seen_don = set()
dups_removed = 0
typos_fixed = 0
for r in raw_don:
    did = r["donation_id"]
    if did in seen_don:
        dups_removed += 1
        continue
    seen_don.add(did)

    raw_cname = r["campaign_name"]
    fixed_cname = raw_cname.strip().title().replace("Anual", "Annual")
    if fixed_cname != raw_cname:
        typos_fixed += 1
    cid_mapped, clean_cname = camp_lookup.get(fixed_cname.lower(), (r["campaign_id"], fixed_cname))
    amt = float(r["amount"])
    cur.execute("INSERT INTO donations VALUES (?,?,?,?,?,?,?,?,?,?)", (
        did, r["constituent_id"], cid_mapped, clean_cname, r["donation_date"],
        amt, 1 if amt < 0 else 0, r["payment_method"],
        1 if r["is_recurring"] == "True" else 0, r["recurring_status"] or "One-Time"
    ))

# 4. Load Grants, Expenses, Volunteers, Engagement
cur.execute("""CREATE TABLE grants (grant_id TEXT PRIMARY KEY, foundation_name TEXT, program_area TEXT,
    awarded_amount REAL, restricted_funds INTEGER, start_date TEXT, end_date TEXT,
    reporting_deadline TEXT, grant_manager TEXT, status TEXT)""")
for r in read_csv("grants.csv"):
    cur.execute("INSERT INTO grants VALUES (?,?,?,?,?,?,?,?,?,?)", (
        r["grant_id"], r["foundation_name"], r["program_area"], float(r["awarded_amount"]),
        1 if r["restricted_funds"] == "True" else 0, r["start_date"], r["end_date"],
        r["reporting_deadline"], r["grant_manager"], r["status"]
    ))

cur.execute("""CREATE TABLE program_expenses (expense_id TEXT PRIMARY KEY, grant_id TEXT,
    program_area TEXT, expense_category TEXT, expense_date TEXT, amount REAL,
    vendor_name TEXT, approval_status TEXT)""")
for r in read_csv("program_expenses.csv"):
    cur.execute("INSERT INTO program_expenses VALUES (?,?,?,?,?,?,?,?)", (
        r["expense_id"], r["grant_id"], r["program_area"], r["expense_category"],
        r["expense_date"], float(r["amount"]), r["vendor_name"], r["approval_status"]
    ))

cur.execute("""CREATE TABLE volunteer_and_outcomes (activity_id TEXT PRIMARY KEY, constituent_id TEXT,
    program_area TEXT, activity_date TEXT, volunteer_hours REAL,
    beneficiaries_served INTEGER, outcome_score INTEGER)""")
for r in read_csv("volunteer_and_outcomes.csv"):
    cur.execute("INSERT INTO volunteer_and_outcomes VALUES (?,?,?,?,?,?,?)", (
        r["activity_id"], r["constituent_id"], r["program_area"], r["activity_date"],
        float(r["volunteer_hours"]), int(r["beneficiaries_served"]), int(r["outcome_score"])
    ))

cur.execute("""CREATE TABLE digital_engagement (engagement_id TEXT PRIMARY KEY, constituent_id TEXT,
    campaign_id TEXT, touchpoint_type TEXT, touchpoint_date TEXT, device_type TEXT)""")
for r in read_csv("digital_engagement.csv"):
    cur.execute("INSERT INTO digital_engagement VALUES (?,?,?,?,?,?)", (
        r["engagement_id"], r["constituent_id"], r["campaign_id"],
        r["touchpoint_type"], r["touchpoint_date"], r["device_type"]
    ))

# 5. Build 5 Executive KPI Marts & Export to data/clean/
marts = {
    "mart_monthly_revenue.csv": """
        SELECT substr(donation_date, 1, 7) AS year_month,
               COUNT(*) AS total_gifts,
               COUNT(DISTINCT constituent_id) AS unique_donors,
               ROUND(SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END), 2) AS gross_revenue,
               ROUND(SUM(amount), 2) AS net_revenue,
               ROUND(AVG(CASE WHEN amount > 0 THEN amount END), 2) AS avg_gift_size
        FROM donations GROUP BY 1 ORDER BY 1""",
    "mart_campaign_roi.csv": """
        SELECT c.campaign_id, c.campaign_name, c.channel, c.program_area,
               c.marketing_budget, c.target_goal,
               COALESCE(ROUND(SUM(d.amount), 2), 0) AS net_raised,
               ROUND(COALESCE(SUM(d.amount), 0) - c.marketing_budget, 2) AS net_profit,
               ROUND((COALESCE(SUM(d.amount), 0) - c.marketing_budget) / c.marketing_budget * 100, 1) AS roi_pct
        FROM campaigns c LEFT JOIN donations d ON c.campaign_id = d.campaign_id
        GROUP BY 1,2,3,4,5,6 ORDER BY roi_pct DESC""",
    "mart_volunteer_crossover.csv": """
        WITH vol AS (SELECT constituent_id, SUM(volunteer_hours) AS hrs FROM volunteer_and_outcomes GROUP BY 1),
             don AS (SELECT constituent_id, COUNT(*) AS gifts, SUM(amount) AS ltv FROM donations WHERE amount > 0 GROUP BY 1)
        SELECT CASE WHEN v.constituent_id IS NOT NULL THEN 'Donor + Volunteer' ELSE 'Donor Only' END AS supporter_segment,
               COUNT(*) AS constituent_count,
               ROUND(AVG(d.gifts), 2) AS avg_gifts_per_person,
               ROUND(AVG(d.ltv), 2) AS avg_lifetime_value,
               ROUND(SUM(d.ltv), 2) AS total_segment_revenue
        FROM don d LEFT JOIN vol v ON d.constituent_id = v.constituent_id
        GROUP BY 1""",
    "mart_program_efficiency.csv": """
        WITH exp AS (SELECT program_area, SUM(amount) AS total_spend FROM program_expenses WHERE approval_status='Approved' GROUP BY 1),
             imp AS (SELECT program_area, SUM(beneficiaries_served) AS people_helped, ROUND(AVG(outcome_score),1) AS avg_outcome FROM volunteer_and_outcomes GROUP BY 1)
        SELECT i.program_area, ROUND(e.total_spend, 2) AS approved_spend, i.people_helped, i.avg_outcome,
               ROUND(e.total_spend / i.people_helped, 2) AS cost_per_beneficiary
        FROM imp i JOIN exp e ON i.program_area = e.program_area ORDER BY cost_per_beneficiary ASC""",
    "mart_action_alerts.csv": """
        SELECT 'Failed Recurring Gift' AS alert_type, d.constituent_id AS record_id,
               c.first_name || ' ' || c.last_name AS title, c.email AS contact_or_owner,
               d.amount AS dollar_impact, d.donation_date AS key_date
        FROM donations d JOIN constituents c ON d.constituent_id = c.constituent_id
        WHERE d.recurring_status = 'Failed Payment'
        UNION ALL
        SELECT 'Grant Deadline / At Risk', grant_id, foundation_name || ' (' || program_area || ')',
               grant_manager, awarded_amount, reporting_deadline
        FROM grants WHERE status = 'At Risk'
        UNION ALL
        SELECT 'Flagged Vendor Expense', expense_id, vendor_name || ' - ' || expense_category,
               program_area, amount, expense_date
        FROM program_expenses WHERE approval_status = 'Flagged'"""
}

conn.commit()
print("\n=== DATA CLEANING & QUALITY AUDIT REPORT ===")
print(f" - Duplicate Donations Removed : {dups_removed:,}")
print(f" - Campaign Name Typos Fixed   : {typos_fixed:,}")
print(f" - Invalid/Missing Emails Flagged: {bad_emails:,}")
print("\n=== EXECUTIVE KPI MARTS EXPORTED TO data/clean/ ===")

for fname, query in marts.items():
    rows = cur.execute(query).fetchall()
    headers = [desc for desc in cur.description]
