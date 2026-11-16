p = "demo-freight-logistics/app.js"
s = open(p, encoding="utf-8").read()

# 1. Clean up left division bar labels & GM% formatting
s = s.replace(
    "r.at(0) + ' (' + Number(r.at(2)).toLocaleString() + ' served | ' + r.at(3) + '/100)'",
    "r.at(0) + ' (' + fmt(r.at(2)) + ' rev)'"
)
s = s.replace(
    "'$' + Number(r.at(4)).toFixed(2) + ' % Margin'",
    "Number(r.at(4)).toFixed(1) + '% GM'"
)

# 2. Fix funnel padding, title, and freight callout copy
s = s.replace("fP = 28;", "fP = 48;")
s = s.replace(
    "Digital Engagement Funnel & Checkout Recovery Opportunity",
    "Freight & Rental Quote Funnel & Bid Recovery"
)
s = s.replace(
    "Checkout Recovery Play: ' + abCount.toLocaleString() + ' supporters abandoned the donation page. Triggering an automated 24-hr reminder email recovers ~15%",
    "Quote Recovery Play: ' + abCount.toLocaleString() + ' freight & fleet rental RFQs sit stalled past 10 days. Automated Sales rep follow-up closes ~15%"
)

open(p, "w", encoding="utf-8").write(s)

# 3. Shorten first funnel label in data.js so it fits cleanly
d_path = "demo-freight-logistics/data.js"
d = open(d_path, encoding="utf-8").read().replace("Freight & Rental RFQs", "Freight RFQs")
open(d_path, "w", encoding="utf-8").write(d)

print("FREIGHT LABELS & FUNNEL FIXED!")
