import csv
import os
import random
from datetime import date, timedelta

random.seed(42)
out_dir = os.path.join("demo-enterprise-impact", "data", "raw")
os.makedirs(out_dir, exist_ok=True)

def write_csv(filename, headers, rows):
    path = os.path.join(out_dir, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f" - {filename}: {len(rows):,} rows | {len(headers)} columns")

# 1. Constituents (8,000 rows)
first_names = ("James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","David","Elizabeth","William","Barbara","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Charles","Karen")
last_names = ("Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin")
cities = (("Charlotte","NC","28202"),("Concord","NC","28025"),("Raleigh","NC","27601"),("Atlanta","GA","30301"),("Greenville","SC","29601"),("Austin","TX","78701"),("Denver","CO","80202"),("Chicago","IL","60601"))
channels = ("Organic Search","Direct Mail","Social Media","Gala/Event","Peer-to-Peer","Corporate Match")

const_rows = []
base_signup = date(2023, 1, 1)
for i in range(8000):
    cid = f"CON-{10000+i}"
    fn, ln = random.choice(first_names), random.choice(last_names)
    email = f"{fn.lower()}.{ln.lower()}{i}@example.org"
    if i % 27 == 0:
        email = ""
    elif i % 65 == 0:
        email = "bad-email@gmail"
    elif 10 <= i < 60:
        email = const_rows[i-10][3]

    p1, p2 = random.randint(200, 999), random.randint(1000, 9999)
    phone = f"({p1}) 555-{p2}" if i % 3 != 0 else (f"{p1}.555.{p2}" if i % 5 != 0 else f"+1{p1}555{p2}")

    city, state, zc = random.choice(cities)
    if i % 4 == 0:
        zc = f"{zc}-{random.randint(1000,9999)}"

    d = base_signup + timedelta(days=random.randint(0, 1400))
    s_date = d.strftime("%Y-%m-%d") if i % 4 != 0 else (d.strftime("%m/%d/%Y") if i % 7 != 0 else d.strftime("%b %d, %Y"))

    ctype = random.choices(("Individual","Corporate","Foundation","Board/Major"), weights=(82,9,5,4))[0]
    wtier = random.choices(("Standard","Mid-Level","Major Prospect"), weights=(75,18,7))[0]
    opt_out = random.random() < 0.09
    const_rows.append((cid, fn, ln, email, phone, city, state, zc, ctype, random.choice(channels), s_date, wtier, opt_out))

# 2. Campaigns (24 rows)
areas = ("Youth Education", "Food Security", "Housing Relief", "Workforce Readiness", "General Operations")
camp_names = ("Annual Gala","Spring Appeal","Summer Match","Back to School","Fall Direct Mail","Giving Tuesday","Year-End Drive","Monthly Sustainer")
camp_rows = []
idx = 0
years_tuple = (2024, 2025, 2026)
for yr in years_tuple:
    for nm in camp_names:
        cid = f"CMP-{100+idx}"
        sd = date(2024, 1, 15) + timedelta(days=idx*45)
        ed = sd + timedelta(days=40)
        budget = random.randint(8000, 45000)
        ch = random.choice(("Email","Direct Mail","Events","Social Media","Multi-Channel"))
        if idx in (4, 12):
            ch = "Direct Mail"
            budget = 68000
        camp_rows.append((cid, f"{yr} {nm}", ch, sd.isoformat(), ed.isoformat(), budget, random.randint(80, 450), random.randint(50000, 350000), random.choice(areas)))
        idx += 1

# 3. Volunteer & Outcomes (6,000 rows)
vol_rows = []
active_vols = tuple(r[0] for r in const_rows[:2200])
for i in range(6000):
    vd = date(2024, 1, 1) + timedelta(days=random.randint(0, 1095))
    vol_rows.append((f"ACT-{20000+i}", random.choice(active_vols), random.choice(areas[:4]), vd.isoformat(), round(random.uniform(1.5, 8.0), 1), random.randint(1, 25), random.randint(68, 99)))

# 4. Donations (35,000 rows + 1,225 duplicates)
reg_consts = tuple(r[0] for r in const_rows[2200:])
don_rows = []
month_weights = (6, 6, 7, 7, 7, 9, 6, 6, 7, 8, 14, 17)
for i in range(35000):
    is_vol = random.random() < 0.45
    cid = random.choice(active_vols) if is_vol else random.choice(reg_consts)
    cmp = random.choice(camp_rows)
    cmp_id = "" if random.random() < 0.04 else cmp[0]
    cname = cmp[1]
    if i % 11 == 0:
        cname = cname.lower() + " "
    elif i % 19 == 0:
        cname = cname.replace("Annual", "Anual")

    yr = random.choices(years_tuple, weights=(28, 34, 38))[0]
    mo = random.choices(range(1, 13), weights=month_weights)[0]
    dd = date(yr, mo, random.randint(1, 28)).isoformat()

    amt = round(random.lognormvariate(4.3, 1.1), 2)
    if is_vol:
        amt = round(amt * 1.45, 2)
    if i % 135 == 0:
        amt = -amt

    is_rec = random.random() < 0.32
    rec_st = random.choices(("Active","Paused","Failed Payment","Cancelled"), weights=(78,7,8,7))[0] if is_rec else ""
    pm = random.choices(("Credit Card","ACH","Check","Donor-Advised Fund","Stock/Crypto"), weights=(55,22,14,7,2))[0]
    don_rows.append((f"DON-{100000+i}", cid, cmp_id, cname, dd, amt, pm, is_rec, rec_st))

