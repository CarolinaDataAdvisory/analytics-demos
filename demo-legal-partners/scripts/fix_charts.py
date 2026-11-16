# 1. Fix Law Firm (Piedmont Legal Partners)
p_law = "demo-legal-partners/app.js"
s_law = open(p_law, encoding="utf-8").read()
s_law = s_law.replace("r.at(0) + ' (' + Number(r.at(2)).toLocaleString() + ' served | ' + r.at(3) + '/100)'", "r.at(0) + ' (' + fmt(r.at(2)) + ' billed)'")
s_law = s_law.replace("'$' + Number(r.at(4)).toFixed(2) + ' % Realized'", "Number(r.at(4)).toFixed(1) + '% Realized'")
s_law = s_law.replace("fP = 28;", "fP = 54;")
s_law = s_law.replace("Digital Engagement Funnel & Checkout Recovery Opportunity", "Intake-to-Retainer Funnel & Consultation Recovery")
s_law = s_law.replace("Checkout Recovery Play: ' + abCount.toLocaleString() + ' supporters abandoned the donation page. Triggering an automated 24-hr reminder email recovers ~15%", "Intake Recovery Play: ' + abCount.toLocaleString() + ' qualified consultations sit unsigned past 10 days. Partner follow-up converts ~15%")
open(p_law, "w", encoding="utf-8").write(s_law)

d_law = open("demo-legal-partners/data.js", encoding="utf-8").read().replace("Qualified Consultations", "Consultations").replace("15% Retainer Recovery", "15% Signed")
open("demo-legal-partners/data.js", "w", encoding="utf-8").write(d_law)

# 2. Apply same polish to HVAC/Plumbing (Carolina Climate & Mechanical)
p_hvac = "demo-hvac-mechanical/app.js"
s_hvac = open(p_hvac, encoding="utf-8").read()
s_hvac = s_hvac.replace("r.at(0) + ' (' + Number(r.at(2)).toLocaleString() + ' served | ' + r.at(3) + '/100)'", "r.at(0) + ' (' + fmt(r.at(2)) + ' rev)'")
s_hvac = s_hvac.replace("'$' + Number(r.at(4)).toFixed(2) + ' % GM'", "Number(r.at(4)).toFixed(1) + '% GM'")
s_hvac = s_hvac.replace("fP = 28;", "fP = 54;")
s_hvac = s_hvac.replace("Digital Engagement Funnel & Checkout Recovery Opportunity", "Replacement Estimate Funnel & Stalled Quote Recovery")
s_hvac = s_hvac.replace("Checkout Recovery Play: ' + abCount.toLocaleString() + ' supporters abandoned the donation page. Triggering an automated 24-hr reminder email recovers ~15%", "Estimate Recovery Play: ' + abCount.toLocaleString() + ' replacement quotes sit stalled past 7 days. Comfort Advisor follow-up closes ~15%")
open(p_hvac, "w", encoding="utf-8").write(s_hvac)

d_hvac = open("demo-hvac-mechanical/data.js", encoding="utf-8").read().replace("In-Home Estimates", "Home Estimates").replace("15% Quote Recovery", "15% Closed")
open("demo-hvac-mechanical/data.js", "w", encoding="utf-8").write(d_hvac)

print("LAW FIRM & HVAC CHARTS POLISHED!")
