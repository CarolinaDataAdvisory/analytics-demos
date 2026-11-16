js = open("demo-enterprise-impact/app.js", encoding="utf-8").read()
for o, n in (
    ("1.18", "1.11"), ("2.5", "2.8"), ("* 0.05", "* 0.08"), ("* 15", "* 25"),
    ("3-Year Net Revenue", "3-Year Gross Revenue"), ("UP 22% YoY Recurring Growth", "~$12.4M/Yr Regional Run-Rate"),
    ("Active Donors (2026)", "Active Homeowners (2026)"), ("Net Donors", "Net Customers"),
    ("H1 2027 Run-Rate Projection", "H1 2027 Seasonal Run-Rate"),
    ("Grants, Audits & Failed Gifts", "Unsold Quotes, Callbacks & Plans"), ("gifts/ea", "service calls"),
    ("donors @ $15", "customers @ $25"), ("5% Full + 10% Half", "16% Reactivation"),
    ("165", "8900"), ("gifts =", "installs ="),
    ("Grant Risk", "Unsold Estimate"), ("Flagged Exp", "Tech Callback"), ("Failed Recur", "Plan Renewal"),
    ("endsWith('-11') || r.at(0).endsWith('-12')", "endsWith('-06') || r.at(0).endsWith('-07') || r.at(0).endsWith('-08')"),
    ("/ person", "% GM"), ("'$' + Number(r.at(4)).toFixed(2) + '% GM'", "Number(r.at(4)).toFixed(1) + '% GM'")
):
    js = js.replace(o, n)
open("demo-hvac-mechanical/app.js", "w", encoding="utf-8").write(js)
print("PART A DONE!")