don_rows.extend(random.sample(don_rows, 1225))

# 5. Grants (75 rows)
foundations = ("Duke Endowment","Knight Foundation","Lilly Endowment","Ford Foundation","Gates Foundation","Bank of America Charitable","Wells Fargo Foundation","Carnegie Corp")
grant_rows = []
for i in range(75):
    gs = date(2024, 1, 1) + timedelta(days=random.randint(0, 900))
    ge = gs + timedelta(days=random.randint(180, 540))
    rep = (ge - timedelta(days=15)).isoformat()
    st = random.choices(("Active","Completed","Pending Renewal","At Risk"), weights=(48,32,12,8))[0]
    if i < 5:
        rep = f"2026-12-0{i+1}"
        st = "At Risk"
    grant_rows.append((f"GRT-{500+i}", random.choice(foundations), random.choice(areas[:4]), random.randint(25000, 250000), random.random() < 0.75, gs.isoformat(), ge.isoformat(), rep, random.choice(("Elena Rostova","Marcus Vance","Priya Patel","Jordan Brooks")), st))

# 6. Program Expenses (3,500 rows)
exp_rows = []
for i in range(3500):
    area = random.choice(areas)
    amt = round(random.uniform(150, 1200) if area == "Workforce Readiness" else random.uniform(300, 2800), 2)
    st = random.choices(("Approved","Pending","Flagged"), weights=(94,4,2))[0]
    if i < 15:
        st = "Flagged"
        amt = round(amt * 3.5, 2)
    gid = random.choice(grant_rows)[0] if random.random() < 0.65 else ""
    ed = (date(2024, 1, 1) + timedelta(days=random.randint(0, 1095))).isoformat()
    exp_rows.append((f"EXP-{30000+i}", gid, area, random.choice(("Direct Client Aid","Program Staffing","Supplies & Materials","Events & Outreach","Admin & Overhead")), ed, amt, random.choice(("Sysco Foods","Staples Business","Carolina Youth Works","Metro Housing Partners","Piedmont Print & Mail","CloudTech Solutions")), st))

# 7. Digital Engagement (15,000 rows)
eng_rows = []
for i in range(15000):
    td = (date(2024, 1, 1) + timedelta(days=random.randint(0, 1095))).isoformat()
    eng_rows.append((f"ENG-{50000+i}", random.choice(const_rows)[0], random.choice(camp_rows)[0], random.choices(("Email Open","Email Click","Webinar Attended","Impact Report Downloaded","Donation Page Abandoned"), weights=(45,22,10,13,10))[0], td, random.choices(("Mobile","Desktop","Tablet"), weights=(54,39,7))[0]))

print("\nSUCCESS! Generated all 7 enterprise CSV datasets in demo-enterprise-impact/data/raw/:")
write_csv("constituents.csv", ("constituent_id","first_name","last_name","email","phone","city","state","zip_code","constituent_type","acquisition_channel","signup_date","wealth_tier","is_opted_out"), const_rows)
write_csv("campaigns.csv", ("campaign_id","campaign_name","channel","start_date","end_date","marketing_budget","staff_hours_allocated","target_goal","program_area"), camp_rows)
write_csv("volunteer_and_outcomes.csv", ("activity_id","constituent_id","program_area","activity_date","volunteer_hours","beneficiaries_served","outcome_score"), vol_rows)
write_csv("donations.csv", ("donation_id","constituent_id","campaign_id","campaign_name","donation_date","amount","payment_method","is_recurring","recurring_status"), don_rows)
write_csv("grants.csv", ("grant_id","foundation_name","program_area","awarded_amount","restricted_funds","start_date","end_date","reporting_deadline","grant_manager","status"), grant_rows)
write_csv("program_expenses.csv", ("expense_id","grant_id","program_area","expense_category","expense_date","amount","vendor_name","approval_status"), exp_rows)
write_csv("digital_engagement.csv", ("engagement_id","constituent_id","campaign_id","touchpoint_type","touchpoint_date","device_type"), eng_rows)
